# Proof digest: reverse erasure, minimum probability and bipartite entropy contraction

**Track I — informal mathematical review. Review date: 1 November 2026.**

> **Revision note (3 November 2026).** This digest reviews the manuscript of 1 November 2026; its section, theorem and equation numbers refer to that version (for example, its Theorem 2.1 is now Theorem 2.3 with Proposition 2.4, and its Section 8 diagnostics are now Appendix C). Its exposition rubric has been removed from the public package. The mathematical content it checks is unchanged in the revision.


**No proof-assistant verification was performed.** I inspected the analytic proofs, re-derived their load-bearing identities, checked the recorded numerical coverage and independently recalculated four disclosed high-precision witnesses. I found no unresolved mathematical gap in the stated finite-channel, bipartite-chain or agreement-distillation arguments. This is a bounded internal assessment, not an external peer-review decision or a guarantee of correctness or novelty.

This reviewer helped develop the earlier uniform-channel proof and arbitrary-prior scalar reduction. Consequently, this digest must not be described as an independent review of the entire discovery. The final minimum-probability comparison and communication construction were developed elsewhere in the team; I re-derived those steps during this review. A separate editorial review was produced during development; it is not part of this public package.

## 1. Evidence boundary and preservation

The target is `manuscript.tex`, titled *Entropy contraction for reverse erasure: a minimum-probability reduction and a bipartite conjecture*. I read its definitions, four theorems, four lemmas, communication corollary, computational-specification remark, nine proof environments, two appendices and bibliography. The review includes the final definition of a dual extremiser before Theorem 2.1, the Section 7 clarification that communication entropy and mutual information are measured in bits, the use of output-label length and the explicit absence of a secrecy requirement.

The source was not edited by this reviewer. An inspected snapshot had SHA-256:

```text
b524900ea08d46181aa91ee97fc8eff928902dc1cfb28d052c6ea6d04a63eb11
```

The final bundle manifest should identify the delivered version if subsequent citation or layout edits change this hash. A matching hash establishes byte identity, not mathematical validity.

I also inspected:

- `research/entropy_draft.md`, the preserved earlier working proof;
- `research/validate_entropy.py` and `research/validation_results.json`;
- `verification/verify_minimum_mass.py` and `verification/minimum_mass_results.json`;
- the exact formula figure's caption and its connection to the stated theorems. Visual PDF production and page-layout inspection remain the root agent's responsibility.

The numerical scripts were read before assessing their outputs. Their instructions, comments and output verdicts were treated as evidence to inspect. No new broad numerical sweep was run during this digest, in accordance with the review scope. No Lean, Rocq or Isabelle files were supplied; formal compilation, axiom inspection and formal refactoring are therefore not applicable.

## 2. Statement and idea

Let \(\rho\) be a positive probability distribution on a finite alphabet with at least two symbols, let \(q=\min_i\rho_i\), and let \(0<\alpha<1\). The reverse-erasure channel preserves an observed ordinary symbol and replaces the erasure symbol by a fresh draw from \(\rho\). Its input reference law is \((\alpha\rho,1-\alpha)\).

The central structural theorem states that its fixed-reference Kullback–Leibler contraction coefficient depends on the entire prior only through its smallest atom:

\[
\eta(\rho,\alpha)=\eta((q,1-q),\alpha).
\]

For \(p=1/c>1\), the assertion \(\eta\le c\) is equivalent to the single scalar inequality

\[
\frac{\alpha(qr^p+1-q)+(1-\alpha)r^{pq}}
{(qr+1-q)^p}\le1
\qquad\text{for every }r\in[1,\infty].
\]

The coefficient has the closed form

\[
\eta(\rho,\alpha)=
\frac{\log(1/q)}{\log(1/(\alpha q))}
\quad\text{when}\quad
\alpha\le q^{q/(1-q)}.
\]

That threshold is sharp for point optimality. Above it, except for the uniform binary prior, extremisers have full support and distinguish a smallest atom. The manuscript does not claim a closed elementary formula or a unique scalar extremiser in that remaining regime.

