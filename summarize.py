"""Compute every table in SUMMARY.md from PLANTS.csv, FINDINGS.csv and MUTATION.csv (standard library only).
Usage: python3 -I -B summarize.py            -> rewrites SUMMARY.md next to this file
       python3 -I -B summarize.py --check    -> exit 1 if SUMMARY.md differs from a fresh computation
MIT licence.
"""
import csv, os, sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
CLASSES = OrderedDict([("B", "boundary or off-by-one"), ("G", "check weakened or removed"),
                       ("W", "wrong object or value sent or used"), ("L", "computation or decision logic"),
                       ("O", "ordering or timing of side effects"), ("S", "state or marker handling"),
                       ("C", "concurrency or atomicity"), ("R", "resource or scale"),
                       ("E", "configuration or environment"), ("F", "output or format")])
# The scope memo's evidence table, file-backed rows with plants: row -> (package, round, made, caught, missed)
SCOPE_ROWS = [(1, "one-job submit script", "r1", 60, 48, 12), (2, "one-job submit script", "r2", 44, 33, 11),
              (3, "one-job submit script", "r3", 30, 23, 7), (4, "once-only sealed evaluator", "r1", 30, 20, 10),
              (5, "once-only sealed evaluator", "r2", 50, 35, 15), (6, "once-only sealed evaluator", "r3", 68, 59, 9),
              (7, "once-only sealed evaluator", "r4", 35, 28, 7), (11, "GPU training kernel", "r1", 20, 11, 9),
              (14, "static-site release tooling v2", "r1", 32, 29, 3), (16, "inference release package", "r3", 10, 3, 7),
              (17, "inference release package", "r4", 21, 20, 1), (18, "evaluation-record audit harness", "r1", 12, 8, 4),
              (19, "evaluation-record audit harness", "r2", 16, 14, 2), (21, "browser puzzle game", "r1", 5, 4, 1)]
SCOPE_TOTAL = (433, 335, 98)
# The scope memo's nine file-backed green-suite cases: scope row -> the (package, round) keys they cover here
SCOPE_GREEN = OrderedDict([(1, [("one-job submit script", "r1")]), (2, [("one-job submit script", "r2")]),
                           (4, [("once-only sealed evaluator", "r1")]), (5, [("once-only sealed evaluator", "r2")]),
                           (8, [("once-only sealed evaluator", "r4"), ("post-processing selection programs", "r4")]),
                           (11, [("GPU training kernel", "r1")]), (13, [("static-site release tooling v1", "r2")]),
                           (18, [("evaluation-record audit harness", "r1")]), (20, [("evaluation-run wrapper", "as run")])])
