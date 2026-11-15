"""Recompute every number in preprint.md / preprint.tex from the public CSVs and the agreement output.

usage: py -3.12 -I -B verify_numbers.py [DATA_DIR] [SECOND_RATER_DIR] [AGREEMENT_DIR]

Standard library only. Prints one line per number: MATCH or MISMATCH, the name, the value the preprint states,
the value recomputed here, and the basis. Exit code 0 only when every line is MATCH.

Three bases are used and named on every line:
  csv         recomputed from PLANTS.csv, FINDINGS.csv or MUTATION.csv
  labels      recomputed from the blind second rater's LABELS_*.csv against the first rater's columns (Cohen's
              kappa recomputed here, then also compared with AGREEMENT_OUTPUT.txt)
  transcribed the figure has no per-row record in the CSVs (costs, suite sizes, the second machine); the check is
              that the preprint repeats the published SUPPLEMENT.md / PAPER.md wording exactly, at the stated line
"""
import csv
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.dirname(HERE)
DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PUB, "green-suite-data-clone-20261115")
RATER = sys.argv[2] if len(sys.argv) > 2 else os.path.join(PUB, "green-suite-second-rater-20261115")
AGREE = sys.argv[3] if len(sys.argv) > 3 else os.path.join(PUB, "green-suite-rater-agreement-20261115")

BEHAVIOUR = {"behaviour test", "behaviour test (stand-in encoder)"}
SEVERE = ("BLOCKER", "MAJOR", "regression", "stop")
CLASSES = ["B", "G", "W", "L", "O", "S", "C", "R", "E", "F"]

results = []


def check(name, stated, computed, basis):
    ok = stated == computed
    results.append(ok)
    print("%s  %s: stated %r, recomputed %r  [%s]" % ("MATCH   " if ok else "MISMATCH", name, stated, computed, basis))


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def pct(a, b):
    return "%.1f" % (100.0 * a / b)


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return po, (po - pe) / (1 - pe)


def severe(f):
    return f["severity"].split(" ")[0] in SEVERE


P = rows(os.path.join(DATA, "PLANTS.csv"))
F = rows(os.path.join(DATA, "FINDINGS.csv"))
M = rows(os.path.join(DATA, "MUTATION.csv"))
LP = rows(os.path.join(RATER, "LABELS_PLANTS.csv"))
LF = rows(os.path.join(RATER, "LABELS_FINDINGS.csv"))
SUPP = lines(os.path.join(DATA, "SUPPLEMENT.md"))
PAPER = lines(os.path.join(DATA, "PAPER.md"))
AOUT = lines(os.path.join(AGREE, "AGREEMENT_OUTPUT.txt"))


def fid(x):
    return next(f for f in F if f["finding_id"] == x)

# ---------------------------------------------------------------- plants: totals
caught = [p for p in P if p["caught"] == "caught"]
missed = [p for p in P if p["caught"] == "missed"]
rounds = []
for p in P:
    k = (p["package"], p["round"])
    if k not in rounds:
        rounds.append(k)
check("plants", 453, len(P), "csv")
check("review rounds", 15, len(rounds), "csv")
check("packages", 8, len({p["package"] for p in P}), "csv")
check("caught", 346, len(caught), "csv")
check("missed", 107, len(missed), "csv")
check("caught share of chosen plants (percent)", "76.4", pct(len(caught), len(P)), "csv")
kinds = Counter(p["caught_by_kind"] for p in caught)
check("caught by behaviour test", 323, kinds["behaviour test"], "csv")
check("caught by behaviour test with stand-in encoder", 3, kinds["behaviour test (stand-in encoder)"], "csv")
beh = sum(1 for p in caught if p["caught_by_kind"] in BEHAVIOUR)
check("caught by a test of behaviour (both kinds)", 326, beh, "csv")
check("behaviour share of chosen plants (percent)", "72.0", pct(beh, len(P)), "csv")
check("caught only by a static pin test", 12, kinds["static pin test only"], "csv")
check("caught at rehearsal", 5, kinds["rehearsal"], "csv")
check("refused by the derivation step", 2, kinds["refused by the derivation step"], "csv")
check("caught by a suite abort", 1, kinds["suite abort"], "csv")
check("rehearsal + refusal + abort", 8, kinds["rehearsal"] + kinds["refused by the derivation step"] + kinds["suite abort"], "csv")
check("static-only catches all in one package", {"static-site release tooling v2"},
      {p["package"] for p in caught if p["caught_by_kind"] == "static pin test only"}, "csv")
