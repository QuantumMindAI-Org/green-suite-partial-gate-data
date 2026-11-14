# A Green Suite Is a Partial Gate: Planted Faults in Agent-Written Code

*Planted faults, non-author runs and real-size rehearsal in the review of agent-written code: records of 9 to 11 November 2026*

As submitted to the Kaggle "Gemma 4 Developer Agent Paper Track" on 12 November 2026 (non-archival). The tables cut for the track's word limit are in `SUPPLEMENT.md`.

> Drafted by AI agents from the company's own records; every number was re-derived from those records by a non-author agent; the full text was reviewed by Victor Dominguez, then shortened to the word limit (its other tables are in the public supplement).

## Abstract

QuantumMind AI is a one-person company whose software is written, tested and reviewed by AI agents. We report its review records from two machines. On the first, agents that had not written the code planted 453 faults in eight packages over 15 review rounds and reran the authors' suites after each. The suites caught 346. The reviews also found 47 real faults in delivered code, and 44 of them sat under a suite that passed in full. No reviewer planted a fault of resource or scale, yet three such faults were real: reading sizes found two, and a real-size run that stopped found one. On a second machine, whose records were compiled separately and where most reviewers were of another model family than the authors, the records list 11 instances, in 10 versions, of a suite that passed over a real fault. We give a numbered procedure with recorded costs. We claim no causal effect and no frequency beyond these records.

## 1. Introduction

An author agent writes the code and the tests that judge it, and the tests pass. What is that pass worth? The question is sharpest for a developer agent fixing real issues offline on consumer hardware: no person reads each change, and the passing suite is the gate. Some steps can be taken only once (one paid job, one sealed test set, one live install), and a fault found after them cannot be repaired by running again.

This paper reports what happened when agent-written code with a passing suite went to an agent that had not written it. It is a field record, not an experiment. We contribute a classified per-plant record of 453 planted faults and 47 real ones, with the gate that found each; a second, separately compiled body of cases with mostly cross-family reviewers; and a numbered procedure.

## 2. Methods

**Setting and gates.** Agents of several model families write, review and run the company's software on two machines and rented services. Each package arrives with a hash manifest and the author's tests, and a coordinating agent sends it through some of these gates:

- **G1, author tests**, run by the author.
- **G2, non-author runs.** Another agent runs the suite on a scratch copy, plants faults one at a time with a full rerun after each, attacks the package's promises by running it (killed processes, two processes at once, damaged records) and reads the source.
- **G3, text-only reader of another family.** A paid model reads the code and a brief, runs nothing, and returns findings; G2 settles each claim.
- **G4, run at real size:** the real shape and counts of the data, on synthetic stand-ins, before the step that can be taken once.
- **G5, go-ahead:** the one-shot act needs a written go-ahead naming the accepted manifest hash.

On the first machine the run-doing reviewer was of the author's model family, in a separate context, for 44 of the 47 real faults.

**Data.** First machine: every review round dated 10 or 11 November 2026 whose record lists its plants one by one: 15 rounds of 8 packages, 453 plants (433 plants, 335 caught, without a frame-rendering kit reviewed later); supplement Table S1 lists the packages. Real faults (47) are every blocker, major, regression or stop a review named in delivered code, plus the minor items and notes our evidence table cites; gaps shown only by plants are not faults. Second machine: its lead agent compiled 20 rows over 11 cases from existing files, running nothing; its counts stay apart (Section 3.7).

**Plants.** A plant is a small change to delivered code, usually one line, that some test should catch; *caught* means at least one test failed (on one package also its rehearsal or a refusal step, Section 3.4). 440 plants were the reviewer's and 13 the author's own, re-run by the reviewer. At least two change more than one line or one thing; one catch rests on an aborted suite run. For one package as delivered, 0 of 10 plants were killed; 3 only after the reviewer supplied a stand-in for a missing optional package.

**Classes.** One agent gave each plant and fault one of ten classes from the record text, with written tie rules and no second rater.

## 3. Experiments and results

### 3.1 Plants per round

The suites caught 346 of the 453 plants (76.4 percent) and missed 107; per round the share ran from 30.0 to 95.2 percent (supplement Table S3). No round caught every plant, and the share did not rise steadily: the one-job script went 80.0, 75.0, 76.7 percent while its suite grew from 67 to 140 tests. Of the 107 misses, 12 could have changed what is sent or done according to their record, 31 could not, and 64 records do not say.

### 3.2 Re-planted misses were caught; new plants were not

The rounds before a revision missed 68 plants. 55 were re-planted in the next round and all 55 were caught; 13 were not re-planted (11 because one reviewer planted only in the code changed for that round; for 2 the reason is not recorded). Catching misses the author was told about is expected; new plants in revised code (7 rounds) were caught 96 of 143 times (67.1 percent). Revisions also lost ground: 5 earlier catches became misses, and one fix let a deleted marker file allow a second create.

### 3.3 Fault classes: what was planted, what was real

