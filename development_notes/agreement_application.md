# Operational application: agreement from an erased source

Independent source audit and derivation, 1 November 2026.

## 1. Precise corollary suitable for the manuscript

Let \(\mu\) be a positive probability distribution on a finite alphabet with at least two symbols, let \(q=\min_x\mu(x)\), and fix

\[
0<\alpha\le q^{q/(1-q)}.
\]

Generate independent pairs \((E_i,X_i)\), where \(X_i\sim\mu\) and \(E_i=X_i\) with probability \(\alpha\), while \(E_i=*\) otherwise. Erasure decisions are independent of the symbols and of one another. Alice observes \(E^N\), Bob observes \(X^N\), and there is no additional shared randomness.

Alice must produce \(K\in\{0,1\}^k\cup\{\bot\}\), determined by her observation, and send one message of at most \(\ell\) bits to Bob. Bob produces \(\widehat K\) from his observation and the message. We count agreement only when \(K=\widehat K\ne\bot\). Require that \(K\), conditional on \(K\ne\bot\), is exactly uniform on \(\{0,1\}^k\). The sample count \(N\) may depend on \(k\), without an imposed rate or computational constraint.

For protocols with vanishing failure and disagreement, the sharp asymptotic communication cost per output bit is

\[
\boxed{
R_*(\mu,\alpha)
=1-\eta_{\rm KL}(\pi,R_{\mu,\alpha})
=\frac{\log(1/\alpha)}{\log(1/(\alpha q))}.
}\tag{1}
\]

More precisely:

* Every sequence of protocols with agreement probability tending to one satisfies
  \(\liminf_{k\to\infty}\ell_k/k\ge R_*\).
* There are deterministic one-way protocols with
  \(\ell_k=R_*k+O_{\alpha,q}(\log k)\), exactly uniform output conditional on nonfailure, and agreement probability at least \(1-2/k^2\) for all sufficiently large \(k\).
* The explicit protocol below uses \(N_k=O_{\alpha,q}(k2^k\log k)\) source samples. This is a communication-rate result with unlimited source samples; it is not a claim of sample or computational efficiency.

The converse also holds under the weaker requirement that agreement probability stay bounded below by a fixed positive constant, using the established hypercontractive converse in Section 3.2. The vanishing-error result has the self-contained proof in Section 3.1 and Section 4.

For a uniform alphabet of size \(n\), the range and rate become

\[
\alpha\le n^{-1/(n-1)},
\qquad
R_* = \frac{\log(1/\alpha)}{\log(n/\alpha)}.
\]

In particular, when \(\alpha=1/2\),

\[
R_* = \frac{\log2}{\log(2n)}.
\]

The output is common randomness, with no secrecy requirement: the communication may reveal part of it. The direction matters: Alice sees the erased source and Bob sees the original source.

## 2. Prior-art status and source mapping

This corollary applies an established operational connection to the new coefficient calculation. It should not be presented as a new general principle relating contraction and communication.

### Zhao 2021: exact binary antecedent and general formulation

Yu Zhao, *Generalizations and Applications of Hypercontractivity and Small-Set Expansion*, Carnegie Mellon University PhD thesis, CMU-CS-21-137, 26 August 2021.

Primary full text:

https://www.csd.cs.cmu.edu/sites/default/files/phd-thesis/CMU-CS-21-137.pdf

Inspected statements:

* Chapter 3, pp. 23–25, specifies arbitrary finite joint sources, one-way communication, uniform output conditional on a failure symbol, and unrestricted sample count.
* Theorems 3.1.1 and 3.1.2 identify the constant-success asymptotic rate with one minus the appropriate directed contraction coefficient.
* Theorem 3.2.5 gives the fixed-reference KL-divergence characterization.
* Theorem 3.5.4, pp. 37–38, already computes the **uniform binary** reverse-erasure coefficient \(\log2/\log(2/\alpha)\) for \(\alpha\le1/2\). Corollary 3.1.3 states its communication consequence.