check("suite-abort catch", [("one-job submit script", "r1", "P55")],
      [(p["package"], p["round"], p["plant_id"]) for p in caught if p["caught_by_kind"] == "suite abort"], "csv")
origin = Counter(p["planted_by"] for p in P)
check("reviewer-origin plants", 440, origin["reviewer"], "csv")
check("author-origin plants re-run by the reviewer", 13, origin["author (re-run by the reviewer)"], "csv")
author = [p for p in P if p["planted_by"] != "reviewer"]
check("author-origin plants: package and round", {("once-only sealed evaluator", "r4")}, {(p["package"], p["round"]) for p in author}, "csv")
check("author-origin plants caught", 13, sum(p["caught"] == "caught" for p in author), "csv")
impact = Counter(p["miss_could_change_action"] for p in missed)
check("misses that could change an action", 12, impact["yes"], "csv")
check("misses that could not", 31, impact["no"], "csv")
check("misses with no stated impact", 64, impact["not stated"], "csv")
conflict = [i + 2 for i, p in enumerate(P) if p["caught"] == "caught" and "survivor" in p["miss_effect_note"]]
check("PLANTS rows with a catch and a survivor note", 8, len(conflict), "csv")
check("those rows are in the audit harness r1", {("evaluation-record audit harness", "r1")},
      {(P[i - 2]["package"], P[i - 2]["round"]) for i in conflict}, "csv")
noframe = [p for p in P if p["package"] != "frame-rendering kit"]
check("plants without the frame-rendering kit", 433, len(noframe), "csv")
check("caught without the frame-rendering kit", 335, sum(p["caught"] == "caught" for p in noframe), "csv")
check("frame-rendering kit plants / caught", (20, 11),
      (sum(p["package"] == "frame-rendering kit" for p in P), sum(p["package"] == "frame-rendering kit" and p["caught"] == "caught" for p in P)), "csv")
inf3 = [p for p in P if p["package"] == "inference release package" and p["round"] == "r3"]
check("inference release package r3: plants, killed as delivered, caught with a stand-in", (10, 0, 3),
      (len(inf3), sum("killed as delivered on the review machine: no" not in p["miss_effect_note"] and p["caught"] == "caught" for p in inf3),
       sum(p["caught_by_kind"] == "behaviour test (stand-in encoder)" for p in inf3)), "csv")

# ---------------------------------------------------------------- plants: per round (Table 1)
TABLE1 = [
    ("one-job submit script", "r1", 60, 48, 47, 12, "80.0", 4),
    ("one-job submit script", "r2", 44, 33, 33, 11, "75.0", 3),
    ("one-job submit script", "r3", 30, 23, 23, 7, "76.7", 0),
    ("once-only sealed evaluator", "r1", 30, 20, 20, 10, "66.7", 0),
    ("once-only sealed evaluator", "r2", 50, 35, 35, 15, "70.0", 0),
    ("once-only sealed evaluator", "r3", 68, 59, 59, 9, "86.8", 0),
    ("once-only sealed evaluator", "r4", 35, 28, 28, 7, "80.0", 2),
    ("GPU training kernel", "r1", 20, 11, 11, 9, "55.0", 3),
    ("static-site release tooling v2", "r1", 32, 29, 10, 3, "90.6", 0),
    ("inference release package", "r3", 10, 3, 3, 7, "30.0", 0),
    ("inference release package", "r4", 21, 20, 20, 1, "95.2", 0),
    ("evaluation-record audit harness", "r1", 12, 8, 8, 4, "66.7", 0),
    ("evaluation-record audit harness", "r2", 16, 14, 14, 2, "87.5", 0),
    ("browser puzzle game", "r1", 5, 4, 4, 1, "80.0", 0),
    ("frame-rendering kit", "r1", 20, 11, 11, 9, "55.0", 0),
]
shares = []
for pkg, rnd, made, c, b, m, share, act in TABLE1:
    rs = [p for p in P if (p["package"], p["round"]) == (pkg, rnd)]
    got = (len(rs), sum(p["caught"] == "caught" for p in rs), sum(p["caught_by_kind"] in BEHAVIOUR for p in rs),
           sum(p["caught"] == "missed" for p in rs), pct(sum(p["caught"] == "caught" for p in rs), len(rs)),
           sum(p["miss_could_change_action"] == "yes" for p in rs))
    shares.append(float(got[4]))
    check("Table 1 row %s %s (made, caught, by behaviour, missed, share, misses that could change an action)" % (pkg, rnd),
          (made, c, b, m, share, act), got, "csv")
