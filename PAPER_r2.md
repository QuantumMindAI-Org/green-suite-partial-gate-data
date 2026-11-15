# A Green Suite Is a Partial Gate: Planted Faults and Real Faults in Agent-Written Code

**Victor Dominguez**, QuantumMind AI

*Preprint, revision 2 of a paper first circulated on 12 November 2026. Every number in this text is recomputed from the published data by `verify_numbers.py`.*

## Abstract

QuantumMind AI is a one-person company whose software is written, tested and reviewed by AI agents. We report its review records of 9 to 11 November 2026. On the first of two machines, eight packages went through 15 review rounds. After each package's own test suite had passed, an agent that had not written the code reran that suite with 453 planted faults, one at a time: 440 plants of its own and 13 of the author's that it re-ran. 346 plants were caught and 107 were missed. 326 catches came from a test of behaviour, 12 only from a test that pins the delivered bytes, and 8 from a rehearsal, a refusal step or an aborted run. The same reviews found 47 real faults in delivered code; 44 sat under a suite with no recorded failure. They were found by running the code (28), reading the source (12), a text-only reader of another model family (6) and one run at real data size (1). No reviewer planted a fault of resource or scale, yet three real faults were of that class, all under passing suites: two found by reading sizes, one by the run at real size. A blind second rater of another model family reproduced the fault classes with Cohen's kappa 0.776 over the 500 items and placed the same three real faults, and no plant, in the resource class. The plants were chosen, not sampled, so the share caught (76.4 percent; 72.0 percent by a test of behaviour) describes these plants and is not an adequacy measure. For 44 of the 47 real faults the run-doing reviewer was of the author's model family. The record is one company over three days with no control group. We publish the per-plant and per-fault tables, both raters' labels and the scripts that recompute every number, and we describe the review practice we adopted as hypotheses, not as a validated method.

## 1. Introduction

An author agent writes the code and the tests that judge it, and the tests pass. What does that pass show? The question is sharpest where a step can be taken only once (one paid job on a shared processor, one opening of a sealed test set, one live install) and a fault found afterwards cannot be repaired by running again. In this company no person reads each change, so the passing suite is the gate unless something else is added.

This paper reports what happened when agent-written code with a passing suite went to an agent that had not written it. It is a field record, not an experiment. Its contributions are:

1. A per-plant record of 453 planted faults in eight packages over 15 review rounds, with the test that caught each one and whether that test checks behaviour or pins bytes, and a per-fault record of 47 real faults in delivered code, with the gate that found each.
2. A fault-class table in which the class with no plant at all, resource or scale, holds three real faults. A blind second rater of another model family reproduces the class labels (kappa 0.776) and that empty cell.
3. A mechanical mutation control on one package (150 mutants) beside the hand-chosen plants, separating kills by behaviour tests from kills by byte pins.
4. A plain account of what the record cannot show, and the review practice adopted in response, stated as hypotheses.

The practices involved are textbook: fault seeding and mutation analysis, review by someone other than the author, a second rater with an agreement statistic, and a run at real data size before an irreversible step. What is new here is only the setting, in which authors, testers and reviewers are all AI agents, and the record of what each gate found.

## 2. Method

### 2.1 Setting and gates

Agents of several model families write, review and run the company's software on two machines and rented services. Each package arrives with a hash manifest and the author's tests, and a coordinating agent sends it through some of these gates:

- **G1, author tests**, run by the author.
- **G2, non-author runs.** Another agent reruns the suite on a scratch copy, plants faults one at a time with a suite run after each, attacks the package's stated promises by running it (killed processes, two processes at once, damaged records), and reads the source.
- **G3, text-only reader of another model family.** A paid model reads the code and a brief, runs nothing, and returns findings; G2 settles each claim by a run or by reading.
- **G4, run at real size.** The real shape and counts of the data, on synthetic stand-ins, before the step that can be taken once.
- **G5, go-ahead.** The one-shot act needs a written go-ahead naming the accepted manifest hash.

**Independence.** For 44 of the 47 real faults on the first machine, the reviewer that ran the code (G2) was of the same model family as the author, in a separate context with no shared memory; for 3 (F30 to F32) it was of another family. The text-only readers (G3), the auditor of the published data and the second rater were of other families, but they read records; they did not review code by running it. Shared blind spots between author and reviewer are therefore possible and would lower the counts below.

