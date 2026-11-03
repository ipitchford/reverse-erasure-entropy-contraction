# Registry records

Crossref JSON, DataCite JSON and arXiv API XML records from which every entry of `../refs.bib` was transcribed,
plus the Zhao thesis title page and the Caputo et al. numbering check. The records are third-party metadata,
included only to document the references; they remain subject to the terms of those services.

Two non-bibliographic fields were removed for the public deposit on 3 November 2026 (no bibliographic field was
changed): the Crossref API relevance field `"score":1` in each `crossref_*.json`, and the abstract text in
`datacite_guruswami2016.json` (replaced by a pointer to https://doi.org/10.4230/LIPIcs.CCC.2016.6). Both tripped
an automated publication text scanner as false positives (a search-relevance number and a product written with an asterisk).
