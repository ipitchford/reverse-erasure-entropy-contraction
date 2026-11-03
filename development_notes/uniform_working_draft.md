# Sharp entropy contraction for lazy complete bipartite walks and reverse erasure channels

Mathematical working draft prepared on 1 November 2026. This file contains the proof, proposed contribution boundary and source locators. It is not a completed novelty report or external peer review.

## 1. Scope and positioning

Caputo, Chen, Gu and Polyanskiy, *Entropy contractions in Markov chains: Half-step, full-step and continuous-time* (Electronic Journal of Probability, 2025; arXiv:2409.07689), establish the sharp relative-entropy contraction coefficient of the half-lazy walk on the complete bipartite graph K_{3,3}. Proposition 4.5 and the paragraph following its proof conjecture the same formula and equality cases for K_{n,n}, every n >= 3. Their proof for n = 3 combines analytic estimates with a computer-assisted verification of a two-variable inequality.

The proof below establishes their conjecture for all n >= 3. The main mechanism is an exact strong data-processing inequality for the reverse n-ary erasure channel. This reverse-channel result has a sharp phase boundary. We also recover the binary closed form as a check: the a >= 1/2 branch is already covered by Nair--Wang's binary-erasure hypercontractivity theorem, as identified in the independent literature audit, and is not an originality claim. The remaining n-ary regime has an exact one-dimensional variational characterisation, including the shape of every nontrivial dual extremiser.

The underlying inequality between the arithmetic, geometric and power means is classical: Gao (2009), Theorem 1.2, equation (1.7) in the published article, and Theorem 1.2, equation (1.4) in the inspected preprint. In equal weights, setting the two exponents equal gives the inequality used here for n/(n-1) <= p <= 2. We provide an elementary proof for all p >= n/(n-1), but do not claim the mean inequality or this extension to be historically new. The candidate contribution consists of the n-ary entropy-contraction consequences, the solution of the explicit bipartite conjecture and the n-ary reverse-erasure classification. Searches must distinguish those units.

Primary source locators inspected:

* Caputo et al., author PDF, pp. 23--26, Example 4.4, Proposition 4.5 and the conjecture following the proof: https://people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf
* Caputo et al., published DOI: https://doi.org/10.1214/25-EJP1372
* Gao, preprint, pp. 1--2, Theorem 1.2 (1.4): https://rgmia.org/papers/v10n4/AGinequality4rgmia.pdf
* Gao, published article: https://doi.org/10.1155/2009/468290
* Weinberger and Shayevitz, *Guessing with a Bit of Help* (2020), Section 4.1: defines the reverse binary-erasure channel and evaluates its contraction coefficient numerically as a three-dimensional constrained optimisation. https://pmc.ncbi.nlm.nih.gov/articles/PMC7516461/ ; https://doi.org/10.3390/e22010039

## 2. Definitions

All logarithms are natural. For probability distributions v and mu on the same finite set, with mu strictly positive, let

\[
D(v\|\mu)=\sum_x v_x\log(v_x/\mu_x),
\]

with 0 log 0 = 0. For a Markov kernel K with input reference mu and output reference mu K, define

\[
\eta_{\rm KL}(\mu,K)
=\sup_{v\ne\mu}\frac{D(vK\|\mu K)}{D(v\|\mu)}.
\tag{2.1}
\]

An extremiser means a probability distribution v different from mu attaining this ratio. Equality of the entropy inequality at the reference distribution is trivial and is not called an extremiser.

Write u_n for the uniform law on [n], and

\[
d(t\|a)=t\log(t/a)+(1-t)\log((1-t)/(1-a)).
\]

The reverse erasure kernel R_n has input alphabet [n] union {e} and output alphabet [n]. It maps each ordinary symbol i deterministically to i and the erasure symbol e to u_n. Its reference input law is

\[
\mu_{n,a}(i)=a/n,\qquad \mu_{n,a}(e)=1-a,
\qquad 0<a<1,
\tag{2.2}
\]

so that mu_{n,a} R_n = u_n. Parameter a is the retention probability of the forward erasure channel. A general input is v=(t q,1-t), where q is a probability distribution on [n]. Thus

\[
vR_n=tq+(1-t)u_n,
\quad
D(v\|\mu_{n,a})=d(t\|a)+tD(q\|u_n).
\tag{2.3}
\]