### 2.2 Data

**First machine.** Every review round dated 10 or 11 November 2026 whose record lists its plants one by one: 15 rounds of 8 packages, 453 plants. Without the frame-rendering kit, reviewed after the scoping memo, the count is 433 plants with 335 caught. Review rounds whose record has only logs, and reviews reported only in public articles, have no per-plant record and are not included (see "What is not in the data" in the published summary). The record carries no timestamps per plant; the dates are those of the review records.

**Real faults.** Every blocker, major, regression or stop that a review named in delivered code, plus the minor items and notes that the scoping memo's evidence table cites: 47 rows. A test gap shown only by a plant is not a real fault. This population is the set of faults the reviews found; nothing in it measures faults the reviews missed.

**Second machine.** Its lead agent compiled 20 rows over 11 cases from existing files, running nothing. Its counts are kept apart (Section 3.8); its underlying sheet is not published.

### 2.3 Plants

A plant is a small change to delivered code, usually one line, that some test should catch. *Caught* means at least one test failed; on one package it also counts the package's own rehearsal step and a refusal by its derivation step, and one catch is a suite run that aborted. 440 of the 453 plants were made by the reviewer; 13, all in the sealed evaluator's fourth round, were the author's own plants that the reviewer re-ran, and all 13 were caught. At least two plants change more than one thing (the evaluator's r4 M1 removes both an existence check and an exclusive flag; the GPU kernel's P09 transposes two map sets). For the inference release package as delivered on the review machine, 0 of 10 plants were killed; 3 were caught only after the reviewer supplied a stand-in for a missing optional encoder.

Every plant was chosen by a reviewer, aimed at the promise the package makes (what is sent, how many times, which verdict is written). The catch share therefore measures a suite against one reviewer's imagination, not against a sampled fault distribution; it is not a mutation score and is not comparable across packages or classes. Section 3.4 gives the one mechanical sample.

We separate, for every catch, whether the failing test checks behaviour or pins the delivered bytes (a test that compares an output file to a stored copy, byte for byte). A byte pin detects a change; it does not show that the change matters.

### 2.4 Classes and raters

Each plant and real fault was given exactly one of ten classes from the record text by one agent, using a written codebook with two examples per class and five tie rules (published as `TAXONOMY.md`). A second rater of another model family then classified all 500 items blind: it saw only the codebook and the item texts, with every label and outcome removed, and it recorded a confidence (high, medium, low) for each item. Agreement was computed afterwards by a script written by an agent that rated nothing (Section 4). We report Cohen's kappa [Cohen 1960] and per-class agreement.

### 2.5 What is published

The per-plant table (`PLANTS.csv`), the per-fault table (`FINDINGS.csv`), the mutation table (`MUTATION.csv`), the codebook, the second rater's labels with confidence, and scripts that recompute every table and every number in this paper (Section 8). Package names are functional; the packages' code and the internal review records are not released, so a row can be checked for arithmetic and consistency but a plant cannot be re-run from the repository.

## 3. Results

### 3.1 Plants per round

Table 1 gives the 15 rounds. 346 of the 453 plants were caught and 107 missed. Of the 346 catches, 326 were by a test of behaviour (323, plus 3 with the stand-in encoder), 12 only by a byte-pin test, 5 by a rehearsal, 2 by a refusal of the derivation step and 1 by an aborted suite run. All 12 byte-pin-only catches and all 7 rehearsal and refusal catches are in one package, the static-site release tooling, where 10 of 32 plants were caught by a test of behaviour. Per round, the share caught ran from 30.0 to 95.2 percent; no round caught every plant, and the share did not rise steadily with suite size: the one-job script went 80.0, 75.0 and 76.7 percent while its suite grew from 67 to 103 to 140 tests.

Of the 107 misses, 12 could have changed what is sent or done according to their record, 31 could not, and 64 records do not say. Nothing in the data measures how likely a missed fault was to occur.

**Table 1. Plants per review round, first machine.** *Behaviour* counts catches by a test of behaviour (including the three with a stand-in encoder). *Share* is the share of these chosen plants that was caught by any means; it is a description, not an adequacy rate.

