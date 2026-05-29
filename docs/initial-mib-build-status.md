# Initial MIB Build Status Report

Generated: 2026-05-29 14:48:20

## Overview

This report analyzes build output from the `log/` directory produced by `scripts/vendorsingle.sh`, which runs three `mibdump` passes per vendor/standard directory:

| Build type | Output | Flags |
|------------|--------|-------|
| `nt` | `output/notexts/` | Strict (errors fail the pass) |
| `t` | `output/texts/` | Strict + MIB text generation |
| `j` | `output/json/` | `--ignore-errors` (continues on MIB failures) |

### Executive summary

- **Total vendor/standard directories built:** 300
- **Fully passing (all 3 build types):** 208 (69.3%)
- **With at least one failure:** 92 (30.7%)
- **Unique MIB modules with failures:** 543
- **Total failure events (across all build types):** 1595
- **Build crashes (tracebacks):** 0

### Standard vs vendor MIBs

| Segment | Total | Passing | Failing | Pass rate |
|---------|------:|--------:|--------:|----------:|
| Standard (`atmforum`, `iana`, `iec`, `iee`, `ietf`, `internet-drafts`) | 6 | 5 | 1 | 83.3% |
| Vendor MIBs | 294 | 203 | 91 | 69.0% |

## Pass/fail by build type

| Build type | Description | Pass | Partial fail | Crash | Total | Pass rate |
|------------|-------------|-----:|-------------:|------:|------:|----------:|
| `nt` | No-texts (PySNMP modules, strict) | 214 | 86 | 0 | 300 | 71.3% |
| `t` | Texts (MIB text generation, strict) | 214 | 86 | 0 | 300 | 71.3% |
| `j` | JSON (JSON output, ignore-errors) | 208 | 92 | 0 | 300 | 69.3% |

> **Note:** `partial_fail` means one or more MIB modules within the directory failed to compile, but the build step itself completed. Strict builds (`nt`, `t`) treat any failed MIB as a failed pass; the JSON build (`j`) uses `--ignore-errors` but still records failures in stderr.

## Failure categories

Failures are categorized from the `Failed MIBs:` section in each `*.err` file.

### By unique MIB module (deduplicated across build types)

| Category | Unique MIBs | Description |
|----------|------------:|-------------|
| `symbol_table_dependency` | 220 | Imported module not loaded or missing from symbol table |
| `grammar_parse_error` | 159 | ASN.1/SMI grammar errors (bad tokens, malformed OBJECT-TYPE blocks) |
| `missing_symbol` | 74 | Referenced symbol/OID not defined in the importing MIB |
| `other` | 38 | Unclassified error message |
| `duplicate_definition` | 35 | Duplicate OID, name, or object definition |
| `pysmi_fake_column` | 9 | PySMI placeholder column (`pysmiFakeCol*`) — unsupported table structure |
| `unknown_type_or_object` | 6 | Unknown type, object, or notification reference |
| `invalid_identifier` | 2 | Invalid SMI identifier syntax (e.g., trailing hyphen) |

### By failure event (includes repeats across nt/t/j builds)

| Category | Events |
|----------|-------:|
| `symbol_table_dependency` | 660 |
| `grammar_parse_error` | 477 |
| `missing_symbol` | 206 |
| `other` | 114 |
| `duplicate_definition` | 105 |
| `unknown_type_or_object` | 18 |
| `pysmi_fake_column` | 9 |
| `invalid_identifier` | 6 |

## Passing vendors and standards

The following **208** directories passed all three build types with zero failed MIBs:

- `2n`, `2wcom`, `3com`, `accedian`, `adtran`, `adva`, `advantech`, `aerohive`
- `airport`, `akcp`, `albala`, `alcatel`, `alcoma`, `algcom`, `allied`, `alpha`
- `alteonos`, `altergy`, `alvarion`, `apc`, `arbornet`, `arista`, `arraynetworks`, `arris`
- `ascom`, `asentria`, `ateme`, `aten`, `atmforum`, `ats`, `avamar`, `avaya`
- `aviat-wtm`, `avocent`, `avtech`, `axis`, `barco`, `barracuda`, `benuos`, `bktel`
- `bladeshelter`, `bluecatnetworks`, `bluecoat`, `broadsoft`, `brother`, `bti`, `carel`, `ccpower`
- `checkpoint`, `citrix`, `cloudgenix`, `cohesity`, `controlbox`, `corero`, `cradlepoint`, `ctm`
- `cxr-networks`, `cyberpower`, `dantel`, `dantherm`, `datadomain`, `dataprobe`, `ddn`, `delta`
- `dpstelecom`, `drac`, `eaton`, `edgeswitch`, `efficientip`, `ekinops`, `eltek`, `eltex`
- `emc`, `enlogic`, `enterasys`, `equallogic`, `ericsson`, `eso`, `ewc`, `exagrid`
- `exalt`, `extrahop`, `f5`, `fujitsu`, `gamatronic`, `garderos`, `gemds`, `gepower`
- `gigamon`, `greenbone`, `gude`, `halon`, `haproxy`, `hirschmann`, `hitachi`, `hpmsm`
- `hwg`, `hytera`, `iana`, `icotera`, `iec`, `iee`, `ifotec`, `imco`
- `infoblox`, `ingrasys`, `innovaphone`, `inteno`, `internet-drafts`, `ionodes`, `irt`, `ixia`
- `ixsystems`, `jacarta`, `jacques`, `janitza`, `jds`, `kemp`, `lancom`, `lantronix`
- `liebert`, `logmaster`, `maipu`, `mcafee`, `meinberg`, `microsemi`, `mikrotik`, `mimosa`
- `mitel`, `moxa`, `mrv`, `mystro`, `netapp`, `netbotz`, `netonix`, `netping`
- `nexans`, `nimble`, `nortel`, `nti`, `omnitron`, `oneaccess`, `openbsd`, `opengear`
- `oracle`, `osnexus`, `packetflux`, `packetlight`, `paloaltonetworks`, `pegasus`, `peplink`, `pfsense`
- `picos`, `planet`, `plugpower`, `powerwalker`, `procera`, `pulse`, `pure`, `qnap`
- `radlan`, `radware`, `radwin`, `raritan`, `ray`, `rittal`, `riverbed`, `ros`
- `rs`, `saeurope`, `saf`, `sap`, `schleifenbauer`, `schneider`, `sensatronics`, `sentry`
- `serverscheck`, `siae`, `siklu`, `silverpeak`, `sinetica`, `smartoptics`, `snr`, `socomec`
- `squid`, `stormshield`, `sub10`, `supermicro`, `synology`, `tait`, `tegile`, `teldat`
- `thales`, `toshiba`, `tycon`, `ucopia`, `veeam`, `veritas`, `vertiv`, `vigintos`
- `viprinet`, `vmware`, `waystream`, `westmountainradio`, `wisi`, `wollongong`, `wti`, `zte`

## Failing vendors and standards

The following **92** directories had one or more MIB compilation failures:

| Directory | nt | t | j | Failed MIBs | Top failure categories |
|-----------|:--:|:--:|:--:|------------:|------------------------|
| `4rf` | FAIL | FAIL | FAIL | 2 | `symbol_table_dependency` (3), `grammar_parse_error` (3) |
| `a10` | PASS | PASS | FAIL | 1 | `missing_symbol` (1) |
| `arubaos` | FAIL | FAIL | FAIL | 1 | `other` (3) |
| `audiocodes` | FAIL | FAIL | FAIL | 2 | `invalid_identifier` (6) |
| `bdcom` | FAIL | FAIL | FAIL | 7 | `grammar_parse_error` (21) |
| `bintec` | FAIL | FAIL | FAIL | 3 | `symbol_table_dependency` (6), `grammar_parse_error` (3) |
| `calix` | FAIL | FAIL | FAIL | 12 | `symbol_table_dependency` (24), `grammar_parse_error` (12) |
| `cambium` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `cdata` | FAIL | FAIL | FAIL | 3 | `other` (3), `grammar_parse_error` (3), `duplicate_definition` (3) |
| `ceraos` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `chatsworth` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `ciena` | FAIL | FAIL | FAIL | 3 | `other` (9) |
| `cirpack` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `cisco` | PASS | PASS | FAIL | 5 | `pysmi_fake_column` (5) |
| `comet` | PASS | PASS | FAIL | 1 | `missing_symbol` (1) |
| `comtrol` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `comware` | FAIL | FAIL | FAIL | 1 | `unknown_type_or_object` (3) |
| `cyberark` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `cyberoam` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `dahua` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `dasan` | FAIL | FAIL | FAIL | 16 | `symbol_table_dependency` (30), `grammar_parse_error` (12), `duplicate_definition` (3) |
| `dataaire` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `datacom` | FAIL | FAIL | FAIL | 1 | `other` (3) |
| `dcn` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `deliberant` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `dell` | FAIL | FAIL | FAIL | 4 | `grammar_parse_error` (9), `duplicate_definition` (3) |
| `dkt` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `dlink` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `dragonwave` | FAIL | FAIL | FAIL | 2 | `unknown_type_or_object` (6) |
| `edgecos` | FAIL | FAIL | FAIL | 8 | `grammar_parse_error` (21), `unknown_type_or_object` (3) |
| `eds` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `emerson` | FAIL | FAIL | FAIL | 3 | `grammar_parse_error` (6), `pysmi_fake_column` (1) |
| `endrun` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `extreme` | FAIL | FAIL | FAIL | 2 | `other` (6) |
| `fiberhome` | FAIL | FAIL | FAIL | 2 | `grammar_parse_error` (3), `duplicate_definition` (3) |
| `fibernet` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `firebrick` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `fortinet` | FAIL | FAIL | FAIL | 2 | `duplicate_definition` (3), `other` (3) |
| `fs` | FAIL | FAIL | FAIL | 41 | `symbol_table_dependency` (75), `grammar_parse_error` (42), `duplicate_definition` (3) |
| `gandi` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `geist` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `gwd` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `hikvision` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `hillstone` | FAIL | FAIL | FAIL | 15 | `grammar_parse_error` (33), `symbol_table_dependency` (9), `duplicate_definition` (3) |
| `himoinsa` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `hp` | FAIL | FAIL | FAIL | 137 | `symbol_table_dependency` (348), `other` (30), `missing_symbol` (18) |
| `huawei` | FAIL | FAIL | FAIL | 6 | `grammar_parse_error` (6), `other` (6), `duplicate_definition` (3) |
| `ibm` | FAIL | FAIL | FAIL | 14 | `other` (15), `grammar_parse_error` (6), `duplicate_definition` (6) |
| `ict` | FAIL | FAIL | FAIL | 1 | `other` (3) |
| `ietf` | FAIL | FAIL | FAIL | 1 | `other` (3) |
| `ignitenet` | FAIL | FAIL | FAIL | 2 | `other` (3), `duplicate_definition` (3) |
| `juniper` | FAIL | FAIL | FAIL | 57 | `missing_symbol` (168), `grammar_parse_error` (3) |
| `lenovo` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `linksys` | FAIL | FAIL | FAIL | 1 | `other` (3) |
| `netsnmp` | FAIL | FAIL | FAIL | 1 | `other` (3) |
| `nokia` | FAIL | FAIL | FAIL | 21 | `grammar_parse_error` (51), `missing_symbol` (12) |
| `openaccess` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `orvaldi` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `panasonic` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `panduit` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `papouch` | PASS | PASS | FAIL | 1 | `pysmi_fake_column` (1) |
| `patton` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `pbi` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `pbn` | FAIL | FAIL | FAIL | 2 | `grammar_parse_error` (3), `duplicate_definition` (3) |
| `perle` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `poweralert` | FAIL | FAIL | FAIL | 2 | `grammar_parse_error` (6) |
| `proware` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `qtech` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `quanta` | FAIL | FAIL | FAIL | 55 | `symbol_table_dependency` (159), `duplicate_definition` (6) |
| `raisecom` | FAIL | FAIL | FAIL | 4 | `grammar_parse_error` (6), `symbol_table_dependency` (3), `duplicate_definition` (3) |
| `redlion` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `riedo` | FAIL | FAIL | FAIL | 2 | `grammar_parse_error` (3), `other` (3) |
| `riello` | FAIL | FAIL | FAIL | 2 | `grammar_parse_error` (3), `duplicate_definition` (3) |
| `ruckus` | FAIL | FAIL | FAIL | 1 | `unknown_type_or_object` (3) |
| `ruijie` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `screenos` | FAIL | FAIL | FAIL | 2 | `grammar_parse_error` (6) |
| `siemens` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `snrerd` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `sonicwall` | FAIL | FAIL | FAIL | 1 | `other` (3) |
| `sophos` | FAIL | FAIL | FAIL | 1 | `duplicate_definition` (3) |
| `synso` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `teleste` | PASS | PASS | FAIL | 1 | `pysmi_fake_column` (1) |
| `teltonika` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `tplink` | FAIL | FAIL | FAIL | 2 | `duplicate_definition` (3), `grammar_parse_error` (3) |
| `ubiquoss` | FAIL | FAIL | FAIL | 35 | `grammar_parse_error` (99), `duplicate_definition` (3), `other` (3) |
| `ubnt` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `unitrends` | FAIL | FAIL | FAIL | 1 | `other` (3) |
| `watchguard` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `wut` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `xirrus_aos` | PASS | PASS | FAIL | 1 | `missing_symbol` (1) |
| `zmtel` | FAIL | FAIL | FAIL | 1 | `grammar_parse_error` (3) |
| `zyxel` | FAIL | FAIL | FAIL | 10 | `duplicate_definition` (15), `grammar_parse_error` (9), `symbol_table_dependency` (3) |

### Failed MIB modules by directory

#### `4rf` (2 failed MIBs, 9 analyzed, 9 JSON outputs created)

- `APRISAXE-MIB-4RF` — `symbol_table_dependency`: no module "APRISAXE-TC-4RF" in symbolTable at MIB APRISAXE-MIB-4RF
- `APRISAXE-TC-4RF` — `grammar_parse_error`: Bad grammar near token type HEX_STRING, value 'E0'h at MIB APRISAXE-TC-4RF, line 221

#### `a10` (1 failed MIBs, 86 analyzed, 86 JSON outputs created)

- `ACOS-SCTP-GLOBAL-MIB` — `missing_symbol`: no symbol "global" in module "ACOS-SCTP-GLOBAL-MIB" at MIB ACOS-SCTP-GLOBAL-MIB

#### `arubaos` (1 failed MIBs, 66 analyzed, 67 JSON outputs created)

- `WLSX-WLAN-MIB` — `other`: Unknown parents for symbols: wlanAPDual5GMode, wlanAPSplit5GMode at MIB WLSX-WLAN-MIB

#### `audiocodes` (2 failed MIBs, 33 analyzed, 34 JSON outputs created)

- `AC-CONTROL-MIB` — `invalid_identifier`: Identifier should not end with '-': g723High- at MIB AC-CONTROL-MIB, line 590
- `AC-MEDIA-MIB` — `invalid_identifier`: Identifier should not end with '-': acNetCoder-9- at MIB AC-MEDIA-MIB, line 4187

#### `bdcom` (7 failed MIBs, 12 analyzed, 13 JSON outputs created)

- `NMS-CARD-SYS-MIB` — `grammar_parse_error`: Bad grammar near token type INTEGER, value INTEGER at MIB NMS-CARD-SYS-MIB, line 2367
- `NMS-CHASSIS` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value nmsAuxEntry at MIB NMS-CHASSIS, line 1155
- `NMS-EPON-OLT-PON` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value FiberProtectGroup at MIB NMS-EPON-OLT-PON, l
- `NMS-FAN-TRAP` — `grammar_parse_error`: Bad grammar near token type INTEGER, value INTEGER at MIB NMS-FAN-TRAP, line 31
- `NMS-GPON-MIB` — `grammar_parse_error`: Bad grammar near token type ACCESS, value ACCESS at MIB NMS-GPON-MIB, line 2354
- `NMS-OPTICAL-PORT-MIB` — `grammar_parse_error`: Bad grammar near token type INTEGER, value INTEGER at MIB NMS-OPTICAL-PORT-MIB, line 1173
- `NMS-POWER-MIB` — `grammar_parse_error`: Bad grammar near token type INTEGER, value INTEGER at MIB NMS-POWER-MIB, line 25

#### `bintec` (3 failed MIBs, 10 analyzed, 9 JSON outputs created)

- `BIANCA-BRICK-MIB` — `symbol_table_dependency`: no module "BINTEC-MIB" in symbolTable at MIB BIANCA-BRICK-MIB
- `BIANCA-BRICK-MIBRES-MIB` — `symbol_table_dependency`: no module "BINTEC-MIB" in symbolTable at MIB BIANCA-BRICK-MIBRES-MIB
- `BINTEC-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value InetAddressV6 at MIB BINTEC-MIB, line 227

#### `calix` (12 failed MIBs, 52 analyzed, 45 JSON outputs created)

- `AE-ALARM-TABLE-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB AE-ALARM-TABLE-MIB, line 945
- `AE-PM-TABLE-MIB` — `symbol_table_dependency`: no module "AE-ALARM-TABLE-MIB" in symbolTable at MIB AE-PM-TABLE-MIB
- `AE-VOICE-STATS-MIB` — `symbol_table_dependency`: no module "AE-ALARM-TABLE-MIB" in symbolTable at MIB AE-VOICE-STATS-MIB
- `E5-120-AS-ATM-MIB` — `symbol_table_dependency`: no module "E5-120-MIB" in symbolTable at MIB E5-120-AS-ATM-MIB
- `E5-120-IESCOMMON-MIB` — `symbol_table_dependency`: no module "E5-120-MIB" in symbolTable at MIB E5-120-IESCOMMON-MIB
- `E5-120-MIB` — `grammar_parse_error`: Bad grammar near token type QUOTED_STRING, value "0:00" at MIB E5-120-MIB, line 15645
- `E5-120-TRAPS-MIB` — `symbol_table_dependency`: no module "E5-120-MIB" in symbolTable at MIB E5-120-TRAPS-MIB
- `E5-121-AS-ATM-MIB` — `symbol_table_dependency`: no module "E5-121-MIB" in symbolTable at MIB E5-121-AS-ATM-MIB
- `E5-121-IESCOMMON-MIB` — `symbol_table_dependency`: no module "E5-121-MIB" in symbolTable at MIB E5-121-IESCOMMON-MIB
- `E5-121-MIB` — `grammar_parse_error`: Bad grammar near token type QUOTED_STRING, value "0:00" at MIB E5-121-MIB, line 15865
- `E5-121-TRAPS-MIB` — `symbol_table_dependency`: no module "E5-121-MIB" in symbolTable at MIB E5-121-TRAPS-MIB
- `E7-Calix-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value E7OperStatus at MIB E7-Calix-MIB, line 55

#### `cambium` (1 failed MIBs, 18 analyzed, 19 JSON outputs created)

- `CAMBIUM-PTP800-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value Renamed at MIB CAMBIUM-PTP800-MIB, line 67