check("per-round caught share, lowest and highest", ("30.0", "95.2"), ("%.1f" % min(shares), "%.1f" % max(shares)), "csv")
check("rounds that caught every plant", 0, sum(s == 100.0 for s in shares), "csv")

# ---------------------------------------------------------------- plants: revision (Section 3.2)
by_round = {}
for p in P:
    by_round.setdefault(p["package"], {}).setdefault(p["round"], []).append(p)
re_miss_caught = re_miss_missed = miss_not_replanted = re_catch_caught = re_catch_missed = 0
new_made = new_caught = 0
revised_rounds = 0
not_replanted_by_pkg = Counter()
for pkg, rmap in by_round.items():
    order = sorted(rmap, key=lambda r: int(r[1:]))
    seen = set()
    for i, r in enumerate(order):
        ids = {p["plant_id"]: p for p in rmap[r]}
        if i > 0:
            revised_rounds += 1
            prev = {p["plant_id"]: p for p in rmap[order[i - 1]]}
            for pid, pp in prev.items():
                if pid in ids:
                    now = ids[pid]["caught"] == "caught"
                    if pp["caught"] == "missed":
                        re_miss_caught += now
                        re_miss_missed += not now
                    else:
                        re_catch_caught += now
                        re_catch_missed += not now
                elif pp["caught"] == "missed":
                    miss_not_replanted += 1
                    not_replanted_by_pkg[pkg] += 1
            for pid, p in ids.items():
                if pid not in seen:
                    new_made += 1
                    new_caught += p["caught"] == "caught"
        seen |= set(ids)
check("earlier misses before a revision", 68, re_miss_caught + re_miss_missed + miss_not_replanted, "csv")
check("re-planted misses caught in the next round", (55, 55), (re_miss_caught, re_miss_caught + re_miss_missed), "csv")
check("earlier misses not re-planted", 13, miss_not_replanted, "csv")
check("not re-planted: one-job r2 to r3, evaluator r3 to r4", (11, 2),
      (not_replanted_by_pkg["one-job submit script"], not_replanted_by_pkg["once-only sealed evaluator"]), "csv")
check("re-planted catches: caught again / all", (61, 66), (re_catch_caught, re_catch_caught + re_catch_missed), "csv")
check("re-planted catches that became misses", 5, re_catch_missed, "csv")
check("revised rounds", 7, revised_rounds, "csv")
check("new plants in revised rounds: caught / all", (96, 143), (new_caught, new_made), "csv")
check("new plants caught (percent)", "67.1", pct(new_caught, new_made), "csv")

# ---------------------------------------------------------------- classes (Table 2) and second rater
assert len(LP) == len(P) and len(LF) == len(F)
for x, y in zip(P, LP):
    assert x["plant_id"] == y["plant_id"]
for x, y in zip(F, LF):
    assert x["finding_id"] == y["finding_id"]
