"""
Static discovery of NOTIFICATION-TYPE traps in compiled PySNMP MIB modules.
"""
import fnmatch
import glob
import os
import re
from collections import namedtuple
from typing import Dict, Iterable, List, Optional, Set, Tuple

TrapObject = Tuple[str, str]  # (module, symbol)

NotificationEntry = namedtuple(
    "NotificationEntry",
    [
        "module",
        "vendor",
        "symbol",
        "oid",
        "objects",
        "source_file",
    ],
)

CatalogStats = namedtuple(
    "CatalogStats",
    [
        "modules_scanned",
        "modules_with_traps",
        "trap_count",
        "vendors",
    ],
)

_TRAP_LINE = re.compile(
    r"^(\w+)\s*=\s*NotificationType\(\(([^)]+)\)\)"
    r"(?:\.setObjects\((.*)\))?\s*$"
)
_OID_TUPLE = re.compile(r"\d+")
_VENDOR_PATH = re.compile(r"/vendor/([^/\s]+)/", re.I)
_STANDARD_PATH = re.compile(r"/standard/", re.I)
_OBJECT_REF = re.compile(r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)')


def _repo_root() -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    )


def default_mib_dir() -> str:
    return os.path.join(_repo_root(), "output", "notexts")


def build_module_vendor_map(mibs_src_vendor: Optional[str] = None) -> Dict[str, str]:
    """Map MIB module stem -> vendor from src/vendor/{vendor}/."""
    root = mibs_src_vendor or os.path.join(_repo_root(), "src", "vendor")
    mapping: Dict[str, str] = {}
    if not os.path.isdir(root):
        return mapping
    for vendor in os.listdir(root):
        vendor_dir = os.path.join(root, vendor)
        if not os.path.isdir(vendor_dir):
            continue
        for name in os.listdir(vendor_dir):
            base, ext = os.path.splitext(name)
            stem = base if ext else name
            mapping[stem] = vendor
            mapping[stem.upper()] = vendor
    return mapping


def _parse_oid_tuple(text: str) -> Tuple[int, ...]:
    parts = _OID_TUPLE.findall(text)
    return tuple(int(p) for p in parts)


def _parse_objects(set_objects_text: Optional[str]) -> Tuple[TrapObject, ...]:
    if not set_objects_text:
        return ()
    return tuple(_OBJECT_REF.findall(set_objects_text))


def _detect_vendor(
    header_lines: Iterable[str], module: str, fallback_map: Dict[str, str]
) -> str:
    for line in header_lines:
        m = _VENDOR_PATH.search(line)
        if m:
            return m.group(1).lower()
        if _STANDARD_PATH.search(line):
            return "standard"
    key = module.upper()
    if key in fallback_map:
        return fallback_map[key]
    # Heuristic: CISCO-FOO-MIB -> cisco if in fallback by prefix
    for mod, vendor in fallback_map.items():
        if module.upper().startswith(mod.split("-")[0] + "-"):
            return vendor
    return "unknown"


def scan_mib_dir(
    mib_dir: str,
    mibs_src_vendor: Optional[str] = None,
) -> List[NotificationEntry]:
    if not os.path.isdir(mib_dir):
        raise FileNotFoundError(
            f"Compiled MIB directory not found: {mib_dir}\n"
            "Run `make vendor standard` (or `./scripts/localmibs.sh`) to populate "
            "output/notexts/ — see README.md"
        )

    fallback_map = build_module_vendor_map(mibs_src_vendor)
    entries: List[NotificationEntry] = []
    paths = sorted(glob.glob(os.path.join(mib_dir, "*.py")))

    for path in paths:
        module = os.path.splitext(os.path.basename(path))[0]
        header: List[str] = []
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for i, line in enumerate(fh):
                if i < 20:
                    header.append(line)
                stripped = line.strip()
                m = _TRAP_LINE.match(stripped)
                if not m:
                    continue
                symbol, oid_text, objects_text = m.group(1), m.group(2), m.group(3)
                try:
                    oid = _parse_oid_tuple(oid_text)
                except ValueError:
                    continue
                vendor = _detect_vendor(header, module, fallback_map)
                entries.append(
                    NotificationEntry(
                        module=module,
                        vendor=vendor,
                        symbol=symbol,
                        oid=oid,
                        objects=_parse_objects(objects_text),
                        source_file=path,
                    )
                )

    return entries


def catalog_stats(entries: Iterable[NotificationEntry]) -> CatalogStats:
    modules = set()
    modules_with_traps = set()
    vendors: Dict[str, int] = {}
    count = 0
    for e in entries:
        count += 1
        modules_with_traps.add(e.module)
        vendors[e.vendor] = vendors.get(e.vendor, 0) + 1
    for e in entries:
        modules.add(e.module)
    return CatalogStats(
        modules_scanned=len(modules) or len(modules_with_traps),
        modules_with_traps=len(modules_with_traps),
        trap_count=count,
        vendors=vendors,
    )


def filter_vendor(
    entries: List[NotificationEntry], vendors: Set[str]
) -> List[NotificationEntry]:
    want = {v.lower() for v in vendors}
    return [e for e in entries if e.vendor.lower() in want]


def filter_module(
    entries: List[NotificationEntry], pattern: str
) -> List[NotificationEntry]:
    return [e for e in entries if fnmatch.fnmatch(e.module.upper(), pattern.upper())]


def apply_limit(entries: List[NotificationEntry], limit: Optional[int]) -> List[NotificationEntry]:
    if limit is None or limit <= 0:
        return entries
    return entries[:limit]


def group_by_module(
    entries: Iterable[NotificationEntry],
) -> Dict[str, List[NotificationEntry]]:
    grouped: Dict[str, List[NotificationEntry]] = {}
    for e in entries:
        grouped.setdefault(e.module, []).append(e)
    return grouped


def list_vendors(entries: Iterable[NotificationEntry]) -> List[Tuple[str, int]]:
    counts: Dict[str, int] = {}
    for e in entries:
        counts[e.vendor] = counts.get(e.vendor, 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))
