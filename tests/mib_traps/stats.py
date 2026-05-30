"""
Aggregate and report MIB trap decode test results.
"""
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from tests.mib_traps.catalog import CatalogStats, NotificationEntry, catalog_stats
from tests.mib_traps.resolver import ModuleResult, TrapResult


def format_decode_report(module_results: List[ModuleResult]) -> str:
    """Full per-trap decode lines (numeric OID -> symbolic MIB name)."""
    lines: List[str] = ["=== Decode tests ===", ""]
    for mod in module_results:
        if not mod.loaded:
            lines.append(
                f"[SKIP] {mod.vendor}/{mod.module}: {mod.skip_reason}"
            )
            lines.append("")
            continue
        for tr in mod.traps:
            e = tr.entry
            status = "PASS" if tr.trap_ok else "FAIL"
            lines.append(f"[{e.vendor}/{e.module}] {e.symbol} ({status})")
            lines.append(f"  trap OID: {tr.trap_oid}")
            lines.append(f"       -> {tr.trap_message}")
            for od in tr.object_decodes:
                ostatus = "PASS" if od.ok else "FAIL"
                lines.append(
                    f"  object {od.module}::{od.symbol} ({ostatus})"
                )
                lines.append(f"       -> {od.text}")
            if not tr.object_decodes and e.objects:
                lines.append("  (no object decodes recorded)")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


@dataclass
class RunTotals:
    modules_scanned: int = 0
    modules_loaded: int = 0
    modules_skipped: int = 0
    traps_planned: int = 0
    traps_tested: int = 0
    traps_untested_module_skip: int = 0
    trap_pass: int = 0
    trap_fail: int = 0
    objects_ok: int = 0
    objects_fail: int = 0
    objects_skip: int = 0


@dataclass
class VendorTotals:
    modules: int = 0
    modules_loaded: int = 0
    modules_skipped: int = 0
    traps_planned: int = 0
    traps_tested: int = 0
    traps_untested_module_skip: int = 0
    trap_pass: int = 0
    trap_fail: int = 0
    objects_ok: int = 0
    objects_fail: int = 0
    objects_skip: int = 0


@dataclass
class RunReport:
    catalog: Optional[CatalogStats] = None
    totals: RunTotals = field(default_factory=RunTotals)
    by_vendor: Dict[str, VendorTotals] = field(default_factory=dict)
    failures: List[Dict[str, Any]] = field(default_factory=list)

    def exit_code(self, strict: bool = False) -> int:
        if self.totals.trap_fail or self.totals.objects_fail:
            return 1
        if strict and (self.totals.modules_skipped or self.totals.objects_skip):
            return 1
        return 0


def build_report(
    module_results: List[ModuleResult],
    catalog: Optional[CatalogStats] = None,
    max_failures: int = 50,
) -> RunReport:
    report = RunReport(catalog=catalog)
    t = report.totals
    t.modules_scanned = len(module_results)

    for mod in module_results:
        vt = report.by_vendor.setdefault(mod.vendor, VendorTotals())
        vt.modules += 1

        if not mod.loaded:
            t.modules_skipped += 1
            t.traps_planned += mod.traps_planned
            t.traps_untested_module_skip += mod.traps_planned
            vt.modules_skipped += 1
            vt.traps_planned += mod.traps_planned
            vt.traps_untested_module_skip += mod.traps_planned
            if len(report.failures) < max_failures:
                report.failures.append(
                    {
                        "kind": "module_skip",
                        "vendor": mod.vendor,
                        "module": mod.module,
                        "reason": mod.skip_reason,
                    }
                )
            continue

        t.modules_loaded += 1
        vt.modules_loaded += 1
        t.traps_planned += mod.traps_planned
        vt.traps_planned += mod.traps_planned

        for tr in mod.traps:
            t.traps_tested += 1
            vt.traps_tested += 1
            t.objects_ok += tr.objects_ok
            t.objects_fail += tr.objects_fail
            t.objects_skip += tr.objects_skip
            vt.objects_ok += tr.objects_ok
            vt.objects_fail += tr.objects_fail
            vt.objects_skip += tr.objects_skip

            if tr.trap_ok:
                t.trap_pass += 1
                vt.trap_pass += 1
            else:
                t.trap_fail += 1
                vt.trap_fail += 1
                if len(report.failures) < max_failures:
                    report.failures.append(
                        {
                            "kind": "trap",
                            "vendor": tr.entry.vendor,
                            "module": tr.entry.module,
                            "symbol": tr.entry.symbol,
                            "oid": ".".join(str(x) for x in tr.entry.oid),
                            "reason": tr.trap_message,
                        }
                    )

            for err in tr.object_errors:
                if len(report.failures) >= max_failures:
                    break
                report.failures.append(
                    {
                        "kind": "object",
                        "vendor": tr.entry.vendor,
                        "module": tr.entry.module,
                        "symbol": tr.entry.symbol,
                        "reason": err,
                    }
                )

    return report