| Package, round | Plants | Caught | Behaviour | Missed | Share (%) | Misses that could change an action |
|---|---:|---:|---:|---:|---:|---:|
| One-job submit script, r1 | 60 | 48 | 47 | 12 | 80.0 | 4 |
| One-job submit script, r2 | 44 | 33 | 33 | 11 | 75.0 | 3 |
| One-job submit script, r3 | 30 | 23 | 23 | 7 | 76.7 | 0 |
| Once-only sealed evaluator, r1 | 30 | 20 | 20 | 10 | 66.7 | 0 |
| Once-only sealed evaluator, r2 | 50 | 35 | 35 | 15 | 70.0 | 0 |
| Once-only sealed evaluator, r3 | 68 | 59 | 59 | 9 | 86.8 | 0 |
| Once-only sealed evaluator, r4 | 35 | 28 | 28 | 7 | 80.0 | 2 |
| GPU training kernel, r1 | 20 | 11 | 11 | 9 | 55.0 | 3 |
| Static-site release tooling v2, r1 | 32 | 29 | 10 | 3 | 90.6 | 0 |
| Inference release package, r3 | 10 | 3 | 3 | 7 | 30.0 | 0 |
| Inference release package, r4 | 21 | 20 | 20 | 1 | 95.2 | 0 |
| Evaluation-record audit harness, r1 | 12 | 8 | 8 | 4 | 66.7 | 0 |
| Evaluation-record audit harness, r2 | 16 | 14 | 14 | 2 | 87.5 | 0 |
| Browser puzzle game, r1 | 5 | 4 | 4 | 1 | 80.0 | 0 |
| Frame-rendering kit, r1 | 20 | 11 | 11 | 9 | 55.0 | 0 |
| **All** | **453** | **346** | **326** | **107** | **76.4** | **12** |

### 3.2 After a revision: re-planted misses were all caught; new plants were not all caught

The rounds before a revision missed 68 plants. 55 were re-planted in the next round, with the same plant identifier, and all 55 were caught; 13 were not re-planted (11 in the one-job script's third round, where the reviewer planted only in the code changed for that round; 2 in the evaluator's fourth round, with no reason recorded). Catching misses the author was told about is expected and shows only that the author added the tests asked for. The informative figure is the other one: new plants in revised code, over 7 revised rounds, were caught 96 of 143 times (67.1 percent). Revisions also lost ground: of 66 earlier catches that were re-planted, 5 became misses, and one fix let a deleted marker file allow a second create (F08).

### 3.3 Fault classes: what was planted and what was real

Table 2 gives plants and real faults by class, with the second rater's agreement on the plants of each class. The row to read is resource or scale: none of the 453 plants is of this class, and three real faults are, all under suites with no recorded failure. Two were found by reading array sizes against a 2 GiB peak-memory guard (F22, the sealed evaluator at 63 of 63 tests; F27, the GPU training kernel at 17 of 17) and one by the first run at real shape and counts, which stopped on that guard (F23, the post-processing selection programs, which load the maps of six real training runs before scoring them; they are not among the eight planted packages and appear only in the real-fault record). Both raters put these three faults, and no plant, in this class.

The suites' inputs were small throughout, and the reviewers' plants were small changes to logic, checks and state. The recorded suites did not expose these resource faults; whether a targeted resource check at small size could have is not settled by this record. F27 itself was confirmed by a small run with only the memory reading forced to 4.6 GiB, so a small-input test of the guard is at least possible.

**Table 2. Plants and real faults by class.** *Share* is the share of chosen plants caught by any means. *Rater 2 agrees* is the number of plants of that class (first rater) that the blind second rater put in the same class. Real faults are given as all (under a suite with no recorded failure).