Thus the binary special case of (1) is known. The new content here is the nonbinary/arbitrary-prior evaluation and its explicit parameter range. The construction in Section 4 below is a direct specialisation of the rare-event indexing idea, with an elementary amplification that makes failure vanish.

### Guruswami–Radhakrishnan 2016: the communication converse

Venkatesan Guruswami and Jaikumar Radhakrishnan, *Tight Bounds for Communication-Assisted Agreement Distillation*, CCC 2016, LIPIcs 50, 6:1–6:17.

DOI and primary full text:

https://doi.org/10.4230/LIPIcs.CCC.2016.6

https://drops.dagstuhl.de/storage/00lipics/lipics-vol050-ccc2016/LIPIcs.CCC.2016.6/LIPIcs.CCC.2016.6.pdf

Section 4, Claim 4.2 and equation (15), bound agreement using the number of transcripts and conditional probabilities of Alice's output. Section 4.1, equations (16) and the displayed inequality immediately after it, give the general bound for any hypercontractive source. These arguments require no binary alphabet. The proof below fixes the direction explicitly rather than relying on source-dependent variable names.

### Anantharam–Gohari–Kamath–Nair 2013: contraction equals boundary slope

Venkat Anantharam, Amin Gohari, Sudeep Kamath and Chandra Nair, *On Maximal Correlation, Hypercontractivity, and the Data Processing Inequality studied by Erkip and Cover*, arXiv:1304.6133.

Primary full text:

https://arxiv.org/pdf/1304.6133

Definition 3 defines the norm boundary; Definition 4 defines the directed fixed-reference KL coefficient; Theorem 1(e) identifies its boundary slope at exponent one; Theorem 3 gives tensorisation. Their hypotheses are finite alphabets with positive marginals, not strictly positive joint probabilities, so erasure-source zeros are admissible.

### Binary high-retention antecedent

Chandra Nair and Yan Nan Wang, *Evaluating hypercontractivity parameters using information measures*, ISIT 2016, pp. 570–574.

Primary manuscript:

https://staff.ie.cuhk.edu.hk/~cnair/pub/papers/HC/BEC.pdf

The paper restricts its erasure calculation to uniform binary input. Together with Zhao's calculation it gives the full binary reverse-erasure coefficient: \(\alpha\) when \(\alpha\ge1/2\), and \(\log2/\log(2/\alpha)\) when \(\alpha\le1/2\).

## 3. Converse with every direction explicit

Write \(\pi\) for the marginal law of \(E\); then \(\pi(*)=1-\alpha\), \(\pi(x)=\alpha\mu(x)\), and the conditional law of \(X\) given \(E\) is exactly the reverse-erasure channel \(R_{\mu,\alpha}\).

### 3.1 Self-contained converse for vanishing error

Set \(c=\eta_{\rm KL}(\pi,R_{\mu,\alpha})\). The tensorised KL contraction inequality implies

\[
I(U;X^N)\le cI(U;E^N)
\quad\text{whenever }U-E^N-X^N.
\tag{2a}
\]

Indeed, apply the product-channel KL inequality to the law of \(E^N\) conditional on each value of \(U\), and average. For Alice's deterministic key \(K\), this gives \(I(K;X^N)\le cH(K)\).

Let \(M\) be her message, let \(a_k=\Pr[K=\bot]\), and let \(e_k=\Pr[K\ne\widehat K]\). Exact conditional uniformity gives

\[
H(K)=h_2(a_k)+(1-a_k)k\ge(1-a_k)k.
\]

Fano's inequality for the alphabet of size \(2^k+1\) gives

\[
H(K\mid X^N,M)\le h_2(e_k)+e_kk.
\]

Since \(H(M)\le\ell_k\),