The half-lazy random walk P_n on K_{n,n} has state space {1,2} x [n]. From (b,i), it stays at (b,i) with probability 1/2; with probability 1/2 it chooses a uniform vertex in the other part. Its stationary law pi_n is uniform on 2n states. Its matrix is

\[
P_n=\frac12\begin{pmatrix}I_n&J_n/n\\J_n/n&I_n\end{pmatrix}.
\tag{2.4}
\]

This precise laziness convention is essential. The non-lazy bipartite walk is periodic and has a different contraction coefficient.

## 3. Entropy and exponential-moment duality

**Lemma 3.1 (finite-channel duality).** Let mu have full support and let lambda=mu K have full support. For c>0, the inequality

\[
D(vK\|\lambda)\le cD(v\|\mu)\quad\hbox{for every }v
\tag{3.1}
\]

holds if and only if, for every real function f on the output alphabet,

\[
c\log\sum_x\mu_x\exp((Kf)_x/c)
\le\log\sum_y\lambda_y e^{f_y}.
\tag{3.2}
\]

*Proof.* Use the finite variational formula

\[
D(q\|\lambda)=\sup_f\{qf-\log\lambda(e^f)\}.
\]

Inequality (3.1) is equivalent to

\[
vf_K-cD(v\|\mu)\le\log\lambda(e^f)
\]

for every v,f, where f_K=Kf. Taking the supremum over v gives (3.2), again by the variational formula. Reversing these steps proves sufficiency. This proof also covers output distributions with zeros by taking the supremum over finite f and then passing to a limit. QED.

For reverse erasure and p=1/c, put z_i=e^{f_i}. The dual condition is

\[
\frac an\sum_i z_i^p+(1-a)\Big(\prod_i z_i\Big)^{p/n}
\le\Big(\frac1n\sum_i z_i\Big)^p
\quad\hbox{for every }z_i\ge0.
\tag{3.3}
\]

Strictness will be useful: if (3.2) is strict for every finite nonconstant f, then (3.1) is strict whenever vK has full support and differs from lambda. Indeed f=log((vK)/lambda) is then a finite nonconstant maximiser of the output variational formula.

## 4. A mean inequality and its elementary proof

**Lemma 4.1 (mean inequality, with classical attribution).** Let n>=2 and p>=n/(n-1). For z_i>=0,

\[
\Big(\sum_{i=1}^n z_i\Big)^p
\ge \sum_{i=1}^n z_i^p
+(n^p-n)\Big(\prod_{i=1}^n z_i\Big)^{p/n}.
\tag{4.1}
\]

Unless n=p=2, equality for a nonzero vector holds exactly when all entries are equal or exactly one entry is positive. When n=p=2, (4.1) is an identity. For n/(n-1)<=p<=2, this is the equal-weight specialisation of Gao (2009), Theorem 1.2 (1.7); no originality claim is made for the mean inequality.

*Proof.* By homogeneity normalise sum z_i=1. We prove a more general structural fact. For any B>0, let

\[
F(z)=\sum_i z_i^p+B\Big(\prod_i z_i\Big)^{p/n}.
\tag{4.2}
\]

It is continuous on the compact simplex and has a maximiser. On its boundary, the product term vanishes; since p>1, sum z_i^p<=1, with equality only at a vertex.

At an interior stationary point put G=(product z_i)^{1/n} and T=BG^p/n. Lagrange multipliers give

\[
z_i^{p-1}+T/z_i=\lambda,
\quad\hbox{equivalently}\quad z_i^p-\lambda z_i+T=0.
\tag{4.3}
\]

The function in the last equation is strictly convex on (0,infinity), so there are at most two distinct coordinate values. If they are x<y, subtracting their stationary equations gives

\[
T=xy\frac{y^{p-1}-x^{p-1}}{y-x}<(p-1)y^p.
\tag{4.4}
\]

For completeness, setting b=x/y in (0,1) reduces the strict inequality to

\[
\frac{b(1-b^{p-1})}{1-b}<p-1.
\]

This follows by writing 1-b^{p-1}=(p-1) integral_b^1 s^{p-2} ds: throughout the interval, b s^{p-2}<1. If two coordinates both equal y, change them to y+h,y-h. The second derivative of F in this direction at h=0 equals

\[
\frac{2p}{y^2}\{(p-1)y^p-T\}>0,
\tag{4.5}
\]

contradicting a local maximum. Consequently every nonuniform interior maximum has exactly one large coordinate. Up to scaling and permutation its vector is (r,1,...,1), r>1.