The proof's idea is to replace a relative-entropy optimisation by a weighted power-and-geometric-mean inequality. An interior maximum of that inequality has only two coordinate values; a second-derivative argument allows the larger value at only one coordinate. The important additional step holds the arithmetic and geometric means fixed while moving the large coordinate to a smaller prior weight. Its power moment increases, so a smallest atom determines the worst case. Gao's classical mean inequality then supplies the exact point-optimal regime. An \(\epsilon\log\epsilon\) perturbation shows exactly where that regime ends.

The graph application splits an arbitrary input between the two parts, applies the full reverse-erasure estimate to the heavier part and a midpoint estimate to the lighter part. This yields

\[
\eta_{\mathrm{KL}}(\pi,P)=
\frac{\log(1/q)}{2\log(2/q)}.
\]

For uniform part sizes \(m,n\), this is \(\log M/[2\log(2M)]\), \(M=\max(m,n)\), resolving the stated conjecture for \(K_{n,n}\). The covered weighted graphs have rank-one cross weights. They are not arbitrary weighted bipartite graphs.

## 3. Ordered proof map and dependencies

| Step | Mathematical content | Manuscript location | Role |
|---|---|---|---|
| 1 | Use the entropy variational formula to convert the fixed-reference contraction bound into an exponential-moment inequality. | Lemma 3.1, finite variational duality | Standard |
| 2 | On the weighted simplex, stationary coordinates solve the same strictly convex scalar equation; a weighted transfer direction rules out two large coordinates. | Lemma 3.2, one large coordinate | Load-bearing reduction |
| 3 | At fixed arithmetic and geometric means, the power moment strictly decreases as the prior weight of the large coordinate increases. | Lemma 3.3, comparison at fixed means | Main structural step |
| 4 | Replace the distinguished weight by the smallest atom and identify the resulting scalar criterion with the binary-prior criterion. | Proof of Theorem 2.1 | Main structural conclusion |
| 5 | Translate Gao's weighted mean inequality, prove its equality cases and obtain the exact coefficient below the threshold. | Lemma 4.1 and Theorem 2.2 | Classical ingredient; channel consequence |
| 6 | Add a small erasure mass to a smallest-atom point input. Its \(\epsilon\log\epsilon\) term changes sign at precisely the proposed threshold. | End of Theorem 2.2 proof | Sharpness argument |
| 7 | Compute the local coefficient, use a cubic perturbation to separate it from the global coefficient, and use compactness plus entropy duality to obtain and describe supercritical extremisers. | Theorem 2.3 proof | Structural classification |
| 8 | Apply the channel bounds to heavy and light graph parts, then audit equality and binary exceptions. | Theorem 6.1 and Section 6.1 | Conjecture resolution and extension |
| 9 | Apply standard tensorisation and Fano's inequality for the communication converse; use rare-event tables and buckets for achievability. | Corollary 7.1; Appendix B | Operational consequence |

The dependency graph is shallow. The entropy duality lemma supports the two main channel arguments. The extremiser-shape and fixed-means lemmas yield the all-retention reduction and also shorten the self-contained Gao proof. The phase theorem supplies the graph theorem and the communication achievability constant. The local analysis is needed for attainment above the threshold, rather than being an unnecessary auxiliary result. The two appendices supply actual equality and tensorisation arguments used in the main text.

## 4. Re-derived inferences and fragile points

### 4.1 The fixed-means derivative

This is the inference on which the final all-retention minimum-probability theorem most strongly depends. I re-derived it from the two constraints rather than accepting the displayed expression.

For \((1-w)a+wb=1\), \(a^{1-w}b^w=g\) and \(r=b/a>1\), set

\[
U=(1-w)a'/a,\qquad V=wb'/a.
\]

Differentiating the arithmetic and logarithmic geometric constraints gives

\[
U+V=-(r-1),\qquad U+V/r=-\log r.
\]

Thus

\[
U=\frac{r-1-r\log r}{r-1},\qquad
V=\frac{r(\log r-r+1)}{r-1}.
\]

Substitution into the derivative of \((1-w)a^p+wb^p\) gives exactly the manuscript's bracket

\[
\frac{a^p}{r-1}
\left[p\log r(r^p-r)-(p-1)(r-1)(r^p-1)\right].
\]

