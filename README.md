# DocChrono CLI Case File

[![CI](https://github.com/docchrono/docchrono-cli-casefile/actions/workflows/ci.yml/badge.svg)](https://github.com/docchrono/docchrono-cli-casefile/actions/workflows/ci.yml)
[![DocChrono 0.1.0](https://img.shields.io/badge/DocChrono-0.1.0-3776ab)](https://pypi.org/project/docchrono/0.1.0/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

A copy-pasteable command-line example for turning fictional vendor records into a saved chronology and evidence graph—without writing an application first.

It uses the production [`docchrono==0.1.0`](https://pypi.org/project/docchrono/0.1.0/) release and synthetic TXT, Markdown, and email data.

## What this teaches

- Build a case from the shell.
- Fail fast on unreadable input with `--strict`.
- Save deterministic case JSON.
- Inspect summary counts without rebuilding.
- Print a source-linked chronology from the saved case.
- Load the same case from Python when deeper graph queries are needed.

## Five-minute run

Python 3.11–3.13 is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

python generate_data.py --check
mkdir -p output

docchrono build data --strict --output output/vendor.case.json
docchrono inspect output/vendor.case.json --json
docchrono timeline output/vendor.case.json
```

Or run all three commands in one narrated example:

```bash
python demo.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`, then create the directory
with `New-Item -ItemType Directory -Force output | Out-Null` before running the same `python`
and `docchrono` commands.

## The synthetic case

| Source | What it says |
| --- | --- |
| `01_vendor_profile.txt` | Ava Patel created fictional vendor `#N-42`. |
| `02_approval.eml` | Ian Brooks approved the vendor. |
| `03_invoice_record.md` | Northstar Components paid fictional invoice `#884`. |

Every person, company, email address, vendor, invoice, and event is invented. Run `python generate_data.py` to reproduce the fixtures byte-for-byte.

## Continue in Python

```python
from docchrono import Case

case = Case.load("output/vendor.case.json")

for event in case.timeline:
    print(event.title)

print(case.entities)
print(case.relationships)
```

Loading is integrity-checked and does not re-read the original documents.

The full case file retains raw extracted text, evidence quotations, and source paths. Treat it as
sensitive when you adapt this example to real records. From Python, `case.save_sanitized(...)`
removes full document text for sharing, but retains evidence quotations and cannot support the
same raw-text round-trip verification.

## Machine-readable output

Add `--json` to `build`, `inspect`, or `timeline` when another program will consume the output:

```bash
docchrono timeline output/vendor.case.json --json
```

Each timeline record includes its supporting source filenames.

## Verify it

```bash
python -m pytest -q
```

The tests and narrated demo invoke the installed `docchrono` console script—not an internal
Python shortcut. CI repeats that entry-point check on Python 3.11 and 3.13.

## Expected output

See [`expected_output.txt`](expected_output.txt) for a captured run against `docchrono==0.1.0`.

## Scope

The example shows deterministic extraction and inspectable evidence. A production due-diligence process should still review low-confidence or ambiguous findings rather than treating extracted records as legal conclusions.

## License

Apache-2.0. The fictional fixture data are released under the same license.