It remains to check (4.1) on that family. Define

\[
H(r)=(r+n-1)^p-r^p-(n-1)-(n^p-n)r^{p/n}.
\tag{4.6}
\]

We have H(1)=0 and

\[
H'(r)/p=(r+n-1)^{p-1}-r^{p-1}
 -(n^{p-1}-1)r^{p/n-1}.
\tag{4.7}
\]

First suppose n/(n-1)<=p<=2. Concavity of s -> (1+(n-1)s)^{p-1} on [0,1] gives

\[
(1+(n-1)/r)^{p-1}-1\ge (n^{p-1}-1)/r.
\]

Hence

\[
(r+n-1)^{p-1}-r^{p-1}
\ge(n^{p-1}-1)r^{p-2}
\ge(n^{p-1}-1)r^{p/n-1},
\tag{4.8}
\]

where the last step uses p>=n/(n-1). Unless n=p=2, at least one inequality is strict for r>1. This proves H(r)>0 there.

For p>=2, write

\[
(r+n-1)^{p-1}-r^{p-1}
=(p-1)\int_0^{n-1}(r+s)^{p-2}\,ds.
\tag{4.9}
\]

Weighted arithmetic-geometric mean, for 0<=s<=n-1 and r>=1, gives

\[
\frac{r+s}{1+s}\ge r^{1/(1+s)}\ge r^{1/n}.
\]

Therefore (4.9) is at least

\[
r^{(p-2)/n}(p-1)\int_0^{n-1}(1+s)^{p-2}\,ds
=(n^{p-1}-1)r^{(p-2)/n}
\ge(n^{p-1}-1)r^{p/n-1}.
\tag{4.10}
\]

The final exponent comparison uses n>=2. Again the result is strict for r>1 except n=p=2. This completes the global maximisation and the equality classification. QED.

The exponent range is sharp for this exact coefficient. If 1<p<n/(n-1), evaluating at (r,1,...,1) as r tends to infinity gives

\[
H(r)=p(n-1)r^{p-1}-(n^p-n)r^{p/n}+o(r^{p/n}),
\]

which is negative eventually because p/n>p-1.

## 5. Sharp reverse-erasure phase boundary

Set

\[
a_n=n^{-1/(n-1)},\qquad
c_0(n,a)=\frac{\log n}{\log(n/a)}.
\tag{5.1}
\]

**Theorem 5.1 (exact point-extremiser regime).** For every n>=2 and 0<a<=a_n,

\[
\eta_{\rm KL}(\mu_{n,a},R_n)=c_0(n,a).
\tag{5.2}
\]

Except for n=2,a=1/2, the only extremisers are the n point distributions on the ordinary input symbols. For a>a_n, every ordinary-symbol point distribution has ratio c_0(n,a), but

\[
\eta_{\rm KL}(\mu_{n,a},R_n)>c_0(n,a).
\tag{5.3}
\]

Thus a_n is the exact point-optimality threshold, including its endpoint.

*Proof.* A point distribution at an ordinary symbol has input divergence log(n/a) and output divergence log n, proving the lower bound c_0. Put p=1/c_0=log(n/a)/log n, so a=n^{1-p}. The condition a<=a_n is exactly p>=n/(n-1). Substituting this a into (3.3) and multiplying by n^p gives exactly (4.1). Lemmas 3.1 and 4.1 prove the upper bound.

For equality, first suppose the input puts positive mass on e. Its output then has full support. A nonuniform output gives strict inequality by the strict dual statement after Lemma 3.1 and the equality cases of Lemma 4.1. A uniform output has zero divergence, so cannot extremise unless its input is the reference, which is excluded. If the input gives e zero mass, write its ordinary-symbol law as q. Its ratio is

\[
\frac{D(q\|u_n)}{\log(1/a)+D(q\|u_n)}.
\]

This strictly increases with D(q||u_n), which is at most log n and equals log n only at a point distribution. This proves uniqueness away from n=2,a=1/2.

To prove failure above the threshold, choose the explicit input

\[
v_\epsilon=(1-\epsilon)\delta_1+\epsilon\delta_e,
\qquad 0<\epsilon<1.
\tag{5.4}
\]

With b=(n-1)/n, its input and output divergences satisfy

\[
D(v_\epsilon\|\mu_{n,a})
=\log(n/a)+\epsilon\log\epsilon+O(\epsilon),
\]