| Class | Plants | Caught | Share (%) | Rater 2 agrees | Real faults (green) |
|---|---:|---:|---:|---:|---:|
| Boundary or off-by-one | 26 | 24 | 92.3 | 22 | 1 (1) |
| Check weakened or removed | 147 | 109 | 74.1 | 129 | 7 (6) |
| Wrong object or value sent or used | 76 | 62 | 81.6 | 65 | 2 (2) |
| Computation or decision logic | 86 | 58 | 67.4 | 62 | 4 (4) |
| Ordering or timing of side effects | 20 | 17 | 85.0 | 20 | 5 (5) |
| State or marker handling | 55 | 43 | 78.2 | 42 | 9 (9) |
| Concurrency or atomicity | 9 | 7 | 77.8 | 9 | 0 |
| **Resource or scale** | **0** | **0** | n/a | 0 | **3 (3)** |
| Configuration or environment | 14 | 9 | 64.3 | 6 | 6 (4) |
| Output or format | 20 | 17 | 85.0 | 13 | 10 (10) |
| **All** | **453** | **346** | **76.4** | **368** | **47 (44)** |

Class-level comparisons should be read with Section 4 in mind: the raters agree fully on concurrency (9 of 9) and ordering (20 of 20) plants and well on weakened checks (129 of 147) and wrong values (65 of 76), but only on 6 of 14 configuration plants, 13 of 20 output plants and 62 of 86 logic plants.

### 3.4 How much of a catch is behaviour: a mechanical control on one package

On a scratch copy of the static-site release tooling, a standard-library script made 150 single-token mutants of the publisher and its seven step scripts (one of four operators each: a comparison flipped, a constant changed, a statement deleted, two operands swapped) and ran the package's own suite on each. None survived. But only 82 (54.7 percent) were killed by a test of behaviour; 68 (45.3 percent) were killed only by the two tests that pin the delivered bytes. When the publisher itself was mutated, its pinned hash was re-pinned so that only the fault differed, as the reviewer had done by hand. Of the 68 mutants not killed by behaviour, 67 were judged by hand and 3 looked equivalent; none of the 82 behaviour kills was judged.

**Table 3. Mechanical mutants on the static-site release tooling, by operator.**

| Operator | Mutants | Killed by a behaviour test | Killed by the byte pins only | Survived |
|---|---:|---:|---:|---:|
| Comparison flipped (CMP) | 37 | 24 | 13 | 0 |
| Constant changed (CONST) | 37 | 15 | 22 | 0 |
| Statement deleted (DEL) | 39 | 17 | 22 | 0 |
| Operands swapped (SWAP) | 37 | 26 | 11 | 0 |
| **All** | **150** | **82** | **68** | **0** |

The kills by behaviour are concentrated. Across the eight target roles, the three step scripts that install, roll back and take a read-only snapshot drew 37 mutants, of which 1 was killed by a test of behaviour. Beside the mechanical sample, the reviewer's 32 hand-chosen plants on the same package were caught 29 times: 10 by a behaviour test, 5 by the package's rehearsal, 2 by a refusal of its derivation step, 12 by byte pins only; 3 were missed. A suite in which nearly half the kills are byte pins is a suite that notices change, not one that checks what the change does; the published summary reports behaviour kills separately for this reason.

### 3.5 Real faults in delivered code

Table 4 gives the 47 real faults by how they were first found. 39 are blockers, majors, regressions or stops (9 blockers, 27 majors, 1 regression, 2 stops); 37 of those 39 sat under a suite with no recorded failure, in 10 distinct package-rounds. 12 of the 47 could, by their record, have caused a wrong or repeated irreversible action; 9 could not; 26 records do not say.

**Table 4. Real faults by how they were first found.**

| How found | Faults | Under a suite with no recorded failure |
|---|---:|---:|
| Running the code | 28 | 26 |
| Reading the source | 12 | 11 |
| Text-only reader of another family, then settled by a run | 5 | 5 |
| Text-only reader of another family, then settled by reading | 1 | 1 |
| Run at real size | 1 | 1 |
| **All** | **47** | **44** |

**What "44 of 47" does and does not say.** Packages went to non-author review after the author's suite had passed; a passing suite was the condition for review. So a fault found by review was, by construction, usually under a passing suite. The three exceptions are two faults in the inference release package, whose suite failed on the review machine (F33, F34), and one in a wrapper whose record has no suite (F39). The figure shows that passing suites did not stop these 44 faults from reaching review, and that running, reading, a text-only reader and a real-size run found them. It does not estimate how often a passing suite hides a fault, because faults the reviews did not find are not in the denominator. "No recorded failure" is the operational definition: the frame-rendering kit's suite recorded 85 of 85 passing with 3 tests skipped.