**Table 1. Plants and real faults by class**

| Class | Plants | Caught % | Real faults (suite green) |
|---|---|---|---|
| Boundary or off-by-one | 26 | 92.3 | 1 (1) |
| Check weakened or removed | 147 | 74.1 | 7 (6) |
| Wrong object or value sent or used | 76 | 81.6 | 2 (2) |
| Computation or decision logic | 86 | 67.4 | 4 (4) |
| Ordering or timing of side effects | 20 | 85.0 | 5 (5) |
| State or marker handling | 55 | 78.2 | 9 (9) |
| Concurrency or atomicity | 9 | 77.8 | 0 |
| **Resource or scale** | **0** | **n/a** | **3 (3)** |
| Configuration or environment | 14 | 64.3 | 6 (4) |
| Output or format | 20 | 85.0 | 10 (10) |
| **All** | **453** | **76.4** | **47 (44)** |

The striking row is resource or scale: none of the 453 plants was of this class, yet three real faults were, all under green suites. Reading sizes found two and a real-size run that stopped found one. The suites' inputs were small throughout, so a plant of this class would have needed a test at real size to be caught.

The 37 blockers, majors, regressions and stops among the 44 green-suite faults fall in 10 distinct package-rounds. Running the code found 28 of the 47 real faults; reading the source 12; other-family readers first raised 6; a real-size run met 1. The plainest: a frame-rendering kit passed 85 tests; the reviewer rendered the frames, looked, and found eight faults, five of them blockers.

### 3.4 How much of a catch is behaviour

On the third-article publisher, a standard-library script made 150 single-token mutants and ran the 38-test suite on each. None survived, but only 82 were killed by a test of behaviour; 68 were killed only by the two tests that pin the delivered bytes. Of the reviewer's 32 hand plants on the same package, 29 were caught: 10 by a behaviour test, 5 by the package's rehearsal, 2 by a refusal of its derivation step, 12 by byte pins only. In three of its step scripts (install, rollback, read-only snapshot), 1 of 37 mutants was killed by behaviour.

### 3.5 Three cases

**A. The one-job script, three rounds.** It had to create exactly one job on a quantum processor and decide the verdict of the reading. Round 1 came with 67 passing tests; against a fake service that counts creates across processes, two submits started at the same instant from two run folders both created, and 12 of 60 plants left all tests passing. Round 2 passed 70 of 70 races between two real processes, yet its 103 tests passed over a false VOID with exit 0 and a deleted-marker path to a second create. In round 3 (140 tests), a second create needed all three independent records of the first to be gone. All these paths were shown against the fake service, never on the processor; on the real service one job was created, with one create attempt.

**Box 1. A worked example from round 1.** *Planted fault:* the check before the create ran on the compiled circuits while the uncompiled circuits were sent (one word changed). *Suite result:* all 67 tests passed; they checked only the number of circuits sent and their shots. *Missing test:* the circuits handed to the create call must hash to the prepared compiled-set hash.

**B. A crash after the only marker.** The evaluator writes a marker, reads the sealed set, scores it and writes one result. Its 15 tests passed. The reviewer ran the registered path end to end on a synthetic world, which no test did: a NameError after the marker, then, patched in memory, a RuntimeError about 80 seconds later. Either would have spent the only opening with no result.

**C. The size-blind fault.** The evaluator's first reviewer noted that all maps are held at once, about 2.6 GB, and judged that fine. The binding limit was the pinned scorer, which refuses once its process's peak resident memory passes 2 GiB. Four suites and four reviews passed, all on small synthetic maps, and no rehearsal at real size had been ordered: the first real run at real size, of a selection program, stopped on the guard. Reading then found the same fault in the evaluator and in a second selection program, before either ran (Table 1 counts the two selection programs as one fault). The fix's tests at real shape fail on the old code (peak 2.508 GiB) and pass on the new (0.460 and 0.971 GiB). The same day, the reviewer of a new GPU training job, whose 17 tests passed with a 1.0 GB dry run, recognised the class by reading sizes: by the reviewer's estimate, that job would have trained for up to 1.75 GPU-hours and ended with no checkpoint.

### 3.6 The text-only reader, and costs

In six text-only reads on the first machine, readers of other families first raised 6 of the 47 real faults: one major (a repeat authorised despite an undecided rule) and five minor items or notes. They also raised independently 4 that runs found. None concerned memory. In one-job script r2, where the runs found a major and a regression, the reader's three findings, all minor, included neither.

Recorded costs: G2 took about 26, 26 and 20 minutes of reviewer time in the one-job script's three rounds; paid G3 reads cost USD 0.43 and about USD 0.14; G4 took 495 s and 859 s for the selection programs and 731.5 to 1,008.9 s for each of six evaluator rehearsal runs. A miss, as reviewers estimated it: a second processor job; up to 1.75 GPU-hours; the only opening of a sealed set. Token costs were not recorded.

### 3.7 The second machine: mostly cross-family reviewers

