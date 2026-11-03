# Rarest-atom reduction for every reverse-erasure parameter

Proof checkpoint, 1 November 2026. The monotonicity calculation below was independently checked by the root and optimisation agents. It strengthens the earlier finite collection of scalar branches to one branch. This file does not modify the frozen main draft.

## 1. The branch to compare

For a retention probability \(0<\alpha<1\), exponent \(p>1\), and \(0<w<1\), define
\[
F_{w,\alpha,p}(r)
=\frac{\alpha(wr^p+1-w)+(1-\alpha)r^{pw}}
{(wr+1-w)^p},\qquad 1\le r<\infty.
\tag{R1}
\]
Its endpoint values are
\[
F_{w,\alpha,p}(1)=1,\qquad
F_{w,\alpha,p}(\infty)=\alpha w^{1-p}.
\tag{R2}
\]

**Theorem R1.** For \(0<v<w<1\),
\[
\sup_{r\in[1,\infty]}F_{v,\alpha,p}(r)
\ge
\sup_{r\in[1,\infty]}F_{w,\alpha,p}(r).
\tag{R3}
\]
More strongly, each finite nonconstant \(w\)-branch point is strictly dominated by a \(v\)-branch point having the same weighted geometric mean after arithmetic normalisation. The vertex value is also strictly larger for \(v\). The common constant-vector value one explains why the suprema themselves need not be strictly ordered for arbitrary prescribed \(p\).

## 2. Parametrisation by the geometric mean

Normalise the branch's weighted arithmetic mean to one:
\[
b=\frac r{wr+1-w},\qquad
a=\frac1{wr+1-w},\qquad
wb+(1-w)a=1.
\]
Its weighted geometric mean is
\[
g(w,r)=b^w a^{1-w}
=\frac{r^w}{wr+1-w}.
\tag{R4}
\]
For each fixed \(w\in(0,1)\),
\[
\frac{\partial}{\partial r}\log g(w,r)
=-\frac{w(1-w)(r-1)}{r(wr+1-w)}<0
\quad(r>1).
\tag{R5}
\]
Moreover, \(g(w,1)=1\) and \(g(w,r)\to0\) as \(r\to\infty\). Thus every \(g\in(0,1)\) determines a unique \(r=r(w,g)>1\). The implicit function theorem makes this parametrisation differentiable in \(w\).

At fixed \(g\), write
\[
M_p(w,g)=wb^p+(1-w)a^p.
\]
Equation (R1) becomes
\[
F_{w,\alpha,p}(r(w,g))
=\alpha M_p(w,g)+(1-\alpha)g^p.
\tag{R6}
\]
It is therefore enough to prove that \(M_p(w,g)\) decreases strictly with \(w\).

## 3. Derivative and its sign

Keep \(g\in(0,1)\) fixed and differentiate
\[
wb+(1-w)a=1,\qquad
w\log b+(1-w)\log a=\log g.
\]
Put \(r=b/a>1\), \(U=wb'\), \(V=(1-w)a'\). Then
\[
U+V=-(b-a),\qquad
\frac Ub+\frac Va=-\log r.
\]
Solving,
\[
U=-\frac{ar}{r-1}(r-1-\log r),\qquad
V=\frac a{r-1}(r-1-r\log r).
\tag{R7}
\]
Consequently
\[
\frac{\partial M_p}{\partial w}
=\frac{a^p}{r-1}
\left[
p\log r\,(r^p-r)
-(p-1)(r-1)(r^p-1)
\right].
\tag{R8}
\]

The bracket is strictly negative for every \(p>1,r>1\). A short sign proof uses \(r=e^{2t}\), \(t>0\). After cancelling the positive factor \(4e^{(p+1)t}\), negativity is equivalent to
\[
p\,t\,\sinh((p-1)t)
<
(p-1)\sinh(pt)\sinh t.
\tag{R9}
\]
For fixed \(t>0\), the function \(s\mapsto\sinh(st)/s\) is strictly increasing on \(s>0\). Its derivative has the sign of
\[
st\cosh(st)-\sinh(st)>0,
\]
because this expression vanishes at zero and has derivative \(st\sinh(st)>0\) with respect to \(st\). Therefore
\[
(p-1)\sinh(pt)>p\sinh((p-1)t).
\]
Multiplying by \(\sinh t>t\) proves (R9).

