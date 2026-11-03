# Verification record

**Revised:** 3 November 2026 (final fix round). **Track:** informal mathematics with reproducible finite diagnostics.
**Proof assistant:** none. **Review:** internal and AI-assisted only; no human peer review.

## 1. What was checked analytically

The proofs in `manuscript.tex` and `block_reset.tex` are analytic and self-contained apart from standard finite
entropy identities. Separate AI reviewers checked, in round 1: entropy duality in both directions; the
one-large-coordinate second variation; the fixed-arithmetic/geometric-mean derivative and its strict sign; the
reduction to the smallest weight; the scalar proof of Gao's inequality and its equality cases; the
epsilon-log-epsilon threshold perturbation; the local quadratic and cubic expansions; compactness and attainment;
the gradient argument for the converse extremiser statement; the bipartite decomposition and its equality cases
(including singleton parts); tensorisation; and the communication converse and construction.

Section 7 (block-reset chains) was added in revision. It was then checked in a separate AI verification
re-review, an AI proof audit and an independent adversarial audit: the weight-monotonicity lemma for every exponent,
the maximal-power-sum lemma (including exponents below one), the block-reset reduction and lift, the closure lemma
and the formula for powers, the star and multipartite corollaries, and the two obstructions to point optimality.
No critical or major mathematical gap was found. One sign slip in the Theorem 6.1 proof (the inequality for
(1-q) log 2 + q log q, where two signs cancelled) and several wording points were corrected in the final round.

A successful audit means no unresolved gap was found in the inspected arguments. It is not a formal certificate.

## 2. Numerical diagnostics (final runs, 3 November 2026)

All four scripts were run with
`uv run --with numpy --with scipy --with mpmath python3 -I -B [-O] SCRIPT --output-dir DIR`
from a scratch working directory outside the package (Python 3.11.14, NumPy 2.4.6, SciPy 1.17.1, mpmath 1.4.1,
as recorded in each output). Each was run twice, without and with `-O`; the two outputs are identical apart from
the elapsed time and the optimisation flag. Outputs, stdout, stderr (empty) and exit status are in
`verification/results/2026-11-03/<script>/{standard,optimize_O}/`. Stdout records the output file name only, not
a local path.

| Script | SHA-256 (recorded in its output) | Gates | Status |
|---|---|---:|---|
| `validate_entropy.py` | `8fac29ce470edefddb963cf5c6dffd8b16fe77c28e07c1443de7662aeac1b347` | 101 | all passed, exit 0 |
| `verify_minimum_mass.py` | `69bfd43a74414c175f9f86f923d799bc7515a594c4d679424d33241e860a4a53` | 2 suites | all passed, exit 0 |
| `negative_controls.py` | `61a88a9f73090f984c30f6c8296dab2f5f143f8ca73e11fc4116fa7b432f3c83` | 56 | all passed, exit 0 |
| `extension_checks.py` | `d3a3677492503a9c2338c872b886d4aa574c97477b4bfc75415bbb6873c2471e` | 122 checks + 5 controls | all passed, exit 0 |

**Script hygiene.** No script contains `assert`. Each records every gate outcome, computes its status from the
failure list, exits 1 on any failure and 2 if the output already exists. An independent re-review set impossible
gates in copies of the scripts and forced a must-fail control to "not detected": every sabotaged copy exited 1,
with and without `-O`. (The 1 November version of `validate_entropy.py` reported success under `-O` in the same
test.)

### 2.1 Random-sample suite (`validate_entropy.py`)

Same checks and random stream as the 1 November run, so the counts reproduce exactly:

| Family | Count | What is checked |
|---|---:|---|
| Complete bipartite inputs | 88,736 | Direct multiplication by full transition matrices; atoms, random and near-atom laws |
| Uniform mean inequalities | 126,000 | Normalised residuals across dimensions and exponents |
| Uniform reverse-erasure inputs | 108,218 | Divergence ratios at and below the threshold |
| Weighted channel and reset-chain inputs | 66,084 | Non-uniform priors and weighted graph transitions |
| Binary endpoint identities | 202 | The exceptional equality families |
| Decimal witnesses above the threshold | 4 | Explicit point perturbations (120 digits) |
| Exact small kernels | 5 | Rational stochasticity, stationarity, detailed balance |