#### `cdata` (3 failed MIBs, 29 analyzed, 30 JSON outputs created)

- `EDFA-oa-MIB` — `other`: Unknown parent symbol: enterprises at MIB EDFA-oa-MIB
- `FD-OLT-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB FD-OLT-MIB, line 2179
- `FD-SWITCH-MIB` — `duplicate_definition`: Duplicate symbol found: swPortId at MIB FD-SWITCH-MIB

#### `ceraos` (1 failed MIBs, 13 analyzed, 14 JSON outputs created)

- `MWRM-NETWORK-MIB` — `duplicate_definition`: Duplicate symbol found: alarmTrap at MIB MWRM-NETWORK-MIB

#### `chatsworth` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `CPI-UNITY-MIB` — `duplicate_definition`: Duplicate symbol found: configuration at MIB CPI-UNITY-MIB

#### `ciena` (3 failed MIBs, 101 analyzed, 101 JSON outputs created)

- `CIENA-CES-BENCHMARK-MIB` — `other`: no such bit as "p" for symbol "cienaCesBenchmarkProfileEntrySPcp" at MIB CIENA-CES-BENCHMARK-MIB
- `CIENA-CES-IP-INTERFACE-MIB` — `other`: Unknown parents for symbols: cienaCesIpDataInterfaceMac, cienaCesIpDataInterfaceStaticArpDestination
- `CIENA-CES-TIME-SYNC-MIB` — `other`: Unknown parents for symbols: cienaCesSyncPTPProfileIdentifier at MIB CIENA-CES-TIME-SYNC-MIB

#### `cirpack` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `KMIB` — `duplicate_definition`: Duplicate symbol found: kKey at MIB KMIB

#### `cisco` (5 failed MIBs, 1666 analyzed, 1662 JSON outputs created)

- `LANOPTICS-ALERTS-MIB` — `pysmi_fake_column`: No generated code for symbol pysmiFakeCol1011 at MIB LANOPTICS-ALERTS-MIB
- `LANOPTICS-ETHERNET-OPTION-MIB` — `pysmi_fake_column`: No generated code for symbol pysmiFakeCol1015 at MIB LANOPTICS-ETHERNET-OPTION-MIB
- `LANOPTICS-HUB-MIB` — `pysmi_fake_column`: No generated code for symbol pysmiFakeCol1000 at MIB LANOPTICS-HUB-MIB
- `LANOPTICS-RING-MANAGER-MIB` — `pysmi_fake_column`: No generated code for symbol pysmiFakeCol1016 at MIB LANOPTICS-RING-MANAGER-MIB
- `LANOPTICS-SYSTEM-MIB` — `pysmi_fake_column`: No generated code for symbol pysmiFakeCol1007 at MIB LANOPTICS-SYSTEM-MIB

#### `comet` (1 failed MIBs, 7 analyzed, 7 JSON outputs created)

- `T3610-MIB` — `missing_symbol`: no symbol "global" in module "T3610-MIB" at MIB T3610-MIB

#### `comtrol` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `COMTROL-ES8510-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB COMTROL-ES8510-MIB, line 2345

#### `comware` (1 failed MIBs, 320 analyzed, 320 JSON outputs created)

- `HH3C-ACFP-MIB` — `unknown_type_or_object`: unknown type "(('Integer32', ''), '')" for defval "hh3cAcfpServerMaxLifetime" of symbol "hh3cAcfpPol

#### `cyberark` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `CYBER-ARK-MIB` — `duplicate_definition`: Duplicate symbol found: cyberArkTrapGroup at MIB CYBER-ARK-MIB

#### `cyberoam` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `CYBEROAM-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB CYBEROAM-MIB, line 773

#### `dahua` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `DAHUA-SNMP-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value regularStreamInfoTableEntry at MIB DAHUA-SNM

#### `dasan` (16 failed MIBs, 110 analyzed, 101 JSON outputs created)

- `DASAN-AUTORESET-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-AUTORESET-MIB
- `DASAN-BRIDGE-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-BRIDGE-MIB
- `DASAN-DHCP-R-MIB` — `symbol_table_dependency`: no module "DASAN-ROUTER-MIB" in symbolTable at MIB DASAN-DHCP-R-MIB
- `DASAN-EPON-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB DASAN-EPON-MIB, line 1471
- `DASAN-GIGABIT-OPTIC-TRANSCEIVER-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-GIGABIT-OPTIC-TRANSCEIVER-MIB
- `DASAN-MCAST-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-MCAST-MIB
- `DASAN-NOTIFICATION` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB DASAN-NOTIFICATION, line 2431
- `DASAN-QOS-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-QOS-MIB
- `DASAN-ROUTER-MIB` — `duplicate_definition`: Duplicate symbol found: dsRouterPortCRCcnt at MIB DASAN-ROUTER-MIB
- `DASAN-SNMP-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-SNMP-MIB
- `DASAN-SWITCH-MIB` — `grammar_parse_error`: Bad grammar near token type NUMBER, value 100 at MIB DASAN-SWITCH-MIB, line 7023
- `DASAN-THRESHOLD-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-THRESHOLD-MIB
- `DASAN-TS-1000-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-TS-1000-MIB
- `DASAN-USER-MANAGEMENT-MIB` — `symbol_table_dependency`: no module "DASAN-SWITCH-MIB" in symbolTable at MIB DASAN-USER-MANAGEMENT-MIB
- `DPW-ATM-MIB` — `other`: Unknown parent symbol: mplsATMPWMIB at MIB DPW-ATM-MIB
- `SLE-PERFORMANCEMGMT-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value sleSfpmonThresholdEntry at MIB SLE-PERFORMAN

#### `dataaire` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `DataAire-dap4-al-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB DataAire-dap4-al-MIB, line 1405

#### `datacom` (1 failed MIBs, 6 analyzed, 7 JSON outputs created)

- `DMswitch-MIB` — `other`: Unknown parents for symbols: switchSessionEntry at MIB DMswitch-MIB

#### `dcn` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `DCN-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value priPowerEntry at MIB DCN-MIB, line 2829

#### `deliberant` (1 failed MIBs, 10 analyzed, 11 JSON outputs created)

- `DLB-RADIO3-DRV-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value dlbRdo3StatsEntry at MIB DLB-RADIO3-DRV-MIB,

#### `dell` (4 failed MIBs, 201 analyzed, 202 JSON outputs created)

- `DELL-SHADOW-MIB` — `duplicate_definition`: Duplicate symbol found: eventStatusChange at MIB DELL-SHADOW-MIB
- `DELL-TL2000-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB DELL-TL2000-MIB, line 85
- `DELL-TL4000-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB DELL-TL4000-MIB, line 85
- `DELLEMC-OS10-CHASSIS-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value os10ChassisProductBase at MIB DELLEMC-OS10-C

#### `dkt` (1 failed MIBs, 9 analyzed, 10 JSON outputs created)

- `IDKT-F2-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value F2FWDMacAddress at MIB IDKT-F2-MIB, line 115

#### `dlink` (1 failed MIBs, 104 analyzed, 105 JSON outputs created)

- `DLINKSW-NETWORK-ACCESS-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value 0xffffffff at MIB DLINKSW-NETWORK-ACCESS-MIB

#### `dragonwave` (2 failed MIBs, 19 analyzed, 18 JSON outputs created)

- `DRAGONWAVE-HORIZON-IDU-MIB` — `unknown_type_or_object`: unknown type "(('OctetString', ''), '')" for defval "on" of symbol "hzIduEnetPort2Description" at MI
- `HORIZON-ODU-MIB` — `unknown_type_or_object`: unknown type "(('OctetString', ''), '')" for defval "on" of symbol "hzOduEnetPort2Description" at MI

#### `edgecos` (8 failed MIBs, 32 analyzed, 32 JSON outputs created)