**Three cases, as the records state them.**

*A. The one-job script.* It had to create exactly one job on a quantum processor and decide the verdict of the reading. In round 1 its 67 tests passed; the reviewer ran submits from two run folders against a stand-in service and two jobs were created (F03), and found four more majors by running and one by a reader of another family (F01 to F06). In round 2, 103 tests passed over a false VOID with exit 0 when a ledger record was missing (F07) and over a deleted-marker path to a second create, a regression from round 1 (F08).

*B. A crash after the only marker.* The sealed evaluator writes a once-only marker, reads the sealed set, scores it and writes one result. Its 15 tests passed. The reviewer ran the registered path end to end on a synthetic world, which no test did: a NameError after the marker (F12), then, patched in memory, a RuntimeError, also after the marker (F13). Either would have spent the only opening with no result.

*C. The size-blind fault.* The pinned scorer refuses once its process's peak resident memory passes 2 GiB. Its suites passed on small synthetic maps. The first run at real shape and counts, of a selection program, stopped on the guard (F23, about 3.3 GiB of maps). Reading then found the same class in the evaluator, which held about 2.5 GiB of maps under the same guard (F22), before it ran. After the fix the selection programs' size tests at real shape peak at 0.460 and 0.971 GiB and the evaluator's rehearsal at 0.671 GiB. The reviewer of a new GPU training kernel, whose 17 tests passed, then recognised the class by reading array sizes (F27): the run would have trained and ended with no checkpoint.

*The frame-rendering kit.* Its suite recorded 85 of 85 tests passing. The reviewer rendered the frames and looked: seven faults were found that way, five of them blockers (numerals not in the source text, text outside its frame, labels covering drawn cells), and one more by reading the source (F47).

### 3.6 The text-only reader of another family

In six text-only reads on the first machine, readers of another model family first raised 6 of the 47 real faults: one major (F06, a repeat job authorised despite an undecided rule, settled by reading) and five lower-severity items settled by a run (F09 to F11, F25, F26). They also raised, independently of the runs that found them, 4 faults the runs had found (F01, F02, F04, F24). None of the reader-first items was of the resource class. In the one-job script's second round, where the runs found a major and a regression, the reader's three findings were all of lower severity and included neither. Text-only reading found things; it did not replace running.

### 3.7 Recorded costs

Costs were recorded for examples, not for every round, and token costs were not recorded. The figures below are transcribed from the review records (published supplement, Table S6); they have no per-row record in the CSV files.

**Table 5. Recorded costs, examples.**

| Gate | Recorded cost |
|---|---|
| G2, one-job script, rounds 1 to 3 | about 26, 26 and 20 minutes of reviewer time |
| G2, static-site release tooling | about 25 minutes for 32 plants |
| G3, paid text-only reads | USD 0.43 (a read cut off at its length limit); another about USD 0.14 |
| G4, selection programs at real shape | 495 s and 859 s |
| G4, evaluator rehearsal at real shape | six runs of 731.5 to 1,008.9 s |

### 3.8 The second machine

The second machine's lead agent compiled, from existing files and running nothing, 20 rows over 11 cases of 9 to 11 November, where authors were mostly of one model family and the run-doing reviewers of another. Its list of suites that passed over a real fault has 11 items covering 10 versions. One example: an agent harness that must hold a money cap passed 148 of 148 tests while probes found 2 blockers and 3 majors, among them 5.40 dollars counted against a 1.00 cap. One pattern recurs: where the sheet reports authors' own plants (20 of 20, 67 of 67 and 4 of 4, 66 of 66), every one was killed, while non-author plants on the same packages survived (7, 11 and 4, after further probes). These rows are compiled, some are open or provisional, and the sheet is not published; they show that passing suites over real faults were also seen where the reviewer was of another family, and nothing more. They are not a control and do not correct the first machine's counts.

## 4. The second rater

The second rater, a model of another family than the first rater and the authors, classified all 453 plants and 47 real faults from the codebook alone, with labels and outcomes removed. It rated 321 plants at high confidence, 116 at medium and 16 at low; 37 real faults at high and 10 at medium.

**Table 6. Agreement between the first rater and the blind second rater.**

