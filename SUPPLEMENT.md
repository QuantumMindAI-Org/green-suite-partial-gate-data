# Supplement to "A Green Suite Is a Partial Gate: Planted Faults in Agent-Written Code"

The paper was submitted to a track with a 3,000-word limit that counts tables. The tables and passages below are
taken word for word from the paper's full text (the version before the cut); only their numbers were changed
(the labels S1 to S6). No number in them differs from the full text. In this supplement, "Table 1 packages"
means Table S1 and "Table 6" means Table S2.

## Table S1. First-machine packages (Table 1 of the full text)

| Package: what it must guarantee | Rounds reviewed | Author tests by round |
|---|---|---|
| One-job script: create exactly one job on a quantum processor and decide the verdict of its reading | 3 | 67, 103, 140 |
| Once-only evaluator: open a sealed test set once; predict, then score | 5 | 15, 35, 50, 63, 143 |
| Selection programs over six real training runs | 1 real run, then the fix | all green; 49 + 69 |
| GPU training job scored by a pinned scorer | 1 | 17 |
| Site publisher, two articles: install once, read every byte back, roll back on failure | 1 | 27 |
| Site publisher, third article | 1 | 38 |
| Inference release package, run on the second machine | 2 | not stated; 82 |
| Audit of an agent evaluation library's result records | 2 | 38; 54 |
| Our own reader of that library's result records | as run | its own checks |
| Tutorial change in a browser game | 1 | 88 |
| Frame-rendering kit for short explainer films | 1 | 85 (3 skipped) |

## Table S2. Second-machine rows with a suite and a non-author review (Table 6 of the full text)

Families: author / finder.

| What it is | Suite on the version reviewed | What the non-author found | Non-author plants: made / killed by the suite / survived | Families |
|---|---|---|---|---|
| Agent harness that must hold a money cap | 148 of 148 † | 2 blockers, 3 majors by probes: a discarded reply re-sent with no cap check, 5.40 dollars counted against a 1.00 cap | 46 / 34 / 7 (3 equivalent; 2 more killed by probes) | B / A |
| Packet that runs a pilot study's generation jobs, first version | 250 of 250 † | blocker: under the pinned library version every real job raises at its first call; list entries promising a marker that cannot exist: 122 of 174 by its review; two later reports give 126, one of them on the next version | 35 / 28 / 7 | B / A |
| Same packet, next version | 263 of 264 | runbook not executable from the packet; code accepted | 21 / 17 / 4 | B / A |
| Sealed package chain deciding what may enter training, first candidate | package suites green; author's 67 plants all killed † | one environment variable admits rows; a half-finished cascade accepted as final; its three attack suites could not fail † | 51 / 40 / 11 (two halves) | A / B and A |
| Same chain, second candidate | groups for the two rulings green † | names that pass the name test build where a final is accepted; attack suites still exit 0 | none by a non-author | A / A and C |
| Program that renders short films from a spec, first delivery | 25 of 25 † | three corrections; four minor faults | 28 / 27 / 1 | B / A |
| Same program, corrections | 40 of 40 † | a decoy tool in the working folder ran; 27 threads instead of 4 | 26 / 18 / 3 (5 more killed by probes) | B / A |
| Module that sends one question to a local model | 104 of 104 † | two low findings | 31 / 27 / 4 | B / A |
| Benchmark runner, later version (provisional) | 196 of 199 | 0 of 118 packet tests run; never-executed list incomplete | 33 / 30 / 3 | B / A |
| Module that calls a hosted model service | 166 of 166 † | major on time only: an attempt can overrun its limit | 13 of 26 planned were run; the suite killed none | B / A |
| Program that builds a results page | 77 of 77 † | major: a directory junction reaches a forbidden folder | 20 / 16 / 4 | B / A |
| Watcher that wakes idle worker consoles | 26 of 26 | no fault; 5 plants survive the suite | 15 / 10 / 5 | B / A |
| Tests-only suite for training-data guards | 148 of 148 | round 0's nine surviving faults, all killed in round 1 | 50 / 48 / 2 (maker not stated in the sheet) | A / B (round 0) |

