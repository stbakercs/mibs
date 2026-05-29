"""
Send SNMPv2c traps built from compiled MIB NOTIFICATION-TYPE definitions.
"""
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence

from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import config, engine
from pysnmp.entity.rfc3413 import ntforg
from pysnmp.proto.api import v2c
from pysnmp.smi import builder, error

from tests.mib_traps.catalog import NotificationEntry, group_by_module
from tests.mib_traps.varbinds import build_trap_var_binds, trap_label


@dataclass
class SendResult:
    sent: List[str] = field(default_factory=list)
    skipped_modules: List[str] = field(default_factory=list)
    skipped_traps: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def configure_snmp_engine(snmp_engine, host: str, port: int) -> None:
    config.addTransport(
        snmp_engine,
        udp.domainName,
        udp.UdpSocketTransport().openClientMode(),
    )
    config.addV1System(
        snmp_engine, "my-area", "public", transportTag="all-my-managers"
    )
    config.addTargetParams(snmp_engine, "my-creds", "my-area", "noAuthNoPriv", 1)
    config.addTargetAddr(
        snmp_engine,
        "my-nms",
        udp.domainName,
        (host, port),
        "my-creds",
        tagList="all-my-managers",
    )
    config.addNotificationTarget(
        snmp_engine, "my-notification", "my-filter", "all-my-managers", "trap"
    )
    config.addContext(snmp_engine, "")
    config.addVacmUser(snmp_engine, 2, "my-area", "noAuthNoPriv", (), (), (1, 3, 6))


def _load_module(mib_dir: str, module_name: str) -> tuple:
    mb = builder.MibBuilder()
    mb.addMibSources(builder.DirMibSource(mib_dir))
    try:
        mb.loadModules(module_name)
        return mb, ""
    except error.MibLoadError as exc:
        return mb, f"MibLoadError: {exc}"
    except Exception as exc:
        return mb, str(exc)


def send_traps(
    entries: Sequence[NotificationEntry],
    mib_dir: str,
    host: str,
    port: int,
    *,
    dry_run: bool = False,
    on_sent: Optional[Callable[[str], None]] = None,
) -> SendResult:
    result = SendResult()
    if not entries:
        return result

    snmp_engine = engine.SnmpEngine()
    configure_snmp_engine(snmp_engine, host, port)
    ntf_org = ntforg.NotificationOriginator()
    pending_errors: List[str] = []

    for module_name, module_entries in sorted(group_by_module(entries).items()):
        mb, skip_reason = _load_module(mib_dir, module_name)
        if skip_reason:
            result.skipped_modules.append(f"{module_name}: {skip_reason}")
            for entry in module_entries:
                result.skipped_traps.append(trap_label(entry))
            continue

        for entry in module_entries:
            label = trap_label(entry)
            try:
                var_binds = build_trap_var_binds(mb, entry)
            except Exception as exc:
                result.skipped_traps.append(f"{label}: {exc}")
                continue

            if dry_run:
                result.sent.append(label)
                if on_sent:
                    on_sent(label)
                continue

            def make_cb(trap_label=label):
                def cb(_snmp_engine, _req_handle, error_indication, *_rest):
                    if error_indication:
                        pending_errors.append(f"{trap_label}: {error_indication}")

                return cb

            ntf_org.sendVarBinds(
                snmp_engine,
                "my-notification",
                None,
                v2c.null,
                var_binds,
                make_cb(),
            )
            result.sent.append(label)
            if on_sent:
                on_sent(label)

    if not dry_run and result.sent:
        snmp_engine.transportDispatcher.runDispatcher()
        snmp_engine.transportDispatcher.closeDispatcher()

    result.errors.extend(pending_errors)
    return result