| Set | Items | Same class | Raw agreement | Cohen's kappa |
|---|---:|---:|---:|---:|
| Planted faults | 453 | 368 | 0.812 | 0.768 |
| Real faults | 47 | 40 | 0.851 | 0.826 |
| All | 500 | 408 | 0.816 | 0.776 |

What holds under the second rater: the resource-or-scale row of Table 2, with 3 real faults and 0 plants; full agreement on concurrency (9 of 9) and ordering (20 of 20) plants. Where they differ: 85 plant disagreements, of which 68 carry the second rater's medium or low confidence and 17 its high. The largest single confusion is logic read as wrong value (19 plants), then state read as weakened check (7) and the reverse (6). These are the codebook's soft edges: tie rule 3 (a changed parameter versus a changed threshold) and rule 4 (state access versus a removed comparison). Among the 7 real-fault disagreements, the audit also noted that F25, a decode error after a marker that fails closed, sits in output or format against tie rule 1; we leave the first rater's label and record the exception.

We therefore keep class-level statements to the classes where the raters agree well, and we treat the configuration, output and logic rows of Table 2 as uncertain at the class boundary. Both raters' labels are published side by side.

## 5. Related work

**Mutation testing and test adequacy.** Judging a test suite by the share of seeded faults it detects goes back to DeMillo, Lipton and Sayward [1978], who stated the competent-programmer and coupling hypotheses that make small seeded faults a stand-in for real ones. Jia and Harman [2011] and Papadakis et al. [2019] survey the field, including the equivalent-mutant problem and mutant selection. Whether mutants stand in for real faults has been tested on human-written programs: Andrews, Briand and Labiche [2005] found generated mutants similar to real faults in detection difficulty, and hand-seeded faults harder to detect than either; Just et al. [2014] found mutant detection correlated with real-fault detection on real Java faults, with a minority of real faults not coupled to any mutant studied. Our plants are the hand-seeded kind: chosen by a reviewer and aimed at a promise. We report their catch share as a description and offer one mechanical sample (Section 3.4) as the comparison, not as a mutation score for the suites. Inozemtseva and Holmes [2014] found coverage not strongly correlated with suite effectiveness once suite size is controlled; our byte-pin finding is a related caution about what a passing or killing test measures. Petrović and Ivanković [2018] describe mutation testing in code review at scale, surfacing surviving mutants to reviewers; our setting puts an agent rather than a person in that reviewer's chair. The byte pin is an oracle of the weakest kind; Barr et al. [2015] survey the oracle problem.

**Agent benchmarks and test-based judging.** Benchmarks for code-writing models judge a candidate by tests: HumanEval [Chen et al. 2021] by hand-written unit tests, SWE-bench [Jimenez et al. 2024] by tests from the repository that must go from failing to passing. The adequacy of those tests is an open question in the same literature. Liu et al. [2023] augmented HumanEval's tests and found that pass rates fell, that is, the original tests had accepted wrong programs; SWE-bench Verified [Princeton NLP 2024] is a 500-task subset human-validated for, among other things, test specificity; Aleithan et al. [2024] report solution leakage and weak tests in SWE-bench instances. These are the same gap we report from the receiving end: a passing suite over a wrong program. Zheng et al. [2023] measure how well a model judging text agrees with people; our text-only reader (G3) is such a judge, and we found that its claims needed settling by a run.

**Field records.** This paper is a case record in the sense of Runeson and Höst [2009]: one organisation, a bounded period, data from its own artefacts, and no control. We follow their advice to state the chain of evidence; the per-row tables, the audit ledger and the agreement script are that chain.

## 6. Threats to validity

**Selection of plants.** Every plant was chosen by a reviewer who had read the code. The 76.4 and 72.0 percent describe those plants and nothing else; they are not adequacy rates, not mutation scores, and not comparable across packages or classes. Class sizes in Table 2 say what reviewers chose to plant.

**Selection of real faults.** The 47 faults are the faults the reviews found, in packages sent to review because their suites had passed. 44 of 47 cannot be read as a rate at which suites miss faults (Section 3.5). A fault invisible to running on synthetic stand-ins, to reading, to a text-only reader and to one real-size run is not counted, and nothing shows accepted packages free of faults.