a_p = [p["fault_class"] for p in P]
b_p = [l["class"] for l in LP]
a_f = [f["fault_class"] for f in F]
b_f = [l["class"] for l in LF]
TABLE2 = {  # class: plants, caught, share, second rater agrees, real faults, of which green
    "B": (26, 24, "92.3", 22, 1, 1), "G": (147, 109, "74.1", 129, 7, 6), "W": (76, 62, "81.6", 65, 2, 2),
    "L": (86, 58, "67.4", 62, 4, 4), "O": (20, 17, "85.0", 20, 5, 5), "S": (55, 43, "78.2", 42, 9, 9),
    "C": (9, 7, "77.8", 9, 0, 0), "R": (0, 0, "n/a", 0, 3, 3), "E": (14, 9, "64.3", 6, 6, 4), "F": (20, 17, "85.0", 13, 10, 10),
}
for c in CLASSES:
    ps = [p for p in P if p["fault_class"] == c]
    fs = [f for f in F if f["fault_class"] == c]
    cc = sum(p["caught"] == "caught" for p in ps)
    got = (len(ps), cc, pct(cc, len(ps)) if ps else "n/a", sum(1 for x, y in zip(a_p, b_p) if x == c and y == c),
           len(fs), sum(f["suite_fully_green"] == "yes" for f in fs))
    check("Table 2 row %s (plants, caught, share, second rater agrees, real faults, green)" % c, TABLE2[c], got, "csv+labels")
check("Table 2 total second-rater agreement on plants", 368, sum(x == y for x, y in zip(a_p, b_p)), "labels")
check("resource-or-scale real faults: how found", {"reading the source": 2, "real-size run": 1},
      dict(Counter(f["how_found"] for f in F if f["fault_class"] == "R")), "csv")
check("second rater: resource class plants / real faults", (0, 3), (b_p.count("R"), b_f.count("R")), "labels")
check("second rater agrees on all 3 resource real faults", 3, sum(1 for x, y in zip(a_f, b_f) if x == "R" and y == "R"), "labels")
po_p, k_p = kappa(a_p, b_p)
po_f, k_f = kappa(a_f, b_f)
po_a, k_a = kappa(a_p + a_f, b_p + b_f)
check("agreement, plants: n, same class, raw, kappa", (453, 368, "0.812", "0.768"),
      (len(a_p), sum(x == y for x, y in zip(a_p, b_p)), "%.3f" % po_p, "%.3f" % k_p), "labels")
check("agreement, real faults: n, same class, raw, kappa", (47, 40, "0.851", "0.826"),
      (len(a_f), sum(x == y for x, y in zip(a_f, b_f)), "%.3f" % po_f, "%.3f" % k_f), "labels")
check("agreement, all: n, same class, raw, kappa", (500, 408, "0.816", "0.776"),
      (len(a_p) + len(a_f), sum(x == y for x, y in zip(a_p + a_f, b_p + b_f)), "%.3f" % po_a, "%.3f" % k_a), "labels")
check("AGREEMENT_OUTPUT.txt plants line", "plants: n=453 agree=368 raw=0.812 kappa=0.768", AOUT[0], "agreement output")
check("AGREEMENT_OUTPUT.txt findings line", "findings: n=47 agree=40 raw=0.851 kappa=0.826", AOUT[14], "agreement output")
check("AGREEMENT_OUTPUT.txt all line", "all: n=500 raw=0.816 kappa=0.776", AOUT[28], "agreement output")
conf = Counter((x, y) for x, y in zip(a_p, b_p) if x != y)
check("plant disagreements", 85, sum(conf.values()), "labels")
check("largest confusion: logic read as wrong value", 19, conf[("L", "W")], "labels")
check("state read as weakened check, and the reverse", (7, 6), (conf[("S", "G")], conf[("G", "S")]), "labels")
conf_by = Counter(l["confidence"] for x, l in zip(a_p, LP) if x != l["class"])
check("plant disagreements at the second rater's medium or low confidence / high", (68, 17),
      (conf_by["medium"] + conf_by["low"], conf_by["high"]), "labels")
check("second rater confidence on plants: high, medium, low", (321, 116, 16),
      tuple(Counter(l["confidence"] for l in LP)[k] for k in ("high", "medium", "low")), "labels")
check("second rater confidence on real faults: high, medium", (37, 10),
      tuple(Counter(l["confidence"] for l in LF)[k] for k in ("high", "medium")), "labels")
check("per-class plant agreement: C, O full", (9, 20), (sum(1 for x, y in zip(a_p, b_p) if x == "C" and y == "C"),
                                                      sum(1 for x, y in zip(a_p, b_p) if x == "O" and y == "O")), "labels")
