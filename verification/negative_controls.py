#!/usr/bin/env python3
"""Negative controls and structured near-extremiser checks.

Why this script exists
----------------------
validate_entropy.py samples inputs at random. Random inputs rarely land near
the delicate extremisers, so a passing random suite says little about the
sharp threshold or about the minimum-probability reduction above it. This
script supplies two complementary kinds of evidence.

1. Negative controls (section A). Each control states a claim that is FALSE
   and must be detected: the mean inequality just below its exponent range,
   the closed formula just above (and well above) the threshold, and a graph
   coefficient shrunk by 0.1%. The script fails unless every false claim is
   detected. For each control it also reports, for information only, whether
   the random sampler of validate_entropy.py would have noticed.

2. Structured families (section B), which must pass: the boundary
   perturbation v_eps = (1-eps) delta_i + eps delta_e in high precision below
   the threshold; one-large-coordinate test vectors (r, 1, ..., 1) placed at
   the rarest and at heavier atoms; the exponential tilt built from the
   tangency system; a brute-force optimisation over the whole simplex compared
   with the scalar criterion for distinct priors with the same smallest atom;
   the weighted mean inequality tested directly; and a table of how small
   eta - c_0 is just above the threshold.

Everything here is a numerical diagnostic, not a proof.

Hygiene: no assert statements; explicit failure list; computed status; exit
status 1 on any failure; --output-dir required; an existing output file is
never overwritten; the JSON records this file's SHA-256.

Usage::

    python3 -I -B negative_controls.py --output-dir NEW_DIRECTORY
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

import mpmath as mp
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import xlogy

SEED = 20261103
OUTPUT_NAME = "negative_controls_results.json"


class Gates:
    def __init__(self) -> None:
        self.total = 0
        self.failures: list[dict] = []

    def check(self, name: str, ok: bool, **detail) -> bool:
        self.total += 1
        ok = bool(ok)
        if not ok:
            self.failures.append({"gate": name, **detail})
        return ok


def s(x, digits=20):
    return mp.nstr(x, digits)


# ---------------------------------------------------------------------------
# Shared high-precision helpers
# ---------------------------------------------------------------------------

def c0(q, alpha):
    return mp.log(1 / q) / mp.log(1 / (alpha * q))


def alpha_threshold(q):
    return q ** (q / (1 - q))


def eps_margin(q, alpha, c, eps):
    """D(v_eps R || rho) - c D(v_eps || m) for v_eps=(1-eps)delta_i+eps delta_e.

    Only the smallest atom's mass q enters, so the prior's other atoms are
    irrelevant here (their contribution is eps*(1-q)*log(eps) in total).
    """
    out_i = 1 - eps * (1 - q)
    d_out = out_i * mp.log(out_i / q) + eps * (1 - q) * mp.log(eps)
    d_in = (1 - eps) * mp.log((1 - eps) / (alpha * q)) + eps * mp.log(eps / (1 - alpha))
    return d_out - c * d_in, d_in


def best_eps_witness(q, alpha, c, kmax=300):
    best = None
    for k in range(1, kmax + 1):
        eps = mp.mpf(10) ** (-k)
        margin, d_in = eps_margin(q, alpha, c, eps)
        if best is None or margin > best[0]:
            best = (margin, k, d_in)
    return best


def logH(q, alpha, p, t):
    """log H_{q,alpha,p}(e^t), computed stably."""
    num = mp.log(alpha * (q * mp.e ** (p * t) + 1 - q) + (1 - alpha) * mp.e ** (p * q * t))
    return num - p * mp.log(q * mp.e ** t + 1 - q)


def root_p(q, alpha, t, p_hi, iters):
    """sup{p in [1,p_hi]: log H(p,t) <= 0}; log H is convex in p and <= 0 at p=1."""
    if logH(q, alpha, p_hi, t) <= 0:
        return p_hi
    lo, hi = mp.mpf(1), p_hi
    for _ in range(iters):
        mid = (lo + hi) / 2
        if logH(q, alpha, mid, t) <= 0:
            lo = mid
        else:
            hi = mid
    return lo


def scalar_eta(q, alpha, iters=110, tmax=3000):
    """eta = 1/p*, p* = min(1/c0, inf_t p(t)) (Theorem 2.2 / Remark 5.1)."""
    p_vertex = 1 / c0(q, alpha)
    grid = [mp.mpf(k) / 20 for k in range(1, 400)] + \
           [mp.mpf(20) * mp.mpf("1.02") ** k for k in range(0, 400) if 20 * 1.02 ** k <= tmax]
    vals = [(root_p(q, alpha, t, p_vertex, iters), t) for t in grid]
    p_best, t_best = min(vals)
    if p_best >= p_vertex:
        return 1 / p_vertex, None
    # golden-section refinement in t around the best grid point
    lo, hi = t_best * mp.mpf("0.95"), t_best * mp.mpf("1.05") + mp.mpf("0.05")
    g = (mp.sqrt(5) - 1) / 2
    a, b = hi - g * (hi - lo), lo + g * (hi - lo)
    fa, fb = root_p(q, alpha, a, p_vertex, iters), root_p(q, alpha, b, p_vertex, iters)
    for _ in range(80):
        if fa < fb:
            hi, b, fb = b, a, fa
            a = hi - g * (hi - lo)
            fa = root_p(q, alpha, a, p_vertex, iters)
        else:
            lo, a, fa = a, b, fb
            b = lo + g * (hi - lo)
            fb = root_p(q, alpha, b, p_vertex, iters)
    t_opt = (lo + hi) / 2
    p_opt = min(p_best, root_p(q, alpha, t_opt, p_vertex, iters))
    return 1 / p_opt, t_opt


def tilt(prior, alpha, p, r):
    """Exponential tilt (eq. tilt): returns (v_ordinary list, v_e)."""
    q = min(prior)
    i = prior.index(q)
    Z = alpha * (q * r ** p + 1 - q) + (1 - alpha) * r ** (p * q)
    v = [alpha * rho / Z for rho in prior]
    v[i] = alpha * q * r ** p / Z
    return v, (1 - alpha) * r ** (p * q) / Z


def ratio_mp(prior, alpha, v, ve):
    out = [vj + ve * rho for vj, rho in zip(v, prior)]
    d_out = mp.fsum(o * mp.log(o / rho) for o, rho in zip(out, prior) if o > 0)
    d_in = mp.fsum(vj * mp.log(vj / (alpha * rho)) for vj, rho in zip(v, prior) if vj > 0)
    if ve > 0:
        d_in += ve * mp.log(ve / (1 - alpha))
    return d_out / d_in


# ---------------------------------------------------------------------------
# Float helpers
# ---------------------------------------------------------------------------

def divergence(p, q):
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    return np.sum(xlogy(p, p / q), axis=-1)


def random_reverse_erasure_residual(prior, alpha, c, rng):
    """The random sampler of validate_entropy.py applied to a (possibly false) claim."""
    mu = np.array(prior)
    reference = np.r_[alpha * mu, 1 - alpha]
    data = np.concatenate([np.eye(len(mu) + 1)] +
                          [rng.dirichlet(np.full(len(mu) + 1, a), size=2000) for a in [.03, .3, 3.]])
    output = data[:, :-1] + data[:, -1, None] * mu
    return float(np.max(divergence(output, mu) - c * divergence(data, reference)))


def log_weighted_gao_gap(prior, p, z_log):
    """log RHS - log LHS of Gao's inequality, LHS=(sum rho z)^p (should be <= 0)."""
    rho = np.asarray(prior)
    q = rho.min()
    log_lhs = p * np.log(np.sum(rho * np.exp(z_log), axis=-1))
    log_pow = np.log(np.sum(rho * np.exp(p * z_log), axis=-1))
    log_geo = p * np.sum(rho * z_log, axis=-1)
    rhs = np.logaddexp((p - 1) * np.log(q) + log_pow, np.log1p(-q ** (p - 1)) + log_geo)
    return rhs - log_lhs


