#!/usr/bin/env python3
"""Finite diagnostics for the all-retention minimum-mass reduction.

Run: python3 -I -B verify_minimum_mass.py --output-dir NEW_DIRECTORY
Output: NEW_DIRECTORY/minimum_mass_results.json. An existing output file is
never overwritten. There are no assert statements, so python -O runs the same
checks; any failed gate gives exit status 1.

Purpose: exercise the new theorem's two numerical ingredients independently of
the older graph and atomic-regime checks: (1) scalar branch envelopes as the
distinguished coordinate's prior mass increases, and (2) power moments compared
at equal weighted arithmetic and geometric means. These fixed-seed, finite
floating-point checks are not proofs, global optimisation certificates, or a
formal verification of the manuscript.

The first check uses 256 parameter choices and a fixed grid in log(r), including
the constant and vertex limits. The second uses 128 weight/geometric-mean
choices at seven exponents, giving 896 moment comparisons. All calculations use
logarithms to avoid overflow. Numerical tolerances are disclosed in the JSON.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq


SEED = 20261101
ENVELOPE_CASES = 256
MOMENT_CASES = 128
EXPONENTS = (1.001, 1.05, 1.5, 2.0, 5.0, 20.0, 100.0)
ORDER_TOLERANCE = 2e-9
CONSTRAINT_TOLERANCE = 5e-12
# Envelopes within this distance of zero (the constant-vector value) make the
# comparison vacuous: neither branch rises measurably above the constant vector.
VACUOUS_TOLERANCE = 1e-12
OUTPUT_NAME = "minimum_mass_results.json"


def log_denominator(w, t):
    """log(w exp(t) + 1 - w), with t = log(r)."""
    return np.logaddexp(math.log(w) + t, math.log1p(-w))


def log_branch(w, alpha, p, t):
    """Log of the arithmetic-normalised scalar dual branch."""
    log_power = np.logaddexp(math.log(w) + p * t, math.log1p(-w))
    log_numerator = np.logaddexp(
        math.log(alpha) + log_power,
        math.log1p(-alpha) + p * w * t,
    )
    return log_numerator - p * log_denominator(w, t)


def envelope_checks(rng):
    # This is a sampled envelope, not a global scalar optimisation.
    t_grid = np.unique(np.r_[np.linspace(0.0, 20.0, 600),
                             np.geomspace(20.0, 2000.0, 150)])
    records = []
    for _ in range(ENVELOPE_CASES):
        q = float(np.exp(rng.uniform(math.log(1e-5), math.log(0.5))))
        w = float(rng.uniform(q, 1 - q))
        alpha = float(rng.uniform(0.001, 0.999))
        p = float(1 + 10 ** rng.uniform(-3.0, 2.0))

        def sampled_envelope(weight):
            values = log_branch(weight, alpha, p, t_grid)
            index = int(np.argmax(values))
            finite_max = float(values[index])
            vertex = math.log(alpha) + (1 - p) * math.log(weight)
            # A maximiser at the last grid point means the branch is still
            # rising towards its r = infinity (vertex) limit.
            at_end = index == len(t_grid) - 1
            return max(0.0, finite_max, vertex), finite_max, vertex, at_end

        q_max = sampled_envelope(q)[0]
        w_max, w_finite, w_vertex, w_at_end = sampled_envelope(w)
        # Classify how informative the comparison is.  If both envelopes are
        # the constant value 0 the comparison is vacuous.  If the heavier
        # envelope is attained by its vertex term, the comparison reduces to
        # w^(1-p) <= q^(1-p), which is automatic.  Otherwise a finite branch
        # value is genuinely compared.
        if max(abs(q_max), abs(w_max)) <= VACUOUS_TOLERANCE:
            kind = "vacuous_both_zero"
        elif w_vertex > 0.0 and (w_vertex >= w_finite or w_at_end):
            kind = "heavier_fixed_by_vertex"
        else:
            kind = "informative_finite_branch"
        records.append({"q": q, "w": w, "alpha": alpha, "p": p,
                        "q_log_envelope": q_max, "w_log_envelope": w_max,
                        "classification": kind,
                        "heavier_minus_rarest": w_max - q_max})
    worst = max(records, key=lambda record: record["heavier_minus_rarest"])
    informative = [r for r in records if r["classification"] == "informative_finite_branch"]
    worst_informative = (max(informative, key=lambda record: record["heavier_minus_rarest"])
                         if informative else None)
    classes = {}
    for record in records:
        classes[record["classification"]] = classes.get(record["classification"], 0) + 1
    return {
        "purpose": "Check sampled scalar branch envelopes at q <= w.",
        "parameter_cases": ENVELOPE_CASES,
        "finite_log_r_grid_points": len(t_grid),
        "finite_branch_evaluations": 2 * ENVELOPE_CASES * len(t_grid),
        "grid": {"linear": [0.0, 20.0, 600],
                 "geometric": [20.0, 2000.0, 150],
                 "duplicate_endpoints_removed": True},
        "extra_limits": ["r=1, value=1", "r=infinity, value=alpha*w^(1-p)"],
        "sampling": {"q": "log-uniform on [1e-5, 0.5]",
                     "w": "uniform on [q, 1-q]",
                     "alpha": "uniform on [0.001, 0.999]",
                     "p": "1 + 10^U, U uniform on [-3, 2]"},
        "tolerance_log_units": ORDER_TOLERANCE,
        "case_classification_counts": classes,
        "vacuous_tolerance_log_units": VACUOUS_TOLERANCE,
        "worst_informative_record": worst_informative,
        "worst_record": worst,
        "passed": worst["heavier_minus_rarest"] <= ORDER_TOLERANCE,
        "limitation": "A fixed grid is not a global envelope certificate; the proof is separate.",
        "records": records,
    }


def normalised_pair(w, log_g):
    """Solve for a < b with weighted arithmetic mean 1 and geometric mean g.

    Solve in t=log(b/a). The displayed upper bound follows from
    log(w exp(t)+1-w) >= log(w)+t; no search over the power moment is used.
    """
    upper = max(1.0, (-log_g - math.log(w)) / (1 - w) + 1.0)
    t = brentq(lambda value: w * value - log_denominator(w, value) - log_g,
               0.0, upper, xtol=1e-12, rtol=1e-14)
    log_a = -float(log_denominator(w, t))
    log_b = t + log_a
    log_arithmetic = float(np.logaddexp(math.log(w) + log_b,
                                        math.log1p(-w) + log_a))
    geometric_residual = w * log_b + (1 - w) * log_a - log_g
    return log_a, log_b, abs(log_arithmetic), abs(geometric_residual)


def log_moment(w, p, pair):
    log_a, log_b = pair[:2]
    return float(np.logaddexp(math.log(w) + p * log_b,
                             math.log1p(-w) + p * log_a))


def fixed_mean_checks(rng):
    records = []
    max_log_arithmetic_error = 0.0
    max_log_geometric_error = 0.0
    for case in range(MOMENT_CASES):
        q = float(np.exp(rng.uniform(math.log(1e-5), math.log(0.49))))
        w = float(rng.uniform(q, 1 - q))
        log_g = float(rng.uniform(-8.0, -0.001))
        rare_pair = normalised_pair(q, log_g)
        heavy_pair = normalised_pair(w, log_g)
        max_log_arithmetic_error = max(max_log_arithmetic_error,
                                       rare_pair[2], heavy_pair[2])
        max_log_geometric_error = max(max_log_geometric_error,
                                      rare_pair[3], heavy_pair[3])
        for p in EXPONENTS:
            rare_moment = log_moment(q, p, rare_pair)
            heavy_moment = log_moment(w, p, heavy_pair)
            records.append({"case": case, "q": q, "w": w,
                            "log_geometric_mean": log_g, "p": p,
                            "q_log_moment": rare_moment,
                            "w_log_moment": heavy_moment,
                            "heavier_minus_rarest": heavy_moment - rare_moment})
    worst = max(records, key=lambda record: record["heavier_minus_rarest"])
    return {
        "purpose": "Compare p-th moments while holding weighted A=1 and G fixed.",
        "weight_geometric_mean_cases": MOMENT_CASES,
        "exponents": list(EXPONENTS),
        "moment_comparisons": len(records),
        "sampling": {"q": "log-uniform on [1e-5, 0.49]",
                     "w": "uniform on [q, 1-q]",
                     "log_g": "uniform on [-8, -0.001]"},
        "root_solver": {"method": "scipy.optimize.brentq",
                        "xtol": 1e-12, "rtol": 1e-14},
        "order_tolerance_log_units": ORDER_TOLERANCE,
        "constraint_tolerance_log_units": CONSTRAINT_TOLERANCE,
        "max_absolute_log_arithmetic_error": max_log_arithmetic_error,
        "max_absolute_log_geometric_error": max_log_geometric_error,
        "worst_record": worst,
        "passed": (worst["heavier_minus_rarest"] <= ORDER_TOLERANCE
                   and max_log_arithmetic_error <= CONSTRAINT_TOLERANCE
                   and max_log_geometric_error <= CONSTRAINT_TOLERANCE),
        "records": records,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Minimum-mass reduction diagnostics")
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="directory for minimum_mass_results.json (created if absent)")
    args = parser.parse_args(argv)
    out_dir = args.output_dir.resolve()
    OUT = out_dir / OUTPUT_NAME
    if OUT.exists():
        print(f"refusing to overwrite existing file: {OUT}", file=sys.stderr)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    rng = np.random.default_rng(SEED)
    envelope = envelope_checks(rng)
    fixed_means = fixed_mean_checks(rng)
    passed = bool(envelope["passed"] and fixed_means["passed"])
    report = {
        "status": "finite diagnostics passed" if passed else "finite diagnostic failed",
        "purpose": "Reproducible numerical smoke check for the all-retention minimum-mass reduction.",
        "not_a_proof": True,
        "scope": "No claim of global optimisation, rigorous floating-point error bounds, or formal proof verification.",
        "seed": SEED,
        "python": platform.python_version(),
        "python_optimize_flag": sys.flags.optimize,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest(),
        "branch_envelopes": envelope,
        "fixed_arithmetic_geometric_means": fixed_means,
        "elapsed_seconds": time.perf_counter() - start,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_file": OUTPUT_NAME, "status": report["status"],
                      "envelope_cases": ENVELOPE_CASES,
                      "moment_comparisons": MOMENT_CASES * len(EXPONENTS),
                      "envelope_case_classes": envelope["case_classification_counts"],
                      "largest_envelope_excess_informative": (envelope["worst_informative_record"] or {}).get("heavier_minus_rarest"),
                      "largest_envelope_excess": envelope["worst_record"]["heavier_minus_rarest"],
                      "largest_moment_excess": fixed_means["worst_record"]["heavier_minus_rarest"],
                      "max_log_arithmetic_error": fixed_means["max_absolute_log_arithmetic_error"],
                      "max_log_geometric_error": fixed_means["max_absolute_log_geometric_error"]},
                     indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
