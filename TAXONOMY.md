# Fault classes used in PLANTS.csv and FINDINGS.csv

Ten classes, built from the 433 planted faults and the 47 real faults in this folder. Each fault gets exactly one class: the one that names **what the change does to the program**, not where it sits or what it costs. When two classes fit, the rules at the end decide. The examples quote the `what_changed` or `fault` column; the ids let a reader find the row.

| code | class | definition |
|---|---|---|
| B | boundary or off-by-one | A comparison operator, an inclusive/exclusive edge, or a threshold constant moved by one step, so that the value at the edge is decided the other way. |
| G | check weakened or removed | A check that should refuse, flag or stop no longer does, or does so for fewer inputs: a guard deleted, a hash compared on a prefix, a tolerance widened, a refusal replaced by a pass. |
| W | wrong object or value sent or used | The right code path runs on the wrong thing: another object is sent, a constant or parameter has another value, two arms are swapped, a wrong file or directory is addressed. |
| L | computation or decision logic | The inputs are right but the program computes a wrong number or reaches a wrong decision from them: statistics, numerics, geometry, verdict rules. |
| O | ordering or timing of side effects | The same side effects happen in another order or at another time, typically an untested step that now runs after an irreversible marker or before a result is safe. |
| S | state or marker handling | Persistent state that guards a once-only act is written, read, scoped or recovered wrongly: once-only markers, ledgers, witnesses, resume state, records written around an irreversible call. |
| C | concurrency or atomicity | Exclusivity or atomicity is lost: a lock not taken, an exclusive create made non-exclusive, a check not repeated under the lock. |
| R | resource or scale | The program fails or misbehaves only at real size: memory, wall time, disk. |
| E | configuration or environment | Behaviour depends on how the program is configured or where it runs: thread counts, paths taken from the environment or an argument, optional packages, machine differences. |
| F | output or format | What is written or shown is wrong in form or content while the computation is right: file encodings, names, record fields, exit codes, rendered text. |

## Two examples per class

- **B**: `hour: < 05:30 written <=` (one-job submit script r1, P02, caught); `low cut >= changed to > (post-processing)` (inference release package r4, N07, missed by all 82 tests). Real fault: an authorised repeat job can be created on the same UTC day as the first run (F02).
- **G**: `freeze-record hash compare on 8 chars` (one-job submit script r1, P46, missed); `typed candidate hash not compared` (once-only sealed evaluator r4, M4a, missed). Real fault: the wrapper's first acceptance check reads a key absent from every record, so it cannot fail (F39).
- **W**: `logical (uncompiled) circuits sent` (one-job submit script r1, P29, missed); `G reported as R2` (once-only sealed evaluator r4, M6b, missed). Real fault: the audit harness serialises records differently from the real wrapper (F35).
- **L**: `unpaired resample C vs G` (once-only sealed evaluator r1, F12, missed); `test maps flipped vertically (test path only)` (GPU training kernel r1, P10, missed). Real fault: the outcome reader misclassifies foreseeable records (F37).
- **O**: `marker created after compute (order)` (once-only sealed evaluator r1, F20, missed); `witness marker not written before the call` (one-job submit script r3, Q13, caught). Real fault: the open step crashes with a NameError after the once-only marker is written (F12).
- **S**: `ledger per root again` (one-job submit script r2, N01, caught); `resume checks only the package marker` (once-only sealed evaluator r3, R13, missed). Real fault: a missing or failed ledger job record makes a good one-job run VOID with exit 0 (F07).
- **C**: `lock opened without O_EXCL` (one-job submit script r2, N03, caught); `O_EXCL dropped on marker create` (once-only sealed evaluator r3, F02, missed). No real fault in this class.
- **R**: no plant in this class. Real faults: peak memory at real size in the sealed evaluator (F22) and in the selection programs (F23); the training kernel's validation scoring refused at real size (F27).
- **E**: `ledger path taken from the environment` (once-only sealed evaluator r3, R05, missed); `pinned split accepted with --allow-short-table` (once-only sealed evaluator r2, N15, missed). Real fault: the documented command stops with a traceback when an optional package is absent (F34).
- **F**: `CSV written with CRLF` (GPU training kernel r1, P14, missed); `failed record writes exit 0` (one-job submit script r3, Q19, caught). Real fault: counters show a numeral that is not in the source text for about 6 s (F40).

## Rules when two classes fit

1. A crash or step that runs after an irreversible marker is **O**, even when its root cause is configuration (F12, F13; the root cause is in `how_found_note`).
2. A tolerance or band widened is **G** (a check weakened), not **B**; an edge operator or a threshold moved by one step is **B**.
3. A constant that changes what is sent or used (shots, seed, stride, device) is **W**; a constant that is a threshold is **B**.
4. A guard that protects once-only state (markers, ledger, witness, resume) is **S** when the plant changes where or whether the state is written or read, and **G** when it only removes a comparison (for example a hash not compared).
5. A wrong verdict that follows from a missing record is **S** (F07); a wrong verdict from complete records is **L** (F01, F04).

## Limits

- The classes were assigned by one agent from the record text, without a second rater. No agreement statistic exists.
- The plants were chosen by reviewers. Class sizes say what reviewers chose to plant, not how often each class occurs.
