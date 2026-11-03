# Caputo--Chen--Gu--Polyanskiy numbering check (3 November 2026)

Two versions of the same paper were inspected directly.

| Item | arXiv:2409.07689v1 (12 Sep 2024; only version listed by the arXiv API record `arxiv_2409.07689.xml`) | Author manuscript (people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf, EJP template) |
|---|---|---|
| Lazy random walk convention | Definition 4 | Definition 2.4 |
| Complete graph example | Example 27 | Example 4.3 |
| Complete bipartite example (numerical observation) | Example 28 | Example 4.4 |
| Proof of the case n = 3 | Proposition 29 | Proposition 4.5 |
| One-large-coordinate step used in that proof | cites [GP23, Prop. 17] | cites [22, Prop. 17] (= Gu--Polyanskiy) |
| Text after the proof | says the same strategy could treat any given n but that it is unclear how to prove all n uniformly | contains the explicit sentence conjecturing the statement of Prop. 4.5 for all n >= 3 |

Method: text extracted with `pdftotext -layout` from the arXiv v1 PDF (arxiv.org/pdf/2409.07689v1) and from the
authors' manuscript PDF (people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf). The published EJP article body
was not retrieved; the Crossref record (`crossref_caputo2025.json`) gives volume 30, pages 1--29. The manuscript
cites the author-manuscript numbering and gives the arXiv numbering in parentheses.

Zhao thesis (no Crossref or arXiv record exists; `zhao2021_titlepage.txt` is the title page of the CMU PDF,
SHA-256 294ecddccdc5e569c770fe089da0cd595c7dd5ed0f540998de614e531d4e9d0b): Corollary 3.1.3 (reverse BEC rate)
and Theorem 3.5.4 (low-retention coefficient) confirmed by text search.

Jadhav arXiv:2606.27073v1: Proposition 9.5 (lazy star) and Remark 9.6 (numerical evidence only, tested up to
n = 50 vertices) confirmed in text extracted with `pdftotext` from the arXiv v1 PDF.
