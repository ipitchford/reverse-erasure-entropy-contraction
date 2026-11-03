# Weighted reverse erasure and weighted bipartite chains

Independent derivation and audit, 1 November 2026.

## A. Definitions

Let \(\mu\) be a strictly positive probability law on a finite set of at least two points, and put \(q=\min_i\mu_i\in(0,1/2]\). For a nonnegative vector \(z\), write

\[
A=\sum_i\mu_i z_i,\qquad M_p=(\sum_i\mu_i z_i^p)^{1/p},\qquad G=\prod_i z_i^{\mu_i}.
\]

The reverse-erasure channel \(R_{\mu,\alpha}\) has input alphabet \(\{*\}\cup\operatorname{supp}\mu\), reference input law \(\pi(*)=1-\alpha\), \(\pi(i)=\alpha\mu_i\), and transition rows \(R(*)=\mu\), \(R(i)=\delta_i\). Its reference output law is \(\mu\).

## B. The sharp weighted mean inequality

For every

\[
p\ge p_0:=\frac1{1-q},
\]

one has

\[
A^p\ge q^{p-1}M_p^p+(1-q^{p-1})G^p.\tag{B1}
\]

For \(p_0\le p\le2\), this is Gao (2009), Theorem 1.2, second inequality, with the power-mean order and outer exponent both equal to \(p\). The inspected preprint labels it (1.4); the published version labels it (1.7).

For \(p\ge2\), it follows from Gao (2003), Theorem 3.1, by setting \(t=1,r=p\) and replacing the variables \(x_i\) with \(z_i^p\). In its rearranged form his inequality is \(M_{1/p}(x)\ge q^{p-1}A(x)+(1-q^{p-1})G(x)\), which is precisely (B1) after substitution.

The exponent threshold is necessary. If \(1<p<p_0\), choose a rarest coordinate \(i\), set \(z_i=r\), and set all other coordinates to one. The difference of the sides of (B1) is

\[
(qr+1-q)^p-q^{p-1}(qr^p+1-q)-(1-q^{p-1})r^{pq}.
\]

As \(r\to\infty\), its leading non-cancelling terms are

\[
p q^{p-1}(1-q)r^{p-1}-(1-q^{p-1})r^{pq}.
\]

Since \(pq>p-1\), the second term dominates and the inequality fails.

### B.1 Equality for nonnegative vectors

Except for \(q=1/2,p=2\), equality in (B1) holds exactly when either all entries of \(z\) coincide, or \(z\) has one positive coordinate \(i\) with \(\mu_i=q\). The all-zero vector is included in the first case.

If \(G=0\), let \(t_i=\mu_i z_i\). Then

\[
A^p=(\sum_i t_i)^p\ge\sum_i t_i^p
\ge q^{p-1}\sum_i\mu_i^{1-p}t_i^p=q^{p-1}M_p^p.
\]

The first inequality is strict unless at most one \(t_i\) is positive. For a positive coordinate, the second is an equality precisely when \(\mu_i=q\). This proves the boundary classification directly.

For positive vectors, strictness can be verified without assuming an unreported equality statement in Gao (2009), as follows.

#### B.1.1 Strictness at the threshold \(p=p_0<2\)

Set \(S=\sum_i\mu_i z_i^p\) and

\[
H(z)=\frac{A^p-q^{p-1}S}{G^p}.
\]

At an all-equal vector, \(H=1-q^{p-1}\). We show that increasing a largest coordinate strictly increases \(H\) whenever the vector is nonconstant. Let \(y=z_j\) be a largest coordinate, of weight \(\mu_j\ge q\). Direct differentiation gives

\[
\frac{yG^p}{p\mu_j}\frac{\partial H}{\partial y}
=A^{p-1}(y-A)-q^{p-1}(y^p-S).\tag{B2}
\]

Define

\[
w_1=\frac{A-qy}{1-q},\qquad
w_p=\left(\frac{S-qy^p}{1-q}\right)^{1/p}.
\]

