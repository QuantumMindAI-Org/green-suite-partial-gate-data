# Summary tables: planted faults, real faults and a mechanical mutation control

Every number below is computed by `summarize.py` from `PLANTS.csv`, `FINDINGS.csv` and `MUTATION.csv` in this folder; `test_summary.py` recomputes them independently and checks this file. Package names are functional. A *plant* is a single-line fault that a non-author agent put into a copy of the delivered code before running the author agent's own test suite; *caught* means at least one test failed (or, where stated, the suite run aborted). Fault classes are defined in `TAXONOMY.md`.

## 1. Plants made, caught and missed, per package and round

Denominator: 453 plants in 15 review rounds of 8 packages (every round whose record lists its plants one by one).
Column *missed, could change an action* counts misses whose record states that the fault, if shipped, could change what is sent or done, or how many irreversible actions happen.

| package | round | made | caught | missed | caught % | missed, could change an action |
|---|---|---|---|---|---|---|
| one-job submit script | r1 | 60 | 48 | 12 | 80.0% | 4 |
| one-job submit script | r2 | 44 | 33 | 11 | 75.0% | 3 |
| one-job submit script | r3 | 30 | 23 | 7 | 76.7% | 0 |
| once-only sealed evaluator | r1 | 30 | 20 | 10 | 66.7% | 0 |
| once-only sealed evaluator | r2 | 50 | 35 | 15 | 70.0% | 0 |
| once-only sealed evaluator | r3 | 68 | 59 | 9 | 86.8% | 0 |
| once-only sealed evaluator | r4 | 35 | 28 | 7 | 80.0% | 2 |
| GPU training kernel | r1 | 20 | 11 | 9 | 55.0% | 3 |
| static-site release tooling v2 | r1 | 32 | 29 | 3 | 90.6% | 0 |
| inference release package | r3 | 10 | 3 | 7 | 30.0% | 0 |
| inference release package | r4 | 21 | 20 | 1 | 95.2% | 0 |
| evaluation-record audit harness | r1 | 12 | 8 | 4 | 66.7% | 0 |
| evaluation-record audit harness | r2 | 16 | 14 | 2 | 87.5% | 0 |
| browser puzzle game | r1 | 5 | 4 | 1 | 80.0% | 0 |
| frame-rendering kit | r1 | 20 | 11 | 9 | 55.0% | 0 |
| **all** |  | 453 | 346 | 107 | 76.4% | 12 |

How the caught plants were caught: behaviour test 323; behaviour test (stand-in encoder) 3; refused by the derivation step 2; rehearsal 5; static pin test only 12; suite abort 1.

## 2. Catch rate by fault class (plants)

| class | name | made | caught | missed | caught % | packages |
|---|---|---|---|---|---|---|
| B | boundary or off-by-one | 26 | 24 | 2 | 92.3% | 6 |
| G | check weakened or removed | 147 | 109 | 38 | 74.1% | 7 |
| W | wrong object or value sent or used | 76 | 62 | 14 | 81.6% | 8 |
| L | computation or decision logic | 86 | 58 | 28 | 67.4% | 6 |
| O | ordering or timing of side effects | 20 | 17 | 3 | 85.0% | 4 |
| S | state or marker handling | 55 | 43 | 12 | 78.2% | 4 |
| C | concurrency or atomicity | 9 | 7 | 2 | 77.8% | 2 |
| R | resource or scale | 0 | 0 | 0 | n/a | 0 |
| E | configuration or environment | 14 | 9 | 5 | 64.3% | 2 |
| F | output or format | 20 | 17 | 3 | 85.0% | 6 |

The plants were chosen by reviewers, not sampled, so the class sizes reflect what reviewers chose to test. Class R (resource or scale) has no plant at all: no reviewer planted a resource fault, and the resource faults in section 4 were found only by reading sizes or by a run at real size.

## 3. Before and after a revision that followed a review

A plant counts as re-planted when the next round of the same package holds a plant with the same id (the reviewer re-applied it to the revised code). *Missed then caught* is the suite getting better exactly where a review showed it weak; *caught then missed* is a regression of the suite.