- `ECS4100-52T-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value radiusServerType at MIB ECS4100-52T-MIB, lin
- `ECS4110-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB ECS4110-MIB, line 1587
- `ECS4210-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB ECS4210-MIB, line 67369
- `ECS4510-MIB` — `unknown_type_or_object`: unknown type "(('OctetString', ''), '')" for defval "none" of symbol "ospfMultiProcessIfAuthKey" at 
- `ECS4610-24F-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB ECS4610-24F-MIB, line 16274
- `ES3510MA-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB ES3510MA-MIB, line 17079
- `ES3528MO-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB ES3528MO-MIB, line 11686
- `ES3528MV2-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB ES3528MV2-MIB, line 20519

#### `eds` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `EDS-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value dTrapEntry at MIB EDS-MIB, line 155

#### `emerson` (3 failed MIBs, 5 analyzed, 5 JSON outputs created)

- `EES-POWER-FERRO-MIB` — `grammar_parse_error`: Bad grammar near token type COLON_COLON_EQUAL, value ::= at MIB EES-POWER-FERRO-MIB, line 2081
- `EES-POWER-MIB` — `pysmi_fake_column`: No generated code for symbol pysmi_global at MIB EES-POWER-MIB
- `NETSURE-MIB-004-A` — `grammar_parse_error`: Bad grammar near token type COLON_COLON_EQUAL, value ::= at MIB NETSURE-MIB-004-A, line 4161

#### `endrun` (1 failed MIBs, 5 analyzed, 6 JSON outputs created)

- `TEMPUSLXUNISON-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value cdmaNTPNotPolling at MIB TEMPUSLXUNISON-MIB,

#### `extreme` (2 failed MIBs, 122 analyzed, 123 JSON outputs created)

- `BROCADE-ACL-MIB` — `other`: Unknown parents for symbols: bcsiL2NamedAclSourceMac, bcsiL2NamedAclSourceMacMask, bcsiL2NamedAclDes
- `FOUNDRY-SN-ROUTER-TRAP-MIB` — `other`: Illegal character '', 0 characters left unparsed at this stage at MIB FOUNDRY-SN-ROUTER-TRAP-MIB, l

#### `fiberhome` (2 failed MIBs, 10 analyzed, 10 JSON outputs created)

- `GEPON-OLT-COMMON-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB GEPON-OLT-COMMON-MIB, line 13903
- `WRI-SMI` — `duplicate_definition`: Duplicate module identity at MIB WRI-SMI

#### `fibernet` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `XMUX4-PLUS` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value muxEntry at MIB XMUX4-PLUS, line 247

#### `firebrick` (1 failed MIBs, 12 analyzed, 13 JSON outputs created)

- `FIREBRICK-VOIP-MIB` — `duplicate_definition`: Duplicate symbol found: fbSipCarrierIndex at MIB FIREBRICK-VOIP-MIB

#### `fortinet` (2 failed MIBs, 43 analyzed, 44 JSON outputs created)

- `FORTINET-FORTIMANAGER-FORTIANALYZER-MIB` — `duplicate_definition`: Duplicate symbol found: fmLogRate at MIB FORTINET-FORTIMANAGER-FORTIANALYZER-MIB
- `MERU-WLAN-MIB` — `other`: Unknown parents for symbols: mwlWiredIfMacAddr, mwlWirelessIfMacAddr, mwlApMacAddr, mwlStationMacAdd

#### `fs` (41 failed MIBs, 48 analyzed, 24 JSON outputs created)

- `ADMIN-MASTER-MIB` — `duplicate_definition`: Duplicate symbol found: S5330_28TX at MIB ADMIN-MASTER-MIB
- `ERRP-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB ERRP-MIB
- `FS-MIB` — `other`: Unknown parents for symbols: pethPseMainExtEntry, pethPsePortExtEntry at MIB FS-MIB
- `GARP-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GARP-MIB
- `GBNDeviceOEM-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNDeviceOEM-MIB
- `GBNDevicePoe-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNDevicePoe-MIB
- `GBNDeviceSWAPI-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value oemQueueWeightEntry at MIB GBNDeviceSWAPI-MI
- `GBNDeviceStack-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNDeviceStack-MIB
- `GBNDeviceSwitch-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNDeviceSwitch-MIB
- `GBNL2Dhcp6Snooping-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNL2Dhcp6Snooping-MIB
- `GBNL2DhcpSnooping-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNL2DhcpSnooping-MIB
- `GBNL2PortSecurity-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNL2PortSecurity-MIB
- `GBNL2PppoePlus-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNL2PppoePlus-MIB
- `GBNL2QACL-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB GBNL2QACL-MIB, line 2256
- `GBNL2Switch-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB GBNL2Switch-MIB, line 632
- `GBNL3-MIB` — `symbol_table_dependency`: no module "GBNL3If-MIB" in symbolTable at MIB GBNL3-MIB
- `GBNL3DhcpRelay-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNL3DhcpRelay-MIB
- `GBNL3IPPool-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value ipPoolEntry at MIB GBNL3IPPool-MIB, line 105
- `GBNL3If-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB GBNL3If-MIB, line 304
- `GBNL3Igmp-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNL3Igmp-MIB
- `GBNL3Ospf-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNL3Ospf-MIB
- `GBNL3PIM-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB GBNL3PIM-MIB, line 90
- `GBNL3Rip-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value gbnL3RipEntry at MIB GBNL3Rip-MIB, line 81
- `GBNL3RouteCommon-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNL3RouteCommon-MIB
- `GBNPlatformChassis-MIB` — `symbol_table_dependency`: no module "ADMIN-MASTER-MIB" in symbolTable at MIB GBNPlatformChassis-MIB
- `GBNPlatformGNLink-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB GBNPlatformGNLink-MIB, line 182
- `GBNPlatformOAM-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB GBNPlatformOAM-MIB, line 1241
- `GBNPlatformOAMMailalarm-MIB` — `symbol_table_dependency`: no module "GBNPlatformOAM-MIB" in symbolTable at MIB GBNPlatformOAMMailalarm-MIB
- `GBNPlatformOAMSntpClient-MIB` — `symbol_table_dependency`: no module "GBNPlatformOAM-MIB" in symbolTable at MIB GBNPlatformOAMSntpClient-MIB
- `GBNPlatformOAMSsh-MIB` — `symbol_table_dependency`: no module "GBNPlatformOAM-MIB" in symbolTable at MIB GBNPlatformOAMSsh-MIB
- ... and 11 more

#### `gandi` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `GANDI-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value pktjTable at MIB GANDI-MIB, line 49

#### `geist` (1 failed MIBs, 4 analyzed, 5 JSON outputs created)

- `GEIST-MIB-V3` — `duplicate_definition`: Duplicate symbol found: geist at MIB GEIST-MIB-V3

#### `gwd` (1 failed MIBs, 6 analyzed, 7 JSON outputs created)

- `GW-EPON-DEV-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value PowerVOLTHighThreshold at MIB GW-EPON-DEV-MI

#### `hikvision` (1 failed MIBs, 4 analyzed, 5 JSON outputs created)

- `HIKVISION-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value hikDiskEntry at MIB HIKVISION-MIB, line 209

#### `hillstone` (15 failed MIBs, 8 analyzed, 6 JSON outputs created)

- `HILLSTONE-DHCP-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-DHCP-MIB, line 367
- `HILLSTONE-DNS-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-DNS-MIB, line 287
- `HILLSTONE-FAN-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-FAN-MIB, line 99
- `HILLSTONE-IF-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-IF-MIB, line 117
- `HILLSTONE-IP-MIB` — `symbol_table_dependency`: no module "HILLSTONE-SMI" in symbolTable at MIB HILLSTONE-IP-MIB
- `HILLSTONE-IPSEC-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-IPSEC-MIB, line 441
- `HILLSTONE-MODULE-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-MODULE-MIB, line 197
- `HILLSTONE-NTP-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-NTP-MIB, line 323
- `HILLSTONE-POWER-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-POWER-MIB, line 233
- `HILLSTONE-PRODUCTS-MIB` — `symbol_table_dependency`: no module "HILLSTONE-SMI" in symbolTable at MIB HILLSTONE-PRODUCTS-MIB
- `HILLSTONE-SMI` — `duplicate_definition`: Duplicate symbol found: hillstoneSlotDown at MIB HILLSTONE-SMI
- `HILLSTONE-STATISTICS-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-STATISTICS-MIB, line 135
- `HILLSTONE-SYSTEM-MIB` — `symbol_table_dependency`: no module "HILLSTONE-SMI" in symbolTable at MIB HILLSTONE-SYSTEM-MIB
- `HILLSTONE-TEMPERATURE-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-TEMPERATURE-MIB, line 99
- `HILLSTONE-ZONE-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB HILLSTONE-ZONE-MIB, line 179

#### `himoinsa` (1 failed MIBs, 9 analyzed, 10 JSON outputs created)

- `DISMUNTELv00-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value PFCTotal at MIB DISMUNTELv00-MIB, line 145

#### `hp` (137 failed MIBs, 481 analyzed, 359 JSON outputs created)