These are means of a probability distribution formed by removing weight \(q\) at coordinate \(j\); consequently \(0<w_1\le w_p<y\) for a nonconstant positive vector. Because \(p=1/(1-q)\), the function

\[
g(w)=(qy+(1-q)w)^{p-1}(y-w)
\]

is strictly decreasing on \((0,y)\): its derivative is \(-w(qy+(1-q)w)^{p-2}\). Thus the right-hand side of (B2) is at least

\[
(1-q)q^{p-1}w_p^p J_a(y/w_p),
\quad a=p-1\in(0,1),
\]

where

\[
J_a(z)=(z+1/a)^a(z-1)-z^{a+1}+1.
\]

Now \(J_a(1)=0\), and with \(u=1/(az)>0\),

\[
J_a'(z)=(a+1)z^a\left[(1+u)^{a-1}(1+(1-a)u)-1\right]>0.
\]

The last inequality is exactly the strict concavity inequality \((1+u)^{1-a}<1+(1-a)u\). Hence \(\partial H/\partial y>0\). Lower the largest coordinate or tied group of largest coordinates to the next level, and repeat. This reaches an all-equal vector while strictly decreasing \(H\), proving strict (B1) at every positive nonconstant vector.

#### B.1.2 Strictness for \(p_0<p\le2\)

Apply Gao (2009) with mean order \(r=p\), but outer exponent \(s=p_0<p\). It gives

\[
A^s\ge b^s M_p^s+(1-b^s)G^s,
\qquad b=q^{(p-1)/p}\in(0,1).
\]

When \(G>0\), put \(U=(A/G)^s\), \(V=(bM_p/G)^s\), and \(B=b^s\). Then \(U-V\ge1-B\). If the vector is nonconstant, strict power-mean inequality gives \(V>B\). For \(k=p/s>1\),

\[
U^k-V^k\ge(V+1-B)^k-V^k>1-B^k,
\]

because \(v\mapsto(v+1-B)^k-v^k\) is strictly increasing. This is the strict version of (B1).

#### B.1.3 Strictness for \(p\ge2\)

Gao (2003), Theorem 3.1, explicitly gives equality only at the appropriate two-point boundary configuration, apart from \(p=2\) with two equal weights. To accommodate repeated values, merge equal-valued coordinates, with new minimum weight \(Q\ge q\). If \(Q>q\), the inequality with coefficient \(Q^{p-1}\) is strictly stronger because \(M_p>G\); if \(Q=q\), Gao's equality classification applies directly. Thus positive nonconstant vectors are strict except at \(q=1/2,p=2\).

When \(q=1/2\), positivity and normalisation force exactly two weights, both \(1/2\). At \(p=2\), (B1) is the identity

\[
\left(\frac{z_1+z_2}{2}\right)^2
=\frac{z_1^2+z_2^2}{4}+\frac{z_1z_2}{2}.
\]

## C. Exact reverse-erasure phase

Define

\[
\alpha_*(q)=q^{q/(1-q)}.
\]

For \(0<\alpha\le\alpha_*(q)\), the exact fixed-reference Kullback–Leibler contraction coefficient of \(R_{\mu,\alpha}\) is

\[
\boxed{\eta_{\mathrm{KL}}(\pi,R_{\mu,\alpha})
=\frac{\log(1/q)}{\log(1/(\alpha q))}.}\tag{C1}
\]

Indeed, put \(p=\log(1/(\alpha q))/\log(1/q)\), so \(\alpha=q^{p-1}\). The condition \(\alpha\le\alpha_*(q)\) is equivalent to \(p\ge p_0\). The entropy duality established in independent_audit.md converts (B1) exactly into (C1)'s upper bound. An input point mass at a rarest non-erasure state has output divergence \(\log(1/q)\) and input divergence \(\log(1/(\alpha q))\), proving sharpness.