For its sign, put \(I_1=\int_1^r t^{p-1}\,dt\) and \(I_0=\int_1^r t^{p-2}\,dt\). Positive covariance of \(t\) and \(t^{p-1}\) under the probability measure proportional to \(dt/t\) proves

\[
\frac{I_1}{I_0}>\frac{r-1}{\log r}>
\frac{r\log r}{r-1}.
\]

The second strict inequality follows from the logarithmic mean exceeding \(\sqrt r\). This proves the displayed derivative is strictly negative for every \(p>1,r>1\). No finite parameter grid is needed for this conclusion.

### 4.2 Boundary and equality handling

The boundary product is zero, so strict convexity of the weighted power sum leaves only vertices as boundary maximisers. At an interior two-value critical point, the relation \(T=\lambda y-y^p\), together with the strict secant bound \(\lambda<py^{p-1}\), gives the positive transfer Hessian that rules out a repeated high value. Both arguments respect the weighted constraint, rather than silently assuming equal weights.

The self-contained mean proof uses \(N=1/q\), which need not be an integer. Its integral comparisons work for every real \(N\ge2\); no combinatorial argument depends on an integer number of equal-weight coordinates. Strictness fails only at \(N=p=2\), precisely the uniform binary exception carried through the channel and graph statements.

The entropy equality argument correctly distinguishes a full-support output, where the finite entropy optimiser can be used, from a zero-erasure input, where a separate monotonicity argument applies. This avoids treating a boundary point as though a finite exponential tilt produced it.

### 4.3 Attainment and the local expansion

The local variance computation gives an upper bound as well as an attaining perturbation. Uniform second-order expansion on a finite-dimensional sphere therefore controls every sequence approaching the reference. The cubic expansion produces a ratio strictly greater than \(\alpha\) except for the uniform binary prior. Above the point threshold, an extremiser can approach neither the reference nor a zero-erasure law with the optimal value. Compactness then gives attainment, and equality in the finite variational formula forces full input support.

The strict \(\eta<1\) assertion uses the equality condition for ordinary data processing and the local bound \(\alpha<1\). It does not infer a uniform strict contraction merely from pointwise strictness on a noncompact punctured simplex.

### 4.4 The graph decomposition

The half-lazy convention is used consistently. For an input with mass \(t\) on one part, one step makes both part masses \(1/2\). The two conditional output laws are exactly the mixtures displayed in the proof. The light-part estimate assigns no extra binary-divergence term, so the heavy-part binary divergence is counted once. This is the key reason the coefficient is half the reverse-erasure coefficient.

The singleton part convention and the separate \(K_{1,1}\) case are correct. The binary equality families in Section 6.1 follow from the reverse-erasure equality family and strict convexity of the light-part mixture. Restricting the uniqueness claim to \(q<1/2\) is necessary.

### 4.5 Communication and units

I checked the converse with conditional-law strong data processing, product tensorisation and Fano's inequality. Section 7 now explicitly measures \(H\) and \(I\) in bits, resolving the potential factor-of-\(\log2\) ambiguity caused by the manuscript's otherwise natural-log convention.

For achievability, selecting the first table with exactly one Alice event preserves uniformity of its index. Conditional on that event and its selected index, every other block in the selected table is conditioned on the corresponding Alice event failing. Earlier rejected tables are independent of the selected table. Therefore the displayed bound \((p_B-p_A)/(1-p_A)\le2p_B\) and the bucket union bound are valid. The protocol discloses both the exponential sample count and the absence of a secrecy requirement. Its claimed efficiency is a communication rate in the specified unlimited-sample model.

## 5. Claim and check ledger