- `CONFIG-MIB` — `other`: Unknown parents for symbols: hpSwitchStpPortPvstFilter, hpSwitchStpPortPvstProtection at MIB CONFIG-
- `FAN-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB FAN-MIB
- `HP-ACCT-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ACCT-MIB
- `HP-AUTH-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-AUTH-MIB
- `HP-AUTZ-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-AUTZ-MIB
- `HP-CAR-MIB` — `missing_symbol`: no symbol "snCAR" in module "HP-SN-SWITCH-GROUP-MIB" at MIB HP-CAR-MIB
- `HP-Color-LaserJet-4500-MIB` — `other`: Unknown parent symbol: enterprises at MIB HP-Color-LaserJet-4500-MIB
- `HP-DOT1X-EXTENSIONS-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-DOT1X-EXTENSIONS-MIB
- `HP-ENTITY-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ENTITY-MIB
- `HP-ENTITY-POWER-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ENTITY-POWER-MIB
- `HP-ICF-8023-RPTR` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-8023-RPTR
- `HP-ICF-ARP-PROTECT` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-ARP-PROTECT
- `HP-ICF-ARP-THROTTLE` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-ARP-THROTTLE
- `HP-ICF-AUTORUN` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-AUTORUN
- `HP-ICF-BASIC` — `other`: Unknown parents for symbols: hpicfTrapDestTimeout at MIB HP-ICF-BASIC
- `HP-ICF-BFD-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-BFD-MIB
- `HP-ICF-BRIDGE` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-BRIDGE
- `HP-ICF-BYOD-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-BYOD-MIB
- `HP-ICF-CHAIN` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-CHAIN
- `HP-ICF-CHASSIS` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-CHASSIS
- `HP-ICF-CONFIG-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-CONFIG-MIB
- `HP-ICF-CONNECTION-RATE-FILTER` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-CONNECTION-RATE-FILTER
- `HP-ICF-CORE-DUMP-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-CORE-DUMP-MIB
- `HP-ICF-DEBUGLOG-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-DEBUGLOG-MIB
- `HP-ICF-DEV-CONF-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-DEV-CONF-MIB
- `HP-ICF-DEVICEIDENTITY-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-DEVICEIDENTITY-MIB
- `HP-ICF-DHCP-SNOOP-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-DHCP-SNOOP-MIB
- `HP-ICF-DHCPCLIENT-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-DHCPCLIENT-MIB
- `HP-ICF-DHCPV4-SERVER-MIB` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-DHCPV4-SERVER-MIB
- `HP-ICF-DHCPv6-RELAY` — `symbol_table_dependency`: no module "HP-ICF-OID" in symbolTable at MIB HP-ICF-DHCPv6-RELAY
- ... and 107 more

#### `huawei` (6 failed MIBs, 270 analyzed, 270 JSON outputs created)

- `HUAWEI-BRAS-IPTN-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value hwIptnEnableEntry at MIB HUAWEI-BRAS-IPTN-MI
- `HUAWEI-MGMD-STD-MIB` — `other`: Illegal character '?', 11961 characters left unparsed at this stage at MIB HUAWEI-MGMD-STD-MIB, line
- `HUAWEI-MIB` — `pysmi_fake_column`: No generated code for symbol pysmi_as at MIB HUAWEI-MIB
- `HUAWEI-QINQ-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value DISABLE at MIB HUAWEI-QINQ-MIB, line 3049
- `HUAWEI-SITE-MONITOR-MIB` — `duplicate_definition`: Duplicate symbol found: hwRectifiersInslotChange at MIB HUAWEI-SITE-MONITOR-MIB
- `HUAWEI-XPON-MIB` — `other`: Unknown parents for symbols: hwEponDeviceOntExtendedFirmwareVersion at MIB HUAWEI-XPON-MIB

#### `ibm` (14 failed MIBs, 83 analyzed, 79 JSON outputs created)

- `GPFS-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB GPFS-MIB, line 255
- `IBM-3200-MIB` — `duplicate_definition`: Duplicate symbol found: eventStatusChange at MIB IBM-3200-MIB
- `IBM-Director-Alert-MIB` — `other`: Unknown parent symbol: enterprises at MIB IBM-Director-Alert-MIB
- `IBM-ELAN-MIB` — `other`: Unknown parents for symbols: atmDevLineSpeed, idleVccTime, lecsMaxVccs at MIB IBM-ELAN-MIB
- `IBM-GbTOR-10G-L2L3-MIB` — `missing_symbol`: no symbol "if" in module "IBM-GbTOR-10G-L2L3-MIB" at MIB IBM-GbTOR-10G-L2L3-MIB
- `IBM-GbTOR-G8052-MIB` — `missing_symbol`: no symbol "if" in module "IBM-GbTOR-G8052-MIB" at MIB IBM-GbTOR-G8052-MIB
- `IBM-GbTOR-G8264-MIB` — `missing_symbol`: no symbol "if" in module "IBM-GbTOR-G8264-MIB" at MIB IBM-GbTOR-G8264-MIB
- `IBM-GbTOR-G8264CS-MIB` — `missing_symbol`: no symbol "if" in module "IBM-GbTOR-G8264CS-MIB" at MIB IBM-GbTOR-G8264CS-MIB
- `IBM-GbTOR-G8264T-MIB` — `missing_symbol`: no symbol "if" in module "IBM-GbTOR-G8264T-MIB" at MIB IBM-GbTOR-G8264T-MIB
- `IBM-LAN-EMULATION-EXTENSION-MIB` — `other`: Unknown parents for symbols: ibmVlanConfAgingTimer at MIB IBM-LAN-EMULATION-EXTENSION-MIB
- `IBM-LES-LECS-MIB` — `other`: Unknown parents for symbols: lesLecsAtmDevLineSpeed at MIB IBM-LES-LECS-MIB
- `IBM-NetFinity-Text-Alert-MIB` — `other`: Illegal character '', 0 characters left unparsed at this stage at MIB IBM-NetFinity-Text-Alert-MIB,
- `IBMIROCAUTH-MIB` — `grammar_parse_error`: Bad grammar near token type ., value . at MIB IBMIROCAUTH-MIB, line 851
- `IMM-MIB` — `duplicate_definition`: Duplicate symbol found: ctrlName at MIB IMM-MIB

#### `ict` (1 failed MIBs, 11 analyzed, 12 JSON outputs created)

- `ICT-DISTRIBUTION-PANEL-MIB` — `other`: Unknown parents for symbols: busEntry at MIB ICT-DISTRIBUTION-PANEL-MIB

#### `ietf` (1 failed MIBs, 342 analyzed, 343 JSON outputs created)

- `TCPIPX-MIB` — `other`: Unknown parents for symbols: tcpUnspecConnEntry at MIB TCPIPX-MIB

#### `ignitenet` (2 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `ES4552BH2-MIB` — `other`: Unknown parents for symbols: pethPseMainExtEntry, pethPsePortExtEntry at MIB ES4552BH2-MIB
- `IGNITENET-MIB` — `duplicate_definition`: Duplicate symbol found: EthernetIndex at MIB IGNITENET-MIB

#### `juniper` (57 failed MIBs, 381 analyzed, 326 JSON outputs created)

- `GGSN-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value pgwApnSaccRatingGroupStats at MIB GGSN-MIB, 
- `IPMCAST-MIB-CAPABILITY` — `missing_symbol`: no symbol "jnxAgentCapability" in module "JUNIPER-SMI" at MIB IPMCAST-MIB-CAPABILITY
- `JNX-DOT3OAM-CAPABILITY` — `missing_symbol`: no symbol "jnxAgentCapability" in module "JUNIPER-SMI" at MIB JNX-DOT3OAM-CAPABILITY
- `JNX-IF-CAPABILITY` — `missing_symbol`: no symbol "jnxAgentCapability" in module "JUNIPER-SMI" at MIB JNX-IF-CAPABILITY
- `JNX-IP-CAPABILITY` — `missing_symbol`: no symbol "jnxAgentCapability" in module "JUNIPER-SMI" at MIB JNX-IP-CAPABILITY
- `JNX-MPLS-TE-P2MP-STD-MIB` — `missing_symbol`: no symbol "jnxP2mpExperiment" in module "JUNIPER-EXPERIMENT-MIB" at MIB JNX-MPLS-TE-P2MP-STD-MIB
- `JNX-OPT-IF-EXT-MIB` — `missing_symbol`: no symbol "jnxoptIfMibRoot" in module "JUNIPER-SMI" at MIB JNX-OPT-IF-EXT-MIB
- `JNX-OPT-IF-MIB` — `missing_symbol`: no symbol "jnxoptIfMibRoot" in module "JUNIPER-SMI" at MIB JNX-OPT-IF-MIB
- `JNX-PPP-MIB` — `missing_symbol`: no symbol "jnxPppMibRoot" in module "JUNIPER-SMI" at MIB JNX-PPP-MIB
- `JNX-PPPOE-MIB` — `missing_symbol`: no symbol "jnxPppoeMibRoot" in module "JUNIPER-SMI" at MIB JNX-PPPOE-MIB
- `JNX-SNMPv2-CAPABILITY` — `missing_symbol`: no symbol "jnxAgentCapability" in module "JUNIPER-SMI" at MIB JNX-SNMPv2-CAPABILITY
- `JUNIPER-ALARM-EXT-MIB` — `missing_symbol`: no symbol "jnxAlarmExtMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-ALARM-EXT-MIB
- `JUNIPER-DOM-MIB` — `missing_symbol`: no symbol "jnxDomMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-DOM-MIB
- `JUNIPER-FABRIC-CHASSIS` — `missing_symbol`: no symbol "jnxDcfMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-FABRIC-CHASSIS
- `JUNIPER-FABRIC-MIB` — `missing_symbol`: no symbol "jnxFabricMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-FABRIC-MIB
- `JUNIPER-FRU-MIB` — `missing_symbol`: no symbol "jnxFruMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-FRU-MIB
- `JUNIPER-IFOPTICS-MIB` — `missing_symbol`: no symbol "jnxOpticsMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-IFOPTICS-MIB
- `JUNIPER-IFOTN-MIB` — `missing_symbol`: no symbol "jnxIfOtnMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-IFOTN-MIB
- `JUNIPER-JDHCP-MIB` — `missing_symbol`: no symbol "jnxJdhcpMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-JDHCP-MIB
- `JUNIPER-JDHCPV6-MIB` — `missing_symbol`: no symbol "jnxJdhcpv6MibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-JDHCPV6-MIB
- `JUNIPER-JVAE-INFRA-MIB` — `missing_symbol`: no symbol "jnxJVAEMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-JVAE-INFRA-MIB
- `JUNIPER-JVAE-NODE-MIB` — `missing_symbol`: no symbol "jnxJVAEMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-JVAE-NODE-MIB
- `JUNIPER-LICENSE-MIB` — `missing_symbol`: no symbol "jnxLicenseMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-LICENSE-MIB
- `JUNIPER-MAG-MIB` — `missing_symbol`: no symbol "jnxMagMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-MAG-MIB
- `JUNIPER-MBG-SMI` — `missing_symbol`: no symbol "jnxMobileGatewayMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-MBG-SMI
- `JUNIPER-MOBILE-GATEWAY-AAA-MIB` — `missing_symbol`: no symbol "jnxMobileGatewayMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-MOBILE-GATEWAY-AAA-MIB
- `JUNIPER-MOBILE-GATEWAY-DHCP-MIB` — `missing_symbol`: no symbol "jnxMobileGatewayMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-MOBILE-GATEWAY-DHCP-MIB
- `JUNIPER-MOBILE-GATEWAY-EXAMPLE-MIB` — `missing_symbol`: no symbol "jnxExampleMibRoot" in module "JUNIPER-EXPERIMENT-MIB" at MIB JUNIPER-MOBILE-GATEWAY-EXAMP
- `JUNIPER-MOBILE-GATEWAY-GTP-MIB` — `missing_symbol`: no symbol "jnxMobileGatewayMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-MOBILE-GATEWAY-GTP-MIB
- `JUNIPER-MOBILE-GATEWAY-RMPS-MIB` — `missing_symbol`: no symbol "jnxMobileGatewayMibRoot" in module "JUNIPER-SMI" at MIB JUNIPER-MOBILE-GATEWAY-RMPS-MIB
- ... and 27 more

