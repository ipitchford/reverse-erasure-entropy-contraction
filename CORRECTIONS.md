# Corrections

## 0.1.1-candidate (11 November 2026)

The abstract of 0.1.0-candidate (and the matching sentence in README.md, CITATION.cff and the Zenodo
description) described the reverse-erasure channel as "keep the current symbol with probability alpha, otherwise
replace it by a fresh draw from a prior rho". That rule is the lazy reset kernel alpha I + (1 - alpha) 1 rho^T
(erasure followed by reverse erasure; Remark 2.1(i)), not the channel R_rho analysed in the paper.

Correct rule (equations (2.1)-(2.2)): R_rho maps [n] together with the blank e to [n]; a visible symbol passes
through unchanged and the blank is replaced by a fresh draw from rho. The retention probability alpha belongs to
the forward erasure channel and enters only through the reference input m_{rho,alpha} = (alpha rho, 1 - alpha).

One lead-in sentence of Section 1.3 was tightened in the same way. No definition, theorem, proof, number, figure,
script or recorded output changed. Version 0.1.0-candidate remains archived unchanged at
https://doi.org/10.5281/zenodo.23921825 and tag v0.1.0-candidate.