def structured_vectors(n, t_grid, position):
    z = np.zeros((len(t_grid), n))
    z[:, position] = t_grid
    return z


# ---------------------------------------------------------------------------
# A. Negative controls (false claims that must be detected)
# ---------------------------------------------------------------------------

def mp_gao_gap(prior, p, t):
    """Relative gap RHS/LHS - 1 of Gao's inequality at z=(e^t,1,...,1), large atom rarest."""
    q = min(prior)
    lhs = (q * mp.e ** t + 1 - q) ** p
    rhs = q ** (p - 1) * (q * mp.e ** (p * t) + 1 - q) + (1 - q ** (p - 1)) * mp.e ** (p * q * t)
    return rhs / lhs - 1


def control_gao_below_range(gates, rng):
    """The violation is relatively small (it is a lower-order term), so it is
    evaluated in 60-digit arithmetic on the structured family (r,1,...,1)."""
    records = []
    for prior in ([0.25] * 4, [0.1] * 10, [0.1, 0.2, 0.7]):
        q = min(prior)
        p = 0.97 / (1 - q)
        qm, pm = mp.mpf(q), mp.mpf(p)
        gaps = [(mp_gao_gap([qm], pm, mp.mpf(k) / 4), k / 4) for k in range(1, 801)]
        structured_max, at_t = max(gaps)
        structured_max = float(structured_max)
        data = np.concatenate([rng.dirichlet(np.full(len(prior), a), size=1500) for a in [.05, .5, 5.]])
        with np.errstate(divide="ignore"):
            random_max = float(np.max(log_weighted_gao_gap(prior, p, np.log(data))))
        detected = structured_max > 1e-30
        gates.check("control_gao_below_range_detected", detected, prior=prior, p=p)
        records.append({"prior": prior, "p": p, "valid_range_begins_at": 1 / (1 - q),
                        "structured_max_relative_violation_60_digits": structured_max,
                        "at_log_r": at_t,
                        "random_sampler_max_log_violation": random_max,
                        "random_sampler_detects": random_max > 1e-9,
                        "detected": detected})
    return records


