# Review summary (internal, AI-assisted)

**What this is.** A plain summary of the internal review of this paper on 3 November 2026: the round-1 objections
to the 1 November manuscript, how the revision responded, and the verification round on the revision. All
reviewers were AI agents. **This is not human peer review**, and nothing here is a formal proof certificate.

## Round 1: who reviewed and what they found

| Role | Focus | Verdict |
|---|---|---|
| Editor | Fit, originality, structure, readability for non-specialists | Minor revision (mainly exposition) |
| Methodology | Line-by-line proofs; the verification scripts | Minor revision; no mathematical error found |
| Domain | Literature placement and attribution; prior-art search | Minor revision; missing references |
| Perspective | Who can use the result; framing; extensions | Minor revision; framing and context |
| Devil's advocate | Attempts to break every main claim | No critical or major correctness gap |
| Adversarial checker (separate model) | Six targeted correctness checks | No critical or major gap; one convention fix |

Every main theorem was independently reproduced numerically (direct optimisation, 50- to 400-digit arithmetic),
and a clean replay of the shipped scripts reproduced the recorded counts.

## Round-1 objections and responses

| Objection | Response |
|---|---|
| The introduction gave no context, no reason the conjecture mattered and no proof idea | New introduction: why contraction coefficients matter; why the conjecture was posed (which inputs are worst, not mixing speed); the one-paragraph idea; results table; roadmap; notation table; worked K_{3,3} example; figure moved to page 3 |
| The new content was not separated from inherited results | Section 1.4 states that, given Gao's inequality, the conjecture needs only the uniform case at retention 1/2 and the two-part decomposition, and lists what is new |
| Theorem statements were bundled and used forward references | Statements made self-contained and split; a plain-English sentence follows each main result |
| Several proof steps were compressed | Written out: the fixed-means elimination, both directions of duality, the uniform second-order step and gradient step, singleton parts and part interchange, the interval property, the communication model (fixed-length messages, private randomness, large-k conditions, tensorised converse), the conditional independences in Appendix B; overloaded symbols renamed |
| Missing literature, including a 2026 preprint leaving the lazy star open | Added Jadhav (2026), now settled as Corollary 6.2; Gu-Polyanskiy; Guruswami-Radhakrishnan and Bogdanov-Mossel with the model difference stated; Anantharam et al.; Raginsky's DOI; standard SDPI references; Caputo et al. numbering checked in both versions; every reference copied from its registry record |
| The main script used `assert` gates and a fixed "passed" status, so `python -O` disabled it, and it overwrote its record | All scripts now collect failures explicitly, compute their status, exit 1 on failure, refuse to overwrite and record their own hash |
| The random tests had little power near the sharp boundaries | New negative controls (ten false claims, all detected; the random sampler alone catches three) and structured near-extremiser families |
| Agreement distillation was unmotivated; laziness, powers and multipartite graphs were untouched | Section 8 motivated and compared with the opposite direction; new Section 7 extends the reduction to block-reset chains (any laziness, powers, stars, multipartite graphs) |

## Verification round on the revision

An AI verification re-review, an AI proof audit and an independent adversarial audit read the revised paper,
including the new Section 7, line by line and reproduced its numbers independently. They found the mathematics
correct and every round-1 item addressed. Remaining points were editorial or packaging, all fixed in the final
round:

- the distributed PDF was a stale build with a placeholder Section 7, and the manifest was stale - rebuilt and
  regenerated;
- the Section 7 numerical script was not shipped - now `verification/extension_checks.py`, with normal and `-O`
  runs recorded;
- a sign slip in the Theorem 6.1 proof (two signs cancelled; the conclusion was right) - corrected;
- numerical wording in Section 7 implied certified lower bounds - now "numerical estimates" without certified
  error bounds, in the paper and the script;
- the lazy star appeared twice; Section 7 notation clashed with Sections 3 and 6; drafting history appeared in a
  remark; the s_- values lacked their n; the four-state corollary omitted the two-singleton case; the multipartite
  corollary needed r >= 2; a hypothesis was placed on both parts of a proposition when only one needed it - all
  fixed;
- the count of informative envelope cases was overstated (196) - reclassified with a tolerance; 143 informative;
- two literature descriptions were imprecise, and the opposite-direction comparison in Remark 8.2 overstated what
  is known above the threshold - reworded;
- local paths and build intermediates in the package - removed; logs keep shortened paths.

## What remains open

Uniqueness and asymptotics above the threshold; the laziness phase diagram and closed forms for powers and
multipartite graphs; non-rank-one weights; the half-step and continuous-time constants for the same family; the
agreement rate above the threshold and its sample cost; the reference-optimised coefficient. Priority rests on a
bounded search.
