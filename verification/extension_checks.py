"""extension_checks.py -- numerical checks for the block-reset extension (sec:blockreset).

Usage: python3 -I -B extension_checks.py --output-dir NEW_DIR
Stdlib + numpy + scipy + mpmath. No assert statements: every check is recorded, a status is
computed, and the script exits with status 1 if any check fails or any negative control is
not detected. Refuses to write into an existing output directory. Records its own SHA-256.
Reported coefficients are numerical estimates: the largest of point-input values, multistart
searches (candidates re-evaluated in extended precision) and the local spectral value, which
may be a limit rather than a value attained at an input. No rigorous error bounds; evidence,
not proofs.
"""
import math
import numpy as np
from scipy.optimize import minimize, brentq


# ---------------------------------------------------------------- basics
def kl(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    m = a > 0
    return float(np.sum(a[m] * np.log(a[m] / b[m])))


def block_reset(mus, a, M, w):
    """Kernel K(x,.) = a_B delta_x + sum_C M[B,C] mu_C on the disjoint union of blocks.

    mus: list of 1-d positive arrays summing to 1; a: stay probabilities;
    M: nonnegative matrix with rows summing to 1 - a_B; w: positive block weights.
    Returns (K, pi, lam, block_index list).
    """
    sizes = [len(m) for m in mus]
    offs = np.cumsum([0] + sizes)
    n = offs[-1]
    K = np.zeros((n, n))
    pi = np.zeros(n)
    w = np.asarray(w, float) / np.sum(w)
    for B, muB in enumerate(mus):
        sl = slice(offs[B], offs[B + 1])
        pi[sl] = w[B] * np.asarray(muB, float)
        for x in range(offs[B], offs[B + 1]):
            K[x, x] += a[B]
            for C, muC in enumerate(mus):
                K[x, offs[C]:offs[C + 1]] += M[B][C] * np.asarray(muC, float)
    lam = pi @ K
    return K, pi, lam, offs


def collapse(mus):
    """Replace each non-singleton block law by the binary law (q_B, 1-q_B)."""
    out = []
    for m in mus:
        m = np.asarray(m, float)
        if len(m) == 1:
            out.append(np.array([1.0]))
        else:
            q = float(m.min())
            out.append(np.array([q, 1.0 - q]))
    return out


def ratio_and_grad(theta, K, pi, lam):
    t = theta - theta.max()
    v = np.exp(t)
    v /= v.sum()
    out = v @ K
    D = float(np.sum(v * np.log(v / pi)))
    N = float(np.sum(out * np.log(out / lam)))
    if D < 1e-14:
        return 0.0, np.zeros_like(theta)
    gN = K @ (np.log(out / lam) + 1.0)
    gD = np.log(v / pi) + 1.0
    gv = (gN * D - N * gD) / D ** 2
    gt = v * (gv - v @ gv)
    return N / D, gt


def point_ratios(K, pi, lam):
    n = len(pi)
    return np.array([kl(K[i], lam) / math.log(1.0 / pi[i]) for i in range(n)])


def eta_bruteforce(K, pi, lam, rng, starts=40, extra=()):
    """Multistart maximisation of KL(vK||lam)/KL(v||pi). Returns (value, v)."""
    n = len(pi)
    pr = point_ratios(K, pi, lam)
    best = float(pr.max())
    bestv = np.eye(n)[int(pr.argmax())]

    def fun(th):
        r, g = ratio_and_grad(th, K, pi, lam)
        return -r, -g

    x0s = []
    for s in range(starts):
        kind = s % 4
        if kind == 0:
            v0 = rng.dirichlet(np.full(n, rng.choice([0.2, 0.5, 1.0, 3.0])))
            x0s.append(np.log(v0 + 1e-12))
        elif kind == 1:
            x = rng.normal(size=n) * 0.3
            x[rng.integers(n)] += rng.uniform(3, 15)
            x0s.append(x)
        elif kind == 2:
            x = rng.normal(size=n) * 0.3
            i, j = rng.choice(n, 2, replace=False)
            x[i] += rng.uniform(3, 10)
            x[j] += rng.uniform(0, 6)
            x0s.append(x)
        else:
            x0s.append(np.log(pi) + rng.normal(size=n) * rng.choice([0.3, 1.0, 2.0]))
    x0s.extend(extra)
    for x0 in x0s:
        try:
            r = minimize(fun, np.asarray(x0, float), jac=True, method="L-BFGS-B",
                         bounds=[(-60, 60)] * n, options={"maxiter": 3000, "ftol": 1e-15, "gtol": 1e-12})
        except Exception:
            continue
        if np.isfinite(r.fun) and -r.fun > best:
            t = r.x - r.x.max()
            v = np.exp(t)
            v = v / v.sum()
            # near the reference the double-precision ratio is a 0/0 cancellation;
            # accept only the high-precision re-evaluated value
            val = float(ratio_mp(v, K, pi, dps=40))
            if val > best:
                best, bestv = val, v
    loc = local_chi2(K, pi, lam)
    return max(best, loc), bestv


def local_chi2(K, pi, lam):
    """Squared second singular value of K from L^2(lam) to L^2(pi): the local (chi^2)
    coefficient, a lower bound for the KL coefficient (approach along the reference)."""
    A = np.diag(np.sqrt(pi)) @ K @ np.diag(1.0 / np.sqrt(lam))
    sv = np.linalg.svd(A, compute_uv=False)
    return float(sv[1] ** 2) if len(sv) > 1 else 0.0


def ratio_mp(v, K, pi, dps=50):
    """Extended-precision re-evaluation of the ratio at a given input v (no error enclosure)."""
    import mpmath as mp
    mp.mp.dps = dps
    n = len(pi)
    vv = [mp.mpf(float(x)) for x in v]
    s = mp.fsum(vv)
    vv = [x / s for x in vv]
    # normalise reference and kernel rows exactly at working precision, so that the
    # input and output laws are exact probability vectors (otherwise O(1e-17) mass
    # defects dominate the ratio near the reference)
    pim = [mp.mpf(float(x)) for x in pi]
    sp = mp.fsum(pim)
    pim = [x / sp for x in pim]
    Km = []
    for i in range(n):
        row = [mp.mpf(float(K[i, j])) for j in range(n)]
        sr = mp.fsum(row)
        Km.append([x / sr for x in row])
    lam = [mp.fsum(pim[i] * Km[i][j] for i in range(n)) for j in range(n)]
    out = [mp.fsum(vv[i] * Km[i][j] for i in range(n)) for j in range(n)]
    N = mp.fsum(out[j] * mp.log(out[j] / lam[j]) for j in range(n) if out[j] > 0)
    D = mp.fsum(vv[i] * mp.log(vv[i] / pim[i]) for i in range(n) if vv[i] > 0)
    return N / D


# ---------------------------------------------------------------- key lemma
def two_value_power(w, g, p):
    """Lemma 3.3 quantities: a<b with (1-w)a+wb=1, a^(1-w) b^w=g; returns M_p(w)."""
    if g >= 1.0:
        return 1.0
    f = lambda lr: w * lr - math.log(1 - w + w * math.exp(lr)) - math.log(g)
    hi = 1.0
    while f(hi) > 0:
        hi *= 2
    lr = brentq(f, 1e-14, hi, xtol=1e-15, rtol=1e-15, maxiter=500)
    r = math.exp(lr)
    a = 1.0 / (1 - w + w * r)
    b = r * a
    return (1 - w) * a ** p + w * b ** p


def _feasible_from_direction(mu, z, g):
    """Map a direction z to the unique y = exp(t z0)/E exp(t z0) (z0 = z - E z, t > 0) with
    E y = 1 and G(y) = g. Every positive y with these means arises this way."""
    z0 = z - mu @ z
    if np.max(np.abs(z0)) < 1e-12:
        return None
    target = -math.log(g)
    def h(t):
        e = t * z0
        m = e.max()
        return m + math.log(float(mu @ np.exp(e - m))) - target
    hi = 1.0
    while h(hi) < 0:
        hi *= 2.0
        if hi > 1e8:
            return None
    t = brentq(h, 0.0, hi, xtol=1e-15, rtol=1e-15, maxiter=500)
    e = t * z0
    lse = e.max() + math.log(float(mu @ np.exp(e - e.max())))
    return e - lse  # log y


def sup_power_fixed_means(mu, g, p, rng, starts=30):
    """Numerical sup of E_mu y^p subject to E_mu y = 1 and G_mu(y) = g, over an exact
    parametrisation of the constraint set (no penalty, no constrained solver)."""
    mu = np.asarray(mu, float)
    n = len(mu)
    def obj(z):
        ly = _feasible_from_direction(mu, z, g)
        if ly is None:
            return 0.0
        m = (p * ly).max()
        return -math.exp(m) * float(mu @ np.exp(p * ly - m))
    best = -np.inf
    for s in range(starts):
        if s < n:
            z0 = np.zeros(n); z0[s] = 1.0
        elif s < 2 * n:
            z0 = np.zeros(n); z0[s - n] = -1.0
        else:
            z0 = rng.normal(size=n)
        r = minimize(obj, z0, method="Nelder-Mead",
                     options={"maxiter": 4000 * n, "xatol": 1e-12, "fatol": 1e-15})
        best = max(best, -r.fun, -obj(z0))
    return best


# ---------------------------------------------------------------- families
def lazy_bipartite(muA, muB, s):
    """sI + (1-s)(cross reset): from A to mu_B, from B to mu_A; stationary weights (1/2,1/2)."""
    return block_reset([muA, muB], [s, s], [[0.0, 1 - s], [1 - s, 0.0]], [0.5, 0.5])


def lazy_bipartite_power(muA, muB, s, k):
    """k-th power of lazy_bipartite in block-reset coordinates (a = s^k)."""
    # coefficients of I, J, J^2 with J^3 = J (J = cross reset, J^2 = own-part reset)
    cI, cJ, cJ2 = 1.0, 0.0, 0.0
    for _ in range(k):
        # (cI I + cJ J + cJ2 J^2)(s I + (1-s) J)
        nI = cI * s
        nJ = cJ * s + cI * (1 - s) + cJ2 * (1 - s)
        nJ2 = cJ2 * s + cJ * (1 - s)
        cI, cJ, cJ2 = nI, nJ, nJ2
    return block_reset([muA, muB], [cI, cI], [[cJ2, cJ], [cJ, cJ2]], [0.5, 0.5]), (cI, cJ, cJ2)


def multipartite_srw(sizes, s):
    """Lazy simple random walk on the complete multipartite graph K_{n_1..n_r}:
    stay w.p. s, else move to a uniform neighbour (all vertices outside own part)."""
    r = len(sizes)
    Ntot = sum(sizes)
    mus = [np.full(n, 1.0 / n) for n in sizes]
    M = [[0.0 if i == j else (1 - s) * sizes[j] / (Ntot - sizes[i]) for j in range(r)] for i in range(r)]
    w = [n * (Ntot - n) for n in sizes]
    return block_reset(mus, [s] * r, M, w)


def point_ratio_lazy(q, s):
    """Rarest-vertex point ratio for lazy_bipartite with q = smallest conditional mass."""
    return (s * math.log(2 * s / q) + (1 - s) * math.log(2 * (1 - s))) / math.log(2 / q)


def eps_edge_condition(q, s):
    """Point input fails (cross-part eps log eps perturbation) iff this is > 0."""
    return point_ratio_lazy(q, s) - (1 - s) * (1 - q)


# ======================================================================== checks
import argparse
import hashlib
import json
import os
import sys
import time
import platform


class Recorder:
    def __init__(self):
        self.records = []

    def check(self, name, ok, **data):
        self.records.append({"name": name, "kind": "check", "ok": bool(ok), **_jsonable(data)})
        return bool(ok)

    def control(self, name, detected, **data):
        """Negative control: a deliberately wrong claim that the suite must reject."""
        self.records.append({"name": name, "kind": "negative_control", "ok": bool(detected),
                             "detected": bool(detected), **_jsonable(data)})
        return bool(detected)

    def observe(self, name, **data):
        self.records.append({"name": name, "kind": "numerical_observation", "ok": True, **_jsonable(data)})

    def failures(self):
        return [r for r in self.records if not r["ok"]]


def _jsonable(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, (np.floating,)):
            v = float(v)
        elif isinstance(v, (np.integer,)):
            v = int(v)
        elif isinstance(v, np.ndarray):
            v = v.tolist()
        elif isinstance(v, (list, tuple)):
            v = [float(x) if isinstance(x, (np.floating, float)) else
                 (x.tolist() if isinstance(x, np.ndarray) else x) for x in v]
        out[k] = v
    return out


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def lift_input(vc, mus, offs_full, offs_coll):
    """Lift a collapsed input to the full chain: rare-atom mass to one rarest atom,
    the remaining block mass spread proportionally to mu on the other atoms."""
    v = np.zeros(offs_full[-1])
    for B, mu in enumerate(mus):
        mu = np.asarray(mu, float)
        if len(mu) == 1:
            v[offs_full[B]] = vc[offs_coll[B]]
            continue
        i = int(np.argmin(mu))
        rest = mu.copy()
        rest[i] = 0.0
        rest /= rest.sum()
        v[offs_full[B]:offs_full[B + 1]] = vc[offs_coll[B] + 1] * rest
        v[offs_full[B] + i] = vc[offs_coll[B]]
    return v


def eta_pair(mus, a, M, w, rng, starts_full=60, starts_coll=60):
    K, pi, lam, of = block_reset(mus, a, M, w)
    cm = collapse(mus)
    Kc, pic, lamc, oc = block_reset(cm, a, M, w)
    ef, vf = eta_bruteforce(K, pi, lam, rng, starts=starts_full)
    ec, vc = eta_bruteforce(Kc, pic, lamc, rng, starts=starts_coll)
    return ef, ec, (K, pi, lam, of, vf), (Kc, pic, lamc, oc, vc)


def main():
    ap = argparse.ArgumentParser(description="Block-reset extension checks")
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--seed", type=int, default=20261103)
    args = ap.parse_args()
    outdir = os.path.abspath(args.output_dir)
    if os.path.exists(outdir):
        print(f"REFUSING: output directory {outdir} already exists; choose a new one.", file=sys.stderr)
        raise SystemExit(2)
    os.makedirs(outdir)
    t0 = time.time()
    me = os.path.abspath(__file__)
    rng = np.random.default_rng(args.seed)
    R = Recorder()
    TOL = 1e-7

    # ------------------------------------------------------------ A. key lemma
    mus_test = [[0.1, 0.2, 0.7], [0.1, 0.45, 0.45], [0.15, 0.15, 0.3, 0.4], [0.05, 0.25, 0.3, 0.4],
                [0.3, 0.3, 0.4]]
    worst = 0.0
    for mu in mus_test:
        q = min(mu)
        for p in (0.3, 0.7, 1.5, 3.0):
            for g in (0.4, 0.9):
                num = sup_power_fixed_means(mu, g, p, rng, starts=10)
                th = two_value_power(q if p > 1 else 1 - q, g, p)
                rel = abs(num - th) / th
                worst = max(worst, rel)
                R.check("keylemma_sup", rel < 1e-8, mu=mu, p=p, g=g, numeric=num, formula=th, rel=rel)
    R.observe("keylemma_worst_rel", worst=worst)
    # negative controls: wrong atom (larger min) for p>1, wrong branch for p<1
    mu = [0.1, 0.2, 0.7]
    num = sup_power_fixed_means(mu, 0.5, 2.0, rng, starts=10)
    wrong = two_value_power(0.2, 0.5, 2.0)
    R.control("NC_keylemma_larger_min_atom", abs(num - wrong) / num > 1e-3, numeric=num, wrong_formula=wrong)
    num = sup_power_fixed_means(mu, 0.5, 0.5, rng, starts=10)
    wrong = two_value_power(0.1, 0.5, 0.5)
    R.control("NC_keylemma_p_below_one_high_at_rarest", abs(num - wrong) / num > 1e-3, numeric=num,
              wrong_formula=wrong)
    # sign of M_p'(w) by finite differences: negative for p>1, positive for 0<p<1
    sign_ok = True
    for p in (0.2, 0.6, 0.9, 1.1, 2.0, 5.0):
        for g in (0.2, 0.6, 0.95):
            for w in np.linspace(0.05, 0.95, 10):
                h = 1e-5
                d = (two_value_power(w + h, g, p) - two_value_power(w - h, g, p)) / (2 * h)
                if (p > 1 and not d < 0) or (p < 1 and not d > 0):
                    sign_ok = False
    R.check("weight_monotonicity_sign", sign_ok)

    # ------------------------------------------------------------ B. reduction on random chains
    above = 0
    worst = 0.0
    lift_worst = 0.0
    for trial in range(24):
        nb = int(rng.integers(2, 4))
        mus = []
        for B in range(nb):
            k = int(rng.integers(1, 4))
            mus.append(rng.dirichlet(np.ones(k) * rng.choice([0.5, 2.0])))
        a = rng.uniform(0, 0.6, size=nb) * (rng.random(nb) < 0.8)
        M = np.array([rng.dirichlet(np.ones(nb) * 0.5) * (1 - a[B]) for B in range(nb)])
        w = rng.uniform(0.2, 1.0, size=nb)
        ef, ec, F, C = eta_pair(mus, a, M, w, rng, 50, 50)
        amin = min([x for x in a if x > 0], default=float("inf"))
        if ef > amin:
            above += 1
        worst = max(worst, abs(ef - ec))
        R.check("reduction_random_chain", abs(ef - ec) <= TOL * max(1.0, ef), trial=trial,
                sizes=[len(m) for m in mus], eta_full=ef, eta_collapsed=ec, a_min=amin,
                beyond_lead_hypothesis=bool(ef > amin))
        # lifting is exact at the level of the ratio
        Kc, pic, lamc, oc, vc = C
        K, pi, lam, of, _ = F
        vl = lift_input(vc, mus, of, oc)
        rl = float(ratio_mp(vl, K, pi, 40))
        rc = float(ratio_mp(vc, Kc, pic, 40))
        lift_worst = max(lift_worst, abs(rl - rc))
    R.check("lift_preserves_ratio", lift_worst < 1e-12, worst=lift_worst)
    R.observe("reduction_random_summary", worst_abs_diff=worst, cases_with_eta_above_min_stay=above,
              cases=24)
    # negative control: collapse with a wrong (larger) minimum atom
    muA = np.array([0.1, 0.2, 0.7])
    muB = np.array([0.25, 0.75])
    K, pi, lam, _ = lazy_bipartite(muA, muB, 0.5)
    ef, _ = eta_bruteforce(K, pi, lam, rng, starts=50)
    Kw, piw, lamw, _ = lazy_bipartite(np.array([0.2, 0.8]), muB, 0.5)
    ew, _ = eta_bruteforce(Kw, piw, lamw, rng, starts=50)
    R.control("NC_collapse_with_larger_min_atom", abs(ef - ew) > 1e-3, eta_full=ef, eta_wrong=ew)

    # ------------------------------------------------------------ C. Theorem 6.1 consistency
    for muA, muB in (([0.1, 0.2, 0.7], [0.3, 0.7]), ([0.2, 0.3, 0.5], [0.15, 0.25, 0.6]),
                     ([1 / 3] * 3, [1 / 3] * 3)):
        muA = np.array(muA)
        muB = np.array(muB)
        ef, ec, _, _ = eta_pair([muA, muB], [0.5, 0.5], [[0, 0.5], [0.5, 0]], [0.5, 0.5], rng, 50, 50)
        q = min(muA.min(), muB.min())
        form = math.log(1 / q) / (2 * math.log(2 / q))
        R.check("thm61_full_vs_formula", abs(ef - form) < TOL, muA=muA, muB=muB, eta_full=ef,
                eta_collapsed=ec, formula=form)
        R.check("thm61_collapsed_vs_formula", abs(ec - form) < TOL, eta_collapsed=ec, formula=form)

    # ------------------------------------------------------------ D. Jadhav lazy star
    for n in range(3, 9):
        N = n - 1
        K, pi, lam, _ = lazy_bipartite(np.array([1.0]), np.full(N, 1.0 / N), 0.5)
        e, v = eta_bruteforce(K, pi, lam, rng, starts=40)
        form = math.log(N) / (2 * math.log(2 * N))
        R.check("star_half_lazy", abs(e - form) < TOL, n_vertices=n, eta=e, formula=form,
                pi_center=float(pi[0]))
    star_rows = []
    for s in (0.3, 0.6, 0.8):
        for n in (4, 6):
            N = n - 1
            ef, ec, _, _ = eta_pair([np.array([1.0]), np.full(N, 1.0 / N)], [s, s],
                                    [[0, 1 - s], [1 - s, 0]], [0.5, 0.5], rng, 50, 50)
            K, pi, lam, _ = lazy_bipartite(np.array([1.0]), np.full(N, 1.0 / N), s)
            pt = float(point_ratios(K, pi, lam).max())
            star_rows.append({"s": s, "n_vertices": n, "eta_full": ef, "eta_3state": ec, "point": pt})
            R.check("star_lazy_s_reduction", abs(ef - ec) < TOL, s=s, n_vertices=n, eta_full=ef,
                    eta_3state=ec, point=pt)
    R.observe("star_lazy_table", rows=json.dumps(star_rows))

    # ------------------------------------------------------------ E. arbitrary laziness on K_{n,n}
    s_grid = np.round(np.arange(0.20, 0.701, 0.01), 3)
    table = []
    summary = {}
    for n in (2, 3, 4, 5, 10, 100):
        q = 1.0 / n
        bq = np.array([q, 1 - q])
        last_point_ok = None
        first_fail_above = None
        lower_edge = None
        lowmax = 0.0
        prev_ok = False
        for s in s_grid:
            K, pi, lam, _ = lazy_bipartite(bq, bq, float(s))
            e, v = eta_bruteforce(K, pi, lam, rng, starts=40)
            c0 = point_ratio_lazy(q, float(s))
            loc = max(s * s, (2 * s - 1) ** 2)
            ok = (e - c0) <= 1e-9
            table.append((n, float(s), e, c0, loc, e - c0))
            if s < 0.5:
                lowmax = max(lowmax, e - max(c0, loc))
                if ok and not prev_ok and lower_edge is None:
                    lower_edge = float(s)
            if s >= 0.5:
                if ok and first_fail_above is None:
                    last_point_ok = float(s)
                if (not ok) and first_fail_above is None:
                    first_fail_above = float(s)
            prev_ok = ok
        try:
            eps_edge = brentq(lambda s: eps_edge_condition(q, s), 0.5 + 1e-12, 0.99) \
                if eps_edge_condition(q, 0.99) > 0 and eps_edge_condition(q, 0.5 + 1e-12) < 0 else 0.5
        except ValueError:
            eps_edge = None
        # lower crossing of c0 and (1-2s)^2
        cross = brentq(lambda s: point_ratio_lazy(q, s) - (1 - 2 * s) ** 2, 0.2, 0.3)
        summary[n] = {"first_grid_s_point_optimal_from_below": lower_edge,
                      "crossing_c0_eq_(1-2s)^2": cross,
                      "last_grid_s_point_optimal_above_half": last_point_ok,
                      "first_grid_s_point_fails_above_half": first_fail_above,
                      "eps_log_eps_edge_c0_eq_(1-s)(1-q)": eps_edge,
                      "max_eta_minus_max(c0,local)_for_s<1/2": lowmax}
        # consistency: the grid failure must not occur below the eps edge minus a step
        if eps_edge is not None and first_fail_above is not None:
            R.check("laziness_grid_vs_eps_edge", first_fail_above >= eps_edge - 1e-9 or n == 2,
                    n=n, eps_edge=eps_edge, first_fail=first_fail_above)
    R.observe("laziness_window_summary", summary=json.dumps(summary))
    with open(os.path.join(outdir, "laziness_table.csv"), "w") as fh:
        fh.write("n,s,eta_4state,point_ratio,local_chi2,eta_minus_point\n")
        for row in table:
            fh.write("%d,%.3f,%.12g,%.12g,%.12g,%.3e\n" % row)
    # high-precision eps perturbation at n=3 (sign of the gain)
    import mpmath as mp
    mp.mp.dps = 220
    for s_val, expect_gain in (("0.525", True), ("0.515", False)):
        s_m = mp.mpf(s_val)
        n = 3
        q = mp.mpf(1) / n
        # chain on K_{3,3} (full, uniform), point at vertex a0, eps mass to b0
        eps = mp.mpf(10) ** -200
        Nst = 6
        pi_m = [mp.mpf(1) / 6] * 6
        Km = [[mp.mpf(0)] * 6 for _ in range(6)]
        for x in range(6):
            Km[x][x] += s_m
            other = range(3, 6) if x < 3 else range(0, 3)
            for y in other:
                Km[x][y] += (1 - s_m) / 3
        def ratio_m(v):
            out = [mp.fsum(v[i] * Km[i][j] for i in range(Nst)) for j in range(Nst)]
            Nn = mp.fsum(out[j] * mp.log(out[j] * 6) for j in range(Nst) if out[j] > 0)
            Dd = mp.fsum(v[i] * mp.log(v[i] * 6) for i in range(Nst) if v[i] > 0)
            return Nn / Dd
        v0 = [mp.mpf(1)] + [mp.mpf(0)] * 5
        v1 = [1 - eps, 0, 0, eps, 0, 0]
        gain = ratio_m(v1) - ratio_m(v0)
        R.check("eps_perturbation_sign_n3", (gain > 0) == expect_gain, s=s_val,
                gain=mp.nstr(gain, 5), expected_gain=expect_gain)
    # validation of the 4-state reduction against the full chains
    for (m_, n_, s) in ((3, 3, 0.26), (3, 3, 0.3), (3, 3, 0.55), (3, 3, 0.6), (4, 4, 0.55),
                        (2, 5, 0.58), (3, 3, 0.15), (4, 4, 0.8)):
        muA = np.full(m_, 1.0 / m_)
        muB = np.full(n_, 1.0 / n_)
        ef, ec, F, C = eta_pair([muA, muB], [s, s], [[0, 1 - s], [1 - s, 0]], [0.5, 0.5], rng, 80, 60)
        R.check("laziness_full_vs_4state", abs(ef - ec) <= 1e-6, m=m_, n=n_, s=s, eta_full=ef,
                eta_4state=ec, point=point_ratio_lazy(1.0 / max(m_, n_), s))
    # negative control: "point inputs optimal at s = 0.6, n = 3"
    K, pi, lam, _ = lazy_bipartite(np.array([1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3]), 0.6)
    e, _ = eta_bruteforce(K, pi, lam, rng, starts=40)
    R.control("NC_point_optimal_at_s0.6_n3", e - point_ratio_lazy(1 / 3, 0.6) > 1e-3, eta=e,
              point=point_ratio_lazy(1 / 3, 0.6))

    # ------------------------------------------------------------ F. powers
    pw = []
    for n in (3, 5):
        mu = np.full(n, 1.0 / n)
        e1 = math.log(n) / (2 * math.log(2 * n))
        for k in (2, 3):
            (K, pi, lam, of), coef = lazy_bipartite_power(mu, mu, 0.5, k)
            # sanity: equals the matrix power
            K1, _, _, _ = lazy_bipartite(mu, mu, 0.5)
            R.check("power_algebra", np.max(np.abs(np.linalg.matrix_power(K1, k) - K)) < 1e-13, n=n, k=k)
            ef, _ = eta_bruteforce(K, pi, lam, rng, starts=60)
            (Kc, pic, lamc, oc), _ = lazy_bipartite_power(np.array([1 / n, 1 - 1 / n]),
                                                         np.array([1 / n, 1 - 1 / n]), 0.5, k)
            ec, vc = eta_bruteforce(Kc, pic, lamc, rng, starts=60)
            pt = float(point_ratios(K, pi, lam).max())
            R.check("power_full_vs_4state", abs(ef - ec) <= 1e-6, n=n, k=k, eta_full=ef, eta_4state=ec)
            R.check("power_submultiplicative", ef <= e1 ** k + 1e-12, n=n, k=k, eta=ef, bound=e1 ** k)
            pw.append({"n": n, "k": k, "eta": ec, "point": pt, "stay": coef[0],
                       "maximiser_4state": [round(float(x), 6) for x in vc]})
    R.observe("powers_table", rows=json.dumps(pw))
    # negative control: "point inputs optimal for P^2, n = 3"
    r = [x for x in pw if x["n"] == 3 and x["k"] == 2][0]
    R.control("NC_point_optimal_P2_n3", r["eta"] - r["point"] > 1e-3, eta=r["eta"], point=r["point"])
    R.check("reviewer_P2_n3_value", abs(r["eta"] - 0.072128) < 2e-6, eta=r["eta"])
    r5 = [x for x in pw if x["n"] == 5 and x["k"] == 2][0]
    R.check("reviewer_P2_n5_value", abs(r5["eta"] - 0.088639) < 2e-6, eta=r5["eta"])

    # ------------------------------------------------------------ G. complete multipartite
    mp_rows = []
    for sizes in ((2, 3, 4), (3, 3, 3), (1, 2, 3), (2, 2, 2, 3)):
        K, pi, lam, of = multipartite_srw(sizes, 0.5)
        # check it is the lazy SRW on the graph (stationary = degree-proportional)
        R.check("multipartite_stationary", np.max(np.abs(lam - pi)) < 1e-14, sizes=list(sizes))
        mus = [np.full(n, 1.0 / n) for n in sizes]
        Ntot = sum(sizes)
        M = [[0.0 if i == j else 0.5 * sizes[j] / (Ntot - sizes[i]) for j in range(len(sizes))]
             for i in range(len(sizes))]
        w = [n * (Ntot - n) for n in sizes]
        ef, ec, F, C = eta_pair(mus, [0.5] * len(sizes), M, w, rng, 60, 60)
        pt = float(point_ratios(K, pi, lam).max())
        R.check("multipartite_full_vs_2r_state", abs(ef - ec) <= 1e-6, sizes=list(sizes), eta_full=ef,
                eta_collapsed=ec, point=pt)
        mp_rows.append({"sizes": list(sizes), "eta": ec, "point": pt, "point_optimal": bool(ec - pt < 1e-9)})
    R.observe("multipartite_table", rows=json.dumps(mp_rows))

    # ------------------------------------------------------------ status
    fails = R.failures()
    checks = [r for r in R.records if r["kind"] == "check"]
    controls = [r for r in R.records if r["kind"] == "negative_control"]
    status = "PASS" if not fails else "FAIL"
    result = {
        "script": os.path.basename(me),
        "script_sha256": sha256_file(me),
        "python": sys.version,
        "optimize_flag": sys.flags.optimize,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "seed": args.seed,
        "elapsed_s": round(time.time() - t0, 1),
        "n_checks": len(checks),
        "n_checks_failed": sum(1 for r in checks if not r["ok"]),
        "n_negative_controls": len(controls),
        "n_negative_controls_undetected": sum(1 for r in controls if not r["ok"]),
        "status": status,
        "failures": fails,
        "records": R.records,
    }
    with open(os.path.join(outdir, "results.json"), "w") as fh:
        json.dump(result, fh, indent=1, default=str)
    lines = [f"status: {status}", f"script_sha256: {result['script_sha256']}",
             f"python -O level: {sys.flags.optimize}", f"elapsed_s: {result['elapsed_s']}",
             f"checks: {len(checks)} (failed {result['n_checks_failed']})",
             f"negative controls: {len(controls)} (undetected {result['n_negative_controls_undetected']})"]
    for r in R.records:
        if r["kind"] == "numerical_observation":
            lines.append(f"[observation] {r['name']}: " +
                         json.dumps({k: v for k, v in r.items() if k not in ('name', 'kind', 'ok')}))
    for r in fails:
        lines.append(f"[FAILED] {r['name']}: {json.dumps(r, default=str)[:400]}")
    with open(os.path.join(outdir, "summary.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    main()
