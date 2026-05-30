#!/usr/bin/env python3
"""
CLI for MIB trap decode validation against output/notexts.

Examples:
    python -m tests.mib_traps.run --discover-only
    python -m tests.mib_traps.run --vendor cisco --limit 50 --verbose
    python -m tests.mib_traps.run --vendor arubaos --show-decodes
    python -m tests.mib_traps.run --all --report json
"""
import argparse
import os
import sys

from tests.mib_traps.catalog import (
    apply_limit,
    catalog_stats,
    default_mib_dir,
    filter_module,
    filter_vendor,
    list_vendors,
    scan_mib_dir,
)
from tests.mib_traps.resolver import run_resolution_tests
from tests.mib_traps.stats import (
    build_report,
    format_decode_report,
    format_json_report,
    format_text_report,
)


def _parse_vendors(values):
    out = set()
    for v in values:
        for part in v.split(","):
            part = part.strip().lower()
            if part:
                out.add(part)
    return out


def build_arg_parser():
    p = argparse.ArgumentParser(
        description="Validate NOTIFICATION-TYPE trap OID and OBJECT decoding in compiled MIBs"
    )
    p.add_argument(
        "--mib-dir",
        default=default_mib_dir(),
        help="Directory of compiled PySNMP MIB .py modules (default: output/notexts)",
    )
    p.add_argument(
        "--vendor",
        action="append",
        default=[],
        metavar="NAME",
        help="Test only these vendors (comma-separated allowed); repeat flag",
    )
    p.add_argument(
        "--all",
        action="store_true",
        help="Test all vendors (may take a long time for ~45k traps)",
    )
    p.add_argument(
        "--module",
        metavar="GLOB",
        help="Filter MIB module names, e.g. CISCO-LWAPP-*",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Maximum number of traps to test",
    )
    p.add_argument(
        "--report",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )
    p.add_argument(
        "--verbose",
        action="store_true",
        help="Print extra catalog detail; store more failures; no 120-char truncation",
    )
    p.add_argument(
        "--show-decodes",
        action="store_true",
        help="Print every trap/object decode test (numeric OID -> symbolic MIB name)",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero on module skip or object skip",
    )
    p.add_argument(
        "--discover-only",
        action="store_true",
        help="Only scan and print catalog statistics",
    )
    p.add_argument(
        "--progress",
        action="store_true",
        help="Print progress while loading modules",
    )
    p.add_argument(
        "--mibs-src-vendor",
        default=None,
        help="Path to src/vendor for module->vendor fallback",
    )
    return p


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    mib_dir = os.path.abspath(args.mib_dir)

    try:
        entries = scan_mib_dir(mib_dir, mibs_src_vendor=args.mibs_src_vendor)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2

    cat = catalog_stats(entries)

    if not args.all and not args.vendor and not args.discover_only:
        print(
            "Catalog loaded. Specify --vendor NAME or --all to run resolution tests.",
            file=sys.stderr,
        )
        print("Top vendors:", file=sys.stderr)
        for vendor, count in list_vendors(entries)[:15]:
            print(f"  {vendor}: {count}", file=sys.stderr)
        report = build_report([], catalog=cat)
        out = (
            format_json_report(report)
            if args.report == "json"
            else format_text_report(report, discover_only=True, verbose=args.verbose)
        )
        print(out)
        return 0

    if args.vendor:
        entries = filter_vendor(entries, _parse_vendors(args.vendor))
    if args.module:
        entries = filter_module(entries, args.module)
    entries = apply_limit(entries, args.limit)

    if args.all and not args.vendor:
        print(
            f"Testing all {len(entries)} traps (catalog had {cat.trap_count}). "
            "This may take a while.",
            file=sys.stderr,
        )

    if args.discover_only:
        report = build_report([], catalog=cat)
        out = (
            format_json_report(report)
            if args.report == "json"
            else format_text_report(
                report, discover_only=True, verbose=args.verbose
            )
        )
        print(out)
        return 0

    if not entries:
        print("No traps match filters.", file=sys.stderr)
        return 1

    module_results = run_resolution_tests(
        entries,
        mib_dir,
        progress=args.progress,
    )
    if args.show_decodes and args.report == "text":
        print(format_decode_report(module_results), end="")

    max_fail = 10000 if args.verbose else 50
    report = build_report(module_results, catalog=cat, max_failures=max_fail)
    if args.report == "json":
        print(format_json_report(report))
    else:
        print(
            format_text_report(
                report,
                verbose=args.verbose,
                full_failures=args.verbose or args.show_decodes,
            )
        )
    return report.exit_code(strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