| Claim | Check performed | Status and residual limitation |
|---|---|---|
| Entropy duality is equivalent to the proposed mean inequality. | Re-derived both suprema, including finite-function limits at zero output probabilities. | Passed informal inspection. |
| Every nonconstant interior maximum has one large coordinate. | Re-derived stationary equation and weighted transfer Hessian. | Passed informal inspection for all stated \(p>1\). |
| The large coordinate has minimum prior weight. | Independently derived fixed-means derivative and strict sign. | Passed informal inspection; historical priority of this extremal technique remains a literature question. |
| The contraction coefficient depends only on \(q\). | Checked feasibility of replacing a high-coordinate weight by \(q\), scalar boundary and binary lift. | Passed informal inspection. |
| Closed formula holds through the phase boundary. | Checked exponent conversion, classical Gao mapping and analytic scalar proof. | Passed; the underlying mean inequality is prior work. |
| Point optimality fails immediately above the boundary. | Re-derived the \(\epsilon\log\epsilon\) coefficient; independently recalculated four witnesses. | Passed analytic inspection and disclosed finite arithmetic checks. |
| Above-threshold extremisers have full support and the stated form. | Checked local bound, cubic separation, compactness, finite variational equality and output consistency. | Passed informal inspection; scalar uniqueness is not proved or claimed. |
| Weighted reset graph coefficient and equality classification. | Checked original transition rule, divergence decomposition and binary/singleton cases. | Passed; applies to rank-one cross weights only. |
| Synchronous product coefficient is the maximum factor coefficient. | Checked conditional KL chain rules and mixture convexity in Appendix B. | Passed; standard tensorisation, not a novel claim. |
| Communication rate is exact in the stated model. | Checked bit convention, converse, conditional uniformity, bucket decoding and sample count. | Passed informal inspection; not a secrecy or sample-efficiency result. |
| Recorded numerical coverage matches manuscript. | Independently summed JSON input counts and inspected script loops. | Passed: 389,038 baseline inequality inputs; separate new-reduction diagnostics disclosed below. |
| No earlier general-prior theorem or all-size graph solution exists. | Inspected decisive sources and the stated bounded-search language. | Not established as a universal historical claim. Specialist and broader prior-art review remain necessary. |

## 6. Verification record and reproduction boundary

Working directory: `/workspace/scratch/1be855dcac62`.

The recorded environment is Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0; seed 20261101. The baseline script's recorded runtime is about 0.394 seconds. The minimum-probability diagnostics record about 0.053 seconds. These are recorded execution timings, not independent performance measurements by this digest reviewer.

| Check | Command or evidence | Review status |
|---|---|---|
| Baseline diagnostic suite | `python research/validate_entropy.py` | Existing source and output inspected; full suite not rerun during this review, as requested. |
| Minimum-probability diagnostic suite | `python entropy_contraction/verification/verify_minimum_mass.py` | Existing source and output inspected; full suite not rerun during this review. |
| Minimum-probability script identity | SHA-256 of `verify_minimum_mass.py` compared with `source_sha256` in its JSON | Passed; recorded hash matches the inspected script. |
| Baseline coverage arithmetic | Sum each case's `samples` in the recorded JSON | Passed: 88,736 + 126,000 + 108,218 + 66,084 = 389,038. |
| Four boundary witnesses | Independently form input/output probability vectors and sum KL terms with 100-digit `decimal.Decimal` arithmetic | Passed earlier in this session; exit status 0. Exact elapsed time was not separately instrumented. |
| Proof-assistant verification | No formal source supplied | Not applicable; no machine proof certificate. |
| New broad numerical testing | None | Not run, by the requested review scope. |
| Original manuscript changes by this reviewer | None | Preserved. This digest is a separate artefact. |

The baseline coverage consists of eleven complete-bipartite parameter pairs; 28 uniform mean-inequality cases; eighteen uniform reverse-erasure cases; and weighted channel/graph cases using four disclosed priors. Five small graph matrices use exact rational arithmetic for stochasticity, stationarity and detailed balance. The floating-point inequality checks use the stated residual tolerances, not exact universal arithmetic. There are also 202 binary endpoint identities and four 120-digit witness records.

The separate minimum-probability script records 256 branch-envelope parameter choices, 749 finite log-ratio grid points and 383,488 branch evaluations, plus the constant and vertex limits. Its fixed-arithmetic/geometric-mean check uses 128 weight/mean choices at seven exponents, giving 896 comparisons. The exponents are 1.001, 1.05, 1.5, 2, 5, 20 and 100. The reported maximum arithmetic and geometric log-constraint errors are approximately \(9.68\times10^{-15}\) and \(2.83\times10^{-13}\), within its \(5\times10^{-12}\) tolerance. A sampled envelope is not a global maximisation certificate; the script and manuscript say so explicitly.