def format_text_report(
    report: RunReport,
    discover_only: bool = False,
    verbose: bool = False,
    full_failures: bool = False,
) -> str:
    lines: List[str] = []

    if report.catalog:
        lines.append("=== Catalog (discover) ===")
        lines.append(f"  MIB modules with traps: {report.catalog.modules_with_traps}")
        lines.append(f"  Trap OIDs cataloged:    {report.catalog.trap_count}")
        lines.append(f"  Vendors in catalog:     {len(report.catalog.vendors)}")
        if verbose:
            for vendor, count in sorted(
                report.catalog.vendors.items(), key=lambda x: (-x[1], x[0])
            )[:30]:
                lines.append(f"    {vendor}: {count}")
        lines.append("")

    if discover_only:
        return "\n".join(lines)

    t = report.totals
    lines.append("=== Totals ===")
    lines.append(f"  Modules scanned:  {t.modules_scanned}")
    lines.append(f"  Modules loaded:   {t.modules_loaded}")
    lines.append(f"  Modules skipped:  {t.modules_skipped}")
    lines.append(f"  Traps planned:    {t.traps_planned}")
    lines.append(f"  Trap OIDs tested: {t.traps_tested}")
    if t.traps_untested_module_skip:
        lines.append(
            f"  Traps untested (module load skip): {t.traps_untested_module_skip}"
        )
    lines.append(f"  Trap pass/fail:   {t.trap_pass} / {t.trap_fail}")
    lines.append(
        f"  Object pass/fail/skip: {t.objects_ok} / {t.objects_fail} / {t.objects_skip}"
    )
    lines.append("")

    lines.append("=== By vendor ===")
    for vendor in sorted(report.by_vendor.keys(), key=lambda v: (-report.by_vendor[v].traps_tested, v)):
        v = report.by_vendor[vendor]
        if v.traps_tested == 0 and v.modules_skipped == 0:
            continue
        lines.append(
            f"  {vendor}: traps {v.trap_pass}/{v.traps_tested} pass, "
            f"objects {v.objects_ok} ok / {v.objects_fail} fail / {v.objects_skip} skip, "
            f"modules {v.modules_loaded} loaded / {v.modules_skipped} skipped"
        )
    lines.append("")

    if report.failures:
        lines.append(f"=== Failures (first {len(report.failures)}) ===")
        for f in report.failures:
            reason = f["reason"] if full_failures else f["reason"][:120]
            if f["kind"] == "module_skip":
                lines.append(
                    f"  [skip] {f['vendor']}/{f['module']}: {reason}"
                )
            elif f["kind"] == "trap":
                lines.append(
                    f"  [trap] {f['vendor']}/{f['module']}::{f['symbol']}: {reason}"
                )
            else:
                lines.append(
                    f"  [object] {f['vendor']}/{f['module']}::{f['symbol']}: {reason}"
                )

    return "\n".join(lines)


def format_json_report(report: RunReport) -> str:
    payload = {
        "catalog": (
            {
                "modules_with_traps": report.catalog.modules_with_traps,
                "trap_count": report.catalog.trap_count,
                "vendors": report.catalog.vendors,
            }
            if report.catalog
            else None
        ),
        "totals": report.totals.__dict__,
        "by_vendor": {k: v.__dict__ for k, v in report.by_vendor.items()},
        "failures": report.failures,
    }
    return json.dumps(payload, indent=2)