| package | rounds | missed then caught | missed then missed | missed, not re-planted | caught then caught | caught then missed | regressed ids |
|---|---|---|---|---|---|---|---|
| one-job submit script | r1 to r2 | 12 | 0 | 0 | 0 | 0 | - |
| one-job submit script | r2 to r3 | 0 | 0 | 11 | 0 | 0 | - |
| once-only sealed evaluator | r1 to r2 | 10 | 0 | 0 | 16 | 4 | F07, F11, F16, F17 |
| once-only sealed evaluator | r2 to r3 | 15 | 0 | 0 | 34 | 1 | F02 |
| once-only sealed evaluator | r3 to r4 | 7 | 0 | 2 | 0 | 0 | - |
| inference release package | r3 to r4 | 7 | 0 | 0 | 3 | 0 | - |
| evaluation-record audit harness | r1 to r2 | 4 | 0 | 0 | 8 | 0 | - |

Totals: 55 of 55 re-planted misses were caught in the next round; 5 of 66 re-planted catches were missed in the next round; 13 earlier misses were not re-planted.

New plants (ids not planted in any earlier round of the package) in the revised rounds:

| package | round | new plants | caught | caught % |
|---|---|---|---|---|
| one-job submit script | r2 | 32 | 21 | 65.6% |
| one-job submit script | r3 | 30 | 23 | 76.7% |
| once-only sealed evaluator | r2 | 20 | 9 | 45.0% |
| once-only sealed evaluator | r3 | 18 | 10 | 55.6% |
| once-only sealed evaluator | r4 | 28 | 21 | 75.0% |
| inference release package | r4 | 11 | 10 | 90.9% |
| evaluation-record audit harness | r2 | 4 | 2 | 50.0% |

New plants in revised rounds: 96 of 143 caught (67.1%), against 55 of 55 (100.0%) for re-planted earlier misses.

## 4. Real faults in delivered code

Denominator: 47 faults (`FINDINGS.csv`): every blocker, major, regression or stop that a review named in delivered code, plus the reader-of-another-family items and notes that the scope memo's evidence table cites. Test gaps shown only by plants are not faults in delivered code and are not counted here.

By how the fault was found:

| how found | faults | with the author's suite fully green | of which blocker, major, regression or stop |
|---|---|---|---|
| running the code | 28 | 26 | 27 |
| other-family text reader, then reading | 1 | 1 | 1 |
| other-family text reader, then run | 5 | 5 | 0 |
| reading the source | 12 | 11 | 10 |
| real-size run | 1 | 1 | 1 |
| **all** | 47 | 44 | 39 |

Suite fully green at the time: no 2; not stated 1; yes 44.
Could have caused a wrong or repeated irreversible action: no 9; not stated 26; yes 12.
Severity as the review gave it: (found by the audit; no severity) 1; BLOCKER 9; MAJOR 27; MINOR (partly confirmed) 1; MINOR to MODERATE 1; cosmetic 1; note 3; open point (ruling not fully implemented) 1; regression (no severity label) 1; stop (ruling) 2.
Rounds until fixed: 1 28; not fixed 1; not fixed in code 2; not stated 16.
Run-doing reviewer: other family 3; same family as author (separate context) 44.

By fault class:

| class | name | faults | with suite fully green |
|---|---|---|---|
| B | boundary or off-by-one | 1 | 1 |
| G | check weakened or removed | 7 | 6 |
| W | wrong object or value sent or used | 2 | 2 |
| L | computation or decision logic | 4 | 4 |
| O | ordering or timing of side effects | 5 | 5 |
| S | state or marker handling | 9 | 9 |
| C | concurrency or atomicity | 0 | 0 |
| R | resource or scale | 3 | 3 |
| E | configuration or environment | 6 | 4 |
| F | output or format | 10 | 10 |

Gate by class (how each real fault was found):

| class | running the code | other-family text reader, then reading | other-family text reader, then run | reading the source | real-size run |
|---|---|---|---|---|---|
| B | 1 | 0 | 0 | 0 | 0 |
| G | 1 | 1 | 0 | 5 | 0 |
| W | 2 | 0 | 0 | 0 | 0 |
| L | 3 | 0 | 0 | 1 | 0 |
| O | 3 | 0 | 0 | 2 | 0 |
| S | 7 | 0 | 2 | 0 | 0 |
| R | 0 | 0 | 0 | 2 | 1 |
| E | 4 | 0 | 1 | 1 | 0 |
| F | 7 | 0 | 2 | 1 | 0 |

### Distinct cases of a fully green suite over a blocker, major, regression or stop

