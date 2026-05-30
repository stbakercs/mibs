# mibs

This MIB Repository is based on the original repository provided by snmplabs with updates from the mib collection from librenms.

In addition, an index is published allowing remote clients to identify a MIB based on OID alone. All hosted on GitHub Pages.

pysnmplib (formerly pysnmp) applications can retrieve MIBs from `https://pysnmp.github.io/mibs/asn1/@mib@`

## Build status

Detailed reports live in `docs/`:

- [Initial baseline](./docs/initial-mib-build-status.md) — frozen snapshot before build fixes (300 directories, 2026-05-29)
- [Current commit](./docs/current-commit-mib-build-status.md) — latest full rebuild after fixes on `custom-py-compat-mibs`

| Metric | [Initial baseline](./docs/initial-mib-build-status.md) | [Current commit](./docs/current-commit-mib-build-status.md) |
|--------|--------------------------------------------------------:|------------------------------------------------------------:|
| Directories built | 300 | 305 |
| Fully passing (all 3 build types) | 208 (69.3%) | 305 (100.0%) |
| Directories with MIB compile failures | 92 (30.7%) | 0 (0.0%) |
| Unique failed MIB modules | 543 | 0 |
| Total failure events (nt + t + j) | 1,595 | 0 |
| `nt` pass rate (strict / notexts) | 71.3% | 100.0% |
| `t` pass rate (strict / texts) | 71.3% | 100.0% |
| `j` pass rate (JSON / ignore-errors) | 69.3% | 100.0% |
| Build crashes (tracebacks) | 0 | 0 |
| Post-build index failures | 3 | 3 |

Build types: `nt` → `output/notexts/`, `t` → `output/texts/`, `j` → `output/json/` (see reports for flags).

**Post-build index messages:** After compilation, `index.py` builds `output/index.csv` by mapping OIDs to MIB module names. A full build may print `Unable to index output/json/...` for three JSON files: `SNMPv2-CONF-v1.json`, `OPENBSD-SNMPD-CONF.json`, and `RADLAN-SNMPv2.json`. These are not mibdump failures—the modules compiled successfully—but they define no assignable OIDs (empty conformance stub, import-only manifest, or textual-convention-only module), so there is nothing to add to the OID lookup index. PySNMP output in `output/notexts/` and `output/texts/` is unaffected.

## Trap decode tests

After `output/notexts/` is built, `tests/mib_traps` scans compiled PySNMP modules for `NOTIFICATION-TYPE` traps and checks that each trap’s symbolic name resolves correctly and that its notification varbind objects decode to symbolic OIDs (using sample table indices where needed). Traps in MIB modules that fail to load are reported as untested skips; individual varbinds that cannot be decoded are object skips. See [local-pysnmp-tests.md](./docs/local-pysnmp-tests.md) for how to run the suite and what skips mean.

Latest full run (`poetry run python -m tests.mib_traps.run --all`):

| Metric | Total |
|--------|------:|
| Trap OIDs cataloged | 45,026 |
| MIB modules with traps | 2,098 |
| Modules loaded / skipped | 1,946 / 152 |
| Traps tested | 39,312 |
| Traps untested (module load skip) | 5,714 |
| Trap pass / fail | 39,312 / 0 |
| Notification object ok / fail / skip | 192,316 / 0 / 945 |

## Documentation

Build analysis reports in [`docs/`](./docs/):

- [initial-mib-build-status.md](./docs/initial-mib-build-status.md) — baseline pass/fail report before build fixes (300 directories; failure categories and per-vendor detail)
- [current-commit-mib-build-status.md](./docs/current-commit-mib-build-status.md) — current full-rebuild report after fixes on `custom-py-compat-mibs` (305 directories; comparison with baseline)
- [local-pysnmp-tests.md](./docs/local-pysnmp-tests.md) — trap decode test framework (run instructions, skip explanations)
