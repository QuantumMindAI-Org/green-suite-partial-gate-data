"""Agreement between the first rater (the published fault_class columns) and a blind second rater.

usage: py -3.12 -I -B agreement.py <PLANTS.csv> <FINDINGS.csv> <LABELS_PLANTS.csv> <LABELS_FINDINGS.csv>
Rows are matched by position (plant ids repeat across packages); the id column of each pair must agree row by row.
Prints counts, raw agreement, Cohen's kappa, per-class agreement and the confusion pairs. Standard library only.
"""
import csv
import sys
from collections import Counter


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


def report(name, first, second, idkey_first, idkey_second):
    assert len(first) == len(second), (name, len(first), len(second))
    for i, (x, y) in enumerate(zip(first, second)):
        assert x[idkey_first] == y[idkey_second], (name, i, x[idkey_first], y[idkey_second])
    a = [x["fault_class"].strip() for x in first]
    b = [y["class"].strip() for y in second]
    po, k = kappa(a, b)
    print("%s: n=%d agree=%d raw=%.3f kappa=%.3f" % (name, len(a), sum(x == y for x, y in zip(a, b)), po, k))
    print("  first rater classes:", dict(sorted(Counter(a).items())))
    print("  second rater classes:", dict(sorted(Counter(b).items())))
    for c in sorted(set(a) | set(b)):
        idx = [i for i, x in enumerate(a) if x == c]
        if idx:
            print("  class %s: first-rater n=%d, second agrees on %d (%.2f)" % (
                c, len(idx), sum(b[i] == c for i in idx), sum(b[i] == c for i in idx) / len(idx)))
    conf = Counter((x, y) for x, y in zip(a, b) if x != y)
    print("  disagreements (first -> second):", ", ".join("%s->%s %d" % (p[0], p[1], n) for p, n in conf.most_common()))
    conf_hi = [(x, y, s.get("confidence", "")) for x, y, s in zip(a, b, second) if x != y]
    print("  disagreements by second-rater confidence:", dict(Counter(c for _, _, c in conf_hi)))
    return a, b


def main(argv):
    pa, pb = report("plants", rows(argv[1]), rows(argv[3]), "plant_id", "plant_id")
    fa, fb = report("findings", rows(argv[2]), rows(argv[4]), "finding_id", "finding_id")
    po, k = kappa(pa + fa, pb + fb)
    print("all: n=%d raw=%.3f kappa=%.3f" % (len(pa) + len(fa), po, k))
    r_first = sum(1 for x in fa if x == "R"), sum(1 for x in pa if x == "R")
    r_second = sum(1 for x in fb if x == "R"), sum(1 for x in pb if x == "R")
    print("resource-or-scale (R): first rater findings %d, plants %d; second rater findings %d, plants %d" % (r_first + r_second))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