| package | round | findings |
|---|---|---|
| one-job submit script | r1 | F01, F02, F03, F04, F05, F06 |
| one-job submit script | r2 | F07, F08 |
| once-only sealed evaluator | r1 | F12, F13, F14, F15, F16, F17, F18 |
| once-only sealed evaluator | r2 | F19, F20 |
| once-only sealed evaluator | r4 | F22 |
| post-processing selection programs | r4 | F23 |
| GPU training kernel | r1 | F27, F28, F29 |
| static-site release tooling v1 | r2 | F30, F31, F32 |
| evaluation-record audit harness | r1 | F35, F36, F37, F38 |
| frame-rendering kit | r1 | F40, F41, F42, F43, F44, F45, F46, F47 |

Count: 10 distinct package-rounds (the shared memory fault of the evaluator r4 and the selection programs r4 is one fault class met twice and is listed under both packages here; the scope memo counted it once as its row 8).

## 5. Missed plants that could change an action

Of 107 missed plants: 12 could change an action according to their record, 31 could not, 64 are not stated. Share: 11.2% of all misses; 27.9% of the misses whose record states either way.

| package | missed, could change an action | missed |
|---|---|---|
| one-job submit script | 7 | 30 |
| once-only sealed evaluator | 2 | 41 |
| GPU training kernel | 3 | 9 |
| static-site release tooling v2 | 0 | 3 |
| inference release package | 0 | 8 |
| evaluation-record audit harness | 0 | 6 |
| browser puzzle game | 0 | 1 |
| frame-rendering kit | 0 | 9 |

## 6. Mechanical mutation control on one package

On a scratch copy of the static-site release tooling v2, a standard-library script made 150 single-token mutants of the publisher and its seven step scripts (fixed seed, about a quarter per operator; mutants that did not compile were skipped: none), ran the package's own 38-test suite on each, and sorted the result. *Static only* means the only failing tests were the two that pin the delivered bytes (the derivation reproduces the candidate byte for byte; the publisher's edits are exactly the disclosed ones): such a mutant is caught by a byte pin, not by any test of behaviour. When the publisher was mutated, its pinned hash was re-pinned so that only the fault differs, as the human reviewer did.

| operator | killed by a behaviour test | killed by the byte pins only | survived (suite green) | other failure | equivalent-looking (hand-judged) | mutants |
|---|---|---|---|---|---|---|
| CMP | 24 | 13 | 0 | 0 | 0 | 37 |
| CONST | 15 | 22 | 0 | 0 | 2 | 37 |
| DEL | 17 | 22 | 0 | 0 | 0 | 39 |
| SWAP | 26 | 11 | 0 | 0 | 1 | 37 |
| **all** | 82 | 68 | 0 | 0 | 3 | 150 |

By target file role:

| target | mutants | killed by a behaviour test |
|---|---|---|
| readback step | 32 | 22 |
| publisher (install and rollback core) | 52 | 35 |
| precheck and go-ahead step | 17 | 13 |
| install step | 17 | 1 |
| rollback step | 14 | 0 |
| rollback go-ahead step | 5 | 5 |
| rehearsal readback step | 7 | 6 |
| read-only snapshot step | 6 | 0 |

Beside it, the reviewer's hand-made plants on the same package: 32 planted, 29 caught; 17 of them by a behaviour test, a rehearsal or a refusal of the derivation step, 12 by the byte pins only. Mechanical: 82 of 150 killed by a behaviour test (54.7%), 68 by the byte pins only (45.3%). Equivalence was judged by hand only for mutants not killed by a behaviour test: 67 judged (see `MUTATION.csv`, column `equivalent_looking`; blank = not judged).

## 7. Reconciliation with the scope memo

