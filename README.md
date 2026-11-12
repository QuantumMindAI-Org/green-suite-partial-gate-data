# Data for "A Green Suite Is a Partial Gate"

Review records from a small company whose software is written, tested and reviewed by AI agents. After each
author agent's test suite passed, a non-author agent ran the package and planted faults to see what the suite
would catch. These files are the per-fault data behind the paper's tables.

| File | What it holds |
|---|---|
| `PLANTS.csv` | One row per planted fault: package (named by what it does), review round, what was changed, fault class, caught or missed, by which test, and the record it comes from |
| `FINDINGS.csv` | One row per real fault found in delivered code: how it was found, whether the author's suite was fully green at the time, fault class, rounds until fixed |
| `MUTATION.csv` | A mechanical mutation run on one package (150 mutants), as a control beside the hand-planted faults |
| `TAXONOMY.md` | The fault classes, each with examples |
| `SUMMARY.md` | The tables computed from the three CSV files |
| `summarize.py` | Recomputes every table in `SUMMARY.md` from the CSV files (Python standard library only) |

Packages are named by what they do. Record identifiers such as `R07:118` point to internal review records that
are not published. The package code is not released, so a row can be checked for arithmetic and consistency but
a planted fault cannot be re-run from this repository.

Limits: one organisation, a few days, faults planted by hand by the reviewer, and no control group. Nothing here
supports a causal claim or a frequency beyond these records.

Licence: Apache License 2.0. Contact: QuantumMind AI LLC, https://qmai.dev