def control_atomic_above_threshold(gates, rng):
    records = []
    cases = [([1 / 3] * 3, "1.04 x threshold"), ([0.1, 0.2, 0.7], "threshold+0.03"),
             ([0.1] * 10, "0.9"), ([1 / 32] * 32, "0.95")]
    for prior, rule in cases:
        q = mp.mpf(min(prior)) if len(set(prior)) > 1 else 1 / mp.mpf(len(prior))
        a_thr = alpha_threshold(q)
        if rule == "1.04 x threshold":
            alpha = a_thr * mp.mpf("1.04")
        elif rule == "threshold+0.03":
            alpha = a_thr + mp.mpf("0.03")
        else:
            alpha = mp.mpf(rule)
        claim = c0(q, alpha)  # the false claim eta = c_0 above the threshold
        margin, k, d_in = best_eps_witness(q, alpha, claim)
        detected = margin > 0
        gates.check("control_atomic_above_threshold_detected", detected, prior_size=len(prior),
                    alpha=s(alpha), margin=s(margin))
        random_res = random_reverse_erasure_residual(prior, float(alpha), float(claim), rng)
        records.append({"prior": prior if len(prior) <= 4 else f"uniform on {len(prior)} symbols",
                        "alpha": s(alpha), "alpha_threshold": s(a_thr), "false_claim_c0": s(claim),
                        "best_epsilon": f"1e-{k}", "witness_margin": s(margin, 8),
                        "improvement_over_claim": s(margin / d_in, 8),
                        "random_sampler_max_residual": random_res,
                        "random_sampler_detects": random_res > 2e-12,
                        "detected": detected})
    return records


