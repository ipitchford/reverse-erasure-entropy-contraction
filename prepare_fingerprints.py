"""Exact finite fingerprints for a known kernel, not a novelty oracle.

Usage: python3 -I -B prepare_fingerprints.py --output-dir NEW_DIRECTORY
Writes fingerprints.json and target.yaml into NEW_DIRECTORY and refuses to
overwrite existing files, so the recorded copies beside this script are never
replaced.
"""
import argparse
import sys
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

_parser = argparse.ArgumentParser(description="Exact finite fingerprints")
_parser.add_argument("--output-dir", required=True, type=Path)
ROOT = _parser.parse_args().output_dir.resolve()
for _name in ("fingerprints.json", "target.yaml"):
    if (ROOT / _name).exists():
        sys.exit(f"refusing to overwrite existing file: {ROOT / _name}")
ROOT.mkdir(parents=True, exist_ok=True)


def mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def fingerprint(m, n):
    N = m + n
    P = [[Q(int(i == j), 2) for j in range(N)] for i in range(N)]
    for i in range(m):
        for j in range(m, N):
            P[i][j], P[j][i] = Q(1, 2 * n), Q(1, 2 * m)
    pi = [Q(1, 2 * m)] * m + [Q(1, 2 * n)] * n
    trans = list(map(list, zip(*P)))
    rev = [list(reversed(row)) for row in reversed(P)]
    swap_order = list(range(m, N)) + list(range(m))
    swapped = [[P[i][j] for j in swap_order] for i in swap_order]
    def digest(M):
        return sha256(json.dumps([[str(x) for x in row] for row in M], separators=(",", ":")).encode()).hexdigest()
    char = [Q(0), Q(-1), Q(1)]
    for _ in range(N - 2):
        char = mul(char, [Q(-1, 2), Q(1)])
    return {
        "m": m, "n": n,
        "matrix": [[str(x) for x in row] for row in P],
        "stationary_law": [str(x) for x in pi],
        "row_sums": [str(sum(row)) for row in P],
        "column_sums": [str(sum(col)) for col in trans],
        "trace": str(sum(P[i][i] for i in range(N))),
        "determinant": "0", "rank": N - 1,
        "characteristic_polynomial": "x*(x-1)*(x-1/2)^(m+n-2)",
        "characteristic_coefficients_ascending": [str(x) for x in char],
        "eigenvalues": {"1": 1, "1/2": N - 2, "0": 1},
        "entry_multiset": {str(x): count for x, count in sorted(Counter(x for row in P for x in row).items())},
        "hashes": {"original": digest(P), "transpose": digest(trans), "index_reversal": digest(rev), "part_swap": digest(swapped)},
        "exact_checks": {
            "stochastic": all(sum(row) == 1 for row in P),
            "stationary": all(sum(pi[i] * P[i][j] for i in range(N)) == pi[j] for j in range(N)),
            "reversible": all(pi[i] * P[i][j] == pi[j] * P[j][i] for i in range(N) for j in range(N)),
        },
    }


matrices = [fingerprint(m, n) for m, n in [(1, 1), (2, 2), (3, 3), (1, 2), (2, 3)]]
(ROOT / "fingerprints.json").write_text(json.dumps({
    "date": "2026-11-01",
    "role": "Object normalisation. The complete-bipartite kernels and their spectra are established objects, not originality claims.",
    "exact_instances": matrices,
    "general_invariants": {
        "rank": "m+n-1", "trace": "(m+n)/2", "determinant": "0",
        "eigenvectors": "constant:1; part difference:0; within-part mean-zero:1/2",
        "resolvent": "sum_{k>=0} t^k P^k = I + t/(1-t)*Pi + (t/2)/(1-t/2)*Q, with Q=I-Pi-S",
        "powers": "P^k=Pi+2^(-k)Q for k>=1; S projects onto the part-difference function",
        "symmetry_uniform": "S_m x S_n, with an additional exchange of parts when m=n",
    },
}, indent=2) + "\n")