*Table 6 note:* † marks a version in the compiler's list of a suite that passed over a real fault. The list has 11 items; two concern the chain's first candidate (its package suites, and its own attack suites), so they cover 10 versions: the 9 marked rows and an earlier version of the benchmark runner (170 of 170) whose unchanged guard code later raised a raw error. Rows still under review are left out.

## Table S3. Planted faults per round, first machine (Table 2 of the full text)

| Package, round | Plants | Caught | Missed | Caught % | Misses that could change an action |
|---|---|---|---|---|---|
| One-job script r1 | 60 | 48 | 12 | 80.0 | 4 |
| One-job script r2 | 44 | 33 | 11 | 75.0 | 3 |
| One-job script r3 | 30 | 23 | 7 | 76.7 | 0 |
| Evaluator r1 | 30 | 20 | 10 | 66.7 | 0 |
| Evaluator r2 | 50 | 35 | 15 | 70.0 | 0 |
| Evaluator r3 | 68 | 59 | 9 | 86.8 | 0 |
| Evaluator r4 | 35 | 28 | 7 | 80.0 | 2 |
| GPU training job r1 | 20 | 11 | 9 | 55.0 | 3 |
| Publisher, third article | 32 | 29 | 3 | 90.6 | 0 |
| Inference package r3 | 10 | 3 | 7 | 30.0 | 0 |
| Inference package r4 | 21 | 20 | 1 | 95.2 | 0 |
| Evaluation audit r1 | 12 | 8 | 4 | 66.7 | 0 |
| Evaluation audit r2 | 16 | 14 | 2 | 87.5 | 0 |
| Browser game | 5 | 4 | 1 | 80.0 | 0 |
| Frame-rendering kit | 20 | 11 | 9 | 55.0 | 0 |
| **All** | **453** | **346** | **107** | **76.4** | **12** |

## Table S4. Plants re-planted after a revision, against new plants in the revised code (Table 3 of the full text)

| Plants | Caught in the next round |
|---|---|
| Earlier misses, re-planted | 55 of 55 (100%) |
| Earlier catches, re-planted | 61 of 66 |
| New plants in revised code (7 rounds) | 96 of 143 (67.1%) |

## Table S5. Plants and real faults by class, and the gate that found the real faults (Table 4 of the full text)

| Class | Plants | Caught % | Real faults (suite green) | Found by running / reader, then confirmed / reading the source / real-size run |
|---|---|---|---|---|
| Boundary or off-by-one | 26 | 92.3 | 1 (1) | 1 / 0 / 0 / 0 |
| Check weakened or removed | 147 | 74.1 | 7 (6) | 1 / 1 / 5 / 0 |
| Wrong object or value sent or used | 76 | 81.6 | 2 (2) | 2 / 0 / 0 / 0 |
| Computation or decision logic | 86 | 67.4 | 4 (4) | 3 / 0 / 1 / 0 |
| Ordering or timing of side effects | 20 | 85.0 | 5 (5) | 3 / 0 / 2 / 0 |
| State or marker handling | 55 | 78.2 | 9 (9) | 7 / 2 / 0 / 0 |
| Concurrency or atomicity | 9 | 77.8 | 0 | - |
| **Resource or scale** | **0** | **n/a** | **3 (3)** | **0 / 0 / 2 / 1** |
| Configuration or environment | 14 | 64.3 | 6 (4) | 4 / 1 / 1 / 0 |
| Output or format | 20 | 85.0 | 10 (10) | 7 / 2 / 1 / 0 |
| **All** | **453** | **76.4** | **47 (44)** | **28 / 6 / 12 / 1** |

## Table S6. Recorded costs (Table 5 of the full text)