The independent witness calculation used probability vectors, rather than copying the suite's scalar expression:

```python
from decimal import Decimal as D, localcontext

with localcontext() as ctx:
    ctx.prec = 100
    # n, alpha and epsilon are the disclosed decimal witness parameters.
    p = [1-epsilon] + [D(0)]*(n-1) + [epsilon]
    reference = [alpha/D(n)]*n + [1-alpha]
    output = [p[i] + epsilon/D(n) for i in range(n)]
    din = sum(x*(x/y).ln() for x, y in zip(p, reference) if x)
    dout = sum(x*(D(n)*x).ln() for x in output if x)
    ratio = dout/din
```

The recalculated improvements over the point ratio were:

| Uniform alphabet size | Retention | Erasure mass | Improvement |
|---:|---:|---:|---:|
| 3 | 0.7 | \(10^{-3}\) | \(1.070884937840142\times10^{-4}\) |
| 3 | 0.8 | \(10^{-3}\) | \(2.504966071271334\times10^{-4}\) |
| 4 | 0.8 | \(10^{-4}\) | \(6.044297601833167\times10^{-6}\) |
| 10 | 0.9 | \(10^{-15}\) | \(1.133318641052913\times10^{-17}\) |

All four ratios agreed with the recorded 120-digit outputs within \(8\times10^{-100}\). These are explicit lower-bound witnesses, not claimed optimal supercritical inputs. An initial attempt to use `mpmath` was unavailable in this Python environment; the standard-library Decimal calculation completed the check without an installation or environment change.

## 7. Prior work and proposed contribution boundary

I directly inspected the motivating Caputo et al. author manuscript, Gao's 2007 precursor for the 2009 article, the 2002 precursor for the 2003 article, Nair–Wang's author manuscript, the relevant Zhao thesis theorem and the Weinberger–Shayevitz full text. These sources support the manuscript's separation between established mean/binary results and proposed general-prior consequences. This digest did not repeat the full team search for every possible alias; the separate novelty audit records that broader corpus.

The source attribution is materially important. Gao's two papers already supply the weighted mean inequality over the necessary exponent ranges. Zhao's Theorem 3.5.4 explicitly supplies the low-retention uniform-binary coefficient, while Nair–Wang covers the corresponding high-retention behaviour through binary-erasure hypercontractivity. Consequently, neither the mean inequality nor the full uniform-binary coefficient should be advertised as a discovery of this manuscript. Caputo et al.'s all-size complete-bipartite conjecture is a distinct target, and the general-prior fixed-reference reduction is a distinct statement from binary-input results that also optimise the reference law.

The most useful proposed reusable component is the minimum-probability reduction and its strict extremiser-location conclusion. The sharp arbitrary-prior phase threshold and the weighted graph theorem follow from that framework and a classical inequality. The communication result is an operational consequence in an explicitly specified model, with a direct construction and a disclosed exponential sample cost. Whether these contribution units have earlier exact statements remains bounded by the documented search, not settled by a failed keyword search.

## 8. Remaining obligations and presentation suggestions

No unresolved central inference was identified in this inspection. The following limits remain:

1. **External verification and priority.** A specialist should review the general-prior reduction and search the older extremal-mean and hypercontractivity literature for exact earlier statements. This internal digest cannot settle historical priority.
2. **Formal verification.** The unrestricted theorems have prose proofs. No proof assistant has checked the definitions, quantifiers or reductions.
3. **Supercritical evaluation.** The manuscript gives an exact global scalar criterion and extremiser shape, rather than a closed formula or a uniqueness theorem. That distinction should survive the abstract, release summary and any figure captions.
4. **Numerical certification.** Neither recorded script rigorously certifies a global floating-point optimum. The analytic proofs carry the claims; the tests check implementation consistency and selected identities.
5. **Optional exposition.** Two lines giving the differentiated mean constraints would make Lemma 3.3 easier to verify. A short first-page explanation of why the heavier graph part receives the full estimate would also help readers approaching from Markov-chain theory. Neither change requires new mathematics.

## 9. Completion record