#### `lenovo` (1 failed MIBs, 13 analyzed, 14 JSON outputs created)

- `LENOVO-PRODUCTS-MIB` — `duplicate_definition`: Duplicate symbol found: ne2572 at MIB LENOVO-PRODUCTS-MIB

#### `linksys` (1 failed MIBs, 120 analyzed, 121 JSON outputs created)

- `LINKSYS-MODEL-MIB` — `other`: Illegal character '', 0 characters left unparsed at this stage at MIB LINKSYS-MODEL-MIB, line 7107

#### `netsnmp` (1 failed MIBs, 19 analyzed, 20 JSON outputs created)

- `NET-SNMP-PASS-MIB` — `other`: Unknown parents for symbols: netSnmpPassInteger64 at MIB NET-SNMP-PASS-MIB

#### `nokia` (21 failed MIBs, 203 analyzed, 200 JSON outputs created)

- `ALCATEL-IND1-GROUP-MOBILITY-MIB` — `missing_symbol`: no symbol "groupmobilityTraps" in module "ALCATEL-IND1-BASE" at MIB ALCATEL-IND1-GROUP-MOBILITY-MIB
- `ALCATEL-IND1-INLINE-POWER-MIB` — `missing_symbol`: no symbol "pethTraps" in module "ALCATEL-IND1-BASE" at MIB ALCATEL-IND1-INLINE-POWER-MIB
- `ALCATEL-IND1-LBD-MIB` — `missing_symbol`: no symbol "alaLbdTraps" in module "ALCATEL-IND1-BASE" at MIB ALCATEL-IND1-LBD-MIB
- `ALCATEL-IND1-WCCP-MIB` — `missing_symbol`: no symbol "wccpTraps" in module "ALCATEL-IND1-BASE" at MIB ALCATEL-IND1-WCCP-MIB
- `OAW-AP1101` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1101, line 703
- `OAW-AP1201` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1201, line 2809
- `OAW-AP1201BG` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1201BG, line 1756
- `OAW-AP1201H` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1201H, line 3160
- `OAW-AP1201HL` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1201HL, line 352
- `OAW-AP1201L` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1201L, line 1405
- `OAW-AP1221` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1221, line 3511
- `OAW-AP1222` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1222, line 352
- `OAW-AP1231` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1231, line 2458
- `OAW-AP1232` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1232, line 1054
- `OAW-AP1251` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1251, line 1756
- `OAW-AP1251D` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1251D, line 1054
- `OAW-AP1321` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1321, line 2107
- `OAW-AP1322` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1322, line 703
- `OAW-AP1361` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1361, line 352
- `OAW-AP1361D` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1361D, line 1405
- `OAW-AP1362` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OAW-AP1362, line 3862

#### `openaccess` (1 failed MIBs, 4 analyzed, 5 JSON outputs created)

- `OACOMMON-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB OACOMMON-MIB, line 509

#### `orvaldi` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `companyMIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value companyMIB at MIB companyMIB, line 19

#### `panasonic` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `ipPbxNs-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value ipPbxNs-MIB at MIB ipPbxNs-MIB, line 13

#### `panduit` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `PANDUIT-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value pdug5IdentEntry at MIB PANDUIT-MIB, line 165

#### `papouch` (1 failed MIBs, 9 analyzed, 9 JSON outputs created)

- `QUIDOS-MIB` — `pysmi_fake_column`: No generated code for symbol pysmi_in at MIB QUIDOS-MIB

#### `patton` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `SMARTNODE-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value cpuEntry at MIB SMARTNODE-MIB, line 1989

#### `pbi` (1 failed MIBs, 10 analyzed, 11 JSON outputs created)

- `PBI-4000P-5000P-MIB` — `duplicate_definition`: Duplicate symbol found: multicastIPAddress at MIB PBI-4000P-5000P-MIB

#### `pbn` (2 failed MIBs, 10 analyzed, 11 JSON outputs created)

- `NMS-IF-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value ifSfpParameterEntry at MIB NMS-IF-MIB, line 
- `PBN-MIB` — `duplicate_definition`: Duplicate symbol found: upTime at MIB PBN-MIB

#### `perle` (1 failed MIBs, 5 analyzed, 6 JSON outputs created)

- `PERLE-IOLAN-SDS-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value Description at MIB PERLE-IOLAN-SDS-MIB, line

#### `poweralert` (2 failed MIBs, 6 analyzed, 7 JSON outputs created)

- `TRIPPLITE-12X` — `grammar_parse_error`: Bad grammar near token type QUOTED_STRING, value "Corrected spelling errors" at MIB TRIPPLITE-12X, l
- `TRIPPLITE-MIB` — `grammar_parse_error`: Bad grammar near token type STRING, value STRING at MIB TRIPPLITE-MIB, line 603

#### `proware` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `proware-SNMP-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value proware-SNMP-MIB at MIB proware-SNMP-MIB, li

#### `qtech` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `QTECH-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value priPowerEntry at MIB QTECH-MIB, line 1407

#### `quanta` (55 failed MIBs, 87 analyzed, 35 JSON outputs created)