| Gate | Recorded cost |
|---|---|
| G2, one-job script, rounds 1 to 3 | about 26, 26 and 20 minutes of reviewer time; suite runs 70.4 s, 14.2 s, 18.0 s |
| G2, third-article publisher | about 25 minutes; 32 plants |
| G3, paid reads | USD 0.43 (a read cut off at its length limit); another about USD 0.14, by the difference of two logged balances |
| G4, selection programs at real shape | 495 s and 859 s |
| G4, evaluator rehearsal | six runs of 731.5 to 1,008.9 s |
| A miss, as reviewers estimated it | a second processor job; up to 1.75 GPU-hours; the only opening of a sealed set; an altered page left in place |

## Passages of the full text that the submitted paper shortens or leaves out

### What a plant is, as recorded

**What a plant is, as recorded.** A small change to delivered code, usually one line, that some test should catch; *caught* means at least one test failed; on the third-article publisher, 5 catches came from its rehearsal and 2 from a refusal of its derivation step. 440 plants were the reviewer's and 13 the author's own, re-run by the reviewer. At least two change more than one line or one thing. 12 catches rest only on tests that pin the delivered bytes, one on an aborted suite run. For one package as delivered, 0 of 10 plants were killed; 3 only after the reviewer supplied a stand-in for a missing optional package.

### Real faults under green suites: the package-rounds

The 37 blockers, majors, regressions and stops among the 44 green-suite faults fall in 10 distinct package-rounds (Table 1 packages: one-job script r1 and r2; evaluator r1, r2, r4; selection programs; GPU training job; publisher for two articles; audit r1; frame-rendering kit); the other 7 (minors, notes and an open point) add evaluator r3 and r5. Running the code found 28 of the 47; reading the source 12; other-family readers first raised 6; a real-size run met 1. The plainest: a frame-rendering kit passed 85 tests; the reviewer rendered the frames, looked, and found eight faults, five of them blockers.

### Box 1. A worked example from the one-job script's first round

| | |
|---|---|
| Planted fault | the check before the create ran on the compiled circuits while the uncompiled circuits were sent (one word changed) |
| Suite result | all 67 tests passed; they checked only the number of circuits sent and their shots |
| Missing test | the circuits handed to the create call must hash to the prepared compiled-set hash |
| Real fault of the same class (wrong object or value used) | the run counted every job on the shared account, so another job there would have voided a good run; shown by a run, all tests green |

### Case D

**D. Faults inherited from a predecessor used live.** The publisher for two articles passed 27 tests and a local rehearsal. A reviewer of another family altered installed bytes: each change failed its check, then the rollback refused, leaving the altered page in place on the reviewer's copy. This and an unrecoverable kill state were inherited unchanged from an earlier publisher that had been used for live installs.

### The text-only reader

In six text-only reads on the first machine, readers of other families first raised 6 of the 47 real faults: one major (a repeat authorised despite an undecided rule) and five minor items or notes. They also raised independently 4 that runs found (three majors in one-job script r1, a note in the evaluator r5). None concerned memory; one, an unreadable index ending in an uncaught decode error on a resume, was a crash after a marker that failed closed. In one-job script r2, where the runs found a major and a regression, the reader's three findings, all minor, included neither.

### The second machine: two patterns

Two patterns repeat. Where the sheet reports authors' own plants (the money-cap harness 20 of 20, the chain's two candidates 67 of 67 and 4 of 4, the results-page program 66 of 66), every one was killed, while non-author plants on the harness, the chain and the results-page program survived (7, 11 and 4; Table 6). And checks that cannot fail recurred: three attack suites exited 0 with a planted admission and with their engine unreadable. The second machine shows that green suites over real faults were also found where the reviewer was of another family; it does not correct the first machine's counts.

## Added after submission (2026-11-13): the preregistered reader test, said exactly

Everything above is as it stood when the paper was submitted on 2026-11-12. This note was added the next day.

The paper's limits section says that a preregistered test of a small open-weights model as the text-only reader
"was not completed and is not reported". More exactly: on 2026-11-11 the test was started on the second machine.
Two of its fifteen planned calls were made and charged, and neither returned any answer text; the run stopped
there by its own rule, and thirteen calls were never made. One further call outside the protocol, with a larger
output limit, also returned no text. No answer was scored, and nothing was seen that bears on the answer key.
The cause was not established. The record of these calls reached the paper's authors only after the submission.