\[
\begin{aligned}
H(K)
&\le I(K;X^N,M)+h_2(e_k)+e_kk\\
&\le cH(K)+\ell_k+h_2(e_k)+e_kk.
\end{aligned}
\]

Consequently,

\[
\boxed{\ell_k\ge(1-c)(1-a_k)k-h_2(e_k)-e_kk.}\tag{2b}
\]

If real agreement tends to one, then \(a_k,e_k\to0\), so \(\liminf\ell_k/k\ge1-c\). Substitution of the reverse-erasure formula gives (1). This proof uses only the entropy contraction theorem, its standard product extension, and elementary information identities; it does not require Zhao's general achievability theorem.

### 3.2 Established stronger converse for constant success

Let \(T\) act on functions of Alice's observation by

\[
Tf(x)=\mathbb E[f(E)\mid X=x].
\]

For \(v>1\), let \(u_*(v)\) be the smallest exponent such that

\[
\|Tf\|_{L^v(\mu)}\le\|f\|_{L^{u_*(v)}(\pi)}
\quad\text{for every real function }f.
\]

The standard hypercontractivity/SDPI relation, with the variable order as in Anantharam et al.'s Theorem 1(e), gives

\[
\lim_{v\downarrow1}\frac{u_*(v)-1}{v-1}
=\eta_{\rm KL}(\pi,R_{\mu,\alpha})=:c.
\tag{2}
\]

The same norm inequality holds for every product source by tensorisation. Fix any admissible \(1<u<v\), and a protocol using at most \(2^\ell\) different messages. For every real key value \(j\), put

\[
a_j=\Pr[K=j]\le2^{-k},\qquad
\beta_j(X^N)=\Pr[K=j\mid X^N].
\]

Given \(X^N\), Bob can output at most \(2^\ell\) different key values as the message varies. Hölder's inequality, followed by Jensen and hypercontractivity, therefore gives

\[
\begin{aligned}
s_k:=\Pr[K=\widehat K\ne\bot]
&\le 2^{\ell(1-1/v)}
 \left(\sum_j\mathbb E[\beta_j(X^N)^v]\right)^{1/v}\\
&\le 2^{\ell(1-1/v)}
 \left(\sum_j a_j^{v/u}\right)^{1/v}\\
&\le 2^{\ell(1-1/v)-k(1/u-1/v)}.
\end{aligned}\tag{3}
\]

The last step uses \(\sum_j a_j\le1\); the failure symbol is excluded from the sum. Rearranging gives

\[
\ell\ge\frac{v-u}{u(v-1)}k
+\frac{v}{v-1}\log_2 s_k.
\tag{4}
\]

For fixed admissible \(u,v\), a positive lower bound on \(s_k\) makes the last term negligible after division by \(k\). Let \(k\to\infty\), then \(v\downarrow1\) along the norm boundary in (2), to obtain

\[
\liminf_{k\to\infty}\frac{\ell_k}{k}\ge1-c.
\]

Substituting the reverse-erasure theorem gives (1). The same calculation also shows that every fixed rate strictly below \(1-c\) forces agreement probability to decay exponentially in \(k\).

## 4. Explicit upper-bound protocol for this source

Fix a rarest symbol \(x_*\), with \(\mu(x_*)=q\), and write

\[
A=\log_2(1/q),\qquad
L=\log_2(1/(\alpha q)),\qquad c=A/L.
\]

For each large integer \(k\), choose

\[
m=\lceil k/L\rceil,\quad M=2^k,
\quad d=\lceil2\log_2k\rceil,
\quad r=\lfloor mA\rfloor-d.
\]

For sufficiently large \(k\), \(0\le r\le k\). A table comprises \(M\) independent source blocks, each of length \(m\). In each block \(j\), Alice declares a mark if all her observations equal \(x_*\). Bob declares a mark if all his original symbols equal \(x_*\). The mark probabilities are

\[
a=(\alpha q)^m,\qquad b=q^m.
\]

