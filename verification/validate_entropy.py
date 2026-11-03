#!/usr/bin/env python3
"""Finite numerical diagnostics for the entropy-contraction manuscript.

What this script does
---------------------
It evaluates the claimed inequalities on many concrete inputs: complete
bipartite chains (using full transition matrices, not the proof's
decomposition), the uniform and weighted mean inequalities, the uniform and
weighted reverse-erasure channels below the threshold, the binary equality
families, and four explicit high-precision witnesses above the threshold.

What it does not do
-------------------
It does not prove anything. Random samples rarely land near extremisers; see
negative_controls.py for checks that show these tests can detect false claims.

Hygiene
-------
* No ``assert`` statements: every gate is an explicit comparison whose outcome
  is recorded, so ``python -O`` cannot silently disable a check.
* The status string is computed from the recorded gates; any failure makes the
  script exit with status 1.
* Output goes to ``--output-dir``; an existing output file is never
  overwritten.
* The JSON records this file's own SHA-256.

Usage::

    python3 -I -B validate_entropy.py --output-dir NEW_DIRECTORY
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import numpy as np
import scipy
from scipy.special import xlogy

SEED = 20261101
RESIDUAL_GATE = 2e-12
IDENTITY_GATE = 2e-14
STATIONARITY_GATE = 1e-15
OUTPUT_NAME = "validation_results.json"


class Gates:
    """Collects every pass/fail decision explicitly."""

    def __init__(self) -> None:
        self.total = 0
        self.failures: list[dict] = []

    def check(self, name: str, ok: bool, **detail) -> bool:
        self.total += 1
        ok = bool(ok)
        if not ok:
            self.failures.append({"gate": name, **detail})
        return ok


def divergence(p, q):
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    return np.sum(xlogy(p, p / q), axis=-1)


def graph(m, n):
    pi = np.r_[np.full(m, 1 / (2 * m)), np.full(n, 1 / (2 * n))]
    P = np.eye(m + n) / 2
    P[:m, m:] = 1 / (2 * n)
    P[m:, :m] = 1 / (2 * m)
    return pi, P


def coefficient(m, n):
    M = max(m, n)
    return math.log(M) / (2 * math.log(2 * M))


def exact_markov_checks(gates):
    records = []
    for m, n in [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]:
        N = m + n
        pi = [Fraction(1, 2 * m)] * m + [Fraction(1, 2 * n)] * n
        P = [[Fraction(int(i == j), 2) for j in range(N)] for i in range(N)]
        for i in range(m):
            for j in range(m, N):
                P[i][j] = Fraction(1, 2 * n)
                P[j][i] = Fraction(1, 2 * m)
        rows = all(sum(row) == 1 for row in P)
        stat = all(sum(pi[i] * P[i][j] for i in range(N)) == pi[j] for j in range(N))
        db = all(pi[i] * P[i][j] == pi[j] * P[j][i] for i in range(N) for j in range(N))
        gates.check("exact_rows_sum_to_one", rows, m=m, n=n)
        gates.check("exact_stationarity", stat, m=m, n=n)
        gates.check("exact_detailed_balance", db, m=m, n=n)
        records.append({"m": m, "n": n, "rows_sum_to_one": rows,
                        "stationarity": stat, "detailed_balance": db,
                        "pi": list(map(str, pi)), "P": [list(map(str, row)) for row in P]})
    return records


def graph_checks(gates, rng):
    records = []
    for m, n in [(1, 1), (1, 2), (2, 2), (1, 3), (2, 3), (3, 3),
                 (3, 4), (2, 10), (7, 11), (10, 10), (3, 100)]:
        pi, P = graph(m, n)
        eta = coefficient(m, n)
        distributions = [np.eye(m + n)]
        for concentration in [.03, .2, 1., 8.]:
            distributions.append(rng.dirichlet(np.full(m + n, concentration), size=2000))
        for eps in [1e-3, 1e-6, 1e-9]:
            distributions.append((1 - eps) * np.eye(m + n) + eps * pi)
        data = np.concatenate(distributions)
        d = divergence(data, pi)
        d_out = divergence(data @ P, pi)
        residual = d_out - eta * d
        ratios = d_out[d > 1e-12] / d[d > 1e-12]
        excess = float(np.max(residual))
        ok = gates.check("bipartite_residual", excess < RESIDUAL_GATE, m=m, n=n, excess=excess)
        records.append({"m": m, "n": n, "samples": int(len(data)),
                        "theorem_coefficient": eta,
                        "largest_observed_ratio": float(max(ratios)),
                        "largest_inequality_residual": excess,
                        "gate": RESIDUAL_GATE, "passed": ok})
    return records


def binary_equality_checks(gates):
    max_error = 0.0
    count = 0
    for s in np.linspace(0, 1, 101):
        for m, n in [(2, 2), (2, 1)]:
            pi, P = graph(m, n)
            v = np.r_[s * s, (1 - s) ** 2, np.full(n, 2 * s * (1 - s) / n)]
            error = abs(float(divergence(v @ P, pi) - divergence(v, pi) / 4))
            max_error = max(max_error, error)
            count += 1
    ok = gates.check("binary_equality_identity", max_error < IDENTITY_GATE, max_error=max_error)
    return {"samples": count, "max_absolute_identity_error": max_error,
            "gate": IDENTITY_GATE, "passed": ok}


def mean_checks(gates, rng):
    records = []
    for n in [2, 3, 4, 5, 10, 32]:
        p0 = n / (n - 1)
        for p in sorted(set([p0, 1 + math.log(2) / math.log(n), 2., 3., 6.])):
            if p < p0 - 1e-14:
                continue
            data = np.concatenate([rng.dirichlet(np.full(n, a), size=1500)
                                   for a in [.05, .5, 5.]])
            positive = np.all(data > 0, axis=1)
            geom = np.zeros(len(data))
            geom[positive] = np.exp(np.mean(np.log(data[positive]), axis=1))
            lhs = np.sum(data ** p, axis=1) + (n ** p - n) * geom ** p
            excess = float(np.max(lhs - 1))
            ok = gates.check("uniform_mean_residual", excess < RESIDUAL_GATE, n=n, p=p, excess=excess)
            records.append({"n": n, "p": p, "samples": int(len(data)),
                            "largest_normalised_residual": excess,
                            "gate": RESIDUAL_GATE, "passed": ok})
    return records


def reverse_erasure_checks(gates, rng):
    records = []
    for n in [2, 3, 4, 10, 32]:
        critical = n ** (-1 / (n - 1))
        for alpha in sorted(set([.02, 1 / n, .5, critical])):
            if alpha > critical + 1e-14:
                continue
            mu = np.r_[np.full(n, alpha / n), 1 - alpha]
            c = math.log(n) / math.log(n / alpha)
            data = np.concatenate([np.eye(n + 1)] +
                                  [rng.dirichlet(np.full(n + 1, a), size=2000)
                                   for a in [.03, .3, 3.]])
            output = data[:, :n] + data[:, n, None] / n
            d = divergence(data, mu)
            o = divergence(output, np.full(n, 1 / n))
            residual = float(np.max(o - c * d))
            ok = gates.check("uniform_reverse_erasure_residual", residual < RESIDUAL_GATE,
                             n=n, alpha=alpha, excess=residual)
            records.append({"n": n, "alpha": alpha, "alpha_critical": critical,
                            "coefficient": c, "samples": int(len(data)),
                            "largest_inequality_residual": residual,
                            "gate": RESIDUAL_GATE, "passed": ok})
    return records


def weighted_checks(gates, rng):
    priors = [[.1, .2, .7], [.49, .51], [.2, .3, .5], [.05, .05, .2, .7]]
    reverse, bipartite = [], []
    for weights in priors:
        mu = np.array(weights)
        q = min(weights)
        critical = q ** (q / (1 - q))
        for alpha in sorted(set([.03, q, .5, critical])):
            reference = np.r_[alpha * mu, 1 - alpha]
            c = math.log(1 / q) / math.log(1 / (alpha * q))
            data = np.concatenate([np.eye(len(mu) + 1)] +
                                  [rng.dirichlet(np.full(len(mu) + 1, a), size=1000)
                                   for a in [.03, .3, 3.]])
            output = data[:, :-1] + data[:, -1, None] * mu
            residual = float(np.max(divergence(output, mu) - c * divergence(data, reference)))
            ok = gates.check("weighted_reverse_erasure_residual", residual < RESIDUAL_GATE,
                             mu=weights, alpha=alpha, excess=residual)
            reverse.append({"mu": weights, "alpha": alpha, "alpha_critical": critical,
                            "coefficient": c, "samples": int(len(data)),
                            "largest_inequality_residual": residual,
                            "gate": RESIDUAL_GATE, "passed": ok})
    for left, right in [(priors[0], priors[1]), (priors[2], priors[3]),
                        ([1.], priors[0]), ([.5, .5], priors[1])]:
        u, v = np.array(left), np.array(right)
        m, n = len(u), len(v)
        pi = np.r_[u / 2, v / 2]
        P = np.eye(m + n) / 2
        P[:m, m:] = v / 2
        P[m:, :m] = u / 2
        stationarity = float(np.max(abs(pi @ P - pi)))
        gates.check("weighted_stationarity", stationarity < STATIONARITY_GATE,
                    left=left, right=right, error=stationarity)
        q = min(min(left), min(right))
        eta = .5 * math.log(1 / q) / math.log(2 / q)
        data = np.concatenate([np.eye(m + n)] +
                              [rng.dirichlet(np.full(m + n, a), size=1500)
                               for a in [.03, .3, 3.]])
        residual = float(np.max(divergence(data @ P, pi) - eta * divergence(data, pi)))
        ok = gates.check("weighted_bipartite_residual", residual < RESIDUAL_GATE,
                         left=left, right=right, excess=residual)
        bipartite.append({"left_prior": left, "right_prior": right,
                          "coefficient": eta, "samples": int(len(data)),
                          "stationarity_error": stationarity,
                          "largest_inequality_residual": residual,
                          "gate": RESIDUAL_GATE, "passed": ok})
    return {"reverse_erasure": reverse, "bipartite_reset": bipartite}


def supercritical_witnesses(gates):
    records = []
    for n, alpha in [(3, .7), (3, .8), (4, .8), (10, .9)]:
        # A double-precision optimiser misses the n=10, alpha=0.9 improvement;
        # use 120-digit decimal arithmetic and an explicit decimal epsilon.
        with localcontext() as ctx:
            ctx.prec = 120
            N, A, one = Decimal(n), Decimal(str(alpha)), Decimal(1)
            cp = N.ln() / (N / A).ln()
            best = None
            for k in range(1, 61):
                eps = Decimal(10) ** (-k)
                q1 = one - (one - one / N) * eps
                din = (one - eps) * ((one - eps) * N / A).ln() + eps * (eps / (one - A)).ln()
                dout = q1 * (N * q1).ln() + (one - one / N) * eps * eps.ln()
                ratio = dout / din
                if best is None or ratio > best[0]:
                    best = (ratio, eps, dout - cp * din)
            ratio, eps, margin = best
            ok = gates.check("supercritical_witness_positive", margin > 0,
                             n=n, alpha=alpha, margin=str(margin))
            records.append({"n": n, "alpha": alpha, "erasure_mass": str(eps),
                            "point_ratio": str(cp), "witness_ratio": str(ratio),
                            "improvement": str(ratio - cp), "inequality_violation": str(margin),
                            "decimal_precision": 120, "passed": ok,
                            "status": "explicit lower bound, not claimed globally optimal"})
    return records


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="directory for validation_results.json (created if absent)")
    args = parser.parse_args(argv)
    out_dir = args.output_dir.resolve()
    out = out_dir / OUTPUT_NAME
    if out.exists():
        print(f"refusing to overwrite existing file: {out}", file=sys.stderr)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    start = time.perf_counter()
    gates = Gates()
    rng = np.random.default_rng(SEED)
    report = {"script": Path(__file__).name,
              "source_sha256": sha256_of(Path(__file__).resolve()),
              "seed": SEED, "python": platform.python_version(),
              "python_optimize_flag": sys.flags.optimize,
              "numpy": np.__version__, "scipy": scipy.__version__,
              "residual_gate": RESIDUAL_GATE}
    # The call order (and hence the random stream) is identical to the
    # 1 November 2026 run, so the sample counts reproduce exactly.
    report["exact_markov"] = exact_markov_checks(gates)
    report["bipartite"] = graph_checks(gates, rng)
    report["binary_equality"] = binary_equality_checks(gates)
    report["power_mean"] = mean_checks(gates, rng)
    report["reverse_erasure"] = reverse_erasure_checks(gates, rng)
    report["weighted"] = weighted_checks(gates, rng)
    report["supercritical_witnesses"] = supercritical_witnesses(gates)
    counts = {
        "graph_samples": sum(x["samples"] for x in report["bipartite"]),
        "mean_samples": sum(x["samples"] for x in report["power_mean"]),
        "erasure_samples": sum(x["samples"] for x in report["reverse_erasure"]),
        "weighted_samples": sum(x["samples"] for x in report["weighted"]["reverse_erasure"])
        + sum(x["samples"] for x in report["weighted"]["bipartite_reset"]),
    }
    report["counts"] = counts
    report["gates_evaluated"] = gates.total
    report["failures"] = gates.failures
    passed = not gates.failures
    report["passed"] = passed
    report["status"] = ("all finite diagnostics passed (numerical evidence only; not a proof)"
                        if passed else f"FAILED: {len(gates.failures)} gate(s) failed")
    report["elapsed_seconds"] = time.perf_counter() - start
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_file": OUTPUT_NAME, "status": report["status"],
                      "gates_evaluated": gates.total, **counts,
                      "elapsed_seconds": report["elapsed_seconds"]}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
