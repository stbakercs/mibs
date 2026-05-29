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
# Catalog only (~18k trap OIDs, vendor breakdown)
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

Reports **trap OID** resolution (`NotificationType` + symbolic name) and each **NOTIFICATION-TYPE OBJECT** with sample instance indices. Module load failures (e.g. circular LWAPP imports) count as **skipped** unless `--strict`.

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