Alice's mark implies Bob's mark in the same block. Also

\[
\alpha q<Ma\le1,
\qquad 2^r b\le2^{-d}\le k^{-2}.
\tag{5}
\]

Call a table valid if Alice has exactly one mark. Its validity probability is

\[
v_k=Ma(1-a)^{M-1}\ge\alpha q\,e^{-2}=:v_0>0,
\tag{6}
\]

using \(a\le1/M\le1/2\) and \(\log(1-a)\ge-2a\).

Take

\[
T_k=\left\lceil\frac{2\log k}{v_0}\right\rceil
\]

independent tables. Alice selects the first valid table. If none exists, she outputs \(\bot\); this event has probability at most

\[
(1-v_k)^{T_k}\le e^{-v_0T_k}\le k^{-2}.
\tag{7}
\]

If the chosen table's unique marked index is \(J\in\{1,\ldots,M\}\), Alice outputs the \(k\)-bit representation of \(J-1\). Exchangeability of the \(M\) blocks implies that this output is exactly uniform conditional on nonfailure, even after selecting the first valid table.

Partition the \(M\) indices into consecutive buckets of size \(2^r\). Alice sends the selected table number and the bucket containing \(J\). Bob examines that bucket in his corresponding table and outputs its unique marked index if it has exactly one.

Conditional on the chosen table being valid with Alice's unique mark at \(J\), every other block is conditioned on lacking Alice's mark. Its probability of having Bob's mark becomes

\[
b'=\frac{b-a}{1-a}\le b.
\]

The blocks remain independent under this conditioning. Since Bob certainly marks \(J\), a union bound gives

\[
\Pr[\text{Bob does not recover }J\mid\text{Alice succeeds}]
\le(2^r-1)b'\le2^rb\le k^{-2}.
\tag{8}
\]

Combining (7) and (8) gives agreement probability at least \(1-2/k^2\). A reserved table-number value handles nonfailure signalling, so the maximum communication is

\[
\begin{aligned}
\ell_k
&\le k-r+\lceil\log_2(T_k+1)\rceil\\
&=(1-c)k+O_{\alpha,q}(\log k).
\end{aligned}
\]

The sample count is \(N_k=T_km2^k=O_{\alpha,q}(k2^k\log k)\). The construction works for any \(0<\alpha<1\); the contraction theorem proves its optimality precisely in the stated atomic phase. Above that phase, the same construction is a valid upper bound on communication cost, but it need not be optimal.

## 5. Suggested short paper insertion

**Corollary (agreement distillation from erasures).** Let \(X\sim\mu\) have finite positive support, \(q=\min_x\mu(x)\), and let \(E\) retain \(X\) with probability \(\alpha\), independently erasing it otherwise. If \(\alpha\le q^{q/(1-q)}\), the optimal asymptotic one-way communication per uniformly generated output bit, with Alice observing \(E^N\), Bob observing \(X^N\), unlimited source samples and vanishing failure and disagreement, equals

\[
\frac{\log(1/\alpha)}{\log(1/(\alpha q))}.
\]

The lower bound follows by averaging the tensorised entropy contraction inequality over the conditional laws given Alice's output, then applying Fano's inequality. An explicit protocol uses rarest-symbol blocks and bucket indices. It uses \(O_{\alpha,q}(k2^k\log k)\) samples, communicates the displayed rate times \(k\) plus \(O_{\alpha,q}(\log k)\) bits, and succeeds with probability \(1-O(k^{-2})\). The established hypercontractive converse [Guruswami–Radhakrishnan 2016, Section 4.1; Zhao 2021, Theorem 3.1.1] gives the same lower bound even for agreement bounded away from zero. For uniform binary sources the coefficient and its communication interpretation were already obtained by Zhao [2021, Theorem 3.5.4 and Corollary 3.1.3]; the present coefficient extends that evaluation to arbitrary finite priors in the stated range.