\[
D(v_\epsilon R_n\|u_n)
=\log n+b\epsilon\log\epsilon+O(\epsilon).
\tag{5.5}
\]

Consequently

\[
D(v_\epsilon R_n\|u_n)-c_0D(v_\epsilon\|\mu_{n,a})
=(b-c_0)\epsilon\log\epsilon+O(\epsilon).
\tag{5.6}
\]

For a>a_n we have c_0>b. Since epsilon log epsilon is negative and dominates epsilon in magnitude, (5.6) is strictly positive for all sufficiently small epsilon. QED.

This proof proves a threshold, not a discontinuity in the coefficient. Immediately above the threshold the improving epsilon may be very small; coarse numerical grids can therefore misidentify the boundary.

## 6. Complete binary formula

**Theorem 6.1.** For n=2 and 0<a<1,

\[
\eta_{\rm KL}(\mu_{2,a},R_2)=
\begin{cases}
\log2/\log(2/a),&0<a\le1/2,\\
a,&1/2\le a<1.
\end{cases}
\tag{6.1}
\]

For a<1/2, only the two ordinary-symbol point distributions extremise. For a>1/2, no nonreference input distribution attains the supremum. At a=1/2, all extremisers are

\[
v_s=(s^2,(1-s)^2,2s(1-s)),
\quad 0\le s\le1,\quad s\ne1/2,
\tag{6.2}
\]

where the coordinates list ordinary symbols 1,2 and then e.

*Proof.* The a<=1/2 coefficient and the a<1/2 equality cases follow from Theorem 5.1. The local chi-squared contraction coefficient is a for every n: perturb only the ordinary-symbol probabilities in a zero-sum direction, keeping the erasure mass fixed. More explicitly, let q_s=u_n+s h with sum h=0 and v_s=(a q_s,1-a). Then

\[
\frac{D(v_sR_n\|u_n)}{D(v_s\|\mu_{n,a})}
=\frac{D(u_n+a s h\|u_n)}{aD(u_n+s h\|u_n)}\longrightarrow a.
\tag{6.3}
\]

The matching local upper bound is also explicit. Write a mean-zero input density perturbation h as h_i=m+g_i on the ordinary symbols, with average_i g_i=0, and as h_e on e. Its mean-zero constraint is a m+(1-a)h_e=0. The output perturbation is a g_i. Hence its output-to-input variance ratio is

\[
\frac{a^2\operatorname{Var}_{u_n}(g)}
{a\operatorname{Var}_{u_n}(g)+a m^2+(1-a)h_e^2}\le a.
\]

Equality is possible by m=h_e=0. The second-order Taylor expansion of finite-alphabet relative entropy is uniform over normalised directions, so every sequence of input distributions approaching the reference has ratio limsup at most a. This proves that the local coefficient is exactly a, not merely at least a.

For a>=1/2, put p=1/a in [1,2]. By homogeneity and permutation, a positive binary vector in (3.3) can be written as (e^u,e^{-u}), u>=0. The required inequality is

\[
\cosh(pu)\le p\cosh(u)^p-p+1.
\tag{6.4}
\]

Both sides equal 1 at u=0. To compare derivatives it is enough to show

\[
\sinh(pu)\le p\sinh(u)\cosh(u)^{p-1}.
\]

Setting v=tanh u transforms this into

\[
(1+v)^p-(1-v)^p\le2pv.
\tag{6.5}
\]

The left side vanishes at v=0, and its derivative is

\[
p\{(1+v)^{p-1}+(1-v)^{p-1}\}\le2p
\]

by concavity of x^{p-1}. This proves (6.4), hence the coefficient upper bound a, matching (6.3).

For 1<p<2 the dual inequality is strict at every finite nonconstant test. An input assigning positive mass to e therefore cannot attain a unless it is the reference. If it assigns zero mass to e, its ratio is at most c_0(2,a), which is strictly smaller than a for 1/2<a<1: the strictly concave function a log(2/a) equals log2 at a=1/2 and at a=1, and exceeds log2 between them.

At a=1/2,p=2 the dual inequality is an identity. If the output law is (s,1-s), equality in the entropy variational formula forces the unique exponential tilt of mu by Rf/c, where f_i=log(2q_i). That tilt is exactly (6.2). Conversely, (6.2) produces output (s,1-s), and direct substitution gives

\[
D(v_s\|\mu_{2,1/2})=2D((s,1-s)\|u_2).
\]