- `NETGEAR-AUTHENTICATION-MANAGER-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-AUTHENTICATION-MANAGER-MIB
- `NETGEAR-BGP-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-BGP-MIB
- `NETGEAR-BOXSERVICES-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-BOXSERVICES-PRIVATE-MIB
- `NETGEAR-CAPTIVE-PORTAL-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-CAPTIVE-PORTAL-MIB
- `NETGEAR-DCBX-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-DCBX-MIB
- `NETGEAR-DENIALOFSERVICE-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-DENIALOFSERVICE-PRIVATE-MIB
- `NETGEAR-DHCPCLIENT-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-DHCPCLIENT-PRIVATE-MIB
- `NETGEAR-DHCPSERVER-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-DHCPSERVER-PRIVATE-MIB
- `NETGEAR-DNS-RESOLVER-CONTROL-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-DNS-RESOLVER-CONTROL-MIB
- `NETGEAR-DOT1X-ADVANCED-FEATURES-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-DOT1X-ADVANCED-FEATURES-MIB
- `NETGEAR-DOT1X-AUTHENTICATION-SERVER-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-DOT1X-AUTHENTICATION-SERVER-MIB
- `NETGEAR-FIPSNOOPING-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-FIPSNOOPING-MIB
- `NETGEAR-GREENETHERNET-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-GREENETHERNET-PRIVATE-MIB
- `NETGEAR-INVENTORY-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-INVENTORY-MIB
- `NETGEAR-IPV6-LOOPBACK-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-IPV6-LOOPBACK-MIB
- `NETGEAR-IPV6-TUNNEL-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-IPV6-TUNNEL-MIB
- `NETGEAR-ISDP-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-ISDP-MIB
- `NETGEAR-KEYING-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-KEYING-PRIVATE-MIB
- `NETGEAR-LLPF-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-LLPF-PRIVATE-MIB
- `NETGEAR-LOGGING-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-LOGGING-MIB
- `NETGEAR-LOOPBACK-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-LOOPBACK-MIB
- `NETGEAR-MGMT-SECURITY-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-MGMT-SECURITY-MIB
- `NETGEAR-MMRP-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-MMRP-MIB
- `NETGEAR-MRP-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-MRP-MIB
- `NETGEAR-MULTICAST-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-MULTICAST-MIB
- `NETGEAR-MVR-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-MVR-PRIVATE-MIB
- `NETGEAR-MVRP-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-MVRP-MIB
- `NETGEAR-NSF-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-NSF-MIB
- `NETGEAR-OUTBOUNDTELNET-PRIVATE-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-OUTBOUNDTELNET-PRIVATE-MIB
- `NETGEAR-PFC-MIB` — `symbol_table_dependency`: no module "QUANTA-LB6M-REF-MIB" in symbolTable at MIB NETGEAR-PFC-MIB
- ... and 25 more

#### `raisecom` (4 failed MIBs, 22 analyzed, 22 JSON outputs created)

- `RAISECOM-COMMON-MANAGEMENT-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB RAISECOM-COMMON-MANAGEMENT-MIB, line 204
- `RAISECOM-FANMONITOR-MIB` — `symbol_table_dependency`: no module "RAISECOM-SYSTEM-MIB" in symbolTable at MIB RAISECOM-FANMONITOR-MIB
- `RAISECOM-PON-DEVICE-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value raisecomSubFanEntry at MIB RAISECOM-PON-DEVI
- `RAISECOM-SYSTEM-MIB` — `duplicate_definition`: Duplicate symbol found: raisecomDeviceType at MIB RAISECOM-SYSTEM-MIB

#### `redlion` (1 failed MIBs, 4 analyzed, 5 JSON outputs created)

- `SIXNET-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value sxRingEntry at MIB SIXNET-MIB, line 603

#### `riedo` (2 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `NETTRACK-E3METER-CTR-SNMP-MIB` — `grammar_parse_error`: Bad grammar near token type NUMBER, value 1 at MIB NETTRACK-E3METER-CTR-SNMP-MIB, line 931
- `NETTRACK-E3METER-SNMP-MIB` — `other`: Unknown parents for symbols: e3IpmRcmTableEntry at MIB NETTRACK-E3METER-SNMP-MIB

#### `riello` (2 failed MIBs, 11 analyzed, 12 JSON outputs created)

- `RIELLOMDU-MIB` — `grammar_parse_error`: Bad grammar near token type UPPERCASE_IDENTIFIER, value Imminent at MIB RIELLOMDU-MIB, line 431
- `RIELLOUPS-MIB` — `duplicate_definition`: Duplicate symbol found: rupsAlarmShutdownImminent at MIB RIELLOUPS-MIB

#### `ruckus` (1 failed MIBs, 28 analyzed, 28 JSON outputs created)

- `RUCKUS-ZD-WLAN-CONFIG-MIB` — `unknown_type_or_object`: unknown type "(('Integer32', ''), '')" for defval "none" of symbol "ruckusZDWLANConfigWirelessWhiteL

#### `ruijie` (1 failed MIBs, 26 analyzed, 26 JSON outputs created)

- `MY-SMI` — `duplicate_definition`: Duplicate module identity at MIB MY-SMI

#### `screenos` (2 failed MIBs, 53 analyzed, 54 JSON outputs created)

- `NETSCREEN-SET-ADMIN-USR-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB NETSCREEN-SET-ADMIN-USR-MIB, line 229
- `NETSCREEN-UAC-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB NETSCREEN-UAC-MIB, line 207

#### `siemens` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `SN-MSPS-SCX200-MIB` — `duplicate_definition`: Duplicate symbol found: snMspsTrapRmActiveState at MIB SN-MSPS-SCX200-MIB

#### `snrerd` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `SNR-ERD-4` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value dtsEntry at MIB SNR-ERD-4, line 82

#### `sonicwall` (1 failed MIBs, 7 analyzed, 8 JSON outputs created)

- `SNWL-SSLVPN-MIB` — `other`: Unknown parent symbol: sonicwall at MIB SNWL-SSLVPN-MIB

#### `sophos` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `SFOS-FIREWALL-MIB` — `duplicate_definition`: Duplicate symbol found: sfosIPSecVpnPolicyName at MIB SFOS-FIREWALL-MIB

#### `synso` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `SYNSO-UPSMIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value syupsOutletEntry at MIB SYNSO-UPSMIB, line 5

#### `teleste` (1 failed MIBs, 13 analyzed, 13 JSON outputs created)

- `TELESTE-LUMINATO-MIB` — `pysmi_fake_column`: No generated code for symbol pysmiFakeCol1000 at MIB TELESTE-LUMINATO-MIB

#### `teltonika` (1 failed MIBs, 5 analyzed, 6 JSON outputs created)