**Independence.** For 44 of the 47 real faults the run-doing reviewer was of the author's model family; shared blind spots may make the counts low. The second machine's cross-family rows are compiled from files, partly open, and unpublished; they are not a control. The second rater and the data audit were by another family, but they classified and checked records; neither reviewed code.

**Scope.** One company, three calendar days of records, eight packages on the first machine, no control group, no causal claim and no frequency claimed beyond these records. Model families are not named, and prompts, patches, package code and primary logs are not released; arithmetic can be reproduced, fault validity cannot.

**Record quality.** Eight rows of `PLANTS.csv` (the audit harness, round 1) record a catch and name failing tests while their note says "survivor; tied to a finding of the review"; we keep the caught field and flag the rows. The "full rerun after each plant" is what the records say; run-level logs are not public, and for the browser game the named failing tests total fewer than the suite size, so a partial record there is possible. 64 of the 107 misses have no stated impact. At least two plants change more than one thing; one catch is an aborted run; three catches needed a stand-in the reviewer supplied. Granularity of a real fault was not prespecified: two selection programs with the same memory fault are one row (F23), and F47 holds two defects.

**Classes.** Two raters, kappa 0.776; agreement is weak on configuration (6 of 14), output (13 of 20) and logic (62 of 86) plants, and the codebook has at least one recorded exception (F25). The resource row does not depend on this: both raters agree on all of it.

**Gate attribution.** "How found" credits a first discovery. Gates ran together and packages received different gates and effort, so Table 4 counts attributions, not gate sensitivity.

**Costs.** Timings cover examples; token costs were not recorded; avoided losses (a second processor job, a GPU run with no checkpoint, the only opening of a sealed set) are reviewers' estimates, not realised losses.

**The uncompleted reader test.** A preregistered test of a small open-weights model as the text-only reader was started on the second machine; two of its fifteen planned calls were made and returned no answer text, the run stopped by its own rule, and thirteen calls were never made. Nothing from it is reported.

## 7. What we changed in practice

The following is the review practice QuantumMind AI adopted during and after these records. It is stated as practice and as the hypothesis each step rests on. None of it has been tested against a control, and this paper does not show that it works.

1. **Treat the author's passing suite as the condition for review, not as the verdict.** Observation: 44 of 47 real faults were found after a pass. Hypothesis: a non-author run finds faults the author's tests do not express.
2. **Plant where the promise lives, rerun after each plant, and record whether each catch is by behaviour or by a byte pin.** Observation: 12 of 346 catches, and 68 of 150 mechanical kills, were byte pins only. Hypothesis: a catch share without this split overstates what a suite checks.
3. **Re-plant last round's misses, and plant the new code.** Observation: re-planted misses were caught 55 of 55; new plants 96 of 143. Hypothesis: the second number, not the first, tracks the suite.
4. **Run the shipped entry point end to end on synthetic stand-ins and look at the output.** Observation: cases B and the frame-rendering kit. This is textbook integration testing; the records show it was missing.
5. **Attack a once-only promise from outside the process:** two processes at once, a kill at each step between marker and act, deleted or linked records. Observation: F03, F08, F15, F20, F31.
6. **Before any one-shot step, run once at real shape and counts, with a check that fails on the old code, and record peak memory.** Observation: F22, F23, F27 and the empty resource row. Hypothesis: resource faults do not appear at small size and reviewers do not plant them.
7. **Send the code to a text-only reader of another family and settle each claim by a run or by reading.** Observation: 6 reader-first faults, 1 major; silence on two run-found severe faults in one round. Hypothesis: a reader adds findings at low cost but its silence is not evidence.
8. **Gate the one-shot act on a written go-ahead naming the accepted manifest hash.** This is textbook release control; it is listed because the records show the acts it guards.

For the paper itself we adopted: a second blind rater for every classification, an audit of the published data by a model of another family before publication, and a script that recomputes every number in the text.

## 8. Data and code availability