The endpoint values follow by continuity. QED.

## 7. Resolution of the complete bipartite conjecture

**Theorem 7.1.** For every n>=3, the half-lazy random walk P_n on K_{n,n} satisfies

\[
\boxed{\eta_{\rm KL}(\pi_n,P_n)=\frac{\log n}{2\log(2n)}}.
\tag{7.1}
\]

Its only extremisers are the 2n point distributions.

*Proof.* Set c=log n/log(2n). Because 1/2<a_n for n>=3, Theorem 5.1 gives

\[
D(tq+(1-t)u_n\|u_n)
\le c\{d(t\|1/2)+tD(q\|u_n)\}.
\tag{7.2}
\]

At t=1/2 this yields

\[
D((q+u_n)/2\|u_n)\le\frac c2D(q\|u_n).
\tag{7.3}
\]

For every 0<=b<=1/2, express bq+(1-b)u_n as the convex combination

\[
2b\,(q+u_n)/2+(1-2b)u_n.
\]

Convexity of relative entropy and (7.3) imply

\[
D(bq+(1-b)u_n\|u_n)\le cbD(q\|u_n).
\tag{7.4}
\]

Represent a general input distribution on the two parts as v=(tq,(1-t)r). Swap the parts if needed so t>=1/2. The input divergence is

\[
D(v\|\pi_n)=d(t\|1/2)+tD(q\|u_n)+(1-t)D(r\|u_n).
\tag{7.5}
\]

After one step the two parts each have mass 1/2, with conditional laws

\[
tq+(1-t)u_n,\qquad (1-t)r+t u_n.
\tag{7.6}
\]

Apply (7.2) to the first law and (7.4), with b=1-t, to the second. Their average divergence is at most c/2 times (7.5), proving the upper bound.

For a point input, the output puts probability 1/2 at the initial vertex and probability 1/(2n) at each opposite-part vertex. Thus its divergence from pi_n is (1/2)log n, while its input divergence is log(2n). This attains (7.1).

For uniqueness, equality in (7.2) requires either its reverse-erasure input to be the reference or to be a point ordinary-symbol input, by Theorem 5.1. The second possibility forces t=1 and q to be a point, which yields a point distribution on K_{n,n}. The first forces t=1/2 and q=u_n. In that case any nonreference full input has r different from u_n; inequality (7.3) for r is strict, since its reverse-erasure input has positive erasure mass. Hence it cannot give equality. This proves the stated equality cases. QED.

**Binary boundary check.** The same coefficient formula gives eta=1/4 for K_{2,2}, and the upper-bound proof remains valid using Theorem 6.1. Its equality set needs separate analysis because the reverse-erasure step has the family (6.2). The conjecture concerns n>=3, so no binary equality statement is needed for its resolution.

**Spectral check.** P_n has eigenvalues 1, 1/2 with multiplicity 2n-2 and 0. Its local chi-squared coefficient is 1/4. Formula (7.1) exceeds 1/4 for n>2 and tends to 1/2 as n tends to infinity. This is consistent with point distributions, rather than perturbations of stationarity, governing worst-case entropy contraction.

## 8. Exact scalar characterisation at every retention probability

The phase boundary leaves a nonpoint regime for n>=3. The following gives an exact one-dimensional criterion, although it is not a closed form.

**Theorem 8.1.** Fix n>=2, 0<a<1 and 0<c<1, and put p=1/c>1. Then

\[
\eta_{\rm KL}(\mu_{n,a},R_n)\le c
\]

if and only if both

\[
a n^{p-1}\le1
\tag{8.1}
\]

and, for every r>=1,

\[
\frac an(r^p+n-1)+(1-a)r^{p/n}
\le\Big(\frac{r+n-1}{n}\Big)^p
\tag{8.2}
\]

hold. Condition (8.1) is also the r-to-infinity limit of (8.2). Thus one may equivalently impose (8.2) on the compactified interval [1,infinity].

*Proof.* Necessity follows by testing (3.3) on a vertex and on (r,1,...,1). For sufficiency, normalise sum z_i=1 in (3.3), multiply by n^p/(a n^{p-1}), and maximise

\[
\sum_i z_i^p+\frac{n(1-a)}a\Big(\prod_i z_i\Big)^{p/n}.
\]

