# Novelty-gate report: reverse-erasure entropy contraction

**Search date:** 1 November 2026.  
**Researchers:** AI research agents working together, with a separate final academic reviewer.  
**Corpus boundary:** two live web indexes; arXiv; primary author manuscripts; RGMIA; university thesis/repository sources; publisher and institutional metadata.  
**Contribution units:** theorem, complete proof, cross-literature identification, exposition and reproducibility artefact.

## 1. Frozen claim

The exact, quantified research target is in `target.yaml`. The final mathematical statements are Theorems 2.1–2.3 and 6.1 and Corollary 7.1 in the paper. For every finite positive prior and every retention probability strictly between zero and one, the reverse-erasure fixed-reference coefficient depends only on the smallest prior atom. Its point-optimal regime has an exact closed formula and a sharp endpoint. It yields a full proof of the stated complete-bipartite conjecture, a rank-one weighted extension, and an exact agreement-distillation rate in the specified regime.

The weighted mean inequality, the uniform binary channel coefficient, entropy duality, tensorisation and the general operational connection are not originality claims. No claim extends to arbitrary graph weights, arbitrary laziness, all matrix powers, a closed supercritical formula or a unique scalar maximiser.

Permitted language is a candidate proof of the precisely identified conjecture and a candidate general-prior entropy theorem, with no matching earlier theorem located within the recorded search. Historical priority is not established by a negative search.

## 2. Normalisation and translation table

| Source or original convention | Canonical convention | Checked translation |
|---|---|---|
| BEC erasure probability epsilon | Retention alpha | `alpha = 1-epsilon` |
| Ordinary input law after retention | Fixed reference `(alpha rho,1-alpha)` | Bayes reversal maps erasure to rho and each retained symbol to itself |
| Entropy constant c | Mean exponent p | `p=1/c`, `z_i=exp(f_i)` |
| Gao's weighted means | Reverse-erasure dual bound | `alpha=q^(p-1)`; both exponents equal p in Gao2009, or substitute variables z_i^p in Gao2003 |
| Balanced half-lazy K_n,n | Rank-one reset chain | Both conditional priors are uniform; side masses are1/2 |
| Unequal K_m,n | Degree-stationary law | Each side still has mass1/2; vertex stationarity is not uniform unless m=n |
| Reference-optimised binary-input SDPI | Fixed-reference coefficient here | Distinct optimisation domains; the former theorem does not automatically yield the latter |
| Communication output size2^k | Entropy and message units in bits | The dimensionless KL ratio is unchanged by log base |

## 3. Fingerprints

`fingerprints.json` contains exact matrices for K_1,1, K_2,2, K_3,3, K_1,2 and K_2,3, including entry multisets, stationarity, detailed balance and hashes under transpose, reversal and part exchange. The spectrum is `1, 1/2 (multiplicity m+n-2), 0`; the characteristic polynomial is `x(x-1)(x-1/2)^(m+n-2)`; rank is `m+n-1`, trace `(m+n)/2`, determinant0. The matrix-power resolvent and coefficient/threshold sequences are in the target record.

These finite kernels are known objects and their spectra are not proposed as discoveries. The originality question concerns the fixed-reference KL functional, its optimiser and its sharp value. OEIS was not used as a clearance test for the analytic logarithmic coefficient formulas or the already-identified standard kernel.

## 4. Alias map

| Analysis | Probability | Combinatorics | Mathematical physics | Information/optimisation |
|---|---|---|---|---|
| Weighted means, Diananda inequalities | Reverse erasure, conditional reset | K_m,n, bipartite adjacency | Reversible transfer operators | SDPI, hypercontractivity |
| Log-Laplace duality | Bayesian reversal | Vertex and part symmetries | Classical erasure channel | Information bottleneck, coarse-graining |
| Fixed arithmetic/geometric mean extremisers | Entropy mixing | Rank-one cross weights | Spectral projections | Agreement distillation, one-variable optimisation |

## 5. Search log

The detailed actual query families, inspected sources and formula substitutions are recorded in `novelty_audit.md` and the final reduction checkpoint in `development_notes/rarest_branch.md`. The principal reruns were:

| Stage | Query family | Decisive inspection | Consequence |
|---|---|---|---|
| Initial finite-chain target | Complete bipartite, entropy contraction, exact log-n/log-2n formulas | Caputo et al., Example4.4, Proposition4.5 and ensuing conjecture | Precise source and already-proved n=3 case identified |
| Mean-inequality simplification | Diananda, Gao, power/arithmetic/geometric means, full exponents | Gao2003 Theorem3.1 and Gao2009 Theorem1.2 | Exact prior-art collision for the entire weighted mean inequality |
| Reverse-channel interpretation | Reverse erasure, Bayesian inverse, SDPI, n-ary/nonuniform priors | Weinberger–Shayevitz §4.1; Nair–Wang2016; Zhao2021 Chapter3 | Model and full uniform binary coefficient are established |
| Arbitrary-prior threshold | Minimum probability, log(1/q), q^(q/(1-q)), reverse KL | Formula and alias searches in detailed audit | No matching general-prior channel formula located |
| Final all-retention reduction | Fixed arithmetic/geometric means, minimum weight, exact binary reduction | Gao2018 Theorem1.1 and complete §2; Ordentlich–Polyanskiy2022 | Related reduction methods and different coefficient domains distinguished |
| Operational interpretation | Reverse BEC, agreement distillation, contraction slope | Zhao2021; Guruswami–Radhakrishnan2016; Anantharam et al.2013 | Existing operational principle and binary precedent credited |

## 6. Verified collisions and bridge

The detailed audit gives exact formula maps. The essential collision is

`A^p >= q^(p-1) E_rho z^p + (1-q^(p-1)) G^p`, for `p>=1/(1-q)`.

Gao2009 covers the interval up to2 and Gao2003 covers exponents at least2. Setting `alpha=q^(p-1)` converts this established inequality into the reverse-erasure dual bound. The paper supplies a self-contained proof, while explicitly crediting the prior theorem.

The reverse binary channel is explicit in Weinberger–Shayevitz. Nair–Wang and Zhao together give its complete uniform binary coefficient. The final minimum-weight theorem treats arbitrary priors and every retention probability, including those beyond the mean inequality's point-optimal range. Gao2018 was checked at statement and proof level: it fixes particular endpoint coefficients and establishes further sufficient exponent ranges; no free-alpha exact reduction or reverse-channel universality was located there. No historical novelty is claimed for the standalone two-point moment comparison.

## 7. Negative evidence and missingness

The search was not exhaustive across all publications, languages, theses or unpublished work. Some publisher bodies and PDF endpoints were inaccessible; accessible author manuscripts were used and their version status is disclosed. The Caputo author PDF retains prepublication header placeholders; final publication metadata were checked separately. No author enquiry was sent, and no manuscript was submitted or posted. A specialist may locate earlier results under other terminology. The strongest current statement is that no exact earlier general-prior theorem or all-n proof was found in the bounded search documented here.

## 8. Outcome by contribution unit

| Unit | Outcome | Evidence strength | Allowed wording | Disallowed inference |
|---|---|---|---|---|
| Weighted mean theorem | **COLLISION** | High: exact formula map | Gao's inequality, with a self-contained derivation | New weighted mean inequality |
| Uniform binary coefficient | **COLLISION** | High: primary theorem inspected | Known boundary case | Newly solved reverse BEC |
| Published graph conjecture statement | **COLLISION** as a stated conjecture | High | The specifically cited conjecture | Newly posed graph question |
| Complete all-n proof and weighted graph consequence | **CLEAR TO PROVE**, within the recorded boundary | Moderate | Candidate proof resolving that statement | Guaranteed first proof |
| General-prior point formula | **BRIDGE** | High formula identity; moderate priority evidence | Sharp information-theoretic consequence of known means | Novel algebraic input |
| All-retention minimum-mass theorem and extremiser localisation | **BOUNDED UNCERTAINTY** on historical priority; mathematical proof supplied | Multiple independent derivations; bounded negative search | Candidate structural theorem; no exact prior match found | Exhaustively proved novel |
| Communication corollary | **BRIDGE / BOUNDED UNCERTAINTY** | Exact model, self-contained proof, known general principle | General-prior evaluation and explicit construction | New general SDPI–communication principle |
| Verification artefact | **CLEAR TO PROVE / COMPUTE** | Reproducible code and hashes | Finite diagnostics and preserved proof record | Numerical proof of the unrestricted theorem |

## 9. Decision

**Proceed with the general-prior information-theoretic contribution and the complete conjecture proof. Retain explicit prior-art attribution and bounded priority language.** The final academic review evaluates the full strengthened paper, not just the original balanced graph calculation.

## 10. Rerun triggers

A future new closed supercritical formula, uniqueness theorem, alternative physical interpretation, broader channel family, or direct prior-source identification would trigger a fresh formula-level audit. The present final reduction and operational interpretation have already received that rerun.

## 11. Revision addendum (3 November 2026)

The review round found one directly relevant 2026 preprint missed by this gate (Jadhav, arXiv:2606.27073, lazy star
left as numerical evidence). It strengthens rather than undermines the contribution: the bipartite theorem settles
that observation. Gu--Polyanskiy (2023), Guruswami--Radhakrishnan (2016), Bogdanov--Mossel (2011) and
Anantharam et al. (2013) were added as context. Details are in the addendum to `novelty_audit.md`. The decision in
Section 9 is unchanged.