check("per-class plant agreement shares E, F, L", ("0.43", "0.65", "0.72"), ("%.2f" % (6 / 14), "%.2f" % (13 / 20), "%.2f" % (62 / 86)), "labels")
fconf = Counter((x, y) for x, y in zip(a_f, b_f) if x != y)
check("real-fault disagreements", 7, sum(fconf.values()), "labels")

# ---------------------------------------------------------------- real faults (Section 3.5, Table 3)
check("real faults", 47, len(F), "csv")
green = Counter(f["suite_fully_green"] for f in F)
check("real faults under a suite with no recorded failure", 44, green["yes"], "csv")
check("real faults with a failing suite / suite not stated", (2, 1), (green["no"], green["not stated"]), "csv")
check("the two with a failing suite are the inference package on the review machine", {"inference release package"},
      {f["package"] for f in F if f["suite_fully_green"] == "no"}, "csv")
how = Counter(f["how_found"] for f in F)
check("found by running the code", 28, how["running the code"], "csv")
check("found by reading the source", 12, how["reading the source"], "csv")
check("first raised by a text-only reader of another family", 6, how["other-family text reader, then run"] + how["other-family text reader, then reading"], "csv")
check("reader items settled by a run / by reading", (5, 1), (how["other-family text reader, then run"], how["other-family text reader, then reading"]), "csv")
check("found by a run at real size", 1, how["real-size run"], "csv")
TABLE3 = {"running the code": (28, 26), "reading the source": (12, 11), "other-family text reader, then reading": (1, 1),
          "other-family text reader, then run": (5, 5), "real-size run": (1, 1)}
for k, v in TABLE3.items():
    check("Table 3 row %s (faults, under green suite)" % k, v, (how[k], sum(f["how_found"] == k and f["suite_fully_green"] == "yes" for f in F)), "csv")
check("blocker, major, regression or stop", 39, sum(severe(f) for f in F), "csv")
check("of those, under a suite with no recorded failure", 37, sum(severe(f) and f["suite_fully_green"] == "yes" for f in F), "csv")
sev = Counter(f["severity"] for f in F)
check("blockers / majors / regressions / stops", (9, 27, 1, 2),
      (sev["BLOCKER"], sev["MAJOR"], sum(v for k, v in sev.items() if k.startswith("regression")), sum(v for k, v in sev.items() if k.startswith("stop"))), "csv")
check("severity breakdown sums to the severe count", 39, sev["BLOCKER"] + sev["MAJOR"] + 1 + 2, "csv")
check("F23 package name", "post-processing selection programs", fid("F23")["package"], "csv")
check("F23 text: six runs of maps loaded before scoring", True, "six runs of maps (about 3.3 GiB) loaded before scoring" in fid("F23")["fault"], "csv")
check("selection programs are not a planted package", False, "post-processing selection programs" in {p["package"] for p in P}, "csv")
pr = {(f["package"], f["round"]) for f in F if severe(f) and f["suite_fully_green"] == "yes"}
check("distinct package-rounds with a severe fault under a green suite", 10, len(pr), "csv")
fam = Counter(f["run_doing_reviewer_family"] for f in F)
check("run-doing reviewer of the author's family / another family", (44, 3), (fam["same family as author (separate context)"], fam["other family"]), "csv")
check("the three other-family faults", ["F30", "F31", "F32"], [f["finding_id"] for f in F if f["run_doing_reviewer_family"] == "other family"], "csv")
irr = Counter(f["could_cause_wrong_or_repeated_irreversible_action"] for f in F)
check("could cause a wrong or repeated irreversible action: yes / no / not stated", (12, 9, 26), (irr["yes"], irr["no"], irr["not stated"]), "csv")
frame = [f for f in F if f["package"] == "frame-rendering kit"]
check("frame-rendering kit faults", 8, len(frame), "csv")
check("frame kit: found by running (rendered frames) / reading", (7, 1),
      (sum(f["how_found"] == "running the code" for f in frame), sum(f["how_found"] == "reading the source" for f in frame)), "csv")