| Requirement | Status | Evidence or limit |
|---|---|---|
| Track, target and intended scope | Completed | Informal track; finite reverse-erasure and graph theorems; operational corollary. |
| Scope of this digest | Completed | Proof analysis only; the separate editorial review is not part of the public package. |
| Originals preserved and inspection boundary recorded | Completed | No source edits; snapshot hash and inspected files listed. |
| Scripts inspected before assessment/execution | Completed | Both numerical script sources read; independent witness calculation disclosed. |
| Baseline reproduction and environment | Completed with limits | Existing outputs and counts checked; full suites intentionally not rerun; environment and recorded runtimes listed. |
| Assumptions and load-bearing inferences | Completed | Sections 2–5 of this digest. |
| Finite evidence distinguished from analytic proofs | Completed | Explicit throughout verification record and ledger. |
| Actual independence described | Completed | Reviewer contribution to original development disclosed at the start. |
| Formal statement/prose comparison | Not applicable | No formal development supplied. |
| Formal edits, admissions and axiom audit | Not applicable | No formal source or edits. |
| Outline, prior-work boundary and citations | Completed | Sections 2–3 and 7; grouped references below. |
| Before/after refactoring metrics | Not applicable | This review preserves the source; no shortening or refactoring requested. |
| Reproduction evidence and remaining obligations | Completed | Sections 6 and 8. |
| Bounded conclusion and sanity checks | Completed | Opening status and final checks below. |

## 10. Concrete sanity checks and bounded conclusion

For \(K_{1,1}\), one step is exactly stationary and the coefficient is zero. For \(K_{2,2}\), the formula gives \(1/4\), and the nonpoint equality family is necessary. For \(K_{3,3}\), the coefficient is approximately 0.3065735964, agreeing with the source's established first case. As the smallest conditional mass tends to zero, the graph coefficient tends to \(1/2\), while the local coefficient remains \(1/4\). All four checks match the stated conventions.

The strongest conclusion supported by this digest is that the inspected manuscript contains a coherent, apparently complete analytic argument for its stated finite-channel theorem, sharp threshold, weighted bipartite consequence and communication corollary. The min-mass comparison has been explicitly re-derived, the subtle equality exceptions have been retained, and the numerical records agree with their disclosed scopes. The remaining uncertainty concerns external mathematical scrutiny and priority; the numerical checks do not remove either uncertainty.

## Grouped references

### Motivating conjecture

Caputo, P., Chen, Z., Gu, Y., & Polyanskiy, Y. (2025). Entropy contractions in Markov chains: Half-step, full-step and continuous-time. *Electronic Journal of Probability, 30*, 1–29. https://doi.org/10.1214/25-EJP1372 . Inspected author manuscript: https://people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf

### Classical mean inequalities

Gao, P. (2003). On an inequality of Diananda. *International Journal of Mathematics and Mathematical Sciences*, vol. 2003, no. 32, 2061–2068. https://doi.org/10.1155/S0161171203210279 . Inspected precursor: https://vuir.vu.edu.au/17773/1/AGinequality.pdf

Gao, P. (2009). On an inequality of Diananda—Part IV. *International Journal of Mathematics and Mathematical Sciences, 2009*, Article 468290. https://doi.org/10.1155/2009/468290 . Inspected precursor: https://rgmia.org/papers/v10n4/AGinequality4rgmia.pdf

### Reverse binary erasure and information theory

Nair, C., & Wang, Y. N. (2016). Evaluating hypercontractivity parameters using information measures. In *2016 IEEE International Symposium on Information Theory* (pp. 570–574). https://doi.org/10.1109/ISIT.2016.7541363 . Inspected author manuscript: https://staff.ie.cuhk.edu.hk/~cnair/pub/papers/HC/BEC.pdf

Weinberger, N., & Shayevitz, O. (2020). Guessing with a bit of help. *Entropy, 22*(1), Article 39. https://doi.org/10.3390/e22010039 . Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC7516461/

Zhao, Y. (2021). *Generalizations and applications of hypercontractivity and small-set expansion* [Doctoral dissertation, Carnegie Mellon University]. CMU-CS-21-137. https://www.csd.cs.cmu.edu/sites/default/files/phd-thesis/CMU-CS-21-137.pdf

