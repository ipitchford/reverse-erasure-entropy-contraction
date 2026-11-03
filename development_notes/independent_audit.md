# Independent entropy audit and extensions

Date: 1 November 2026. Prepared by the optimisation scout for the root research agent.

## 1. KL duality audit

Let a channel K send input law pi to output law u. The inequality

    D(rho K || u) <= c D(rho || pi)  for every rho

is equivalent to

    E_pi exp((K f)/c) <= (E_u exp f)^(1/c)  for every real f.

Indeed, the variational formula for relative entropy gives

    D(rho K||u) = sup_f [E_rho Kf - log E_u exp f].

The asserted entropy bound holds for every rho iff, for every f,

    sup_rho [E_rho Kf - cD(rho||pi)] <= log E_u exp f.

The supremum on the left equals c log E_pi exp(Kf/c). This establishes both directions and fixes the exponent conventions.

For the reverse erasure channel, inputs are {*,1,...,n}; pi(*)=1-alpha and pi(i)=alpha/n. K(*)=u_n and K(i)=delta_i. Put p=1/c and z_i=exp f_i. Its dual inequality is

    (1-alpha) G(z)^p + (alpha/n) sum_i z_i^p <= (sum_i z_i/n)^p.

At alpha=n^(1-p), this is exactly

    sum_i z_i^p + (n^p-n) G(z)^p <= (sum_i z_i)^p.

For alpha=1/2 the exponent is p=log(2n)/log n. This gives the root agent's R(t,nu) with c=log n/log(2n), because rho(*)=1-t and rho(i)=t nu_i imply

    D(rho||pi)=d(t||alpha)+tD(nu||u_n).

No sign or normalisation defect was found.

## 2. Exact unbalanced complete-bipartite coefficient

Let m,n>=1 and let P be the one-half-lazy simple random walk on K_{m,n}. Let pi be the degree-stationary law: each side has mass 1/2, with uniform conditional law on that side. Put M=max(m,n). Then

    eta_KL(pi,P)=log M/[2 log(2M)],

interpreting the expression as zero if M=1.

Write an arbitrary input rho=(t nu_m,(1-t)nu_n), and abbreviate H_j(nu)=D(nu||u_j). One step produces side masses exactly 1/2, and

    D(rho||pi)=d(t||1/2)+t H_m(nu_m)+(1-t) H_n(nu_n),
    D(rho P||pi)=1/2 [H_m(t nu_m+(1-t)u_m)
                    +H_n((1-t)nu_n+t u_n)].

Set c_j=log j/log(2j) for j>=2, c_1=0, and c=c_M. By swapping sides, suppose t>=1/2. The reverse-erasure inequality gives

    H_m(t nu_m+(1-t)u_m) <= c_m[d(t||1/2)+tH_m(nu_m)].

For 0<=a<=1/2, convexity of relative entropy and R(1/2,nu) give

    H_j(a nu+(1-a)u_j)
      <=2a H_j((nu+u_j)/2)
      <=a c_j H_j(nu).

If j=1 both sides vanish. Apply this with a=1-t to the lighter side, then use c_m,c_n<=c. The result is D(rho P||pi)<=cD(rho||pi)/2. A point mass in a side of size M has input divergence log(2M) and output divergence (log M)/2, so the upper bound is exact.

This extension is not restricted to regular graphs. The stationary law is not uniform across all m+n vertices unless m=n.

### Extremisers when M>=3

Assume the sharp mean inequality is strict for positive nonconstant z when n>=3, with boundary equality only at a coordinate vector. Then the reverse-erasure inequality is strict for any nontrivial input with t<1: its output has full support, so the entropy variational optimiser is a finite nonconstant f; the mean inequality is then strict. With t=1, equality is equivalent to D(nu||u_n)=log n, hence nu is a point mass. Thus, for M>=3, all nontrivial extremisers of the bipartite channel are point masses in a largest side. If m=n, every vertex is an extremiser. If m<n, only vertices in the n-side are extremisers.

The dimension-two reverse-erasure exception cannot create further extremisers when M>=3 because c_2<c_M.

## 3. Dimension-two equality family

For n=2, alpha=1/2 and p=2, the mean identity is exact for all z:

    z_1^2+z_2^2+2z_1z_2=(z_1+z_2)^2.

The Gibbs equality condition in duality yields all reverse-erasure equality laws

    rho=(q^2,(1-q)^2,2q(1-q)), 0<=q<=1,

with the erasure mass last. Their output law is (q,1-q). The value q=1/2 is the reference input and has zero divergence; all other q give ratio 1/2.