check("frame kit blockers", 5, sum(f["severity"] == "BLOCKER" for f in frame), "csv")
check("frame kit suite result", {"85/85 (3 skipped)"}, {f["suite_result"] for f in frame}, "csv")
reader_also = [f["finding_id"] for f in F if "reader of another family" in f["how_found_note"] and not f["how_found"].startswith("other-family")]
check("faults a reader also raised independently of a run", 4, len(reader_also), "csv")
reader_first = [f for f in F if f["how_found"].startswith("other-family")]
check("reader-first: one major, five lower-severity", (1, 5), (sum(f["severity"] == "MAJOR" for f in reader_first), sum(f["severity"] != "MAJOR" for f in reader_first)), "csv")
check("reader-first faults in the resource class", 0, sum(f["fault_class"] == "R" for f in reader_first), "csv")
r2 = [f for f in F if f["package"] == "one-job submit script" and f["round"] == "r2"]
check("one-job r2: reader-first items, none severe; run-found severe items", (3, 0, 2),
      (sum(f["how_found"].startswith("other-family") for f in r2), sum(f["how_found"].startswith("other-family") and severe(f) for f in r2),
       sum(f["how_found"] == "running the code" and severe(f) for f in r2)), "csv")

check("F22 suite result", "63/63", fid("F22")["suite_result"], "csv")
check("F22 text: about 2.5 GiB under a 2 GiB guard", True, "about 2.5 GiB of maps under a 2 GiB peak-memory guard" in fid("F22")["fault"], "csv")
check("F22 fix: rehearsal at size peak 0.671 GiB", True, "peak 0.671 GiB" in fid("F22")["fixed_note"], "csv")
check("F23 text: about 3.3 GiB", True, "about 3.3 GiB" in fid("F23")["fault"], "csv")
check("F23 fix: size tests 0.460 and 0.971 GiB", True, "0.460 and 0.971 GiB" in fid("F23")["fixed_note"], "csv")
check("F27 suite result 17/17", "17/17", fid("F27")["suite_result"], "csv")
check("F27 note: memory reading forced to 4.6 GiB", True, "forced to 4.6 GiB" in fid("F27")["how_found_note"], "csv")
check("F12/F13 suite result 15/15", {"15/15"}, {fid("F12")["suite_result"], fid("F13")["suite_result"]}, "csv")
check("F03 suite result 67/67", "67/67", fid("F03")["suite_result"], "csv")
check("F07/F08 suite result 103/103", {"103/103"}, {fid("F07")["suite_result"], fid("F08")["suite_result"]}, "csv")
check("F35 suite result 38/38", "38/38", fid("F35")["suite_result"], "csv")
check("F30-F32 suite result 27/27", {"27/27"}, {fid(x)["suite_result"] for x in ("F30", "F31", "F32")}, "csv")
check("F24 is the one attack of 17 that succeeded", True, "the one attack of 17 that succeeded" in fid("F24")["how_found_note"], "csv")

# ---------------------------------------------------------------- mechanical mutation (Section 3.4, Table 4)
check("mutants", 150, len(M), "csv")
verd = Counter(m["verdict"] for m in M)
check("killed by a behaviour test / only by the byte pins / survived", (82, 68, 0), (verd["killed_behaviour"], verd["killed_static_only"], 150 - verd["killed_behaviour"] - verd["killed_static_only"]), "csv")
check("behaviour-killed share (percent)", "54.7", pct(verd["killed_behaviour"], len(M)), "csv")
check("byte-pin-only share (percent)", "45.3", pct(verd["killed_static_only"], len(M)), "csv")
check("equivalent-looking (hand-judged) / judged", (3, 67), (sum(m["equivalent_looking"] == "yes" for m in M), sum(m["equivalent_looking"] != "" for m in M)), "csv")
static_only = [m for m in M if m["verdict"] == "killed_static_only"]
check("of the 68 byte-pin-only mutants, 67 judged by hand, 3 equivalent-looking", (68, 67, 3),
      (len(static_only), sum(m["equivalent_looking"] != "" for m in static_only), sum(m["equivalent_looking"] == "yes" for m in static_only)), "csv")
