"""
SNMP INDEX encoding helpers for agent wire format vs PySNMP MIB tables.

Cisco LWAPP (and many agents) encode fixed-size OctetString / MacAddress
indices with an explicit length sub-OID (RFC 1902 §7.7 variable-length form),
e.g. MAC f4:74:70:74:bd:90 as ``6.244.116.112.116.189.144``.

Compiled PySNMP MIBs model MacAddress as fixed-length (6 octets) and use
``getAsName`` / ``setFromName`` without a length prefix. This module bridges
the two representations for trap send and MIB resolution tests.
"""
from typing import Any, Optional, Sequence, Tuple

from pysnmp.smi import builder, view
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

# Production ciscoLwappSiSensorCrash capture (PA-EDF-AP-17-02)
EDF_MAC_WIRE = (6, 244, 116, 112, 116, 189, 144)
EDF_MAC_BYTES = bytes([0xF4, 0x74, 0x70, 0x74, 0xBD, 0x90])
EDF_SLOT = 3


def is_fixed_length_octet(syntax) -> bool:
    try:
        return bool(syntax.isFixedLength())
    except AttributeError:
        return False


def fixed_octet_length(syntax) -> Optional[int]:
    if not is_fixed_length_octet(syntax):
        return None
    try:
        return int(syntax.getFixedLength())
    except (TypeError, ValueError, AttributeError):
        return None


def row_for_column(mb: builder.MibBuilder, col) -> Optional[Any]:
    entry_oid = col.getName()[:-1]
    for _mod, syms in mb.mibSymbols.items():
        for _sym, node in syms.items():
            if type(node).__name__ == "MibTableRow" and node.getName() == entry_oid:
                return node
    return None


def normalize_wire_inst_suffix(
    mb: builder.MibBuilder, row, suffix: Sequence[int]
) -> Tuple[int, ...]:
    """
    Strip explicit length sub-OIDs from a table instance suffix (wire -> MIB).
    """
    suffix = list(suffix)
    pos = 0
    parts: list = []
    for _implied, mod_name, sym_name in row.indexNames:
        idx_node = mb.importSymbols(mod_name, sym_name)[0]
        fl = fixed_octet_length(idx_node.syntax)
        if fl is not None:
            chunk = suffix[pos : pos + 1 + fl]
            if len(chunk) >= 1 + fl and chunk[0] == fl:
                parts.extend(chunk[1 : 1 + fl])
                pos += 1 + fl
            elif len(chunk) >= fl:
                parts.extend(chunk[:fl])
                pos += fl
            else:
                break
        else:
            if pos >= len(suffix):
                break
            parts.append(suffix[pos])
            pos += 1
    return tuple(parts)


def to_wire_inst_suffix(
    mb: builder.MibBuilder, row, inst_suffix: Sequence[int]
) -> Tuple[int, ...]:
    """
    Add explicit length sub-OIDs for fixed-size octet indices (MIB -> wire).
    """
    inst_suffix = list(inst_suffix)
    pos = 0
    parts: list = []
    for _implied, mod_name, sym_name in row.indexNames:
        idx_node = mb.importSymbols(mod_name, sym_name)[0]
        fl = fixed_octet_length(idx_node.syntax)
        if fl is not None:
            octets = inst_suffix[pos : pos + fl]
            if len(octets) < fl:
                octets = list(octets) + [0] * (fl - len(octets))
            parts.append(fl)
            parts.extend(octets[:fl])
            pos += fl
        else:
            if pos >= len(inst_suffix):
                break
            parts.append(inst_suffix[pos])
            pos += 1
    return tuple(parts)


def normalize_wire_oid(mb: builder.MibBuilder, oid: Sequence[int]) -> Tuple[int, ...]:
    """If oid uses wire-style index encoding, return MIB-compatible oid."""
    oid = tuple(oid)
    best = None
    for _mod, syms in mb.mibSymbols.items():
        for _sym, node in syms.items():
            if type(node).__name__ != "MibTableColumn":
                continue
            name = node.getName()
            if len(oid) <= len(name) or oid[: len(name)] != name:
                continue
            row = row_for_column(mb, node)
            if row is None:
                continue
            suffix = oid[len(name) :]
            norm_suffix = normalize_wire_inst_suffix(mb, row, suffix)
            if norm_suffix != suffix and (best is None or len(name) > len(best[0])):
                best = (name, norm_suffix)
    if best is None:
        return oid
    name, norm_suffix = best
    return name + norm_suffix


def column_oid_wire(
    mb: builder.MibBuilder, mod: str, sym: str, *index_values: Any
) -> Optional[Tuple[int, ...]]:
    """Build column instance OID using wire-style index encoding."""
    try:
        col = mb.importSymbols(mod, sym)[0]
    except Exception:
        return None
    if type(col).__name__ == "MibScalar":
        return col.getName()
    row = row_for_column(mb, col)
    if row is None:
        return col.getName() + (0,)
    try:
        inst = row.getInstIdFromIndices(*index_values)
    except Exception:
        inst = (0,)
    inst = to_wire_inst_suffix(mb, row, inst)
    return col.getName() + inst


def resolve_varbind_with_mib(
    mib_view: view.MibViewController, oid: Sequence[int], val
):
    """
    Resolve a numeric var-bind OID to symbolic form, accepting wire indices.
    """
    mb = mib_view.mibBuilder
    oid = tuple(oid)
    candidates = [oid]
    normalized = normalize_wire_oid(mb, oid)
    if normalized != oid:
        candidates.append(normalized)
    last_exc = None
    for candidate in candidates:
        try:
            return ObjectType(
                ObjectIdentity(candidate), val
            ).resolveWithMib(mib_view)
        except Exception as exc:
            last_exc = exc
            if "Excessive instance" not in str(exc):
                raise
    if last_exc is not None:
        raise last_exc
    return ObjectType(ObjectIdentity(oid), val).resolveWithMib(mib_view)