For \(\alpha>\alpha_*(q)\), this point-mass ratio is strictly below the true coefficient. This follows already from failure of (B1). An explicit perturbation makes the failure concrete: for a rarest state \(i\), take

\[
\rho_\epsilon=(1-\epsilon)\delta_i+\epsilon\delta_*.
\]

Write \(A_0=\log(1/q)\), \(L_0=\log(1/(\alpha q))\). Then

\[
D(\rho_\epsilon R\|\mu)=A_0+(1-q)\epsilon\log\epsilon+O(\epsilon),
\]

\[
D(\rho_\epsilon\|\pi)=L_0+\epsilon\log\epsilon+O(\epsilon).
\]

Thus the ratio is

\[
\frac{A_0}{L_0}+
\frac{(1-q)L_0-A_0}{L_0^2}\epsilon\log\epsilon+O(\epsilon).
\]

For \(\alpha>\alpha_*\), the coefficient of \(\epsilon\log\epsilon\) is negative, so every sufficiently small positive \(\epsilon\) improves upon the atomic ratio. This is a phase boundary for atomic optimality; it is not a closed formula for the coefficient above the boundary.

### C.1 Extremisers

For \(\alpha\le\alpha_*\), excluding \(q=1/2,\alpha=1/2\), all non-reference equality laws are point masses at non-erasure states with prior mass \(q\).

To see this, write any input as \(\rho=(t\nu,1-t)\). If \(t<1\), its output \(t\nu+(1-t)\mu\) is positive. If it differs from \(\mu\), the entropy variational optimiser is a finite nonconstant vector and strictness in (B1) makes the contraction strict. If the output equals \(\mu\), its divergence vanishes, so equality at a positive coefficient requires \(\rho=\pi\). If \(t=1\), the contraction inequality reads

\[
D(\nu\|\mu)\le c[D(\nu\|\mu)+\log(1/\alpha)].
\]

With \(c\) from (C1), equality requires \(D(\nu\|\mu)=\log(1/q)\), which holds only at rarest atoms: \(D(\nu\|\mu)=\sum_i\nu_i\log(1/\mu_i)-H(\nu)\le\log(1/q)\).

The exceptional \(q=1/2,\alpha=1/2\) is the binary family described in independent_audit.md.

## D. Weighted bipartite theorem

Let \(A,B\) be disjoint finite nonempty sets, and let \(\mu,\nu\) be positive probability laws on them. Define the Markov kernel

\[
P(a,a)=\tfrac12,\quad P(a,b)=\tfrac12\nu_b;
\qquad
P(b,b)=\tfrac12,\quad P(b,a)=\tfrac12\mu_a,
\]

with other entries zero. This is the one-half-lazy random walk on the complete bipartite graph with edge weights \(w_{ab}=\mu_a\nu_b\). Its stationary law is \(\pi=(\mu/2,\nu/2)\).

If both sides are singletons, \(P\) resets to stationarity in one step, so \(\eta=0\). Otherwise set

\[
q=\min\{\min_a\mu_a,\min_b\nu_b\}\le\tfrac12.
\]

Then

\[
\boxed{\eta_{\mathrm{KL}}(\pi,P)
=\frac12\frac{\log(1/q)}{\log(2/q)}.}\tag{D1}
\]

The value depends only on the smallest conditional atom, or equivalently on \(\pi_{\min}=q/2\).

### D.1 Proof

For every \(q\le1/2\), \(1/2\le\alpha_*(q)\). Equivalently,

\[
(1-q)\log2+q\log q\ge0,
\]

which follows because this expression decreases to zero on \((0,1/2]\): its derivative is \(1+\log(q/2)<0\).

Consequently C1 applies to each nontrivial side at \(\alpha=1/2\). Put \(c_\mu=\log(1/q_\mu)/\log(2/q_\mu)\), and similarly \(c_\nu\); assign coefficient zero to a singleton side. For any \(a\le1/2\), convexity and the reverse-erasure inequality at input mass \(1/2\) imply

