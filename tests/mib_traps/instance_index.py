"""
Heuristics for sample SNMP notification instance indices.
"""
from typing import Any, Optional, Sequence, Tuple

from pysnmp.smi import view
from pysnmp.smi.rfc1902 import ObjectIdentity

# Default 6-octet index suffix (e.g. MAC-style tables)
_MAC_INDEX = (0, 0, 0, 0, 0, 1)


def _syntax_name(node) -> str:
    syntax = getattr(node, "syntax", None)
    if syntax is None:
        return ""
    return type(syntax).__name__


def index_suffix_for_object(
    mib_view: view.MibViewController,
    mod_name: str,
    sym_name: str,
) -> Tuple[int, ...]:
    """
    Build a minimal instance index suffix for (module, symbol).
    """
    try:
        oi = ObjectIdentity(mod_name, sym_name)
        oi.resolveWithMib(mib_view, ignoreErrors=True)
        node = oi.getMibNode()
    except Exception:
        return (0,)

    name = type(node).__name__
    if name in ("MibScalar",):
        return ()

    syntax = _syntax_name(node)
    if "MacAddress" in syntax or (
        hasattr(node, "syntax")
        and getattr(node.syntax, "subtypeSpec", None) is not None
    ):
        try:
            size = node.syntax.subtypeSpec[0].size
            if size and size[1] == 6:
                return _MAC_INDEX
        except (IndexError, TypeError, AttributeError):
            pass
        return _MAC_INDEX

    # Table / column: one or more integer indices
    try:
        indices = node.getIndicesFromInstId((0,) * 8)  # may not exist on all nodes
        if indices:
            return tuple(0 for _ in indices)
    except Exception:
        pass

    return (0,)


def shared_instance_index(
    mib_view: view.MibViewController,
    objects: Sequence[Tuple[str, str]],
) -> Tuple[int, ...]:
    """
    Pick one instance suffix shared across notification OBJECTS.
    Prefer MAC-style when any object suggests it.
    """
    if not objects:
        return ()

    suffixes = [
        index_suffix_for_object(mib_view, mod, sym) for mod, sym in objects
    ]
    mac_like = [s for s in suffixes if len(s) == 6]
    if mac_like:
        return mac_like[0]
    if suffixes:
        return suffixes[0]
    return (0,)


def per_object_instance_index(
    mib_view: view.MibViewController,
    mod_name: str,
    sym_name: str,
) -> Tuple[int, ...]:
    return index_suffix_for_object(mib_view, mod_name, sym_name)