Residual gate `2e-12`. Random tests rarely land near extremisers; Section 2.2 addresses that.

### 2.2 Negative controls and structured families (`negative_controls.py`)

*Must be detected (all 10 were):* Gao's inequality just below its exponent range (p = 0.97/(1-q), three priors;
60-digit arithmetic on the vectors (r,1,...,1)); the closed formula claimed just above and well above the threshold
(four priors; boundary perturbation in 400-digit arithmetic, down to epsilon = 1e-74); a bipartite coefficient
shrunk by 0.1% (three graphs; point inputs). The random sampler of Section 2.1 would have detected only 3 of the 10.

*Must pass (all did):* the boundary perturbation never beats c_0 at or below the threshold; the rarest atom
dominates heavier atoms; the exponential tilt from the tangency system reproduces the scalar-criterion value to
more than 20 digits for five priors, identically for priors sharing q; an unconstrained double-precision search
agrees with the scalar criterion to about 1e-15; Gao's weighted inequality holds on structured and random vectors;
the numerical estimate of eta - c_0 is positive and at least the boundary-family lower bound (Table 2).

### 2.3 Minimum-mass reduction (`verify_minimum_mass.py`)

256 envelope comparisons (rarest atom against a heavier atom) and 896 moment comparisons at fixed arithmetic and
geometric means. A case is classed as vacuous when both log-envelopes are within `1e-12` of zero (the
constant-vector value). Envelope cases: **143 informative**, 111 vacuous, 2 decided by the point-input limit.
Over the informative cases the heavier-minus-rarest log-envelope difference is always negative (largest value
`-5.6e-3`); over all cases it never exceeds `1.2e-16`. The largest heavier-minus-rarest log-moment difference is
`-5.02e-6` (always negative, as Lemma 3.3 predicts). A fixed grid is not a global certificate.

### 2.4 Block-reset extension (`extension_checks.py`)

122 checks and 5 must-fail controls (all detected): the maximal-power-sum lemma for exponents above and below one;
24 random block-reset chains, full against collapsed (20 have a reported coefficient above their smallest positive
stay probability; agreement to within 1e-15); the laziness grid on K_{n,n}; the identity for P_{1/2}^k and the
power bound; four complete multipartite graphs; the star at several laziness levels; and the lift of collapsed
inputs. Reported coefficients are the largest of point-input values, multistart searches (candidates re-evaluated
in extended precision) and the local spectral value, which may be a limit rather than a value attained at an input.
They are numerical estimates without rigorous error bounds or certified global optimality.

### 2.5 Earlier outputs

`verification/results/2026-11-01_original/` keeps the first version's outputs, including an independent AI
reviewer's rerun and six exploratory full-simplex comparisons (two marked unresolved at floating-point resolution;
they are not counted as evidence).

## 3. Exact fingerprints

`prepare_fingerprints.py --output-dir NEW` regenerates `fingerprints.json` and `target.yaml` byte for byte. The
kernels and their spectra are established objects, not novelty claims.

## 4. References and sources

Every bibliography entry was transcribed from a saved raw record in `refs_records/`: Crossref JSON for DOIs,
DataCite JSON for the LIPIcs paper, arXiv API XML for preprints, and the thesis title page for Zhao (no Crossref or
arXiv record exists). The Caputo et al. numbering was checked in arXiv v1 (Example 28, Proposition 29,
Definition 4) and in the authors' manuscript (Example 4.4, Proposition 4.5, Definition 2.4); see
`refs_records/ccgp_numbering_check.md`. An independent re-review re-resolved all DOIs and arXiv records against
`refs.bib` and found no mismatch.

## 5. PDF build

Built in a scratch copy with pdfLaTeX, BibTeX (`plainnat`), then pdfLaTeX twice (TinyTeX, TeX Live 2023).
`entropy_contraction.pdf` is the resulting `manuscript.pdf` (27 pages, including Section 7 in full). The final log
has no warnings, no overfull or underfull boxes and no undefined references
(`logs/build_2026-11-03_final_manuscript.log`; local paths shortened). Every page was rendered with Poppler's
`pdftoppm` and inspected visually.

Hashes establish which files were checked; they do not establish mathematical correctness.
