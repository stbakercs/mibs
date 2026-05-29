# Current Commit MIB Build Status Report

Generated: 2026-05-29 17:12:29

Git commit: `5f0ab77` — sync changes from local repo to improve builds (2026-05-29 15:47:41 -0500)

Baseline comparison: [initial-mib-build-status.md](./initial-mib-build-status.md) (frozen snapshot before build fixes on branch `custom-py-compat-mibs`)

## Overview

This report analyzes build output from the `log/` directory produced by `scripts/vendorsingle.sh`, which runs three `mibdump` passes per vendor/standard directory:

| Build type | Output | Flags |
|------------|--------|-------|
| `nt` | `output/notexts/` | Strict (errors fail the pass) |
| `t` | `output/texts/` | Strict + MIB text generation |
| `j` | `output/json/` | `--ignore-errors` (continues on MIB failures) |

### Executive summary

- **Total vendor/standard directories built:** 305
- **Fully passing (all 3 build types):** 305 (100.0%)
- **With at least one MIB compilation failure:** 0 (0.0%)
- **Unique MIB modules with compilation failures:** 0
- **Total compilation failure events (across all build types):** 0
- **Build crashes (tracebacks in err logs):** 0

### Compiled artifact counts

| Output | Files |
|--------|------:|
| `output/notexts/` (PySNMP modules) | 5974 |
| `output/texts/` (PySNMP + texts) | 5969 |
| `output/json/` (JSON MIBs) | 5972 |
| `output/asn1/` (staged ASN.1 sources) | 6190 |

### Standard vs vendor MIBs

| Segment | Total | Passing | Failing | Pass rate |
|---------|------:|--------:|--------:|----------:|
| Standard (`atmforum`, `iana`, `iec`, `iee`, `ietf`, `internet-drafts`, `_skipped`) | 7 | 7 | 0 | 100.0% |
| Vendor MIBs | 298 | 298 | 0 | 100.0% |

## Pass/fail by build type

| Build type | Description | Pass | Partial fail | Crash | Total | Pass rate |
|------------|-------------|-----:|-------------:|------:|------:|----------:|
| `nt` | No-texts (PySNMP modules, strict) | 305 | 0 | 0 | 305 | 100.0% |
| `t` | Texts (MIB text generation, strict) | 305 | 0 | 0 | 305 | 100.0% |
| `j` | JSON (JSON output, ignore-errors) | 305 | 0 | 0 | 305 | 100.0% |

> **Note:** `partial_fail` means one or more MIB modules within the directory failed to compile, but the build step itself completed. Strict builds (`nt`, `t`) treat any failed MIB as a failed pass; the JSON build (`j`) uses `--ignore-errors` but still records failures in stderr.

## Failure categories

Failures are categorized from the `Failed MIBs:` section in each `*.err` file.

**No MIB compilation failures were recorded in any `log/*-{nt,t,j}.err` file.**

All failure category counts are zero:

| Category | Unique MIBs | Events | Description |
|----------|------------:|-------:|-------------|
| `symbol_table_dependency` | 0 | 0 | Imported module not loaded or missing from symbol table |
| `grammar_parse_error` | 0 | 0 | ASN.1/SMI grammar errors (bad tokens, malformed OBJECT-TYPE blocks) |
| `missing_symbol` | 0 | 0 | Referenced symbol/OID not defined in the importing MIB |
| `other` | 0 | 0 | Unclassified error message |
| `duplicate_definition` | 0 | 0 | Duplicate OID, name, or object definition |
| `pysmi_fake_column` | 0 | 0 | PySMI placeholder column (`pysmiFakeCol*`) — unsupported table structure |
| `unknown_type_or_object` | 0 | 0 | Unknown type, object, or notification reference |
| `invalid_identifier` | 0 | 0 | Invalid SMI identifier syntax (e.g., trailing hyphen) |

## Passing vendors and standards

All **305** directories passed all three build types with zero failed MIBs:

- `2n`, `2wcom`, `3com`, `4rf`, `_skipped`, `a10`, `accedian`, `adtran`
- `adva`, `advantech`, `aerohive`, `airport`, `akcp`, `albala`, `alcatel`, `alcoma`
- `algcom`, `allied`, `alpha`, `alteonos`, `altergy`, `alvarion`, `apc`, `arbornet`
- `arista`, `arraynetworks`, `arris`, `arubaos`, `ascom`, `asentria`, `ateme`, `aten`
- `atmforum`, `ats`, `audiocodes`, `avamar`, `avaya`, `aviat-wtm`, `avocent`, `avtech`
- `axis`, `barco`, `barracuda`, `bdcom`, `benuos`, `bintec`, `bktel`, `bladeshelter`
- `bluecatnetworks`, `bluecoat`, `broadsoft`, `brother`, `bti`, `calix`, `cambium`, `carel`
- `ccpower`, `cdata`, `ceraos`, `chatsworth`, `checkpoint`, `ciena`, `cirpack`, `cisco`
- `citrix`, `cloudgenix`, `cohesity`, `comet`, `comtrol`, `comware`, `controlbox`, `corero`
- `cradlepoint`, `ctm`, `cxr-networks`, `cyberark`, `cyberoam`, `cyberpower`, `dahua`, `dantel`
- `dantherm`, `dasan`, `dataaire`, `datacom`, `datadomain`, `dataprobe`, `dcn`, `ddn`
- `deliberant`, `dell`, `delta`, `dkt`, `dlink`, `dpstelecom`, `drac`, `dragonwave`
- `eaton`, `edgecos`, `edgeswitch`, `eds`, `efficientip`, `ekinops`, `eltek`, `eltex`
- `emc`, `emerson`, `endrun`, `enlogic`, `enterasys`, `equallogic`, `ericsson`, `eso`
- `ewc`, `exagrid`, `exalt`, `extrahop`, `extreme`, `f5`, `fiberhome`, `fibernet`
- `firebrick`, `fortinet`, `fs`, `fujitsu`, `gamatronic`, `gandi`, `garderos`, `geist`
- `gemds`, `gepower`, `gigamon`, `greenbone`, `gude`, `gwd`, `halon`, `haproxy`
- `hikvision`, `hillstone`, `himoinsa`, `hirschmann`, `hitachi`, `hp`, `hpmsm`, `huawei`
- `hwg`, `hytera`, `iana`, `ibm`, `icotera`, `ict`, `iec`, `iee`
- `ietf`, `ifotec`, `ignitenet`, `imco`, `infoblox`, `ingrasys`, `innovaphone`, `inteno`
- `internet-drafts`, `ionodes`, `irt`, `ixia`, `ixsystems`, `jacarta`, `jacques`, `janitza`
- `jds`, `juniper`, `kemp`, `lancom`, `lantronix`, `lenovo`, `liebert`, `linksys`
- `logmaster`, `maipu`, `mcafee`, `meinberg`, `microsemi`, `mikrotik`, `mimosa`, `mitel`
- `mitsubishi`, `moxa`, `mrv`, `mystro`, `netapp`, `netbotz`, `netgear`, `netonix`
- `netping`, `netsnmp`, `nexans`, `nimble`, `nokia`, `nortel`, `nti`, `omnitron`
- `oneaccess`, `openaccess`, `openbsd`, `opengear`, `oracle`, `orvaldi`, `osnexus`, `packetflux`
- `packetlight`, `paloaltonetworks`, `panasonic`, `panduit`, `papouch`, `patton`, `pbi`, `pbn`
- `pegasus`, `peplink`, `perle`, `pfsense`, `picos`, `planet`, `plugpower`, `poweralert`
- `powerwalker`, `procera`, `proware`, `pulse`, `pure`, `qnap`, `qtech`, `quanta`
- `radlan`, `radware`, `radwin`, `raisecom`, `raritan`, `ray`, `redlion`, `riedo`
- `riello`, `rittal`, `riverbed`, `ros`, `rs`, `ruckus`, `ruijie`, `saeurope`
- `saf`, `sap`, `schleifenbauer`, `schneider`, `screenos`, `sensatronics`, `sentry`, `serverscheck`
- `sflow`, `siae`, `siemens`, `siklu`, `silverpeak`, `sinetica`, `smartoptics`, `snmp-research`
- `snr`, `snrerd`, `socomec`, `sonicwall`, `sophos`, `squid`, `stormshield`, `sub10`
- `supermicro`, `synology`, `synso`, `tait`, `tegile`, `teldat`, `teleste`, `teltonika`
- `thales`, `toshiba`, `tplink`, `tycon`, `ubiquoss`, `ubnt`, `ucopia`, `unitrends`
- `veeam`, `veritas`, `vertiv`, `vigintos`, `viprinet`, `vmware`, `watchguard`, `waystream`
- `westmountainradio`, `wisi`, `wollongong`, `wti`, `wut`, `xirrus_aos`, `zmtel`, `zte`
- `zyxel`