MAJOR_LIKE = ("BLOCKER", "MAJOR", "regression", "stop")
ROUND_ORDER = {"r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5}

def load(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return None
    with open(p, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def pct(a, b):
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"

def md(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)

def ordered_rounds(rows):
    seen = OrderedDict()
    for r in rows:
        seen.setdefault((r["package"], r["round"]), None)
    return list(seen)

def compute():
    P, F, M = load("PLANTS.csv"), load("FINDINGS.csv"), load("MUTATION.csv")
    res = OrderedDict()
    caught = [r for r in P if r["caught"] == "caught"]
    missed = [r for r in P if r["caught"] == "missed"]
    res["total"] = (len(P), len(caught), len(missed))
    # T1 per package and round
    t1 = []
    for key in ordered_rounds(P):
        rr = [r for r in P if (r["package"], r["round"]) == key]
        c = sum(r["caught"] == "caught" for r in rr)
        m = len(rr) - c
        y = sum(r["miss_could_change_action"] == "yes" for r in rr)
        t1.append((key[0], key[1], len(rr), c, m, pct(c, len(rr)), y))
    res["t1"] = t1
    # T2 by class
    t2 = []
    for k, name in CLASSES.items():
        rr = [r for r in P if r["fault_class"] == k]
        c = sum(r["caught"] == "caught" for r in rr)
        pk = len(set(r["package"] for r in rr))
        t2.append((k, name, len(rr), c, len(rr) - c, pct(c, len(rr)), pk))
    res["t2"] = t2
    # caught-by kind
    res["kind"] = Counter(r["caught_by_kind"] for r in caught)
    # T3 before / after a revision: same plant id, same package, consecutive rounds that both hold it
    trans, newp = [], []
    for pkg in OrderedDict((r["package"], None) for r in P):
        rounds = sorted(set(r["round"] for r in P if r["package"] == pkg), key=lambda x: ROUND_ORDER.get(x, 9))
        seen_ids = set()
        prev = None
        for rnd in rounds:
            cur = {r["plant_id"]: r["caught"] for r in P if r["package"] == pkg and r["round"] == rnd}
            if prev is not None:
                pr, pdict = prev
                mc = sum(1 for i in cur if i in pdict and pdict[i] == "missed" and cur[i] == "caught")
                mm = sum(1 for i in cur if i in pdict and pdict[i] == "missed" and cur[i] == "missed")
                cc = sum(1 for i in cur if i in pdict and pdict[i] == "caught" and cur[i] == "caught")
                cm = [i for i in cur if i in pdict and pdict[i] == "caught" and cur[i] == "missed"]
                notre = sum(1 for i in pdict if pdict[i] == "missed" and i not in cur)
                trans.append((pkg, "%s to %s" % (pr, rnd), mc, mm, notre, cc, len(cm), ", ".join(sorted(cm)) or "-"))
                new = [i for i in cur if i not in seen_ids]
                nc = sum(cur[i] == "caught" for i in new)
                newp.append((pkg, rnd, len(new), nc, pct(nc, len(new))))
            seen_ids |= set(cur)
            prev = (rnd, cur)
    res["t3"], res["t3new"] = trans, newp
    # T5 missed plants that could change an action
    res["t5"] = Counter(r["miss_could_change_action"] for r in missed)
    res["t5_by_pkg"] = [(k, sum(r["miss_could_change_action"] == "yes" for r in missed if r["package"] == k),
                         sum(r["package"] == k for r in missed)) for k in OrderedDict((r["package"], None) for r in P)]
    # Findings
    res["f_total"] = len(F)
    res["f_how"] = [(h, sum(r["how_found"] == h for r in F),
                     sum(r["how_found"] == h and r["suite_fully_green"] == "yes" for r in F),
                     sum(r["how_found"] == h and r["severity"].startswith(MAJOR_LIKE) for r in F))
                    for h in OrderedDict((r["how_found"], None) for r in F)]
    res["f_green"] = Counter(r["suite_fully_green"] for r in F)
    res["f_irrev"] = Counter(r["could_cause_wrong_or_repeated_irreversible_action"] for r in F)
    res["f_class"] = [(k, CLASSES[k], sum(r["fault_class"] == k for r in F),
                       sum(r["fault_class"] == k and r["suite_fully_green"] == "yes" for r in F)) for k in CLASSES]
    res["f_sev"] = Counter(r["severity"] for r in F)
    res["f_fixed"] = Counter(r["rounds_until_fixed"] for r in F)
    res["f_family"] = Counter(r["run_doing_reviewer_family"] for r in F)
    # gate x class (findings)
    hows = list(OrderedDict((r["how_found"], None) for r in F))
    res["gate_class"] = (hows, [(k,) + tuple(sum(r["fault_class"] == k and r["how_found"] == h for r in F) for h in hows)
                                for k in CLASSES if any(r["fault_class"] == k for r in F)])
    # green-suite distinct cases (major-like severity)
    cases = OrderedDict()
    for r in F:
        if r["suite_fully_green"] == "yes" and r["severity"].startswith(MAJOR_LIKE):
            cases.setdefault((r["package"], r["round"]), []).append(r["finding_id"])
    res["green_cases"] = cases
    # reconciliation per scope row
    rec = []
    for row, pkg, rnd, m, c, x in SCOPE_ROWS:
        rr = [r for r in P if r["package"] == pkg and r["round"] == rnd]
        cc = sum(r["caught"] == "caught" for r in rr)
        rec.append((row, pkg, rnd, "%d/%d/%d" % (m, c, x), "%d/%d/%d" % (len(rr), cc, len(rr) - cc),
                    "same" if (m, c, x) == (len(rr), cc, len(rr) - cc) else "DIFFERS"))
    res["recon"] = rec
    keys = set((pkg, rnd) for _, pkg, rnd, _, _, _ in SCOPE_ROWS)
    sub = [r for r in P if (r["package"], r["round"]) in keys]
    sc = sum(r["caught"] == "caught" for r in sub)
    res["scope_sub"] = (len(sub), sc, len(sub) - sc)
    late = [r for r in P if (r["package"], r["round"]) not in keys]
    res["late"] = (len(late), sum(r["caught"] == "caught" for r in late))
    res["author_planted"] = sum(r["planted_by"].startswith("author") for r in P)
    res["static_only"] = sum(r["caught_by_kind"] == "static pin test only" for r in P)
    gre = []
    for row, keys in SCOPE_GREEN.items():
        here = [k for k in keys if k in cases]
        gre.append((row, "; ".join("%s %s" % k for k in keys), "yes" if here else "no",
                    ", ".join(i for k in here for i in cases[k]) or "-"))
    res["recon_green"] = gre
    scope_keys = set(k for ks in SCOPE_GREEN.values() for k in ks)
    res["green_new"] = [(k, v) for k, v in cases.items() if k not in scope_keys]
    # mutation census
    if M:
        ops = list(OrderedDict((r["operator"], None) for r in M))
        verdicts = ["killed_behaviour", "killed_static_only", "survived", "killed_other"]
        res["mut"] = [(op,) + tuple(sum(r["operator"] == op and r["verdict"] == v for r in M) for v in verdicts)
                      + (sum(r["operator"] == op and r["equivalent_looking"] == "yes" for r in M),
                         sum(r["operator"] == op for r in M)) for op in ops]
        res["mut_tot"] = tuple(sum(r["verdict"] == v for r in M) for v in verdicts) + (
            sum(r["equivalent_looking"] == "yes" for r in M), len(M))
        res["mut_judged"] = sum(r["equivalent_looking"] in ("yes", "no") for r in M)
        res["mut_target"] = [(t, sum(r["target"] == t for r in M),
                              sum(r["target"] == t and r["verdict"] == "killed_behaviour" for r in M))
                             for t in OrderedDict((r["target"], None) for r in M)]
    tk = [r for r in P if r["package"] == "static-site release tooling v2"]
    res["mut_ref"] = (len(tk), sum(r["caught"] == "caught" for r in tk),
                      sum(r["caught_by_kind"] in ("behaviour test", "rehearsal", "refused by the derivation step") for r in tk),
                      sum(r["caught_by_kind"] == "static pin test only" for r in tk))
    return res

def render(res):
    n, c, m = res["total"]
    o = []
    o.append("# Summary tables: planted faults, real faults and a mechanical mutation control\n")
    o.append("Every number below is computed by `summarize.py` from `PLANTS.csv`, `FINDINGS.csv` and `MUTATION.csv` in this "
             "folder; `test_summary.py` recomputes them independently and checks this file. Package names are functional. "
             "A *plant* is a single-line fault that a non-author agent put into a copy of the delivered code before running "
             "the author agent's own test suite; *caught* means at least one test failed (or, where stated, the suite run "
             "aborted). Fault classes are defined in `TAXONOMY.md`.\n")
    o.append("## 1. Plants made, caught and missed, per package and round\n")
    o.append("Denominator: %d plants in %d review rounds of %d packages (every round whose record lists its plants one by one)."
             % (n, len(res["t1"]), len(set(t[0] for t in res["t1"]))))
    o.append("Column *missed, could change an action* counts misses whose record states that the fault, if shipped, could change "
             "what is sent or done, or how many irreversible actions happen.\n")
    o.append(md(["package", "round", "made", "caught", "missed", "caught %", "missed, could change an action"],
                res["t1"] + [("**all**", "", n, c, m, pct(c, n), res["t5"].get("yes", 0))]))
    o.append("\nHow the caught plants were caught: " + "; ".join("%s %d" % (k, v) for k, v in sorted(res["kind"].items())) + ".\n")
    o.append("## 2. Catch rate by fault class (plants)\n")
    o.append(md(["class", "name", "made", "caught", "missed", "caught %", "packages"], res["t2"]))
    o.append("\nThe plants were chosen by reviewers, not sampled, so the class sizes reflect what reviewers chose to test. "
             "Class R (resource or scale) has no plant at all: no reviewer planted a resource fault, and the resource faults in "
             "section 4 were found only by reading sizes or by a run at real size.\n")
    o.append("## 3. Before and after a revision that followed a review\n")
    o.append("A plant counts as re-planted when the next round of the same package holds a plant with the same id (the reviewer "
             "re-applied it to the revised code). *Missed then caught* is the suite getting better exactly where a review showed "
             "it weak; *caught then missed* is a regression of the suite.\n")
    o.append(md(["package", "rounds", "missed then caught", "missed then missed", "missed, not re-planted", "caught then caught",
                 "caught then missed", "regressed ids"], res["t3"]))
    mc = sum(t[2] for t in res["t3"]); mm = sum(t[3] for t in res["t3"]); cm = sum(t[6] for t in res["t3"])
    cc = sum(t[5] for t in res["t3"]); nr = sum(t[4] for t in res["t3"])
    o.append("\nTotals: %d of %d re-planted misses were caught in the next round; %d of %d re-planted catches were missed in the "
             "next round; %d earlier misses were not re-planted.\n" % (mc, mc + mm, cm, cm + cc, nr))
    o.append("New plants (ids not planted in any earlier round of the package) in the revised rounds:\n")
    o.append(md(["package", "round", "new plants", "caught", "caught %"], res["t3new"]))
    tn = sum(t[2] for t in res["t3new"]); tc = sum(t[3] for t in res["t3new"])
    o.append("\nNew plants in revised rounds: %d of %d caught (%s), against %d of %d (%s) for re-planted earlier misses.\n"
             % (tc, tn, pct(tc, tn), mc, mc + mm, pct(mc, mc + mm)))
    o.append("## 4. Real faults in delivered code\n")
    o.append("Denominator: %d faults (`FINDINGS.csv`): every blocker, major, regression or stop that a review named in delivered "
             "code, plus the reader-of-another-family items and notes that the scope memo's evidence table cites. Test gaps shown "
             "only by plants are not faults in delivered code and are not counted here." % res["f_total"])
    o.append("\nBy how the fault was found:\n")
    o.append(md(["how found", "faults", "with the author's suite fully green", "of which blocker, major, regression or stop"],
                res["f_how"] + [("**all**", res["f_total"], res["f_green"].get("yes", 0),
                                 sum(t[3] for t in res["f_how"]))]))
    o.append("\nSuite fully green at the time: " + "; ".join("%s %d" % (k, v) for k, v in sorted(res["f_green"].items())) + ".")
    o.append("Could have caused a wrong or repeated irreversible action: " +
             "; ".join("%s %d" % (k, v) for k, v in sorted(res["f_irrev"].items())) + ".")
    o.append("Severity as the review gave it: " + "; ".join("%s %d" % (k, v) for k, v in sorted(res["f_sev"].items())) + ".")
    o.append("Rounds until fixed: " + "; ".join("%s %d" % (k, v) for k, v in sorted(res["f_fixed"].items())) + ".")
    o.append("Run-doing reviewer: " + "; ".join("%s %d" % (k, v) for k, v in sorted(res["f_family"].items())) + ".\n")
    o.append("By fault class:\n")
    o.append(md(["class", "name", "faults", "with suite fully green"], res["f_class"]))
    hows, rows = res["gate_class"]
    o.append("\nGate by class (how each real fault was found):\n")
    o.append(md(["class"] + hows, rows))
    o.append("\n### Distinct cases of a fully green suite over a blocker, major, regression or stop\n")
    o.append(md(["package", "round", "findings"], [(k[0], k[1], ", ".join(v)) for k, v in res["green_cases"].items()]))
    o.append("\nCount: %d distinct package-rounds (the shared memory fault of the evaluator r4 and the selection programs r4 is one "
             "fault class met twice and is listed under both packages here; the scope memo counted it once as its row 8).\n"
             % len(res["green_cases"]))
    o.append("## 5. Missed plants that could change an action\n")
    t5 = res["t5"]
    o.append("Of %d missed plants: %d could change an action according to their record, %d could not, %d are not stated. "
             "Share: %s of all misses; %s of the misses whose record states either way.\n"
             % (m, t5.get("yes", 0), t5.get("no", 0), t5.get("not stated", 0), pct(t5.get("yes", 0), m),
                pct(t5.get("yes", 0), t5.get("yes", 0) + t5.get("no", 0))))
    o.append(md(["package", "missed, could change an action", "missed"], res["t5_by_pkg"]))
    o.append("\n## 6. Mechanical mutation control on one package\n")
    rt, rc, rb, rs = res["mut_ref"]
    if "mut" in res:
        kb, ks, sv, ko, eq, tot = res["mut_tot"]
        o.append("On a scratch copy of the static-site release tooling v2, a standard-library script made %d single-token mutants "
                 "of the publisher and its seven step scripts (fixed seed, about a quarter per operator; mutants that did not "
                 "compile were skipped: none), ran the package's own 38-test suite on each, and sorted the result. *Static only* "
                 "means the only failing tests were the two that pin the delivered bytes (the derivation reproduces the candidate "
                 "byte for byte; the publisher's edits are exactly the disclosed ones): such a mutant is caught by a byte pin, not "
                 "by any test of behaviour. When the publisher was mutated, its pinned hash was re-pinned so that only the fault "
                 "differs, as the human reviewer did.\n" % tot)
        o.append(md(["operator", "killed by a behaviour test", "killed by the byte pins only", "survived (suite green)",
                     "other failure", "equivalent-looking (hand-judged)", "mutants"],
                    res["mut"] + [("**all**", kb, ks, sv, ko, eq, tot)]))
        o.append("\nBy target file role:\n")
        o.append(md(["target", "mutants", "killed by a behaviour test"], res["mut_target"]))
        o.append("\nBeside it, the reviewer's hand-made plants on the same package: %d planted, %d caught; %d of them by a behaviour "
                 "test, a rehearsal or a refusal of the derivation step, %d by the byte pins only. Mechanical: %d of %d killed by a "
                 "behaviour test (%s), %d by the byte pins only (%s). Equivalence was judged by hand only for mutants not killed by a behaviour test: %d judged "
                 "(see `MUTATION.csv`, column `equivalent_looking`; blank = not judged).\n"
                 % (rt, rc, rb, rs, kb, tot, pct(kb, tot), ks, pct(ks, tot), res["mut_judged"]))
    else:
        o.append("MUTATION.csv is absent: the census did not run.\n")
    o.append("## 7. Reconciliation with the scope memo\n")
    o.append(md(["scope row", "package", "round", "scope made/caught/missed", "here made/caught/missed", "result"], res["recon"]))
    o.append("\nTotals: scope %d/%d/%d; here, the same rows %d/%d/%d; here, all rows %d/%d/%d (the difference is the "
             "frame-rendering kit's %d plants, %d caught, reviewed after the scope memo).\n"
             % (SCOPE_TOTAL + res["scope_sub"] + (n, c, m) + res["late"]))
    o.append("Green-suite cases, scope memo's nine file-backed rows against this table (blocker, major, regression or stop, "
             "suite fully green):\n")
    o.append(md(["scope row", "covers here", "reproduced", "findings"], res["recon_green"]))
    o.append("\nCases here that the scope memo did not count: " +
             ("; ".join("%s %s (%s)" % (k[0], k[1], ", ".join(v)) for k, v in res["green_new"]) or "none") + ".\n")
    t5 = res["t5"]
    o.append(NOTES % dict(author=res["author_planted"], n=n, static=res["static_only"], nst=t5.get("not stated", 0), m=m))
    return "\n".join(o)

NOTES = """Why the scope memo's row 20 is not reproduced: the evaluation-run wrapper's fault (F39) is a check that could not
fail. Its record shows the check passing on all four records but no test suite, so "a suite that passed in full" is
not stated for it. The frame-rendering kit (F40-F47: 85 of 85 tests green with 3 skipped, five blockers in the frames)
was reviewed after the scope memo was written.

## 8. What is NOT in the data

- **Choice of plants.** Every plant was chosen by a reviewer (%(author)d of the %(n)d, in the evaluator's round r4, were the
  author agent's own plants re-run by the reviewer; column `planted_by`). Catch rates are not mutation scores and are not
  comparable across packages or classes. Section 6 is the only mechanical sample, on one package.
- **What "caught" rests on.** %(static)d catches (all in the static-site release tooling v2) rest only on tests that pin the
  delivered bytes, not on a test of behaviour; 1 (one-job submit script r1, P55) is a suite run that aborted; 3 (inference
  release package r3) were caught only after the reviewer supplied a stand-in for a missing optional package: as
  delivered on the review machine, 0 of those 10 plants were killed.
- **Single line.** Plants are described by their records as single-line faults; at least one (evaluation-record audit
  harness r1, M7) removes a three-line raise, and one evaluator plant changes two things at once (r4, M1: the existence check and the exclusive flag).
- **The impact column** is filled only where the record says it: %(nst)d of the %(m)d misses have no stated impact. Nothing here
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
"""

if __name__ == "__main__":
    text = render(compute())
    path = os.path.join(HERE, "SUMMARY.md")
    if "--check" in sys.argv:
        sys.exit(0 if open(path, encoding="utf-8").read() == text + "\n" else 1)
    open(path, "w", encoding="utf-8").write(text + "\n")
    print("wrote", path)
