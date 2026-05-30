"""
Runtime MIB load and trap / notification-object resolution tests.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from pysnmp.smi import builder, error, view
from pysnmp.smi.rfc1902 import ObjectIdentity

from tests.mib_traps.catalog import NotificationEntry, group_by_module
from tests.mib_traps.instance_index import (
    per_object_instance_index,
    shared_instance_index,
)
from tests.mib_traps.varbinds import sample_index_value
from tests.mib_traps.wire_index import column_oid_wire, resolve_varbind_with_mib


@dataclass
class ObjectDecode:
    module: str
    symbol: str
    ok: bool
    text: str  # resolved MIB name or error detail


@dataclass
class TrapResult:
    entry: NotificationEntry
    trap_ok: bool
    trap_message: str = ""
    trap_oid: str = ""
    objects_ok: int = 0
    objects_fail: int = 0
    objects_skip: int = 0
    object_errors: List[str] = field(default_factory=list)
    object_decodes: List[ObjectDecode] = field(default_factory=list)


@dataclass
class ModuleResult:
    module: str
    vendor: str
    loaded: bool
    skip_reason: str = ""
    traps_planned: int = 0
    traps: List[TrapResult] = field(default_factory=list)


def _is_symbolic(name: str) -> bool:
    return "::" in name and not name.startswith("1.3.6")


def _check_trap_oid(
    mib_view: view.MibViewController, entry: NotificationEntry
) -> Tuple[bool, str]:
    """Resolve the catalogued NOTIFICATION-TYPE by module/symbol (not numeric OID).

    Many vendor MIBs assign the same OID to a v1 TRAP-TYPE and v2 NOTIFICATION-TYPE,
    or to both a notification and a sibling OBJECT IDENTIFIER subtree. Numeric OID
    lookup is ambiguous in those cases; symbolic resolution is what trap decoding uses.
    """
    try:
        oi = ObjectIdentity(entry.module, entry.symbol).resolveWithMib(mib_view)
        node = oi.getMibNode()
        if type(node).__name__ != "NotificationType":
            return (
                False,
                f"node type {type(node).__name__!r}, expected NotificationType",
            )
        resolved_oid = tuple(oi.getOid())
        if resolved_oid != entry.oid:
            return (
                False,
                f"OID mismatch: got {'.'.join(str(x) for x in resolved_oid)}, "
                f"expected {'.'.join(str(x) for x in entry.oid)}",
            )
        pretty = oi.prettyPrint()
        if not _is_symbolic(pretty):
            return False, f"trap OID not symbolic: {pretty}"
        return True, pretty
    except Exception as exc:
        return False, str(exc)


def _resolve_object_symbolic(
    mib_view: view.MibViewController,
    obj_mod: str,
    obj_sym: str,
    instance_index: Tuple[int, ...],
) -> Tuple[bool, str]:
    try:
        oi = ObjectIdentity(obj_mod, obj_sym, *instance_index).resolveWithMib(
            mib_view, ignoreErrors=False
        )
        name = oi.prettyPrint()
        if _is_symbolic(name):
            return True, name
        return False, name
    except Exception as exc:
        return False, str(exc)


def _resolve_object_wire_oid(
    mib_view: view.MibViewController, obj_mod: str, obj_sym: str
) -> Tuple[bool, str]:
    """Resolve using wire-format instance OIDs (length-prefixed MacAddress, etc.)."""
    mb = mib_view.mibBuilder
    try:
        col = mb.importSymbols(obj_mod, obj_sym)[0]
    except Exception as exc:
        return False, str(exc)
    if type(col).__name__ == "MibScalar":
        oid = col.getName()
    else:
        from tests.mib_traps.wire_index import row_for_column

        row = row_for_column(mb, col)
        if row is None:
            return False, "no table row"
        index_values = [
            sample_index_value(mb.importSymbols(mod_name, sym_name)[0])
            for _implied, mod_name, sym_name in row.indexNames
        ]
        oid = column_oid_wire(mb, obj_mod, obj_sym, *index_values)
        if oid is None:
            return False, "column_oid_wire failed"
    try:
        oi = resolve_varbind_with_mib(mib_view, oid, col.getSyntax().clone())
        name = oi[0].prettyPrint()
        if _is_symbolic(name):
            return True, name
        return False, name
    except Exception as exc:
        return False, str(exc)


def resolve_trap_varbind_oid(
    mib_view: view.MibViewController, oid: Sequence[int], val
) -> Tuple[bool, str]:
    """Resolve a numeric trap var-bind OID (handles wire index encoding)."""
    try:
        oi, _v = resolve_varbind_with_mib(mib_view, oid, val)
        name = oi.prettyPrint()
        if _is_symbolic(name):
            return True, name
        return False, name
    except Exception as exc:
        return False, str(exc)


def _check_notification_objects(
    mib_view: view.MibViewController,
    entry: NotificationEntry,
) -> Tuple[int, int, int, List[str], List[ObjectDecode]]:
    if not entry.objects:
        return 0, 0, 0, [], []

    ok = fail = skip = 0
    errors: List[str] = []
    decodes: List[ObjectDecode] = []
    shared_inst = shared_instance_index(mib_view, entry.objects)

    for obj_mod, obj_sym in entry.objects:
        per_inst = per_object_instance_index(mib_view, obj_mod, obj_sym)
        tried = []
        good = False
        msg = ""
        for suffix in (shared_inst, per_inst, ()):
            if suffix in tried:
                continue
            tried.append(suffix)
            good, msg = _resolve_object_symbolic(
                mib_view, obj_mod, obj_sym, suffix
            )
            if good:
                ok += 1
                decodes.append(
                    ObjectDecode(obj_mod, obj_sym, True, msg)
                )
                break
        if not good:
            good, msg = _resolve_object_wire_oid(mib_view, obj_mod, obj_sym)
            if good:
                ok += 1
                decodes.append(
                    ObjectDecode(obj_mod, obj_sym, True, msg)
                )
        if not good:
            if msg.startswith("1.3.6"):
                fail += 1
            else:
                skip += 1
            errors.append(f"{obj_mod}::{obj_sym}: {msg}")
            decodes.append(ObjectDecode(obj_mod, obj_sym, False, msg))

    return ok, fail, skip, errors, decodes


def test_trap(
    mib_view: view.MibViewController, entry: NotificationEntry
) -> TrapResult:
    trap_ok, trap_msg = _check_trap_oid(mib_view, entry)
    o_ok, o_fail, o_skip, o_errs, o_decodes = _check_notification_objects(
        mib_view, entry
    )
    return TrapResult(
        entry=entry,
        trap_ok=trap_ok,
        trap_message=trap_msg,
        trap_oid=".".join(str(x) for x in entry.oid),
        objects_ok=o_ok,
        objects_fail=o_fail,
        objects_skip=o_skip,
        object_errors=o_errs,
        object_decodes=o_decodes,
    )


def _load_module(mib_dir: str, module_name: str) -> Tuple[builder.MibBuilder, str]:
    mb = builder.MibBuilder()
    mb.addMibSources(builder.DirMibSource(mib_dir))
    try:
        mb.loadModules(module_name)
        return mb, ""
    except error.MibLoadError as exc:
        return mb, f"MibLoadError: {exc}"
    except Exception as exc:
        err = str(exc)
        if "circular" in err.lower():
            return mb, f"circular import: {exc}"
        return mb, str(exc)


def run_resolution_tests(
    entries: Sequence[NotificationEntry],
    mib_dir: str,
    progress: bool = False,
    progress_every: int = 25,
) -> List[ModuleResult]:
    grouped = group_by_module(entries)
    results: List[ModuleResult] = []
    total = len(grouped)
    done = 0

    for module_name in sorted(grouped.keys()):
        module_entries = grouped[module_name]
        vendor = module_entries[0].vendor if module_entries else "unknown"
        mb, skip_reason = _load_module(mib_dir, module_name)
        mod_result = ModuleResult(
            module=module_name,
            vendor=vendor,
            loaded=not skip_reason,
            traps_planned=len(module_entries),
        )

        if skip_reason:
            mod_result.skip_reason = skip_reason
            results.append(mod_result)
            done += 1
            if progress and done % progress_every == 0:
                print(f"  progress: {done}/{total} modules", flush=True)
            continue

        mib_view = view.MibViewController(mb)
        for entry in module_entries:
            mod_result.traps.append(test_trap(mib_view, entry))

        results.append(mod_result)
        done += 1
        if progress and done % progress_every == 0:
            print(f"  progress: {done}/{total} modules", flush=True)

    return results