def control_shrunk_graph(gates, rng):
    records = []
    for m, n in [(3, 3), (3, 100), (2, 5)]:
        pi = np.r_[np.full(m, 1 / (2 * m)), np.full(n, 1 / (2 * n))]
        P = np.eye(m + n) / 2
        P[:m, m:] = 1 / (2 * n)
        P[m:, :m] = 1 / (2 * m)
        M = max(m, n)
        claim = 0.999 * math.log(M) / (2 * math.log(2 * M))
        atoms = np.eye(m + n)
        atom_res = float(np.max(divergence(atoms @ P, pi) - claim * divergence(atoms, pi)))
        data = np.concatenate([rng.dirichlet(np.full(m + n, a), size=2000) for a in [.03, .2, 1., 8.]])
        rand_res = float(np.max(divergence(data @ P, pi) - claim * divergence(data, pi)))
        detected = atom_res > 1e-9
        gates.check("control_shrunk_graph_detected", detected, m=m, n=n)
        records.append({"m": m, "n": n, "false_claim": claim,
                        "point_input_max_residual": atom_res,
                        "random_sampler_without_atoms_max_residual": rand_res,
                        "random_sampler_detects": rand_res > 2e-12, "detected": detected})
    return records


# ---------------------------------------------------------------------------
# B. Structured families (true claims that must pass)
# ---------------------------------------------------------------------------

def family_eps_below_threshold(gates):
    records = []
    for q, label in [(1 / mp.mpf(3), "uniform n=3"), (mp.mpf("0.1"), "q=0.1"), (mp.mpf("0.45"), "q=0.45")]:
        a_thr = alpha_threshold(q)
        for alpha in (mp.mpf("0.5") * a_thr, mp.mpf("0.999") * a_thr, a_thr):
            claim = c0(q, alpha)
            margin, k, _ = best_eps_witness(q, alpha, claim)
            ok = gates.check("family_eps_below_threshold_nonpositive", margin <= mp.mpf(10) ** -50,
                             q=s(q), alpha=s(alpha), margin=s(margin))
            records.append({"prior_min": label, "alpha": s(alpha), "alpha_threshold": s(a_thr),
                            "largest_margin_over_eps_grid": s(margin, 8), "at_epsilon": f"1e-{k}",
                            "passed": ok})
    return records


def family_one_large_coordinate(gates):
    """(r,1,...,1) with the large coordinate at each atom; rarest must dominate."""
    records = []
    t_grid = np.linspace(0.0, 80.0, 4001)
    prior = [0.1, 0.2, 0.7]
    q = 0.1
    for alpha in (0.3, 0.7, 0.9):
        a_thr = q ** (q / (1 - q))
        claim = math.log(1 / q) / math.log(1 / (alpha * q))
        p = 1 / claim
        envelopes = []
        for position in range(len(prior)):
            z = structured_vectors(len(prior), t_grid, position)
            rho = np.array(prior)
            log_lhs = np.logaddexp(math.log(alpha) + np.log(np.sum(rho * np.exp(p * z), axis=1)),
                                   math.log1p(-alpha) + p * np.sum(rho * z, axis=1))
            log_rhs = p * np.log(np.sum(rho * np.exp(z), axis=1))
            envelopes.append(float(np.max(log_lhs - log_rhs)))
        rarest_dominates = envelopes[0] >= max(envelopes[1:]) - 1e-12
        gates.check("family_rarest_atom_dominates", rarest_dominates, alpha=alpha, envelopes=envelopes)
        subcritical = alpha <= a_thr
        if subcritical:
            gates.check("family_subcritical_criterion_holds", envelopes[0] <= 1e-12,
                        alpha=alpha, envelope=envelopes[0])
        records.append({"prior": prior, "alpha": alpha, "alpha_threshold": a_thr,
                        "exponent_p_equals_1_over_c0": p,
                        "log_envelope_by_large_atom": dict(zip(["0.1", "0.2", "0.7"], envelopes)),
                        "subcritical": subcritical, "rarest_dominates": rarest_dominates,
                        "note": ("above the threshold the rarest envelope is positive at p=1/c0, "
                                 "which is the failure of point optimality" if not subcritical else
                                 "below the threshold every envelope is <= 0")})
    return records


