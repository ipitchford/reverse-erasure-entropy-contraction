# Formula-first novelty audit: reverse erasure and bipartite entropy contraction

Audit checkpoint, 1 November 2026. This records a bounded live literature search and inspected mathematical passages. It is not a certificate that no prior proof exists. The proof manuscript and its correctness checks are separate documents.

## 1. Exact object being audited

Let \(\mu=(\mu_1,\ldots,\mu_n)\) be a strictly positive probability law with \(n\ge2\). A reverse-erasure kernel \(R_\mu\), from \([n]\cup\{e\}\) to \([n]\), has rows

\[
R_\mu(i,\cdot)=\delta_i,\qquad R_\mu(e,\cdot)=\mu.
\]

The reference input is \(\rho_{\mu,a}(i)=a\mu_i\), \(\rho_{\mu,a}(e)=1-a\), where \(0<a<1\); its output is \(\mu\). This is the Bayesian reverse of the usual erasure channel with retention probability \(a\), when the forward input law is \(\mu\). The object is the fixed-reference coefficient

\[
\eta(\rho_{\mu,a},R_\mu)
=\sup_{\nu\ne\rho_{\mu,a}}
\frac{D(\nu R_\mu\Vert\mu)}{D(\nu\Vert\rho_{\mu,a})}.
\tag{A1}
\]

It must not be conflated with a coefficient also maximised over the reference law. The latter is one for this kernel because of its distinct deterministic rows.

The strongest proposed result under audit is **all-retention minimum-mass universality**: with \(q=\min_i\mu_i\),

\[
\eta(\rho_{\mu,a},R_\mu)
=\eta(\rho_{(q,1-q),a},R_{(q,1-q)})
\quad\text{for every }0<a<1.
\tag{A2a}
\]

Thus the coefficient depends on an arbitrary positive finite prior only through its smallest atom. This is an exact reduction to a generally nonuniform binary prior, not a claim that the remaining scalar optimisation always has a closed form. Its proof is recorded in `research/rarest_branch.md` and incorporated into the final manuscript. In the atomic regime, with \(L=\log(1/q)\), the coefficient is explicit:

\[
\eta(\rho_{\mu,a},R_\mu)
=\frac{L}{L-\log a}
\quad\text{for}\quad
0<a\le q^{q/(1-q)}.
\tag{A2}
\]

The proposed equality statement singles out point measures on minimum-mass ordinary symbols, apart from the exceptional uniform binary case at \(a=1/2\). Above this threshold, these point measures cease to be optimal. The final exact decision criterion for all parameters uses only the smallest weight: with \(p=1/c\),

\[
\eta(\rho_{\mu,a},R_\mu)\le c
\quad\Longleftrightarrow\quad
a(qr^p+1-q)+(1-a)r^{pq}\le(qr+1-q)^p
\quad\text{for all }r\ge1.
\tag{A3}
\]

The vertex condition is included by the limit \(r\to\infty\). A stationary-point and second-variation argument first reduces the problem to one distinguished large coordinate. Comparing the resulting two-point power moments at fixed arithmetic and geometric means then proves that the smallest coordinate weight is always most demanding. Consequently (A3) is a single one-variable decision problem, including outside the closed-form regime. Every finite nonconstant sharp dual extremiser singles out a minimum-mass symbol; the full-support primal extremisers inherit this shape. No uniqueness of the scalar optimiser is asserted, and no historical novelty is claimed for the elementary moment-comparison technique by itself.

For two output laws on two disjoint parts, the half-lazy chain stays at its current state with probability \(1/2\), and otherwise samples the other part from its reference law. The proposed consequence is

\[
\eta_{\rm KL}=\frac{L}{2(L+\log2)},
\tag{A4}
\]

where \(q\) is the smallest atom of either part law. Uniform parts of size \(n\) give \(\log n/[2\log(2n)]\), the explicit Caputo--Chen--Gu--Polyanskiy conjecture. Uniform unequal parts yield the same expression with \(n\) replaced by the larger part size. The exact chain convention, the reference law with mass \(1/2\) on each part, and the use of KL divergence are essential identifiers.