target = {
    "target_id": "reverse-erasure-minimum-mass-and-bipartite-entropy",
    "search_date": "2026-11-01",
    "intended_contribution_unit": ["theorem", "proof", "bridge", "computation", "exposition"],
    "claim": {
        "exact_statement": "For every finite full-support prior rho on n>=2 states, q=min rho_i, and every alpha in (0,1), the fixed-reference KL coefficient of R(i)=delta_i, R(e)=rho under m=(alpha*rho,1-alpha) equals its value for prior(q,1-q). It is log(1/q)/log(1/(alpha*q)) precisely throughout the point-optimal regime alpha<=q^(q/(1-q)). Above that threshold the coefficient is strictly larger. The half-lazy bipartite reset chain with conditional laws mu,nu has coefficient log(1/q)/(2 log(2/q)) for q=min(mu,nu), with singleton and binary exceptions described in the manuscript.",
        "exclusions": [
            "No originality claim for the weighted mean inequality, entropy duality, tensorisation or the uniform binary coefficient.",
            "No claim of priority from a failed search.",
            "No formula for arbitrary cross-edge weights or arbitrary laziness.",
            "No elementary closed form or scalar uniqueness claim above the threshold for q<1/2.",
            "No statement that point inputs optimise powers P^k for k>=2.",
        ],
    },
    "source": {
        "originating_reference": "Caputo, Chen, Gu and Polyanskiy (2025), Entropy contractions in Markov chains: Half-step, full-step and continuous-time, Example4.4 and conjecture following Proposition4.5 in author manuscript.",
        "url": "https://people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf",
        "published_doi": "https://doi.org/10.1214/25-EJP1372",
    },
    "normalisation": {
        "indices": "Ordinary channel states 1..n, erasure last. Graph part A followed by part B.",
        "scaling": "Row-stochastic kernels; laziness exactly1/2; alpha is retention, source epsilon=1-alpha. Logs natural; operational H,I measured in bits.",
        "basis_order": "A then B; ordinary symbols then erasure",
        "symmetries": ["Relabel equal-prior states", "Exchange graph parts together with conditional laws"],
    },
    "sequences": [
        {"name": "balanced graph coefficient for n=1..6", "exact_values": ["0", "1/4", "log(3)/(2log(6))", "1/3", "log(5)/(2log(10))", "log(6)/(2log(12))"], "natural_scalings": ["twice the graph coefficient equals reverse-erasure coefficient at alpha=1/2"]},
        {"name": "balanced graph eigenvalues", "exact_values": ["1", "1/2 repeated 2n-2 times", "0"], "natural_scalings": ["2P has eigenvalues2,1,0"]},
        {"name": "uniform point threshold", "exact_values": ["1/2", "3^(-1/2)", "4^(-1/3)", "5^(-1/4)", "6^(-1/5)", "7^(-1/6)"]},
    ],
    "generating_functions": [{"name": "matrix-power resolvent", "expression": "I+t/(1-t)*Pi+(t/2)/(1-t/2)*Q", "variables": ["t"], "denominator": "(1-t)(1-t/2)", "role": "Known spectral fingerprint, not the target contraction theorem"}],
    "matrices": [{"name": f"half_lazy_K_{x['m']}_{x['n']}", "entries": x["matrix"]} for x in matrices[:3]],
    "aliases": {
        "analysis": ["Diananda inequality", "weighted arithmetic geometric power means", "entropy variational duality", "hypercontractive boundary"],
        "probability": ["half-lazy complete bipartite walk", "Bayesian reverse erasure", "bipartite reset chain", "fixed-prior strong data processing", "conditional resampling"],
        "combinatorics": ["K_m,n", "complete bipartite adjacency and transition kernels"],
        "mathematical_physics": ["Markov transfer operator", "reversible stochastic kernel", "classical erasure channel"],
        "statistics_optimisation_ml": ["information bottleneck", "KL contraction", "single-coordinate extremiser", "coarse-graining", "agreement distillation"],
    },
    "known_invariants": {"matrix_fingerprints": "fingerprints.json", "minimum_prior_statistic": "q=min rho_i", "local_reverse_coefficient": "alpha", "local_graph_coefficient": "1/4 unless both parts are singletons"},
    "search_constraints": {
        "primary_sources_only_for_technical_claims": True,
        "databases_or_corpora": ["Two live web search indexes", "arXiv and primary author PDFs", "RGMIA and university repositories", "Publisher/institutional metadata", "CMU thesis repository"],
        "limitations": "No exhaustive database, language or unpublished-proof coverage. No author enquiry or publication performed. OEIS was not used to adjudicate these analytic contraction formulas: the finite kernels/spectra are known objects and are explicitly not novelty claims.",
    },
}
# JSON is a strict subset of YAML 1.2 and avoids an extra dependency.
(ROOT / "target.yaml").write_text(json.dumps(target, indent=2) + "\n")
print("Wrote five exact fingerprints and target.yaml")