def brute_force_ratio(prior, alpha, rng, n_starts=60):
    mu = np.array(prior)
    reference = np.r_[alpha * mu, 1 - alpha]

    def negative_ratio(x):
        w = np.exp(x - x.max())
        v = w / w.sum()
        d_in = divergence(v, reference)
        if d_in < 1e-10:
            return 0.0
        out = v[:-1] + v[-1] * mu
        return -divergence(out, mu) / d_in

    best = 0.0
    for _ in range(n_starts):
        x0 = rng.normal(scale=3.0, size=len(mu) + 1)
        res = minimize(negative_ratio, x0, method="Nelder-Mead",
                       options={"xatol": 1e-12, "fatol": 1e-15, "maxiter": 20000, "maxfev": 40000})
        best = max(best, -res.fun)
    return best


def family_tilt_and_brute_force(gates, rng):
    records = []
    for q_text, alpha_text, priors in [("0.3", "0.9", [[0.3, 0.7], [0.3, 0.3, 0.4], [0.3, 0.35, 0.35]]),
                                       ("0.25", "0.8", [[0.25, 0.75], [0.25, 0.25, 0.5]])]:
        q, alpha = mp.mpf(q_text), mp.mpf(alpha_text)
        eta, t_opt = scalar_eta(q, alpha)
        p_opt = 1 / eta
        r_opt = mp.e ** t_opt
        dH = mp.diff(lambda t: logH(q, alpha, p_opt, t), t_opt)
        per_prior = []
        for prior_f in priors:
            prior = [mp.mpf(str(x)) for x in prior_f]
            v, ve = tilt(prior, alpha, p_opt, r_opt)
            ratio = ratio_mp(prior, alpha, v, ve)
            brute = brute_force_ratio(prior_f, float(alpha), rng)
            ok_tilt = gates.check("family_tilt_matches_scalar", abs(ratio - eta) < mp.mpf(10) ** -15,
                                  prior=prior_f, ratio=s(ratio), eta=s(eta))
            ok_brute = gates.check("family_brute_force_matches_scalar",
                                   (brute <= float(eta) + 1e-9) and (brute >= float(eta) - 1e-7),
                                   prior=prior_f, brute=brute, eta=s(eta))
            per_prior.append({"prior": prior_f, "tilt_ratio": s(ratio, 25),
                              "brute_force_double_precision": brute,
                              "tilt_passed": ok_tilt, "brute_force_passed": ok_brute})
        records.append({"q": q_text, "alpha": alpha_text, "alpha_threshold": s(alpha_threshold(q)),
                        "scalar_criterion_eta": s(eta, 25), "c0": s(c0(q, alpha), 25),
                        "eta_minus_c0": s(eta - c0(q, alpha), 8),
                        "tangency_log_r": s(t_opt, 15), "tangency_dlogH_dt": s(dH, 5),
                        "priors": per_prior})
    return records


def family_weighted_gao(gates, rng):
    records = []
    t_grid = np.linspace(0.0, 60.0, 3001)
    for prior in ([0.1, 0.2, 0.7], [0.05, 0.05, 0.2, 0.7], [0.3, 0.7]):
        q = min(prior)
        for p in sorted({1 / (1 - q), 1.5, 2.0, 3.0, 6.0}):
            if p < 1 / (1 - q):
                continue
            worst = -np.inf
            for position in range(len(prior)):
                gap = log_weighted_gao_gap(prior, p, structured_vectors(len(prior), t_grid, position))
                worst = max(worst, float(np.max(gap)))
            data = np.concatenate([rng.dirichlet(np.full(len(prior), a), size=1500) for a in [.05, .5, 5.]])
            with np.errstate(divide="ignore"):
                worst = max(worst, float(np.max(log_weighted_gao_gap(prior, p, np.log(data)))))
            ok = gates.check("family_weighted_gao_holds", worst <= 1e-12, prior=prior, p=p, worst=worst)
            records.append({"prior": prior, "p": p, "max_log_rhs_minus_log_lhs": worst, "passed": ok})
    return records