Consequently, for K_{2,2}, eta=1/4 and all nontrivial equality laws, up to swapping sides and permuting within sides, are

    (q^2,(1-q)^2,q(1-q),q(1-q)), q in [0,1] excluding 1/2.

For K_{1,2}, eta=1/4 and the equality family is

    (q^2,(1-q)^2,2q(1-q)),

where the first two entries are the leaves and the last entry is the singleton side.

To check completeness: in the heavier-side proof, t>=1/2. If t<1, strict convexity in the lighter-side bound forces its conditional law to be uniform whenever t>1/2; at t=1/2 the reverse-erasure equality condition itself forces both conditionals to be uniform. The heavy reverse-erasure equality condition gives t=q^2+(1-q)^2 and the displayed law.

## 4. Synchronous products

Let (pi_j,P_j), j=1,...,d, be any of the preceding chains, and let pi=product pi_j and P=tensor product P_j. Standard relative-entropy tensorisation gives

    eta_KL(pi,P)=max_j eta_KL(pi_j,P_j).

For completeness, under an arbitrary joint input X and independent coordinate channels X_j->Y_j,

    D(Law(Y)||product pi_j)
      =sum_j E[D(Law(Y_j|Y_<j)||pi_j)]
      <=eta_max sum_j E[D(Law(X_j|Y_<j)||pi_j)]
      <=eta_max sum_j E[D(Law(X_j|X_<j)||pi_j)]
      =eta_max D(Law(X)||product pi_j).

The second inequality is conditional Jensen/data processing: given Y_<j, the law of X_j is a mixture of its laws given X_<j. Equality of constants follows by varying only a coordinate that attains eta_max and leaving all others stationary. This is a corollary of known tensorisation, not a new general tensorisation theorem.

Do not claim the analogous random-scan bound is exact merely by convexity. It generally is not.

## 5. Caution on powers

For a bipartite one-half-lazy chain, P^2 is strictly positive. Therefore point masses are not nontrivial maximisers for P^k when k>=2: mix an atom with epsilon of a full-support law. The positive output makes output divergence differentiable at epsilon=0, whereas input divergence decreases by a leading epsilon log epsilon term. The ratio therefore initially increases. The one-step point-extremiser theorem must not be extrapolated to powers.

## 6. Audit of the general-exponent scalar inequality

The probability scout's self-contained extension uses

    F(r)=(r+n-1)^p-r^p-(n-1)-(n^p-n)r^(p/n), r>=1.

For n/(n-1)<=p<=2, write q=p-1. The ratio

    [(r+n-1)^q-r^q]/[n^q-1]

is a weighted average of ((r+s)/(1+s))^(p-2), 0<=s<=n-1. Since (r+s)/(1+s)<=r and p-2<=0, it is at least r^(p-2), which is at least r^(p/n-1) precisely when p>=n/(n-1). Thus F'(r)>=0.

For p>=2, weighted arithmetic-geometric mean gives

    (r+s)/(1+s)>=r^(1/(1+s))>=r^(1/n).

Therefore the same ratio is at least r^((p-2)/n)>=r^(p/n-1), using n>=2. Again F'(r)>=0. Strictness holds for r>1 except when n=p=2. This independently verifies the most delicate scalar comparison in the extension.

## Inspected primary sources

- Gao, P. (2007 preprint; published 2009). On an inequality of Diananda, IV. Theorem 1.2, Eq. (1.4). https://rgmia.org/papers/v10n4/AGinequality4rgmia.pdf ; published DOI https://doi.org/10.1155/2009/468290
- Caputo, P., Chen, Z., Gu, Y., & Polyanskiy, Y. Entropy contractions in Markov chains: Half-step, full-step and continuous-time. Example 4.4 and Proposition 4.5. https://people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf ; https://arxiv.org/abs/2409.07689
- Raginsky, M. (2016). Strong data processing inequalities and Phi-Sobolev inequalities for discrete channels. IEEE Transactions on Information Theory, 62(6), 3355-3389. https://arxiv.org/abs/1411.3575 (abstract inspected; tensorisation proof supplied independently above).

## Bounded novelty searches

Searched the public web on 1 November 2026 for exact title and variants of 'complete bipartite contraction coefficient entropy', 'K_{m,n} entropy contraction', and 'complete bipartite log(2 entropy Caputo'. The directly relevant result found was Caputo et al.'s balanced K_{n,n} conjecture and n=3 theorem. No unbalanced exact coefficient surfaced. This is bounded negative evidence, not proof of priority.