check("behaviour-killed mutants judged by hand", 0, sum(m["equivalent_looking"] != "" for m in M if m["verdict"] == "killed_behaviour"), "csv")
TABLE4 = {"CMP": (37, 24, 13), "CONST": (37, 15, 22), "DEL": (39, 17, 22), "SWAP": (37, 26, 11)}
for op, v in TABLE4.items():
    ms = [m for m in M if m["operator"] == op]
    check("Table 4 row %s (mutants, behaviour, byte pins only)" % op, v, (len(ms), sum(m["verdict"] == "killed_behaviour" for m in ms), sum(m["verdict"] == "killed_static_only" for m in ms)), "csv")
steps = [m for m in M if m["target"] in ("install step", "rollback step", "read-only snapshot step")]
check("three step scripts: mutants / killed by behaviour", (37, 1), (len(steps), sum(m["verdict"] == "killed_behaviour" for m in steps)), "csv")
check("mutation target roles", 8, len({m["target"] for m in M}), "csv")
hand = [p for p in P if p["package"] == "static-site release tooling v2"]
hk = Counter(p["caught_by_kind"] for p in hand)
check("hand plants on the same package: planted, caught, behaviour, rehearsal, refusal, byte pins only, missed",
      (32, 29, 10, 5, 2, 12, 3), (len(hand), sum(p["caught"] == "caught" for p in hand), hk["behaviour test"], hk["rehearsal"],
                                  hk["refused by the derivation step"], hk["static pin test only"], hk["none"]), "csv")

# ---------------------------------------------------------------- transcribed figures (no per-row record in the CSVs)
def transcribed(name, text, src, lineno):
    line = src[lineno - 1]
    check(name, True, text in line, "transcribed from %s line %d" % ("SUPPLEMENT.md" if src is SUPP else "PAPER.md", lineno))


transcribed("one-job script author tests by round 67, 103, 140", "| 3 | 67, 103, 140 |", SUPP, 12)
transcribed("G2 one-job reviewer minutes", "about 26, 26 and 20 minutes of reviewer time", SUPP, 95)
transcribed("G2 publisher minutes", "about 25 minutes; 32 plants", SUPP, 96)
transcribed("G3 paid reads USD 0.43 and about 0.14", "USD 0.43 (a read cut off at its length limit); another about USD 0.14", SUPP, 97)
transcribed("G4 selection programs 495 s and 859 s", "495 s and 859 s", SUPP, 98)
transcribed("G4 evaluator rehearsal six runs 731.5 to 1,008.9 s", "six runs of 731.5 to 1,008.9 s", SUPP, 99)
transcribed("second machine: 11 items covering 10 versions", "The list has 11 items; two concern the chain's first candidate", SUPP, 44)
transcribed("second machine money-cap harness 148 of 148; 2 blockers, 3 majors; 5.40 against 1.00", "| 148 of 148 † | 2 blockers, 3 majors by probes: a discarded reply re-sent with no cap check, 5.40 dollars counted against a 1.00 cap |", SUPP, 30)
transcribed("second machine author plants 20 of 20, 67 of 67 and 4 of 4, 66 of 66; survivors 7, 11, 4", "the money-cap harness 20 of 20, the chain's two candidates 67 of 67 and 4 of 4, the results-page program 66 of 66), every one was killed, while non-author plants on the harness, the chain and the results-page program survived (7, 11 and 4", SUPP, 131)
transcribed("preregistered reader test: two of fifteen calls made", "Two of its fifteen planned calls were made and charged, and neither returned any answer text", SUPP, 139)
transcribed("preregistered reader test: thirteen never made", "thirteen calls were never made", SUPP, 140)
transcribed("six text-only reads", "In six text-only reads on the first machine", SUPP, 127)
transcribed("records of 9 to 11 November 2026", "records of 9 to 11 November 2026", PAPER, 3)
transcribed("first-machine rounds dated 10 or 11 November 2026", "every review round dated 10 or 11 November 2026", PAPER, 31)
transcribed("second machine: 20 rows over 11 cases, running nothing", "its lead agent compiled 20 rows over 11 cases from existing files, running nothing", PAPER, 31)
transcribed("version 1 submitted 12 November 2026", "on 12 November 2026", PAPER, 5)

n = len(results)
print()
print("%d numbers checked: %d MATCH, %d MISMATCH" % (n, sum(results), n - sum(results)))
sys.exit(0 if all(results) else 1)