def family_near_threshold_excess(gates):
    """How small is eta - c_0 just above the threshold? (Remark in Section 5.)"""
    records = []
    for q_text, alphas in [("0.1", ["0.85", "0.9", "0.95"]), ("0.3", ["0.65", "0.7", "0.8", "0.9"])]:
        q = mp.mpf(q_text)
        for a_text in alphas:
            alpha = mp.mpf(a_text)
            claim = c0(q, alpha)
            eta, _ = scalar_eta(q, alpha)
            margin, k, d_in = best_eps_witness(q, alpha, claim)
            witness = margin / d_in
            delta = claim - (1 - q)
            K = q * mp.log(1 / q) + delta + claim * mp.log(1 - alpha)
            heuristic = delta * mp.e ** (-1 + K / delta) / mp.log(1 / (alpha * q))
            ok = gates.check("family_excess_consistent", (eta - claim > 0) and (witness <= eta - claim),
                             q=q_text, alpha=a_text, excess=s(eta - claim), witness=s(witness))
            records.append({"q": q_text, "alpha": a_text, "alpha_threshold": s(alpha_threshold(q), 8),
                            "c0": s(claim, 15), "eta_scalar_criterion": s(eta, 25),
                            "eta_minus_c0": s(eta - claim, 6),
                            "v_eps_witness_lower_bound": s(witness, 6), "witness_epsilon": f"1e-{k}",
                            "delta_c0_minus_1_plus_q": s(delta, 6), "K_linear_coefficient": s(K, 6),
                            "heuristic_delta_exp(-1-|K|/delta)/log(1/(alpha q))": s(heuristic, 6),
                            "passed": ok})
    return records


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Negative controls and structured families")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    out_dir = args.output_dir.resolve()
    out = out_dir / OUTPUT_NAME
    if out.exists():
        print(f"refusing to overwrite existing file: {out}", file=sys.stderr)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    start = time.perf_counter()
    mp.mp.dps = 400  # epsilon down to 1e-300 in the boundary perturbations
    gates = Gates()
    rng = np.random.default_rng(SEED)
    report = {"script": Path(__file__).name,
              "source_sha256": sha256_of(Path(__file__).resolve()),
              "seed": SEED, "python": platform.python_version(),
              "python_optimize_flag": sys.flags.optimize,
              "numpy": np.__version__, "scipy": scipy.__version__, "mpmath": mp.__version__,
              "not_a_proof": True}
    controls = {
        "gao_inequality_below_its_exponent_range": control_gao_below_range(gates, rng),
        "closed_formula_claimed_above_threshold": control_atomic_above_threshold(gates, rng),
        "graph_coefficient_shrunk_by_0.1_percent": control_shrunk_graph(gates, rng),
    }
    report["A_negative_controls_must_be_detected"] = controls
    report["A_summary"] = {
        "controls": sum(len(v) for v in controls.values()),
        "detected": sum(r["detected"] for v in controls.values() for r in v),
        "random_sampler_would_detect": sum(r["random_sampler_detects"] for v in controls.values() for r in v),
    }
    families = {"eps_perturbation_at_or_below_threshold": family_eps_below_threshold(gates),
                "one_large_coordinate_at_each_atom": family_one_large_coordinate(gates),
                "weighted_gao_inequality_direct": family_weighted_gao(gates, rng)}
    mp.mp.dps = 60  # scalar-criterion computations
    families["tilt_and_brute_force_equal_q_priors"] = family_tilt_and_brute_force(gates, rng)
    families["near_threshold_excess_eta_minus_c0"] = family_near_threshold_excess(gates)
    report["B_structured_families_must_pass"] = families
    report["gates_evaluated"] = gates.total
    report["failures"] = gates.failures
    passed = not gates.failures
    report["passed"] = passed
    report["status"] = ("all controls detected and all structured families passed "
                        "(numerical evidence only; not a proof)" if passed
                        else f"FAILED: {len(gates.failures)} gate(s) failed")
    report["elapsed_seconds"] = time.perf_counter() - start
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_file": OUTPUT_NAME, "status": report["status"],
                      "gates_evaluated": gates.total, **report["A_summary"],
                      "elapsed_seconds": report["elapsed_seconds"]}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