## 2. Formula identity: the mean inequality is established prior art

Let \(A_\mu(x)=\sum_i\mu_i x_i\), \(G_\mu(x)=\prod_i x_i^{\mu_i}\), and \(M_{\mu,s}(x)=(\sum_i\mu_i x_i^s)^{1/s}\). The algebraic input is

\[
M_{\mu,1/p}(x)
\ge q^{p-1}A_\mu(x)+(1-q^{p-1})G_\mu(x),
\quad p\ge\frac1{1-q}.
\tag{A5}
\]

Equivalently, after \(x_i=z_i^p\),

\[
A_\mu(z)^p
\ge q^{p-1}A_\mu(z^p)
 +(1-q^{p-1})G_\mu(z)^p.
\tag{A6}
\]

For uniform \(\mu\), multiplying by \(n^p\) gives

\[
\left(\sum_i z_i\right)^p
\ge\sum_i z_i^p+(n^p-n)\left(\prod_i z_i\right)^{p/n},
\quad p\ge\frac n{n-1}.
\tag{A7}
\]

**Prior-art determination: (A5)--(A7), including the full exponent range, are known.** They must not be presented as new inequalities, a new extension to \(p>2\), or a new arbitrary-weight result.

### Gao 2003: the entire range \(p\ge2\)

