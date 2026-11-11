# Entropy contraction on complete bipartite graphs via reverse erasure

**Status:** unrefereed research candidate, prepared with AI assistance. Internal AI-assisted review only; no human
peer review; no formal (proof-assistant) proof. Numerical diagnostics are evidence, not proofs.
Version 0.1.1-candidate, revised 11 November 2026 (see `CORRECTIONS.md`). Author: Anonymous. Text CC0-1.0, code MIT (see `LICENSE.md`).

## The result in three sentences

Caputo, Chen, Gu and Polyanskiy conjectured that one step of the half-lazy random walk on the complete bipartite
graph K_{n,n} keeps at most the fraction log n / (2 log 2n) of relative entropy, with single vertices as the only
worst starts; they proved n = 3 by computer. This paper proves it for every n (and for K_{m,n}, rank-one weights and
the lazy star), by noticing that one step of the walk is two copies of the *reverse-erasure* channel: a visible
symbol passes through unchanged and a blank (erased with probability 1 - alpha) is redrawn from a prior. For that channel the contraction coefficient
depends on the prior only through its rarest symbol, at every alpha, with the closed form
log(1/q) / log(1/(alpha q)) up to the sharp threshold alpha = q^(q/(1-q)).

What is inherited: the weighted mean inequality behind the closed form is Gao's; the uniform binary case is known
(Nair-Wang; Zhao). What is new is listed in Section 1.4 and Table 1 of the paper.

## Read in this order

1. **`entropy_contraction.pdf`** - the paper. Section 1 gives context, the proof idea, a results table and a worked
   K_{3,3} example; Section 10 states how the work was checked.
2. **`REVIEW_SUMMARY.md`** - what the internal review round found and what the revision changed.
3. **`VERIFICATION.md`** - what was checked analytically and numerically, and how to reproduce it.
4. **`AI_INDEX.md`** - a linked index of every file, for readers and agents.
5. **`proof_digest.md`** - an informal proof outline and claim ledger (written for the 1 November version).
6. **`novelty_gate_report.md`**, **`novelty_audit.md`** - prior-art gate and source-by-source audit, with a
   3 November addendum.

## How to reproduce without overwriting the recorded outputs

The recorded outputs live in `verification/results/` and beside `prepare_fingerprints.py`. Every script now
requires `--output-dir` and **refuses to overwrite an existing output file**, so a rerun cannot replace the record.
Run from any scratch directory, pointing at a new, empty output directory:

```bash
PKG=/path/to/this/package          # absolute path
mkdir -p /tmp/ent-rerun && cd /tmp/ent-rerun
uv run --with numpy --with scipy --with mpmath python3 -I -B "$PKG/verification/validate_entropy.py"    --output-dir /tmp/ent-rerun/validate
uv run --with numpy --with scipy --with mpmath python3 -I -B "$PKG/verification/verify_minimum_mass.py" --output-dir /tmp/ent-rerun/minmass
uv run --with numpy --with scipy --with mpmath python3 -I -B "$PKG/verification/negative_controls.py"   --output-dir /tmp/ent-rerun/controls
uv run --with numpy --with scipy --with mpmath python3 -I -B "$PKG/verification/extension_checks.py"    --output-dir /tmp/ent-rerun/extension
uv run python3 -I -B "$PKG/prepare_fingerprints.py" --output-dir /tmp/ent-rerun/fingerprints
```

Each script exits 0 only if every gate passes, 1 if any gate fails, 2 if asked to overwrite (`extension_checks.py`
refuses any existing output directory). Adding `-O` after `python3` must give the same results (the scripts contain
no `assert`). Runtimes are about 1, 1, 25 and 75 seconds. Compare your JSON with the recorded files: everything
except the elapsed time and the optimisation flag should match, up to last-digit floating-point differences across
platforms.

To rebuild the figure and the paper (TeX Live with pdfLaTeX and BibTeX), work in a copy so that no build
intermediates enter the package:

```bash
cp -R "$PKG" /tmp/ent-build && cd /tmp/ent-build
uv run --with matplotlib --with numpy python3 -I -B make_figure.py      # rewrites figures/exact_coefficients.png
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
cp manuscript.pdf entropy_contraction.pdf
```

The distributed PDF `entropy_contraction.pdf` is `manuscript.pdf` from exactly this sequence (pdflatex, bibtex,
pdflatex twice; 27 pages). The figure plots proved formulas only. Build logs (with local paths shortened) are in
`logs/`.

## Files

| Path | Purpose |
|---|---|
| `manuscript.tex`, `block_reset.tex`, `refs.bib` | LaTeX source of the paper (Section 7 is `block_reset.tex`); bibliography |
| `entropy_contraction.pdf` | Compiled paper |
| `figures/exact_coefficients.png`, `make_figure.py` | Figure 1 and its script |
| `verification/validate_entropy.py` | Random-sample suite (graphs, mean inequalities, channels, witnesses) |
| `verification/verify_minimum_mass.py` | Minimum-mass reduction diagnostics, with informative-case counts |
| `verification/negative_controls.py` | Ten must-fail controls and structured near-extremiser families |
| `verification/extension_checks.py` | Numerical checks for Section 7 (block-reset chains): 122 checks, 5 must-fail controls |
| `verification/results/2026-11-03/` | Recorded outputs of the four scripts, normal and `-O` runs |
| `verification/results/2026-11-01_original/` | Outputs of the first version (kept for comparison) |
| `prepare_fingerprints.py`, `fingerprints.json`, `target.yaml` | Exact small kernels and normalised research target |
| `refs_records/` | Crossref, DataCite and arXiv records for every reference (two non-bibliographic fields removed; see `refs_records/README.md`); Caputo et al. numbering check |
| `development_notes/` | Preserved working proofs and audits; the paper supersedes them |
| `logs/` | Build and verification provenance |
| `original_manifest.json` | Hashes of the 1 November development inputs, and the list of public-package changes |
| `CITATION.cff`, `.zenodo.json` | Citation and deposit metadata |
| `RESEARCH_GATES.json` | Machine-readable prior-art map, limitation triage and extension scout |
| `requirements.txt`, `.github/workflows/replay.yml` | Pinned NumPy/SciPy/mpmath versions and the CI replay (quick checks blocking; slow suites non-blocking) |
| `MANIFEST.sha256` | SHA-256 of every file in the package except itself |

## How to cite

Anonymous (2026). *Entropy contraction on complete bipartite graphs via reverse erasure: only the rarest symbol matters*. Version 0.1.1-candidate. Unrefereed research candidate. Zenodo.
https://doi.org/10.5281/zenodo.24142198

All versions: https://doi.org/10.5281/zenodo.23921824. Release page: https://evidencepress.org/releases/reverse-erasure-entropy-contraction/.
Machine-readable citation metadata: `CITATION.cff`.

## Boundaries

No paper has been submitted to a journal or sent to an author. This version is deposited on Zenodo with DOI
[10.5281/zenodo.24142198](https://doi.org/10.5281/zenodo.24142198) (version 0.1.0-candidate: [10.5281/zenodo.23921825](https://doi.org/10.5281/zenodo.23921825)) (Section 10 of the paper).
Priority rests on a bounded literature search.