The structural maximisation argument in Lemma 4.1 applies for every p>1 and every positive coefficient B, independently of the exponent restriction used later in that lemma. Every boundary maximum is a vertex. Every interior maximum is uniform or, up to permutation, has one large coordinate and n-1 equal small coordinates. The uniform vector gives equality automatically; (8.1) handles the boundary and (8.2) handles the remaining family. Lemma 3.1 completes the proof. QED.

For computation define

\[
\mathcal H_{n,a,p}(r)=
\frac{a n^{p-1}(r^p+n-1)+(1-a)n^p r^{p/n}}
{(r+n-1)^p}.
\tag{8.3}
\]

Then p_* = sup{p>1 : sup_{r>=1} H_{n,a,p}(r)<=1} and eta=1/p_*. This formula requires global maximisation on the scalar interval and care near r=1 and infinity; an unconstrained floating-point optimiser alone is not a certificate.

For n>=3 and a>a_n, the sharp coefficient is strictly above c_0 and hence strictly above a. The second inequality follows because log n>1 and the function a -> a log(n/a) increases strictly on (0,1), reaching log n only at a=1. Its supremum therefore cannot arise only from an infinitesimal perturbation of the reference.

At the sharp exponent p_* the vertex condition is strict, since eta>c_0. A nonuniform finite dual maximiser must therefore exist, and it has the form (r_*,1,...,1), r_*>1. It satisfies

\[
\mathcal H_{n,a,p_*}(r_*)=1,
\qquad \partial_r\mathcal H_{n,a,p_*}(r_*)=0.
\tag{8.4}
\]

One way to justify existence without importing an extremiser theorem is to maximise the primal ratio on the probability simplex with a small neighbourhood of the reference removed. The ratio extends continuously at every nonreference point, while every sequence approaching the reference has limsup at most the local chi-squared coefficient a. Because eta>a, a maximum occurs away from the reference. The corresponding output has full support: if its erasure mass were zero, its ratio would be at most c_0<eta. The finite output variational maximiser then supplies a finite dual equality vector. The maximisation argument yields the one-large-coordinate form.

The corresponding primal extremisers are exponentially tilted versions of mu_{n,a}. Given a finite dual extremiser z=(r,1,...,1), define

\[
Z=\frac an(r^p+n-1)+(1-a)r^{p/n}.
\]

Then, up to permutation of ordinary symbols,

\[
v_1=\frac{a r^p}{nZ},\quad
v_i=\frac{a}{nZ}\ (2\le i\le n),\quad
v_e=\frac{(1-a)r^{p/n}}Z.
\tag{8.5}
\]

All these coordinates are strictly positive. Formula (8.5), together with (8.4), characterises all nonreference extremisers in the nonpoint regime, without asserting uniqueness of r_* or of p/r stationary solutions. At an actual sharp equality point the output variational consistency follows from differentiating the dual inequality at its equality vector; alternatively it follows from the primal attainment argument above. To use (8.4) as a numerical construction one must still check the global inequality (8.2), because a stationary equality point alone is not sufficient.

## 9. Arbitrary output laws: exact scalar reduction and supercritical classification

This section extends the structural argument without assuming a uniform output law. The root agent is independently integrating the weighted mean inequality and weighted bipartite theorem; the source-dependent attribution for the weighted point-optimality result must be retained in the final manuscript.

Let rho=(rho_1,...,rho_n) have full support, n>=2, and let q=min_i rho_i. The reverse erasure channel R_rho maps ordinary symbol i to i and e to rho. Its input reference is

\[
m_{\rho,a}=(a\rho_1,\ldots,a\rho_n,1-a),
\]

and its output reference is rho. For a vector z, write G_rho(z)=product_i z_i^{rho_i}. The exact entropy dual criterion is

\[
a\sum_i\rho_i z_i^p+(1-a)G_\rho(z)^p
\le\Big(\sum_i\rho_i z_i\Big)^p,
\qquad p=1/c.
\tag{9.1}
\]

**Theorem 9.1 (finite scalar reduction for arbitrary prior).** For p>1, inequality (9.1) holds for every nonnegative z if and only if

\[
a q^{1-p}\le1
\tag{9.2}
\]

and, for every distinct weight w among rho_1,...,rho_n and every r>=1,

\[
a\{wr^p+1-w\}+(1-a)r^{pw}
\le(wr+1-w)^p.
\tag{9.3}
\]

Thus the sharp coefficient is determined by at most n one-dimensional branches, together with their boundary limits. No assertion is made that the smallest-weight branch is always the worst branch outside the point-optimality regime.

