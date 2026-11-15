# Data for "A Green Suite Is a Partial Gate"

**The paper itself: [`PAPER.md`](PAPER.md)** (as submitted, 12 November 2026), with the cut tables in [`SUPPLEMENT.md`](SUPPLEMENT.md).

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
| `SUPPLEMENT.md` | Tables and passages of the paper's full text that did not fit the track's word limit: the package table (S1), the second machine's table (S2, compiled separately; its underlying sheet is not published), plants per round (S3), re-planted faults (S4), classes by gate (S5), recorded costs (S6) |

Packages are named by what they do. Record identifiers such as `R07:118` point to internal review records that
are not published. The package code is not released, so a row can be checked for arithmetic and consistency but
a planted fault cannot be re-run from this repository.

Limits: one organisation, a few days, faults planted by hand by the reviewer, and no control group. Nothing here
supports a causal claim or a frequency beyond these records.

Licence: Apache License 2.0. Contact: QuantumMind AI LLC, https://qmai.dev

## Revision 2 (15 November 2026)

The paper's revision 2, [`PAPER_r2.md`](PAPER_r2.md), adds a blind second rater and a script that recomputes every
number in the text. New files:

| File | What it holds |
|---|---|
| `LABELS_PLANTS.csv`, `LABELS_FINDINGS.csv` | The blind second rater's fault class for every plant and real fault, with confidence and a short reason |
| `agreement.py` | Computes agreement (raw and Cohen's kappa) between the first rater's classes and the second rater's labels |
| `AGREEMENT_OUTPUT.txt` | Its output: kappa 0.768 on 453 plants, 0.826 on 47 real faults, 0.776 overall |
| `CLAIM_LEDGER.csv` | The audit's claim ledger: each claim in the paper checked against these files |
| `verify_numbers.py` | Recomputes every number in revision 2 from the files here and prints MATCH or MISMATCH per number |
| `VERIFY_OUTPUT.txt` | Its output from this repository: 161 numbers checked, 161 MATCH, 0 MISMATCH |

To reproduce from a clone of this repository (Python 3, standard library only):

    python3 agreement.py PLANTS.csv FINDINGS.csv LABELS_PLANTS.csv LABELS_FINDINGS.csv
    python3 verify_numbers.py . . .