An alternative independent check uses
\[
I_1=\int_1^r u^{p-1}\,du,\qquad
I_0=\int_1^r u^{p-2}\,du.
\]
The bracket in (R8) is negative exactly when
\[
\frac{I_1}{I_0}>\frac{r\log r}{r-1}.
\]
Positive covariance of the strictly increasing functions \(u\) and \(u^{p-1}\) under the probability law proportional to \(du/u\) gives
\[
\frac{I_1}{I_0}>\frac{r-1}{\log r}.
\]
The logarithmic mean \((r-1)/\log r\) exceeds \(\sqrt r\), so it in turn exceeds \(r\log r/(r-1)\).

Equation (R8) proves strict decrease of \(M_p\) at fixed \(g\). Integrating over \(v<w\), using (R6), proves strict domination of every finite nonconstant branch point. The two endpoint values in (R2) complete the proof of Theorem R1.

## 4. Exact binary reduction

Let \(\mu=(\mu_i)\) be a positive finite law, \(q=\min_i\mu_i\), and let \(R_\mu\) be reverse erasure with reference input
\[
\rho_{\mu,\alpha}(i)=\alpha\mu_i,\qquad
\rho_{\mu,\alpha}(e)=1-\alpha.
\]
Write \(\eta(\mu,\alpha)=\eta_{\rm KL}(\rho_{\mu,\alpha},R_\mu)\).

The previously established stationary-point argument says that the dual inequality for coefficient \(c\in(0,1)\), \(p=1/c\), is equivalent to testing the constant vector, vertices, and the branches (R1) at each coordinate weight \(\mu_i\). Theorem R1 reduces all these tests to \(w=q\). The binary reference law \((q,1-q)\) has the same most demanding branch \(q\), since \(q\le1-q\). Therefore
\[
\boxed{\eta(\mu,\alpha)=\eta((q,1-q),\alpha)
\quad\text{for every }0<\alpha<1.}
\tag{R10}
\]

Thus the coefficient depends on the original law only through its smallest atom, for all retention probabilities. The exact scalar decision criterion becomes
\[
\eta(\mu,\alpha)\le c
\quad\Longleftrightarrow\quad
\alpha(qr^p+1-q)+(1-\alpha)r^{pq}
\le(qr+1-q)^p
\quad\text{for every }r\ge1,
\quad p=1/c.
\tag{R11}
\]
The vertex test is included by taking \(r\to\infty\).

No uniqueness of a nonconstant scalar optimiser \(r\) is asserted. Equality of the full channel coefficients follows from equality of the sets of admissible \(c\), so no attainment assumption is needed for (R10).

## 5. Extremiser consequence

Suppose the sharp dual constant admits a finite nonconstant maximiser. The stationary-point argument already implies its positive coordinates have exactly one large value and a common smaller value elsewhere. If the large coordinate had weight \(w>q\), Theorem R1 would produce a dual vector at weight \(q\) with strictly larger value, violating the sharp inequality. Hence its distinguished coordinate must have mass \(q\).

In the supercritical regime, where the main proof supplies a full-support primal extremiser, its finite output log-density is a nonconstant sharp dual maximiser. Every such primal extremiser is consequently a tilt of a rarest ordinary symbol. After normalising the smaller dual value to one and writing the larger one as \(r>1\), the Gibbs variational equality gives
\[
Z=\alpha(qr^p+1-q)+(1-\alpha)r^{pq},
\]
\[
\nu_i=\frac{\alpha q r^p}{Z},\qquad
\nu_j=\frac{\alpha\mu_j}{Z}\ (j\ne i),\qquad
\nu_e=\frac{(1-\alpha)r^{pq}}Z,
\quad \mu_i=q.
\tag{R12}
\]
At dual equality, \(Z=(qr+1-q)^p\). Different rarest coordinates are related by the obvious relabelling of their equal reference masses. The calculation does not exclude several admissible values of \(r\).

The uniform binary high-retention regime must retain its separate interpretation: the sharp value is the local coefficient \(\alpha\), and for \(\alpha>1/2\) no nonconstant extremiser is supplied by this reduction. At \(q=\alpha=1/2\), \(p=2\), every scalar branch value is one; this is the previously identified exceptional equality family.