\[
D(a\rho+(1-a)\mu\|\mu)
\le2aD((\rho+\mu)/2\|\mu)
\le a c_\mu D(\rho\|\mu).\tag{D2}
\]

Write an arbitrary input as \(\lambda=(t\rho,(1-t)\sigma)\), and interchange the two sides if needed so that \(t\ge1/2\). Then

\[
D(\lambda\|\pi)
=d(t\|1/2)+tD(\rho\|\mu)+(1-t)D(\sigma\|\nu),
\]

\[
D(\lambda P\|\pi)
=\frac12\left[
D(t\rho+(1-t)\mu\|\mu)
+D((1-t)\sigma+t\nu\|\nu)\right].
\]

Apply C1 to the first term and D2 to the second. Since \(c_\mu,c_\nu\le c(q)\), this proves the upper bound in D1. A point mass at a vertex whose conditional probability is \(q\) has input divergence \(\log(2/q)\) and output divergence \(\tfrac12\log(1/q)\), establishing equality.

### D.2 Equality

If \(q<1/2\), the only nontrivial extremisers are point masses at the rarest vertices, meaning vertices with conditional mass \(q\). Strictness follows from C.1 on any side attaining the smallest conditional atom. A side with larger minimum conditional mass has a strictly smaller coefficient and cannot create an additional equality case.

If \(q=1/2\), every non-singleton side consists of exactly two equally weighted points. Thus the only possibilities, apart from the trivial two-singleton chain, are \(K_{1,2}\), \(K_{2,1}\), and \(K_{2,2}\). Their complete extremiser families are given in independent_audit.md.

For uniform side laws this reduces to

\[
\eta_{\mathrm{KL}}(K_{m,n})
=\frac{\log\max\{m,n\}}{2\log(2\max\{m,n\})}.
\]

### D.3 Local coefficient and products

On \(L^2(\pi)\), the spectrum of \(P\) is \(1\) on constants, \(0\) on the function distinguishing the two sides, and \(1/2\) on the conditional mean-zero functions within either side. Hence, whenever at least one side has two points,

\[
\eta_{\chi^2}(\pi,P)=1/4.
\]

In contrast, (D1) tends to \(1/2\) as \(q\downarrow0\). Thus rare atoms control the worst global relative-entropy contraction even while the local quadratic contraction remains fixed.

Synchronous products of these chains have exact KL coefficient equal to the largest factor coefficient by the tensorisation proof in independent_audit.md. These are applications of known spectral and tensorisation facts, not separate novelty claims.

## E. Source and novelty limits

The weighted mean inequalities are prior results. The proposed contribution is their exact information-theoretic translation, the sharp atomic phase boundary and extremiser classification for reverse erasure, and the resulting complete weighted bipartite contraction formula. Do not claim a new general mean inequality.

Primary sources inspected:

- Gao, P. (2003). On an inequality of Diananda. *International Journal of Mathematics and Mathematical Sciences*, vol. 2003, no. 32, 2061–2068. https://doi.org/10.1155/S0161171203210279 . Inspected manuscript: https://vuir.vu.edu.au/17773/1/AGinequality.pdf . Theorem 3.1 and Eq. (3.7).
- Gao, P. (2009). On an inequality of Diananda—Part IV. *International Journal of Mathematics and Mathematical Sciences, 2009*, Article 468290. https://doi.org/10.1155/2009/468290 . Inspected preprint: https://rgmia.org/papers/v10n4/AGinequality4rgmia.pdf . Theorem 1.2, Eq. (1.4).
- Caputo, P., Chen, Z., Gu, Y., & Polyanskiy, Y. Entropy contractions in Markov chains: Half-step, full-step and continuous-time. https://arxiv.org/abs/2409.07689 . Inspected full text: https://people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf . Example 4.4 and Proposition 4.5.

All statements concerning the reverse-erasure coefficient beyond the phase boundary must be limited to strict failure of the atomic formula unless a separate calculation supplies the actual coefficient.