- `TELTONIKA-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB TELTONIKA-MIB, line 63

#### `tplink` (2 failed MIBs, 25 analyzed, 26 JSON outputs created)

- `TPLINK-POWER-OVER-ETHERNET-MIB` — `duplicate_definition`: Duplicate symbol found: tpPoeRecoveryPort at MIB TPLINK-POWER-OVER-ETHERNET-MIB
- `TPLINK-SYSINFO-MIB` — `grammar_parse_error`: Bad grammar near token type NUMBER, value 9600 at MIB TPLINK-SYSINFO-MIB, line 231

#### `ubiquoss` (35 failed MIBs, 43 analyzed, 44 JSON outputs created)

- `UBIQUOSS-10GEPON-PM-GROUP-MIB` — `duplicate_definition`: Duplicate symbol found: pm10gHqosQueue0Bytes at MIB UBIQUOSS-10GEPON-PM-GROUP-MIB
- `UBIQUOSS-10GEPON-PON-MAC-GROUP-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB UBIQUOSS-10GEPON-PON-MAC-GROUP-MIB
- `UBIQUOSS-10GEPON-PON-PROFILE-GROUP-MIB` — `grammar_parse_error`: Bad grammar near token type COLON_COLON_EQUAL, value ::= at MIB UBIQUOSS-10GEPON-PON-PROFILE-GROUP-M
- `UBIQUOSS-10GEPON-SOFTWARE-MANAGEMENT-GROUP-MIB` — `other`: Unknown parent symbol: ubiSoftwareMIB at MIB UBIQUOSS-10GEPON-SOFTWARE-MANAGEMENT-GROUP-MIB
- `UBIQUOSS-EPON-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBIQUOSS-EPON-MIB, line 2571
- `UBIQUOSS-EPON-ONTMANAGER-GROUP-MIB` — `grammar_parse_error`: Bad grammar near token type (, value ( at MIB UBIQUOSS-EPON-ONTMANAGER-GROUP-MIB, line 355
- `UBIQUOSS-EPON-PM-GROUP-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBIQUOSS-EPON-PM-GROUP-MIB, line 6075
- `UBIQUOSS-EPON-PM-MIB` — `grammar_parse_error`: Bad grammar near token type COLON_COLON_EQUAL, value ::= at MIB UBIQUOSS-EPON-PM-MIB, line 127
- `UBIQUOSS-EPON-PON-MAC-GROUP-MIB` — `grammar_parse_error`: Bad grammar near token type OBJECT_TYPE, value OBJECT-TYPE at MIB UBIQUOSS-EPON-PON-MAC-GROUP-MIB, l
- `UBIQUOSS-EPON-PON-PROFILE-GROUP-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBIQUOSS-EPON-PON-PROFILE-GROUP-MIB, line 7623
- `UBIQUOSS-EPON-SERVICE-POLICY-GROUP-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBIQUOSS-EPON-SERVICE-POLICY-GROUP-MIB, line 707
- `UBIQUOSS-EPON-SOFTWARE-MANAGEMENT-GROUP-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBIQUOSS-EPON-SOFTWARE-MANAGEMENT-GROUP-MIB, line 1353
- `UBIQUOSS-SWITCH-INTERFACE-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB UBIQUOSS-SWITCH-INTERFACE-MIB, line 1801
- `UBQS-ACCESS-LIST-MIB` — `grammar_parse_error`: Bad grammar near token type (, value ( at MIB UBQS-ACCESS-LIST-MIB, line 2361
- `UBQS-ARP-MIB` — `grammar_parse_error`: Bad grammar near token type (, value ( at MIB UBQS-ARP-MIB, line 495
- `UBQS-AUTO-RESET-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-AUTO-RESET-MIB, line 3369
- `UBQS-CFM-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-CFM-MIB, line 3777
- `UBQS-CPU-MAC-FILTER-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-CPU-MAC-FILTER-MIB, line 389
- `UBQS-DOT1BRIDGE-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-DOT1BRIDGE-MIB, line 399
- `UBQS-ENTITY-ALARM-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-ENTITY-ALARM-MIB, line 573
- `UBQS-ENTITY-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-ENTITY-MIB, line 1845
- `UBQS-ERPS-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-ERPS-MIB, line 195
- `UBQS-INTERFACE-MIB` — `grammar_parse_error`: Bad grammar near token type (, value ( at MIB UBQS-INTERFACE-MIB, line 2183
- `UBQS-MPLS-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-MPLS-MIB, line 1721
- `UBQS-MPLS-PW-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-MPLS-PW-MIB, line 1309
- `UBQS-MPLS-RSVP-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-MPLS-RSVP-MIB, line 5279
- `UBQS-NTP-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-NTP-MIB, line 11931
- `UBQS-OSPF-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-OSPF-MIB, line 2015
- `UBQS-PB-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-PB-MIB, line 6913
- `UBQS-PON-LAG-MIB` — `grammar_parse_error`: Bad grammar near token type }, value } at MIB UBQS-PON-LAG-MIB, line 503
- ... and 5 more

#### `ubnt` (1 failed MIBs, 8 analyzed, 9 JSON outputs created)

- `UBNT-AirFIBER-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB UBNT-AirFIBER-MIB, line 163

#### `unitrends` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `UNITRENDS-SNMP` — `other`: Unknown parents for symbols: eventlogProbeTableEntry at MIB UNITRENDS-SNMP

#### `watchguard` (1 failed MIBs, 21 analyzed, 22 JSON outputs created)

- `WATCHGUARD-POLICY-MIB` — `grammar_parse_error`: Bad grammar near token type {, value { at MIB WATCHGUARD-POLICY-MIB, line 587

#### `wut` (1 failed MIBs, 10 analyzed, 11 JSON outputs created)

- `WebGraph-Thermo-Hygro-Barometer-MIB` — `grammar_parse_error`: Bad grammar near token type COLON_COLON_EQUAL, value ::= at MIB WebGraph-Thermo-Hygro-Barometer-MIB,

#### `xirrus_aos` (1 failed MIBs, 4 analyzed, 4 JSON outputs created)

- `XIRRUS-MIB` — `missing_symbol`: no symbol "global" in module "XIRRUS-MIB" at MIB XIRRUS-MIB

#### `zmtel` (1 failed MIBs, 0 analyzed, 2 JSON outputs created)

- `ZMTEL-ODU-MIB` — `grammar_parse_error`: Bad grammar near token type MODULE_IDENTITY, value MODULE-IDENTITY at MIB ZMTEL-ODU-MIB, line 39

#### `zyxel` (10 failed MIBs, 34 analyzed, 33 JSON outputs created)

- `IES5206-MIB` — `grammar_parse_error`: Bad grammar near token type NUMBER, value 1 at MIB IES5206-MIB, line 20749
- `IES5206-TRAPS-MIB` — `symbol_table_dependency`: no module "IES5206-MIB" in symbolTable at MIB IES5206-TRAPS-MIB
- `ZYXEL-ES-COMMON` — `duplicate_definition`: Duplicate module identity at MIB ZYXEL-ES-COMMON
- `ZYXEL-GS2200-24-MIB` — `duplicate_definition`: Duplicate symbol found: newRoot at MIB ZYXEL-GS2200-24-MIB
- `ZYXEL-GS4012F-MIB` — `duplicate_definition`: Duplicate symbol found: newRoot at MIB ZYXEL-GS4012F-MIB
- `ZYXEL-IES5000-MIB` — `grammar_parse_error`: Bad grammar near token type MAX_ACCESS, value MAX-ACCESS at MIB ZYXEL-IES5000-MIB, line 19337
- `ZYXEL-MGS3712-MIB` — `duplicate_definition`: Duplicate symbol found: newRoot at MIB ZYXEL-MGS3712-MIB
- `ZYXEL-PRESTIGE-MIB` — `other`: Unknown parents for symbols: bridgeStaticRouteEtherAddr at MIB ZYXEL-PRESTIGE-MIB
- `ZYXEL-SAM1216` — `duplicate_definition`: Duplicate symbol found: igmpGroupIp at MIB ZYXEL-SAM1216
- `ZYXEL-ZYWALL-ZLD-COMMON-MIB` — `grammar_parse_error`: Bad grammar near token type LOWERCASE_IDENTIFIER, value vpnStatusEntry at MIB ZYXEL-ZYWALL-ZLD-COMMO

## Most frequently failing MIB modules

Top 30 MIB modules by number of vendor directories affected:

| MIB module | Vendors affected | Primary category |
|------------|----------------:|------------------|
| `AC-CONTROL-MIB` | 1 | `invalid_identifier` |
| `AC-MEDIA-MIB` | 1 | `invalid_identifier` |
| `ACOS-SCTP-GLOBAL-MIB` | 1 | `missing_symbol` |
| `ADMIN-MASTER-MIB` | 1 | `duplicate_definition` |
| `AE-ALARM-TABLE-MIB` | 1 | `grammar_parse_error` |
| `AE-PM-TABLE-MIB` | 1 | `symbol_table_dependency` |
| `AE-VOICE-STATS-MIB` | 1 | `symbol_table_dependency` |
| `ALCATEL-IND1-GROUP-MOBILITY-MIB` | 1 | `missing_symbol` |
| `ALCATEL-IND1-INLINE-POWER-MIB` | 1 | `missing_symbol` |
| `ALCATEL-IND1-LBD-MIB` | 1 | `missing_symbol` |
| `ALCATEL-IND1-WCCP-MIB` | 1 | `missing_symbol` |
| `APRISAXE-MIB-4RF` | 1 | `symbol_table_dependency` |
| `APRISAXE-TC-4RF` | 1 | `grammar_parse_error` |
| `BIANCA-BRICK-MIB` | 1 | `symbol_table_dependency` |
| `BIANCA-BRICK-MIBRES-MIB` | 1 | `symbol_table_dependency` |
| `BINTEC-MIB` | 1 | `grammar_parse_error` |
| `BROCADE-ACL-MIB` | 1 | `other` |
| `CAMBIUM-PTP800-MIB` | 1 | `grammar_parse_error` |
| `CIENA-CES-BENCHMARK-MIB` | 1 | `other` |
| `CIENA-CES-IP-INTERFACE-MIB` | 1 | `other` |
| `CIENA-CES-TIME-SYNC-MIB` | 1 | `other` |
| `COMTROL-ES8510-MIB` | 1 | `grammar_parse_error` |
| `CONFIG-MIB` | 1 | `other` |
| `CPI-UNITY-MIB` | 1 | `duplicate_definition` |
| `CYBER-ARK-MIB` | 1 | `duplicate_definition` |
| `CYBEROAM-MIB` | 1 | `grammar_parse_error` |
| `DAHUA-SNMP-MIB` | 1 | `grammar_parse_error` |
| `DASAN-AUTORESET-MIB` | 1 | `symbol_table_dependency` |
| `DASAN-BRIDGE-MIB` | 1 | `symbol_table_dependency` |
| `DASAN-DHCP-R-MIB` | 1 | `symbol_table_dependency` |

## Observations and recommendations

1. **High pass rate overall:** 69.3% of directories compile cleanly across all three output formats.
2. **Grammar/parse errors dominate:** Many failures are vendor MIB syntax issues (`Bad grammar near token...`) rather than missing dependencies in this collection.
3. **Symbol table / import chain failures:** Failures like `No module X in symbolTable` often cascade — fixing a root MIB (e.g., `E5-120-MIB`, `AE-ALARM-TABLE-MIB`) may resolve multiple dependent modules.
4. **Cisco LANOPTICS MIBs:** Six `LANOPTICS-*` modules fail with `pysmiFakeCol*` placeholder errors — likely unsupported INDEX/table conventions in legacy MIBs.
5. **Strict vs JSON divergence:** JSON builds (`j`) report slightly more partial failures (92) vs nt/t (86) because `--ignore-errors` allows the pass to complete while still listing failed MIBs.
6. **Post-build indexing:** `index.py` reported 3 JSON files it could not index (`SNMPv2-CONF-v1.json`, `OPENBSD-SNMPD-CONF.json`, `RADLAN-SNMPv2.json`) — separate from mibdump compilation failures.