## 6. Implication for a self-contained weighted mean proof

The earlier all-weight mean inequality can now be reduced to the rarest branch. Put \(N=1/q\ge2\), which need not be an integer. At the atomic coefficient \(\alpha=q^{p-1}\), the scalar inequality is exactly
\[
(r+N-1)^p-r^p-(N-1)
-(N^p-N)r^{p/N}\ge0.
\tag{R13}
\]
The existing uniform proof uses only \(N\ge2\) and \(p\ge N/(N-1)\), not integrality, so it applies verbatim. This gives a shorter self-contained proof and the required strictness, while the inequality itself remains attributed to Gao 2003 and Gao 2009.

## 7. Bounded prior-art rerun

The new simplification prompted searches for the exact object and its mean-inequality aliases:

- "fixed arithmetic and geometric means" power
- "fixed arithmetic and geometric means" weights
- "power means" "minimum weight" "two"
- "geometric mean" "arithmetic mean" "smallest weight" maximum
- "Diananda" "two" "weights" reduction
- "power mean" "fixed arithmetic" "geometric" maximum
- "erasure" "contraction" "smallest" probability
- "strong data processing" "minimum probability" binary
- "relative entropy" "smallest mass" erasure
- "reverse erasure" "binary"

No exact statement of (R10) or (R11) was found in this bounded search. The general technique of reducing inequalities of weighted means to few values is established. In particular, Gao 2009, Theorem 3.1, studies two-variable reductions for another family of mean inequalities; that general proof style is not a novelty claim here. The source is [the published article](https://doi.org/10.1155/2009/468290), with [accessible primary precursor](https://vuir.vu.edu.au/17591/1/AGinequality4rgmia.pdf).

A new near match was inspected: Christoph Hirche and Oxana Shaya, *Partial orders and contraction for BISO channels*, arXiv:2504.16726v1, 23 April 2025, [primary HTML](https://arxiv.org/html/2504.16726v1). Its equation (II.6) maximises over both reference input laws; Lemma II.2 gives an exact expression for binary-input symmetric-output channels. This differs from the fixed-reference ternary-input binary-output kernel on the right of (R10). Its coefficient, channel orientation and constraint set do not match the present theorem.

The novelty claim should attach to the information-theoretic consequence (R10), the sharp threshold and extremisers, and the bipartite solution. No historical novelty is asserted for a standalone two-point moment monotonicity argument. The bounded search does not rule out an older version of that elementary lemma or an unindexed information-theoretic application.

### Gao 2018 check after the final reduction

Peng Gao, *Some extensions of Diananda's inequality*, arXiv:1807.06290v1, submitted 17 July 2018: [primary HTML](https://arxiv.org/html/1807.06290v1), [PDF](https://arxiv.org/pdf/1807.06290). Theorem 1.1, Corollary 1.1, and the complete proof in Section 2, equations (2.1)–(2.5), were inspected. Its coefficient is prescribed as \(q^{(r-1)p/r}\) or \((1-q)^{(r-1)p/r}\). The result extends sufficient exponent ranges for those inequalities. The proof merges the remaining coordinates using power-mean monotonicity and then bounds the weight parameter by its symmetric endpoint. It does not state the exact reduction for a free coefficient \(\alpha\), or identify all admissible coefficients by the rarest branch. Theorem 1.2 instead concerns variance remainders. Thus this paper is relevant background for the known mean inequality and its reduction techniques, but does not supply (R10) or the unrestricted criterion (R11) in the inspected statements or proof.

Additional searches used “weighted power mean fixed arithmetic geometric mean maximum minimum weight two values”, “fixed arithmetic and geometric”, “power means minimum weight extremal”, and Rényi/reverse-KL aliases. No additional exact collision was located. This is a bounded audit, not a proof of historical priority.

### Numerical smoke check

A vectorised grid check compared 3,000 random parameter triples with \(10^{-5}\le q\le1/2\), \(q\le w\le1-q\), \(0<\alpha<1\), and \(1.001\lesssim p\lesssim101\). It included the constant and vertex limits and logarithmic branch coordinates up to 2,000. The largest observed excess of the heavier-weight logarithmic envelope was \(2.22\times10^{-16}\), consistent with rounding. This is only a smoke check; the derivative proof establishes the theorem for every allowed parameter.