Peng Gao, *On an inequality of Diananda*, International Journal of Mathematics and Mathematical Sciences 2003, no. 32, 2061--2068, DOI [10.1155/S0161171203210279](https://doi.org/10.1155/S0161171203210279).

Primary manuscript inspected: [VU repository PDF](https://vuir.vu.edu.au/17773/1/AGinequality.pdf), dated 4 November 2002. **Theorem 3.1, equation (3.1)** gives the weighted result for \(r\ge2\). **Equation (3.7)** explicitly rewrites its \(t=1\) case as
\[
A-G\ge\frac{A-M_{1/r}}{1-q^{r-1}}.
\]
Rearrangement with \(r=p\) is exactly (A5). The theorem's equality statement, under its distinct-coordinate convention, allows the two-coordinate boundary configuration and the uniform binary \(r=2\) identity. Thus it also supplies positive nonconstant strictness for \(p\ge2\), except for that identity.

### Gao 2009: the remaining range

Peng Gao, *On an Inequality of Diananda--Part IV*, International Journal of Mathematics and Mathematical Sciences 2009, Article 468290, 24 pages, DOI [10.1155/2009/468290](https://doi.org/10.1155/2009/468290).

Primary passages inspected: [publisher article](https://onlinelibrary.wiley.com/doi/10.1155/2009/468290); [author-uploaded published text](https://www.researchgate.net/publication/220678551_On_an_Inequality_of_Diananda_-_Part_IV); [VU precursor PDF](https://vuir.vu.edu.au/17591/1/AGinequality4rgmia.pdf). The precursor is dated 29 November 2007. The published article records receipt 19 August 2009 and acceptance 2 December 2009; Wiley lists first publication 31 December 2009.

**Theorem 1.2, equation (1.7)** in the published article, **equation (1.4)** in the precursor, states for \(1<r\le2\), \(s\ge1/(1-q)\):
\[
A_\mu(z)^s
\ge q^{(r-1)s/r}M_{\mu,r}(z)^s
+(1-q^{(r-1)s/r})G_\mu(z)^s.
\]
Set \(s=r=p\) to obtain (A6) for \(1/(1-q)\le p\le2\). Combined with Gao 2003, this exhausts the proposed range. Section 2 supplies the proof; its published equations (2.14)--(2.18) are the relevant derivative reduction. Equality at the endpoint should be justified in the manuscript, rather than attributed to an unstated equality clause in this theorem.

### What changes in the proposed application

For finite kernels, entropy variational duality makes \(D(\nu R\Vert\mu)\le cD(\nu\Vert\rho)\) equivalent to
\[
c\log\sum_x\rho_x\exp((Rf)_x/c)
\le\log\sum_i\mu_i e^{f_i}
\quad\text{for all finite }f.
\tag{A8}
\]

For reverse erasure, put \(p=1/c\), \(z_i=e^{f_i}\). Equation (A8) becomes
\[
aA_\mu(z^p)+(1-a)G_\mu(z)^p\le A_\mu(z)^p.
\tag{A9}
\]
The choice \(a=q^{p-1}\) identifies (A9) with (A6). Solving this relation gives \(c=L/(L-\log a)\), and \(p\ge1/(1-q)\) gives \(a\le q^{q/(1-q)}\). A point mass at an atom of mass \(q\) has exactly this divergence ratio.

This is an explicit map between established mean inequalities and the proposed atomic-regime channel theorem. The finite entropy/log-Laplace duality is classical. Its short proof can be included for completeness, but should not itself be an originality claim. The strongest proposed novelty is the all-retention minimum-mass reduction (A2a), supplemented by the sharp general-prior coefficient, its extremisers and threshold, and the bipartite application.

## 3. Reverse-erasure and binary hypercontractivity precedents

### Weinberger--Shayevitz: the same binary reverse channel is explicit

Nir Weinberger and Ofer Shayevitz, *Guessing with a Bit of Help*, Entropy 22(1), 39 (2020), DOI [10.3390/e22010039](https://doi.org/10.3390/e22010039); online publication 26 December 2019. [Full primary text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7516461/).

Inspected **Section 4, equations (89)--(91)**: the authors define the reverse-channel fixed-reference KL coefficient and use it in a guessing bound. **Section 4.1, equation (92)** gives ordinary symbols deterministically preserved and the erasure symbol mapped to \(\operatorname{Ber}(1/2)\), with prior \(((1-\epsilon)/2,\epsilon,(1-\epsilon)/2)\). Their following paragraph describes numerical constrained optimisation and Figure 4 plots the resulting bound. Parameter mapping: our \(a=1-\epsilon\).

This is a direct object collision. The model, its reverse orientation, and the usefulness of its SDPI constant are established. The inspected section does not state the proposed exact formula or general-prior result.

### Nair--Wang 2016: exact theorem and careful endpoint map

Chandra Nair and Yan Nan Wang, *Evaluating hypercontractivity parameters using information measures*, ISIT 2016, pp. 570--574, DOI [10.1109/ISIT.2016.7541363](https://doi.org/10.1109/ISIT.2016.7541363). [Author PDF](https://staff.ie.cuhk.edu.hk/~cnair/pub/papers/HC/BEC.pdf); [institutional publication record](https://research.cuhk.edu.hk/en/publications/evaluating-hypercontractivity-parameters-using-information-measur-2/) lists publication 10 August 2016 and conference 10--15 July 2016.

Let \(X\) be uniform binary and \(Y=\operatorname{BEC}(\epsilon)(X)\). Their **Theorem 1** identifies hypercontractivity with
\[
\frac{D(\nu_X\Vert\mu_X)}{\lambda_1}
+\frac{D(\nu_Y\Vert\mu_Y)}{\lambda_2}
\le D(\nu_{XY}\Vert\mu_{XY}).
\tag{A10}
\]
Theorem 3, on \((\lambda_1-1)(\lambda_2-1)=1-\epsilon\), says hypercontractivity holds exactly when
\[
\epsilon-\tfrac12\le\tfrac32(\lambda_2-1).
\tag{A11}
\]
Theorem 3 and Remark 1 cover the entire correlation boundary for \(\epsilon\le1/2\), and only part for larger erasure.

Here is the endpoint calculation, carried out in this audit rather than quoted from that paper. Choose \(\nu_{XY}=\nu_Y\mu_{X|Y}\). Then \(D(\nu_{XY}\Vert\mu_{XY})=D(\nu_Y\Vert\mu_Y)\), so (A10) implies
\[
D(\nu_X\Vert\mu_X)
\le\frac{\lambda_1(\lambda_2-1)}{\lambda_2}
D(\nu_Y\Vert\mu_Y).
\]
Write \(a=1-\epsilon\), \(\lambda_2=1+t\), \(\lambda_1=1+a/t\). The coefficient becomes \((a+t)/(1+t)\). If \(a\ge1/2\), condition (A11) holds for every \(t>0\); letting \(t\downarrow0\) gives \(\eta\le a\). The local quadratic coefficient is \(a\), giving equality. Therefore
\[
\eta(\rho_{u_2,a},R_{u_2})=a,\qquad a\ge1/2,
\tag{A12}
\]
is already a consequence of Nair--Wang. It is not a new part of the proposed classification. Their correlation-bound theorem does not give the low-retention branch at this endpoint, but that branch is also prior art, as established by Zhao below.

### Zhao 2021: the low-retention uniform binary formula is also known

Yu Zhao, *Generalizations and Applications of Hypercontractivity and Small-Set Expansion*, Carnegie Mellon University doctoral thesis, CMU-CS-21-137, dated 26 August 2021. [Primary thesis PDF](https://www.csd.cs.cmu.edu/sites/default/files/phd-thesis/CMU-CS-21-137.pdf).

**Theorem 3.5.4, printed pages 37--38**, explicitly gives the directed coefficient \(s^*(x;y)=[-\log_2((1-\epsilon)/2)]^{-1}\) for a uniform binary symbol \(y\) and its erased observation \(x\), when \(1/2\le\epsilon<1\). Its proof writes the fixed-reference KL ratio for precisely this reverse kernel; equations (3.4)--(3.8) identify the interior optimisation. Substituting \(a=1-\epsilon\) gives
\[
\eta(\rho_{u_2,a},R_{u_2})
=\frac{\log2}{\log(2/a)},\qquad 0<a\le\frac12.
\tag{A12b}
\]
Theorem 3.2.5 supplies the fixed-reference divergence characterisation; Example 3.5.3 gives the communication application. Hence **the complete uniform binary coefficient is established prior art**: combine Zhao's low-retention branch with Nair--Wang's high-retention branch. The proposed contribution concerns general priors, including nonuniform binary priors, the all-retention dependence on the minimum mass, and the bipartite conjecture. The broader operational bridge is also prior art; its mapping is documented in `research/agreement_application.md`.

### Nair--Wang 2017: “reverse hypercontractivity” is a different reversal

Chandra Nair and Yan Nan Wang, *Reverse hypercontractivity region for the binary erasure channel*, ISIT 2017, pp. 938--942, DOI [10.1109/ISIT.2017.8006666](https://doi.org/10.1109/ISIT.2017.8006666). [Author PDF](https://staff.ie.cuhk.edu.hk/~cnair/pub/papers/HC/revhc-bec.pdf); conference June 2017.

The paper reverses the norm inequality. Its **Theorem 3 / equation (3)** states, for \(\lambda_2<0\),
\[
\lambda_1\le
\frac{\log2}
{\log2-\frac{\lambda_2-1}{\lambda_2}
\log\!\left[(1-\epsilon)2^{1/(\lambda_2-1)}+\epsilon\right]}.
\tag{A13}
\]
**Theorem 1(iii)** is the distinct regime \(\lambda_1<0<\lambda_2<1\). The paragraph before Theorem 3 explicitly leaves this third regime undetermined. Thus the exact-looking formula (A13) is not an exact reverse-channel KL coefficient and cannot be substituted for (A2). The full displayed formula and its parameter domain were inspected, not inferred from the title.

### Recent restatement requiring care

Bao, Dong, Ou and Yao, *Hypercontractivity for Quantum Erasure Channels via Variable Multipartite Log-Sobolev Inequality*, manuscript dated 21 January 2026, [primary CWI PDF](https://ir.cwi.nl/pub/35176/35176.pdf), **Theorems 1.1--1.2** inspected. Their main new theorem concerns quantum erasure tensorisation. The literal all-parameter formulation of their background Theorem 1.1 omits Nair--Wang's restriction and should not be used to infer a classical reverse coefficient for every retention value.

An independent check exhibits the issue. In their norm notation take binary \(f=(1,0)\), retention \(a=0.2\), input exponent \(20.8\), output exponent \(100\). The stated correlation condition holds with equality, but
\[
(0.1+0.8\,2^{-100})^{1/100}>2^{-1/20.8}.
\]
The original Nair--Wang theorem predicts failure in this range. This discrepancy is an audit note, not a claim about the correctness of the later paper's main quantum results.

### Information-bottleneck and privacy-funnel aliases

Shahab Asoodeh and Flavio P. Calmon, *Bottleneck Problems: An Information and Estimation-Theoretic View*, Entropy 22(11), 1325, published 20 November 2020, DOI [10.3390/e22111325](https://doi.org/10.3390/e22111325), [primary text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7712227/). **Lemma 1 and its proof** give a linear bottleneck/privacy-funnel formula when the relevant channel is the forward erasure channel: \(D(Q_Y\Vert P_Y)=(1-\delta)D(Q_X\Vert P_X)\). This is an exact result for the opposite channel orientation. It does not evaluate (A1).

## 4. Explicit open-problem source and known reductions

Pietro Caputo, Zongchen Chen, Yuzhou Gu and Yury Polyanskiy, *Entropy contractions in Markov chains: Half-step, full-step and continuous-time*, Electronic Journal of Probability 30 (2025), DOI [10.1214/25-EJP1372](https://doi.org/10.1214/25-EJP1372); arXiv:2409.07689. Inspected [author-hosted manuscript](https://people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf), printed pages 23--26, and [institutional journal metadata](https://iris.uniroma3.it/handle/11590/525097). The hosted manuscript retains prepublication header placeholders, so its header is not evidence of final publication details.

Example 4.4 states the complete-bipartite coefficient conjecture and point-only equality. Proposition 4.5 proves \(n=3\). **Equations (4.16)--(4.18)** give the point lower bound; **(4.19)--(4.25)** give the entropy decomposition and a three-variable reduction. The proof cites an earlier proposition to restrict fixed-entropy mixtures to a one-large-coordinate family. Therefore the general idea of reducing symmetric distributions to a two-value family is prior art, even if the proposed log-Laplace scalar criterion has a different parameterisation.

No later proof of the exact all-\(n\) statement was located in the inspected results. This is bounded search evidence, not a guarantee that the conjecture remains open everywhere on the search date.

## 5. Claim-by-claim disposition

| Unit | Audit disposition | Appropriate manuscript treatment |
|---|---|---|
| Weighted mean inequality (A5), all admissible exponents | Exact prior-art collision: Gao 2003 plus Gao 2009 | Cite and reuse; a new proof can be labelled a self-contained proof, without historical novelty claim. |
| Entropy/log-Laplace duality (A8) | Classical variational principle | State as a standard lemma; include proof for transparency. |
| Reverse-erasure channel | Explicit binary precedent in Weinberger--Shayevitz; the general Bayesian reversal is standard | Define unambiguously, without model-novelty language. |
| Complete uniform binary coefficient | Exact prior art: Nair--Wang 2016 for \(a\ge1/2\), Zhao 2021, Theorem 3.5.4 for \(a\le1/2\) | Identify the whole binary formula as recovered prior art. |
| All-retention minimum-mass universality (A2a) | No exact matching fixed-reference channel theorem located in the bounded audit | Strongest proposed structural result; distinguish from arbitrary-reference binary-input SDPI reductions and from the known uniform binary coefficient. |
| General-prior exact coefficient (A2) and sharp threshold | No exact information-theoretic collision located | Candidate new application of known mean inequalities; priority remains provisional. |
| Point-only equality and support transition | No exact matching prior result located | Prove completely; retain the binary exception. |
| Single-rarest-branch scalar criterion (A3) for general priors | No exact matching criterion located; moment, stationary-point and second-variation methods are established | Claim the exact channel reduction and rarest-coordinate extremiser consequence, not a new optimisation method. |
| All-\(n\) half-lazy \(K_{n,n}\) coefficient and equality | Explicit conjecture in inspected 2024/25 source, proved there only for \(n=3\) | State as a proof of that precisely identified conjecture, subject to independent correctness review and bounded novelty caveat. |
| Weighted/unequal-part bipartite extension (A4) | No exact collision located | A generalisation strengthening the channel application, without claiming this graph family is the most important open problem in mathematics. |

The strongest defensible positioning is all-retention minimum-mass universality for a fixed-reference channel, a sharp general-prior phase transition, and resolution of a stated finite-chain conjecture. The closed-form regime uses an explicit bridge to known mean inequalities. Originality of that algebraic inequality and of the complete uniform binary coefficient is disproved by this audit. No general duality, operational communication principle, or proof technique is being advertised as new.

## 6. Search log and limits

Searches used two live web indexes, with source inspection when results were close. Formula searches were rerun after the initial uniform channel simplified to a weighted mean inequality, after generalisation to arbitrary priors, and after the final minimum-mass reduction. The last rerun and its fixed-arithmetic/geometric-mean aliases are recorded in `research/rarest_branch.md`. The following are representative exact queries actually issued; the search did not exhaust every citation graph or every unpublished manuscript.

### Channel identity and direction

- `"reverse erasure" "relative entropy"`
- `"reverse erasure" "contraction"`
- `"reverse erasure channel" "contraction"`
- `"erasure channel" "reverse" "strong data processing"`
- `"erasure" "reverse channel" SDPI exact`
- `"erasure" "adjoint" "entropy" channel`
- `"erasure" "adjoint" "contraction" entropy`
- `"erasure" "Bayesian inverse" entropy`
- `"reverse" "erasure" "SDPI constant"`
- `"erasure" "q-ary" "reverse" "entropy"`
- `"hypercontractivity" "erasure" "q-ary"`
- `"erasure" "s*" "Anantharam" reverse`

Additional information-bottleneck alias queries:

- "information bottleneck" "erasure" "reverse"
- "bottleneck" "reverse erasure"
- "erasure" "information bottleneck" "ternary"
- "erasure" "privacy funnel" "contraction"

### Arbitrary-prior and formula aliases

- `"minimum probability" "reverse erasure" contraction`
- `"erasure" "minimum mass" entropy contraction`
- `"erasure" "minimum probability" "contraction"`
- `"reverse erasure" "nonuniform"`
- `"erasure channel" "reverse" "non-uniform"`
- `"erasure" "SDPI" "nonuniform"`
- `"q^{q/(1-q)}" erasure`
- `"q^{q/(1-q)}" inequality`
- `"q^(q/(1-q))" inequality`
- `"erasure" "log(1/q)"`
- `"erasure" "log(1/p)" "contraction"`
- `"erasure" "contraction coefficient" "log(1"`
- `"erasure" "entropy contraction" "singleton"`

### Mean-inequality identity and possible bridge

- `"Gao" "2009" "Diananda" "1/2"`
- `"Diananda" "1/r-1"`
- `"M_{n,r}" "q^{1/r-1}"`
- `"Gao" "n/(n-1)" inequality`
- `"(n^p-n)" inequality`
- `"n^p - n" inequality geometric`
- `"inequality" "(n^r-n)"`
- `"reverse erasure" "Gao"`
- `"Diananda" "entropy"`
- `"Diananda" "Markov"`
- `"Diananda" "strong data processing"`
- `"Caputo" "Diananda"`
- `"erasure" "power means"`

### Target conjecture and possible later resolution

- `"Caputo" "complete bipartite" "entropy" conjecture`
- `"complete bipartite" "entropy contraction" conjecture proof`
- `"complete bipartite" "strong data processing"`
- `"complete bipartite" "relative entropy" contraction`
- `"K_{n,n}" "entropy" "log"`
- `"log(2n)" "Caputo" entropy`
- `"log n" "log(2n)" "entropy" contraction`
- `"Entropy Contractions in Markov Chains" "conjecture"`
- `site:github.com/openai/math "bipartite" entropy`
- `site:sites.pitt.edu/~hajlasz/OpenAI_Math_Catalogue.html "bipartite"`

Other near matches included forward erasure contraction, privacy-utility functions, quantum erasure inequalities, degree-based graph entropy and continuous-time mixing. These differ in kernel orientation, reference measure, quantity, or time convention. Search snippets alone were not treated as evidence of an exact mathematical collision.

Access limitations included failed direct retrievals of the Hindawi PDF host, Project Euclid's article body, some arXiv HTML endpoints, and one NSF-hosted privacy article. Accessible author manuscripts or author-uploaded full text were used where available. The complete OpenAI mathematics catalogue was not downloaded or exhaustively checked. New results, alternative notation, poorly indexed publications, theses and unpublished proofs remain possible omissions. The appropriate confidence statement is: **exact collisions were found for the weighted mean inequality and uniform binary coefficient; no exact all-prior/all-retention channel theorem or all-\(n\) bipartite proof was found in this bounded search. Independent specialist literature review is still needed before asserting priority.**

# Final structural simplification audit: Gao 2018

The exact all-retention minimum-mass reduction and its proof are recorded in `research/rarest_branch.md`. Gao's *Some extensions of Diananda's inequality*, arXiv:1807.06290v1 (17 July 2018), was checked in full primary HTML, especially Theorem 1.1 and Section 2, equations (2.1)–(2.5): https://arxiv.org/html/1807.06290v1. It extends exponent ranges for fixed endpoint coefficients, using power-mean reduction, rather than proving the free-coefficient binary reduction. The detailed object comparison and additional query record are in the rarest-branch checkpoint. The standalone moment monotonicity technique is not claimed historically new.


# Addendum, 3 November 2026 (revision round)

Internal AI-assisted review of the 1 November manuscript identified works that this audit had missed. None of them
contains the minimum-atom reduction or an all-n proof of the bipartite conjecture; all are now cited in the paper.

- **Jadhav, arXiv:2606.27073v1 (25 June 2026).** Proposition 9.5 computes the point-mass value for the lazy star on n
  vertices and Remark 9.6 reports numerical evidence (tested up to n = 50) that point masses are optimal, explicitly
  "not an analytic proof". The star is K_{1,N}, N = n - 1, in the rank-one bipartite family, so Theorem 6.1 of the
  revised paper settles it (Corollary 6.2). This was a gap in the 2025-26 search for work on the same quantity.
- **Gu and Polyanskiy, Comm. Math. Phys. 404 (2023), doi:10.1007/s00220-023-04851-1.** Their Prop. 17 is the primal
  one-large-coordinate reduction that Caputo et al. use for n = 3; Lemma 3.2 is its dual counterpart.
- **Guruswami and Radhakrishnan, CCC 2016, doi:10.4230/LIPIcs.CCC.2016.6, and Bogdanov and Mossel, IEEE Trans. Inf.
  Theory 57 (2011), doi:10.1109/TIT.2011.2134067.** Origin of the agreement-distillation problem. Their model uses
  constant success probability; the paper's corollary uses vanishing error.
- **Anantharam, Gohari, Kamath and Nair, arXiv:1304.6133.** Hypercontractivity dictionary (eta = s*).
- **Numbering.** Caputo et al. arXiv:2409.07689v1 numbers the bipartite items Example 28 / Proposition 29; the authors'
  manuscript numbers them Example 4.4 / Proposition 4.5 (see `refs_records/ccgp_numbering_check.md`).

Raw bibliographic records for every reference are in `refs_records/`.