*Proof.* Normalise sum_i rho_i z_i=1 and maximise

\[
F(z)=\sum_i\rho_i z_i^p+B G_\rho(z)^p,
\qquad B=(1-a)/a>0.
\]

The feasible simplex is compact. On its boundary the geometric-mean term vanishes. The strictly convex power sum has its maximum at a vertex z_i=1/rho_i, z_j=0 for j different from i; the largest value is q^{1-p}. This gives (9.2).

At an interior stationary point, Lagrange differentiation and division by p rho_i gives

\[
z_i^{p-1}+T/z_i=\lambda,\qquad T=B G_\rho(z)^p.
\tag{9.4}
\]

As before there are at most two distinct values x<y, with

\[
T=xy\frac{y^{p-1}-x^{p-1}}{y-x}<(p-1)y^p.
\tag{9.5}
\]

If two or more coordinates equal y, choose a nonzero perturbation h supported on those coordinates with sum_i rho_i h_i=0. Its second directional derivative is

\[
\frac{p}{y^2}\{(p-1)y^p-T\}
\sum_i\rho_i h_i^2>0,
\tag{9.6}
\]

contradicting local maximality. Hence every nonuniform interior maximum has one large coordinate, say i, and a common smaller value on the remaining coordinates. Dividing by that common value gives z_i=r>1 and z_j=1 otherwise. Substitution yields (9.3) with w=rho_i. The uniform vector gives equality automatically. These possibilities exhaust all global maxima. QED.

**Corollary 9.2 (binary coarse-graining identity).** For every full-support rho and 0<a<1,

\[
\eta_{\rm KL}(m_{\rho,a},R_\rho)
=\max_i\eta_{\rm KL}(m_{(\rho_i,1-\rho_i),a},R_{(\rho_i,1-\rho_i)}).
\tag{9.7}
\]

*Proof.* A dual test function constant on the complement of {i} lifts each test function for the binary coarse-graining to a test for the original channel. Thus the original coefficient is at least every binary coefficient. Conversely, if c bounds all those binary coefficients, every one-large-coordinate test (9.3) satisfies the dual inequality, including its boundary limit. Theorem 9.1 then proves the original coefficient is at most c. QED.

This identity is an exact reduction, not a statement that the prior is equivalent to its smallest atom. The binary coefficients still depend on both entries, and maximisation over i remains part of the statement. Its historical status requires the same prior-art check as the other entropy consequences.

**Weighted point threshold (to be integrated with the independently checked mean theorem).** The weighted mean inequality with minimum weight q gives

\[
a_c(\rho)=q^{q/(1-q)},\qquad
c_0(\rho,a)=\frac{\log(1/q)}{\log(1/(aq))},
\tag{9.8}
\]

and

\[
\eta_{\rm KL}(m_{\rho,a},R_\rho)=c_0(\rho,a)
\quad\hbox{for }0<a\le a_c(\rho).
\tag{9.9}
\]

Above a_c, point masses cease to optimise. The proof of this necessity is independent of the weighted mean theorem: choose an atom of weight q and use input (1-epsilon)delta_i+epsilon delta_e. The output has total mass (1-q)epsilon outside i. Expanding as in (5.5) gives

\[
D(v_\epsilon R_\rho\|\rho)
-c_0D(v_\epsilon\|m_{\rho,a})
=(1-q-c_0)\epsilon\log\epsilon+O(\epsilon).
\tag{9.10}
\]

The coefficient 1-q-c_0 is negative exactly when a>a_c, so these explicit perturbations beat every point input in that regime. The smallest atom gives the largest point ratio because x/(x+log(1/a)) strictly increases with x=log(1/rho_i).

**Proposition 9.3 (strictly nonlocal contraction except the uniform binary law).** Unless rho=(1/2,1/2), the reverse-erasure coefficient is strictly greater than a for every 0<a<1.

*Proof.* For any real g with E_rho g=0, define an input perturbation

\[
v_s=(a\rho_i(1+s g_i))_{i=1}^n\oplus(1-a),
\]

for s sufficiently small to preserve positivity. Its output is (rho_i(1+a s g_i))_i. If V=E g^2>0 and M=E g^3, the Taylor expansion of relative entropy gives