| scope row | package | round | scope made/caught/missed | here made/caught/missed | result |
|---|---|---|---|---|---|
| 1 | one-job submit script | r1 | 60/48/12 | 60/48/12 | same |
| 2 | one-job submit script | r2 | 44/33/11 | 44/33/11 | same |
| 3 | one-job submit script | r3 | 30/23/7 | 30/23/7 | same |
| 4 | once-only sealed evaluator | r1 | 30/20/10 | 30/20/10 | same |
| 5 | once-only sealed evaluator | r2 | 50/35/15 | 50/35/15 | same |
| 6 | once-only sealed evaluator | r3 | 68/59/9 | 68/59/9 | same |
| 7 | once-only sealed evaluator | r4 | 35/28/7 | 35/28/7 | same |
| 11 | GPU training kernel | r1 | 20/11/9 | 20/11/9 | same |
| 14 | static-site release tooling v2 | r1 | 32/29/3 | 32/29/3 | same |
| 16 | inference release package | r3 | 10/3/7 | 10/3/7 | same |
| 17 | inference release package | r4 | 21/20/1 | 21/20/1 | same |
| 18 | evaluation-record audit harness | r1 | 12/8/4 | 12/8/4 | same |
| 19 | evaluation-record audit harness | r2 | 16/14/2 | 16/14/2 | same |
| 21 | browser puzzle game | r1 | 5/4/1 | 5/4/1 | same |

Totals: scope 433/335/98; here, the same rows 433/335/98; here, all rows 453/346/107 (the difference is the frame-rendering kit's 20 plants, 11 caught, reviewed after the scope memo).

Green-suite cases, scope memo's nine file-backed rows against this table (blocker, major, regression or stop, suite fully green):

| scope row | covers here | reproduced | findings |
|---|---|---|---|
| 1 | one-job submit script r1 | yes | F01, F02, F03, F04, F05, F06 |
| 2 | one-job submit script r2 | yes | F07, F08 |
| 4 | once-only sealed evaluator r1 | yes | F12, F13, F14, F15, F16, F17, F18 |
| 5 | once-only sealed evaluator r2 | yes | F19, F20 |
| 8 | once-only sealed evaluator r4; post-processing selection programs r4 | yes | F22, F23 |
| 11 | GPU training kernel r1 | yes | F27, F28, F29 |
| 13 | static-site release tooling v1 r2 | yes | F30, F31, F32 |
| 18 | evaluation-record audit harness r1 | yes | F35, F36, F37, F38 |
| 20 | evaluation-run wrapper as run | no | - |

Cases here that the scope memo did not count: frame-rendering kit r1 (F40, F41, F42, F43, F44, F45, F46, F47).

Why the scope memo's row 20 is not reproduced: the evaluation-run wrapper's fault (F39) is a check that could not
fail. Its record shows the check passing on all four records but no test suite, so "a suite that passed in full" is
not stated for it. The frame-rendering kit (F40-F47: 85 of 85 tests green with 3 skipped, five blockers in the frames)
was reviewed after the scope memo was written.

## 8. What is NOT in the data

- **Choice of plants.** Every plant was chosen by a reviewer (13 of the 453, in the evaluator's round r4, were the
  author agent's own plants re-run by the reviewer; column `planted_by`). Catch rates are not mutation scores and are not
  comparable across packages or classes. Section 6 is the only mechanical sample, on one package.
- **What "caught" rests on.** 12 catches (all in the static-site release tooling v2) rest only on tests that pin the
  delivered bytes, not on a test of behaviour; 1 (one-job submit script r1, P55) is a suite run that aborted; 3 (inference
  release package r3) were caught only after the reviewer supplied a stand-in for a missing optional package: as
  delivered on the review machine, 0 of those 10 plants were killed.
- **Single line.** Plants are described by their records as single-line faults; at least one (evaluation-record audit
  harness r1, M7) removes a three-line raise, and one evaluator plant changes two things at once (r4, M1: the existence check and the exclusive flag).
- **The impact column** is filled only where the record says it: 64 of the 107 misses have no stated impact. Nothing here
  measures how likely a miss was to occur.
- **Rows left out.** The scope memo's log-only rows (22 to 25: 59 plants, 25 caught) and the public-article rows (26 and 27:
  173 plants, 82 caught) have no per-plant record on this machine and are not in PLANTS.csv. The GPU training kernel's
  second review had logs only (no review text) when read. The frame-rendering kit was reviewed after the scope memo; its 20
  plants are included here and listed apart in the reconciliation.
- **Findings left out.** Minors and notes (except those the scope memo's evidence table cites), test gaps shown only by
  plants, a release condition that is not code (static-site release tooling v2, its blocker B1), a design point its own
  review calls "not a code defect" (sealed evaluator r4, MAJ-1), and a predecessor's fault known only from a log line.
- **Classes** were assigned by one agent from the record text, with no second rater (TAXONOMY.md).
- **No control group, no cost data** (token or dollar costs of the agents were not recorded), one organisation, two
  days. Nothing here shows that accepted packages are free of faults.