The second machine's lead compiled its own record of 9 to 11 November: authors mostly of one family, run-doing reviewers of another. Its compiler sets three limits: nothing was found at real size or in a real environment, beyond one run inside an installed copy of a pinned library; rows under review are open; one row is provisional. Supplement Table S2 gives its rows. Its list of suites that passed over a real fault has 11 items covering 10 versions; for example, an agent harness that must hold a money cap passed 148 of 148 tests while probes found 2 blockers and 3 majors, among them 5.40 dollars counted against a 1.00 cap.

One pattern repeats. Where the sheet reports authors' own plants (the money-cap harness 20 of 20, a sealed package chain's two candidates 67 of 67 and 4 of 4, a results-page program 66 of 66), every one was killed, while non-author plants on the harness, the chain and the results-page program survived (7, 11 and 4). The second machine shows that green suites over real faults were also found where the reviewer was of another family; it does not correct the first machine's counts.

## 4. The procedure

1. **Treat the author's green suite as an entry ticket.** Rerun it from the manifest in a scratch copy; 44 of the 47 real faults sat under one.
2. **Plant where the promise lives** (what is sent, how many times, which verdict is written), rerun the full suite after each plant, and record whether each catch is by behaviour or only by a byte pin.
3. **Re-plant last round's misses, and plant the new code:** re-planted misses were all caught; new plants, two times in three.
4. **Run the shipped entry point end to end on stand-ins** and look at its output (case B).
5. **Attack a once-only promise from outside the process:** two real processes at once, a kill at every step between marker and act, deleted or linked records (case A).
6. **Before any one-shot step, run once at real shape and counts,** with a control that fails on the old code, and record peak memory (case C).
7. **Send the code to a text-only reader of another model family** and settle each claim by a run; its silence is not a run.
8. **Gate the one-shot act on a written go-ahead** naming the accepted manifest hash.

## 5. Discussion: what this means for a local developer agent

A developer agent fixing real issues offline on consumer hardware is the plainest case of what we studied: one model writes the change and its tests, and nobody else reads it. Here a pass was a ticket, not a verdict. Non-author runs with planted faults cost minutes per round, if the plants move with the code and catches are checked for behaviour. Text-only readers of another family cost cents and first raised one major decision fault and five minor items; they did not replace running. The resource faults were found only by reading sizes or by a run at real size. In our view these gates could sit inside an agent harness; we did not test that.

## 6. Limits

This is one organisation over three days, with no control group. We make no causal claim and claim no frequency beyond these records. Accepted packages are not shown to be free of faults; the evidence after acceptance is operational only: one processor job created once, one sealed opening with exit 0, one page installed with 238 of 238 readback checks. On the first machine the run-doing reviewer shared the author's model family for 44 of 47 real faults; shared blind spots may make our counts low. The second machine's cross-family reviews are separate records, compiled from files, with some rows open or provisional; they are not a control.

Every plant was chosen, not sampled, so "caught" measures a suite against someone's imagination; catch rates are not mutation scores, and the one mechanical sample covers one package. Classes come from one rater. 64 of 107 misses have no stated impact. Relevance to a small local developer agent is argued, not measured. A preregistered test of a small open-weights model as the text-only reader was not completed and is not reported.

## 7. Related work

Mutation testing judges a suite by the share of seeded faults it detects [3]; whether seeded faults stand in for real ones has been studied on human-written programs [4]. A widely used benchmark of model-written patches judges a patch by tests from the repository [5]; whether such tests are adequate to show a patch correct is itself an open question. Our plants are hand-chosen and aimed at stated promises; one mechanical census is the comparison. We add the receiving end for agent-written code: what a passing suite hid and which gate found it. Earlier single cases from the same company are public [1, 2].

## Data and reproducibility

The first machine's per-plant table, findings table, mutation table, taxonomy and summary script are published at https://github.com/QuantumMindAI-Org/green-suite-partial-gate-data , with SUPPLEMENT.md holding Tables S1 (packages), S2 (second machine), S3 (plants per round) and the re-plant, class-by-gate and cost tables. The second machine's underlying sheet is not published. Package names are functional; the packages' code is not released.

## References

1. QuantumMind AI. "All 177 acceptance cases passed; the notebook as shipped failed 16 lines past where they stopped." November 2026. https://qmai.dev/research/articles/green-tests-dead-notebook-2026-11-11/
2. QuantumMind AI. "The deploy instruction said to copy two files; a hash check before starting the container found two others out of date." November 2026. https://qmai.dev/research/articles/hash-check-before-container-start-2026-11-11/
3. R. A. DeMillo, R. J. Lipton, F. G. Sayward. "Hints on Test Data Selection: Help for the Practicing Programmer." Computer 11(4), 1978.
4. R. Just et al. "Are Mutants a Valid Substitute for Real Faults in Software Testing?" FSE 2014.
5. C. E. Jimenez et al. "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" ICLR 2024.
