"""
Build SNMPv2c trap var-binds from catalog NotificationEntry records.
"""
from typing import Any, List, Optional, Sequence, Tuple

from pysnmp.proto.api import v2c
from pysnmp.smi import builder

from tests.mib_traps.catalog import NotificationEntry
from tests.mib_traps.wire_index import row_for_column, to_wire_inst_suffix

VarBind = Tuple[Tuple[int, ...], Any]

_SYS_UP_TIME = (1, 3, 6, 1, 2, 1, 1, 3, 0)
_SNMP_TRAP_OID = (1, 3, 6, 1, 6, 3, 1, 1, 4, 1, 0)
_LAB_MAC_BYTES = bytes([0x00, 0x11, 0x22, 0x33, 0x44, 0x55])
_LAB_DATE_AND_TIME = v2c.OctetString(hexValue="07EA05150E1E0000")


def _syntax_name(node) -> str:
    syntax = getattr(node, "syntax", None)
    if syntax is None:
        return ""
    return type(syntax).__name__


def _first_enum_value(syntax) -> Optional[int]:
    named = getattr(syntax, "namedValues", None)
    if not named:
        return None
    try:
        return int(next(iter(named.values())))
    except (StopIteration, TypeError, ValueError):
        return None


def sample_index_value(idx_node) -> Any:
    """Sample value for one table index component (not unpacked)."""
    syntax = _syntax_name(idx_node)
    if "MacAddress" in syntax:
        return _LAB_MAC_BYTES
    if syntax in ("IpAddress",):
        return "192.168.1.1"
    if syntax in ("Integer32", "Unsigned32", "Gauge32", "Counter32", "Counter64"):
        enum_val = _first_enum_value(idx_node.syntax)
        return enum_val if enum_val is not None else 0
    if "TruthValue" in syntax:
        return 1
    if syntax in ("OctetString",) or "String" in syntax or "DisplayString" in syntax:
        return b"eth0"
    return 0


def sample_snmp_value(node) -> Any:
    """Sample SNMP value for a notification OBJECT var-bind."""
    syntax = _syntax_name(node)
    enum_val = _first_enum_value(node.syntax)

    if syntax in ("Integer32",):
        return v2c.Integer32(enum_val if enum_val is not None else 1)
    if syntax in ("Unsigned32", "Gauge32"):
        return v2c.Unsigned32(enum_val if enum_val is not None else 1)
    if syntax in ("Counter32",):
        return v2c.Counter32(0)
    if syntax in ("Counter64",):
        return v2c.Counter64(0)
    if syntax in ("TimeTicks",):
        return v2c.TimeTicks(12345)
    if syntax in ("IpAddress",):
        return v2c.IpAddress("192.168.1.1")
    if "MacAddress" in syntax:
        return v2c.OctetString(hexValue="001122334455")
    if "DateAndTime" in syntax:
        return _LAB_DATE_AND_TIME
    if syntax in ("ObjectIdentifier",):
        return v2c.ObjectIdentifier((1, 3, 6, 1, 2, 1, 1, 1, 0))
    if syntax in ("Bits",):
        return v2c.Bits("")
    if "TruthValue" in syntax:
        return v2c.Integer32(1)
    if syntax in ("OctetString",) or "String" in syntax or "DisplayString" in syntax:
        return v2c.OctetString("lab-test")
    return v2c.OctetString("")


def _object_oid(mb: builder.MibBuilder, mod: str, sym: str) -> Optional[Tuple[int, ...]]:
    try:
        node = mb.importSymbols(mod, sym)[0]
    except Exception:
        return None

    kind = type(node).__name__
    if kind == "MibScalar":
        return node.getName()

    if kind != "MibTableColumn":
        return node.getName()

    row = row_for_column(mb, node)
    if row is None:
        return node.getName() + (0,)

    index_values = [
        sample_index_value(mb.importSymbols(mod_name, sym_name)[0])
        for _implied, mod_name, sym_name in row.indexNames
    ]
    try:
        inst = row.getInstIdFromIndices(*index_values)
        inst = to_wire_inst_suffix(mb, row, inst)
    except Exception:
        inst = (0,)
    return node.getName() + inst


def build_trap_var_binds(
    mb: builder.MibBuilder,
    entry: NotificationEntry,
    uptime: int = 12345,
) -> List[VarBind]:
    """Return var-binds for one SNMPv2c notification PDU."""
    var_binds: List[VarBind] = [
        (_SYS_UP_TIME, v2c.TimeTicks(uptime)),
        (_SNMP_TRAP_OID, v2c.ObjectIdentifier(entry.oid)),
    ]

    for obj_mod, obj_sym in entry.objects:
        oid = _object_oid(mb, obj_mod, obj_sym)
        if oid is None:
            continue
        try:
            node = mb.importSymbols(obj_mod, obj_sym)[0]
            value = sample_snmp_value(node)
        except Exception:
            value = v2c.OctetString("")
        var_binds.append((oid, value))

    return var_binds


def trap_label(entry: NotificationEntry) -> str:
    return f"{entry.module}::{entry.symbol}"