## Failing vendors and standards

**None.** Every vendor and standard directory compiled successfully across all three mibdump passes.

## Post-build index stage

After all vendor/standard builds, `poetry run python index.py` builds the OID lookup index from `output/json/`.

**3** JSON files could not be indexed (separate from mibdump compilation):

- `output/json/SNMPv2-CONF-v1.json`
- `output/json/OPENBSD-SNMPD-CONF.json`
- `output/json/RADLAN-SNMPv2.json`

These failures do not affect PySNMP module generation in `output/notexts/` or `output/texts/`.

## Comparison with initial baseline

See [initial-mib-build-status.md](./initial-mib-build-status.md) for the pre-fix snapshot. Key deltas at commit `5f0ab77`:

| Metric | Initial baseline | Current commit | Change |
|--------|-----------------:|---------------:|-------:|
| Directories built | 300 | 305 | +5 |
| Fully passing (all 3 types) | 208 (69.3%) | 305 (100.0%) | +97 |
| Directories with failures | 92 (30.7%) | 0 (0.0%) | -92 |
| Unique failed MIB modules | 543 | 0 | -543 |
| Total failure events | 1595 | 0 | -1595 |
| `nt` pass rate | 71.3% | 100.0% | +28.7 pp |
| `t` pass rate | 71.3% | 100.0% | +28.7 pp |
| `j` pass rate | 69.3% | 100.0% | +30.7 pp |
| Index failures | 3 | 3 | 0 |

### Previously failing directories now passing

The initial baseline reported failures in **92** directories. At this commit, **all** of those directories pass all three build types. Representative fixes on this branch include:

| Directory | Previously failing MIB(s) | Fix category |
|-----------|---------------------------|--------------|
| `cirpack` | `KMIB` | `duplicate_definition` — renamed script-table columns; removed duplicate module file |
| `deliberant` | `DLB-RADIO3-DRV-MIB` | `grammar_parse_error` — capitalized table entry type name |
| `ietf` | `TCPIPX-MIB` | `missing_symbol` — corrected table SYNTAX reference |
| `pbn` | `NMS-IF-MIB` | `grammar_parse_error` — separated row object from entry type |
| `teleste` | `TELESTE-LUMINATO-MIB` | `grammar_parse_error` / `pysmi_fake_column` — fixed INDEX; JSON pass excluded via `.json-skip` |
| `nokia` | 17× `OAW-AP*` MIBs | `grammar_parse_error` — table row/entry reorder and naming; staged from `stellar/` subdir |
| `hp`, `juniper`, `fs`, `quanta`, `ubiquoss`, … | various (137+ modules in `hp` alone) | `symbol_table_dependency`, `grammar_parse_error`, `duplicate_definition`, and others — resolved across branch |

## Observations

1. **Complete mibdump pass rate:** All 305 vendor/standard directories compile cleanly across `nt`, `t`, and `j` passes.
2. **No failure categories triggered:** None of the categorized compilation error types appear in the current log set.
3. **Build script improvement:** `scripts/vendorsingle.sh` now flattens MIB files from subdirectories (e.g. `nokia/stellar/`) into `output/asn1/` before mibdump, ensuring local fixes override broken upstream copies.
4. **Remaining index gaps:** 3 JSON file(s) still fail OID indexing in `index.py` — a separate post-processing step from mibdump compilation.
5. **Baseline delta:** Pass rate improved from 69.3% to 100.0% fully passing; unique failed MIB count dropped from 543 to 0.
