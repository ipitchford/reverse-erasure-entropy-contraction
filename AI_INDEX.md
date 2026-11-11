# AI_INDEX: entropy contraction via reverse erasure

Machine- and human-readable index of this package. Paths are relative to the package root. Version 0.1.1-candidate, revised 11 November 2026 (abstract wording correction; see `CORRECTIONS.md`).
Status: unrefereed research candidate; internal AI-assisted review only; no human peer review; no formal proof.

## Claims (where stated, where proved, how checked)

| ID | Claim | Paper location | Status | Numerical evidence |
|---|---|---|---|---|
| C1 | Reverse-erasure coefficient depends on the prior only through its smallest atom q, for every retention alpha | Thm 2.3, proof in Sec. 3 | New (bounded search) | `verification/negative_controls.py` (tilt and brute force for equal-q priors); `verification/verify_minimum_mass.py` |
| C2 | Exact one-variable criterion H_{q,alpha,p}(r) <= 1; dual extremisers have one large coordinate at a rarest atom | Prop. 2.4, Sec. 3 | New | `verify_minimum_mass.py` (envelopes, moments) |
| C3 | eta = log(1/q)/log(1/(alpha q)) for alpha <= q^(q/(1-q)), point extremisers only; sharp threshold | Thm 2.5, Sec. 4 | Upper bound = Gao's inequality (known); sharpness and general-prior form new | `validate_entropy.py`; controls in `negative_controls.py` |
| C4 | Local coefficient alpha; eta < 1; eta > alpha except uniform binary with alpha >= 1/2 | Prop. 2.6, Sec. 5 | New for general priors | - |
| C5 | Above the threshold: attainment, full support, exponential tilt from the tangency system; converse | Thm 2.7, Sec. 5 | New | `negative_controls.py` (tilt reproduces scalar value to >20 digits) |
| C6 | How small eta - c_0 is just above the threshold (numerical observation, not a theorem) | Remark 5.2, Table 2 | Observation | `negative_controls.py`, family `near_threshold_excess_eta_minus_c0` |
| C7 | Half-lazy rank-one bipartite chain: eta = log(1/q)/(2 log(2/q)); K_{m,n}: log M/(2 log 2M); point extremisers only for q < 1/2; proves the Caputo-Chen-Gu-Polyanskiy conjecture | Thm 6.1, Sec. 6 | Conjecture known; proof new | `validate_entropy.py` (88,736 full-matrix inputs) |
| C8 | Lazy star K_{1,N}: log N/(2 log 2N), leaf point masses only for N >= 3 (settles Jadhav 2026, Remark 9.6); any laziness reduces to three states (Remark 7.8) | Cor. 6.2, Rem. 7.8 | New | C7 checks; `extension_checks.py` (star_half_lazy, star_lazy_s_reduction) |
| C9 | Block-reset reduction: the coefficient of any block-reset chain equals that of a chain with at most two states per block (laziness, powers, stars, multipartite graphs); values there are computed numerically | Thm 7.4, Cor. 7.6, 7.9, Prop. 7.10, Rem. 7.11 | New | `verification/extension_checks.py` (24 random chains full vs collapsed; laziness grid; powers; multipartite; 5 controls) |
| C10 | Exact one-way agreement-distillation rate log(1/alpha)/log(1/(alpha q)) below the threshold (vanishing-error model) | Cor. 8.1, Sec. 8 | Uniform binary case known (Zhao); general prior new | - |

## Inherited results (not claimed)

Gao's weighted mean inequality (Lemma 4.1; Gao 2003, 2009); the uniform binary coefficient (Appendix A; Nair-Wang
2016, Zhao 2021); KL tensorisation (Appendix B); entropy duality; the one-large-coordinate idea in primal form
(Gu-Polyanskiy 2023, Prop. 17); the SDPI-to-agreement connection (Zhao 2021, Ch. 3).

## Files

### Paper
- [`entropy_contraction.pdf`](entropy_contraction.pdf) - compiled paper (start here).
- [`manuscript.tex`](manuscript.tex) - source; [`block_reset.tex`](block_reset.tex) - Section 7 source;
  [`refs.bib`](refs.bib) - bibliography.