The data repository (Apache License 2.0) holds `PLANTS.csv`, `FINDINGS.csv`, `MUTATION.csv`, `TAXONOMY.md`, `SUMMARY.md` and `summarize.py`, and the first version of this paper with its supplement: https://github.com/QuantumMindAI-Org/green-suite-partial-gate-data. This revision adds the second rater's labels (`LABELS_PLANTS.csv`, `LABELS_FINDINGS.csv`, with confidence and reasons), the agreement script (`agreement.py`) and its output, the audit's claim ledger, and `verify_numbers.py`, which recomputes every number in this text and prints MATCH or MISMATCH per number; its output accompanies the source. The second machine's sheet and the internal review records are not published.

## 9. AI-authorship disclosure

The software described here was written, tested and reviewed by AI agents of several model families; the engineering decisions, the plants, the reviews and the classifications in the record are theirs. This text was drafted by an AI agent from the company's records and the published data, by an agent that did not write the first version. Every number was recomputed from the published files by a script (`verify_numbers.py`); the published data were audited by an agent of another model family, whose corrections (among them the 440 and 13 split and the seven-by-rendering, one-by-reading count for the frame kit) are incorporated; the fault classes were rated blind by a second agent of another family. The author reviewed and approved the text and is responsible for it. No person other than the author took part.

## References

- Aleithan, R., Xue, H., Mohajer, M. M., Nnorom, E., Uddin, G., Wang, S. (2024). SWE-Bench+: Enhanced Coding Benchmark for LLMs. arXiv:2410.06992.
- Andrews, J. H., Briand, L. C., Labiche, Y. (2005). Is mutation an appropriate tool for testing experiments? In *Proceedings of the 27th International Conference on Software Engineering (ICSE '05)*, 402–411. ACM. doi:10.1145/1062455.1062530.
- Barr, E. T., Harman, M., McMinn, P., Shahbaz, M., Yoo, S. (2015). The Oracle Problem in Software Testing: A Survey. *IEEE Transactions on Software Engineering* 41(5), 507–525. doi:10.1109/TSE.2014.2372785.
- Chen, M., Tworek, J., Jun, H., et al. (2021). Evaluating Large Language Models Trained on Code. arXiv:2107.03374.
- Cohen, J. (1960). A Coefficient of Agreement for Nominal Scales. *Educational and Psychological Measurement* 20(1), 37–46. doi:10.1177/001316446002000104.
- DeMillo, R. A., Lipton, R. J., Sayward, F. G. (1978). Hints on Test Data Selection: Help for the Practicing Programmer. *Computer* 11(4), 34–41. doi:10.1109/C-M.1978.218136.
- Inozemtseva, L., Holmes, R. (2014). Coverage is not strongly correlated with test suite effectiveness. In *Proceedings of the 36th International Conference on Software Engineering (ICSE 2014)*, 435–445. ACM. doi:10.1145/2568225.2568271.
- Jia, Y., Harman, M. (2011). An Analysis and Survey of the Development of Mutation Testing. *IEEE Transactions on Software Engineering* 37(5), 649–678. doi:10.1109/TSE.2010.62.
- Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? *ICLR 2024*. arXiv:2310.06770.
- Just, R., Jalali, D., Inozemtseva, L., Ernst, M. D., Holmes, R., Fraser, G. (2014). Are mutants a valid substitute for real faults in software testing? In *Proceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering (FSE 2014)*, 654–665. ACM. doi:10.1145/2635868.2635929.
- Liu, J., Xia, C. S., Wang, Y., Zhang, L. (2023). Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation. arXiv:2305.01210.
- Princeton NLP (2024). SWE-bench Verified: a human-validated subset of 500 SWE-bench tasks. Dataset card, princeton-nlp/SWE-bench_Verified, Hugging Face. https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified
- Papadakis, M., Kintis, M., Zhang, J., Jia, Y., Le Traon, Y., Harman, M. (2019). Mutation Testing Advances: An Analysis and Survey. *Advances in Computers* 112, 275–378. Elsevier. doi:10.1016/bs.adcom.2018.03.015.
- Petrović, G., Ivanković, M. (2018). State of mutation testing at Google. In *Proceedings of the 40th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP '18)*, 163–171. ACM. doi:10.1145/3183519.3183521.
- Runeson, P., Höst, M. (2009). Guidelines for conducting and reporting case study research in software engineering. *Empirical Software Engineering* 14(2), 131–164. doi:10.1007/s10664-008-9102-8.
- Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS 2023 Datasets and Benchmarks Track*. arXiv:2306.05685.
