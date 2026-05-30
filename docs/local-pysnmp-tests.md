## MIB trap decode test framework

These tests validate that NOTIFICATION-TYPE traps in the compiled PySNMP MIB modules under `output/notexts/` resolve to symbolic OIDs and that their notification objects decode correctly.

### Prerequisites

Install PySNMP (and pytest if you use it):

```bash
pip install pysnmp
# optional, for pytest-based wrappers:
pip install pytest
```

Build the MIB tree first so `output/notexts/` is populated:

```bash
make vendor standard
# or compile a single vendor directory:
# ./scripts/localmibs.sh src/vendor/cisco
```

### Running tests

```bash
# Catalog only (~45k trap OIDs, vendor breakdown)
python -m tests.mib_traps.run --discover-only

# Smoke: one vendor, first 50 traps
python -m tests.mib_traps.run --vendor cisco --limit 50 --verbose

# Print every decode test (numeric OID -> symbolic name)
python -m tests.mib_traps.run --vendor arubaos --show-decodes
python -m tests.mib_traps.run --vendor cisco --limit 10 --show-decodes

# Full vendor (may take several minutes)
python -m tests.mib_traps.run --vendor cisco --progress

# All vendors (long run)
python -m tests.mib_traps.run --all --progress

# Use a different compiled MIB directory
python -m tests.mib_traps.run --mib-dir output/notexts --vendor cisco --limit 10
```

Reports **trap OID** resolution (`NotificationType` + symbolic name) and each **NOTIFICATION-TYPE OBJECT** with sample instance indices. See [Understanding skips](#understanding-skips) below for what skipped results mean.

### Understanding skips

The framework reports several “skip” outcomes. By default they do **not** fail the run (exit code 0). Use **`--strict`** to treat module skips and object skips as failures (exit code 1).

#### Module skips — traps never tested

When a compiled MIB module cannot be loaded by PySNMP, every trap in that module is skipped. No trap or object checks run for those entries.

Typical causes:

- **Broken generated Python** — traceback while importing the module
- **Missing or unloadable dependencies** — the module imports another MIB that fails to load
- **Circular imports** — e.g. some Cisco LWAPP modules referencing each other

Examples: `ADVA-FSPR7-CFM-EXTENSION-MIB`, `AH-TRAP-MIB`, Nokia `ALCATEL-IND1-*`, `ASCOM-IPDECT-MIB`.

In the text report:

```
Modules skipped: 152
Traps untested (module load skip): 5714
```

Under `=== Failures ===` these appear as `[skip] vendor/MODULE: MibLoadError: ...`.

These indicate **MIB build or load problems**, not trap decode failures on traps that were actually tested.

#### Object skips — trap OK, varbind object not decoded

For traps whose module loaded successfully, each `NOTIFICATION-TYPE` lists **OBJECTS** (notification varbinds). The test tries to resolve each object to a symbolic name using, in order:

1. Shared table index heuristics
2. Per-object index heuristics
3. Empty index
4. Wire-format OID encoding (e.g. length-prefixed MAC-style indices)

If all attempts fail:

- **Skip** — the error is not a bare numeric OID (e.g. `No symbol …`, `no table row`, missing import). The test could not build a plausible instance or find the symbol.
- **Fail** — resolution returns only a numeric OID (`1.3.6…`), meaning symbolic decode clearly did not work.

Common object skip reasons:

- The trap references a symbol **not present** in the loaded MIB tree
- The object is a **table column** and sample index heuristics do not match agent encoding
- The object is defined in a **different module** that was not loaded

The trap itself can still **pass**; only that notification object is marked skipped.

#### Outcomes that are not skips

| Outcome | Meaning |
|--------|---------|
| **Trap pass** | Notification symbol resolves and its OID matches the catalog |
| **Trap fail** | Symbol, OID, or `NotificationType` check failed |
| **Object fail** | Object resolved only as a numeric OID |
| **Untested traps** | Module skip only — not counted as pass or fail |

#### How the numbers add up

On a full `--all` run (approximate):

```
Traps planned:     45,026   (everything in the catalog)
Traps tested:      39,312   (module loaded successfully)
Traps untested:     5,714   (module load skip)
Trap pass/fail:    39,312 / 0

Object ok / fail / skip:  192,316 / 0 / 945
```

`Traps planned = Traps tested + Traps untested (module load skip)`.

Skips mean **“could not test”** (module) or **“could not decode this varbind with our heuristics”** (object) — not that trap OID resolution failed for traps that did run.

### Viewing full skip/load errors

The default **text** report truncates failure reasons to 120 characters (so `=== Failures ===` lines often end mid-traceback). Use **`--show-decodes`** to print every trap and notification-object resolution (`trap OID: … -> MODULE::symbol`, plus each `object … -> …`). **`--verbose`** also prints full failure text (not truncated) and expands the catalog vendor list.

**Full message from a test run** (JSON report):

```bash
python -m tests.mib_traps.run --vendor arubaos --report json | python3 -c "
import json, sys
for f in json.load(sys.stdin).get('failures', []):
    print(f['kind'], f.get('module', ''))
    print(f['reason'])
    print('---')
"
```

With `jq`:

```bash
python -m tests.mib_traps.run --vendor arubaos --report json | jq -r '.failures[0].reason'
```

**Reproduce a module load failure directly**:

```bash
python -c "
from pysnmp.smi import builder
mb = builder.MibBuilder()
mb.addMibSources(builder.DirMibSource('output/notexts'))
mb.loadModules('WLSX-TRAP-MIB')  # module name from the [skip] line
"
```

Replace `WLSX-TRAP-MIB` with the module shown in `[skip] vendor/MODULE: ...`.

### Paths used by the test suite

| Purpose | Default path |
|---------|----------------|
| Compiled PySNMP modules | `output/notexts/` |
| Vendor MIB source (module → vendor map) | `src/vendor/` |

Override with `--mib-dir` and `--mibs-src-vendor` when needed.

### How compiled MIBs are produced

This repo builds PySNMP modules with `mibdump` via `make vendor standard` (see [README.md](../README.md)). The strict **notexts** pass writes to `output/notexts/`; a **texts** pass writes to `output/texts/`.

PySNMP uses **compiled Python MIB modules** (`.py`), not raw ASN.1 (`.mib`) files. In code:

```python
from pysnmp.smi import builder

mb = builder.MibBuilder()
mb.addMibSources(builder.DirMibSource("output/notexts"))
mb.loadModules("CISCO-LWAPP-AP-MIB", "CISCO-LWAPP-SI-MIB")
```

Or point PySNMP at the directory with:

```bash
export PYSNMP_MIB_DIRS="$(pwd)/output/notexts"
```