- [`figures/exact_coefficients.png`](figures/exact_coefficients.png) from [`make_figure.py`](make_figure.py):
  proved formulas only, with K_{n,n} points marked.

### Orientation
- [`README.md`](README.md) - summary, read order, reproduction commands that cannot overwrite recorded outputs.
- [`REVIEW_SUMMARY.md`](REVIEW_SUMMARY.md) - internal review findings and how the revision responds.
- [`VERIFICATION.md`](VERIFICATION.md) - analytic and numerical verification record, script hashes, run details.
- [`LICENSE.md`](LICENSE.md) - CC0-1.0 for text and data, MIT for code.

### Verification code and outputs
- [`verification/validate_entropy.py`](verification/validate_entropy.py) - random-sample suite; 101 gates.
- [`verification/verify_minimum_mass.py`](verification/verify_minimum_mass.py) - minimum-mass envelopes and
  fixed-means moments; reports informative-case counts (143 of 256; 111 vacuous, 2 vertex-limited).
- [`verification/negative_controls.py`](verification/negative_controls.py) - 10 must-fail controls, structured
  families, near-threshold table; 56 gates.
- [`verification/extension_checks.py`](verification/extension_checks.py) - Section 7 checks; 122 checks and 5
  must-fail controls. Reported coefficients are numerical estimates without certified error bounds.
- [`verification/results/2026-11-03/`](verification/results/2026-11-03/) - recorded JSON, stdout, stderr and exit
  status for each of the four scripts, under `standard/` and `optimize_O/`.
- [`verification/results/2026-11-01_original/`](verification/results/2026-11-01_original/) - first-version outputs.
- [`prepare_fingerprints.py`](prepare_fingerprints.py), [`fingerprints.json`](fingerprints.json),
  [`target.yaml`](target.yaml) - exact rational kernels and the normalised research target.

### Sources and provenance
- [`refs_records/`](refs_records/) - Crossref/DataCite JSON and arXiv XML for every reference
  ([`refs_records/README.md`](refs_records/README.md) lists two non-bibliographic fields removed for deposit);
  [`refs_records/ccgp_numbering_check.md`](refs_records/ccgp_numbering_check.md) - numbering in both versions of
  Caputo et al.; [`refs_records/zhao2021_titlepage.txt`](refs_records/zhao2021_titlepage.txt).
- [`novelty_gate_report.md`](novelty_gate_report.md), [`novelty_audit.md`](novelty_audit.md) - prior-art gate and
  audit (1 November), with 3 November addenda (Jadhav, Gu-Polyanskiy, Guruswami-Radhakrishnan, Bogdanov-Mossel,
  Anantharam et al.).
- [`proof_digest.md`](proof_digest.md) - informal proof outline and claim ledger for the 1 November version.
- [`development_notes/`](development_notes/) - preserved working proofs: uniform draft, weighted extension,
  rarest-branch reduction, agreement application, independent audit. Superseded by the paper.
- [`logs/`](logs/) - LaTeX build logs (local paths shortened) and verification provenance (1 and 3 November).
- [`original_manifest.json`](original_manifest.json) - hashes of 1 November development inputs and the list of
  changes made for the public package.
- [`CITATION.cff`](CITATION.cff), [`.zenodo.json`](.zenodo.json) - citation and deposit metadata (DOI 10.5281/zenodo.24142198; 0.1.0-candidate: 10.5281/zenodo.23921825).
- [`CORRECTIONS.md`](CORRECTIONS.md) - dated corrections between versions.
- [`RESEARCH_GATES.json`](RESEARCH_GATES.json) - machine-readable prior-art contribution map, limitation triage and extension scout.
- [`requirements.txt`](requirements.txt), [`.github/workflows/replay.yml`](.github/workflows/replay.yml) - pinned numerical
  libraries and the CI replay.
- [`MANIFEST.sha256`](MANIFEST.sha256) - SHA-256 of every file except itself.

## Open problems (Section 9 of the paper)

Uniqueness and asymptotics above the threshold; the laziness and matrix-power phase diagram; non-rank-one cross
weights; half-step and MLSI constants for the same family; agreement rate above the threshold and sample
efficiency; the reference-optimised coefficient.