\[
\frac{D(v_sR_\rho\|\rho)}{D(v_s\|m_{\rho,a})}
=a\left\{1+(1-a)\frac{M}{3V}s+O(s^2)\right\}.
\tag{9.11}
\]

If M is nonzero, choose the sign of s to make the linear correction positive. Such a g exists unless the prior is the uniform binary law: choose an event A with weight w different from 0,1/2,1, and put g=1_A-w. Then M=w(1-w)(1-2w), which is nonzero. For a nonuniform binary law a singleton is such an event. For every law with at least three positive atoms, at least one singleton has weight strictly between 0 and 1/2. QED.

The local coefficient itself is exactly a. To see the upper bound, write an arbitrary mean-zero input density perturbation as h_i=m+g_i on the ordinary symbols, with E_rho g=0, and h_e on e. Then a m+(1-a)h_e=0, the output perturbation is a g_i, and its variance ratio is

\[
\frac{a^2 E_\rho g^2}
{a E_\rho g^2+a m^2+(1-a)h_e^2}\le a.
\tag{9.12}
\]

The lower bound follows by taking m=h_e=0. Uniform second-order Taylor expansion on the finite-dimensional unit sphere then bounds the limsup of any sequence approaching the reference by a.

**Corollary 9.4 (supercritical attainment and shape).** Suppose rho is not the uniform binary law and a>a_c(rho). Then

\[
\eta_{\rm KL}(m_{\rho,a},R_\rho)>
\max\{a,c_0(\rho,a)\}.
\tag{9.13}
\]

The supremum is attained. Every extremising input has full support. Every corresponding finite nonconstant dual extremiser has, up to a scalar multiple, one large coordinate r>1 and all other coordinates equal to 1.

*Proof.* The strict point bound follows from (9.10), and the strict local bound from Proposition 9.3. The ratio is continuous at all nonreference input laws. Every sequence approaching the reference has limsup at most a, so compactness gives an attained maximum away from the reference.

An input with zero erasure mass, having ordinary-symbol law v, has ratio

\[
\frac{D(v\|\rho)}{\log(1/a)+D(v\|\rho)}
\le c_0,
\]

because D(v||rho)<=log(1/q). Thus an extremiser has positive erasure mass, giving a strictly positive output. Its output entropy variational maximiser f=log((vR_rho)/rho) is finite. Equality in the input variational formula forces v to be the unique exponential tilt of the positive reference m_{rho,a}; consequently every input coordinate is positive. The resulting dual equality vector is an interior global maximum, and Theorem 9.1 supplies its one-large-coordinate shape. QED.

For a branch with high-coordinate weight w=rho_i, the dual ratio is

\[
H_{w,a,p}(r)=
\frac{a(wr^p+1-w)+(1-a)r^{pw}}{(wr+1-w)^p}.
\tag{9.14}
\]

At a supercritical optimum it equals 1 and has derivative zero at some finite r>1. The associated input tilt is

\[
Z=a(wr^p+1-w)+(1-a)r^{pw},
\]

\[
v_i=\frac{a w r^p}{Z},\quad
v_j=\frac{a\rho_j}{Z}\ (j\ne i),\quad
v_e=\frac{(1-a)r^{pw}}Z.
\tag{9.15}
\]

Global verification of every branch in (9.3) is still necessary to certify a numerical candidate. The theorem does not prove uniqueness of the branch or of the scalar stationary point.

## 10. Priority and proof-audit boundaries

The following points require explicit treatment in a final paper and report.

1. The complete bipartite walk must be the half-lazy walk of (2.4), matching Definition 2.4 and Example 4.4 of the source. A non-lazy convention would invalidate the stated result.
2. Gao's exact formula-level collision must be credited. The result does not introduce the arithmetic-geometric-power-mean inequality.
3. The reverse-erasure theorem should be searched under reverse erasure, Bayesian erasure, strong data processing, contraction coefficients, entropy contraction, hypercontractivity and mean inequalities.
4. The n=2,a=1/2 equality family is an exception, not a minor endpoint detail.
5. The n>=3 nonpoint regime has an exact scalar characterisation. A closed elementary expression or uniqueness of its scalar maximiser has not been proved here.
6. Numerical experiments should test random full-simplex inputs as well as the reduced scalar formula, several n and a values, rare-erasure perturbations near the phase boundary, and equality cases. Their role is to catch implementation or algebra errors, not to replace the proof.
7. This working draft establishes a research candidate. Any assessment of significance requires a review of prior art beyond correctness.

