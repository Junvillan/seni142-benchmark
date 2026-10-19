# INTELLECTUAL-PROPERTY STATEMENT
## Submission TPWRS-SENI-142-2026 — IEEE Transactions on Power Systems
### Date: 2026-10-19 · Author and Principal Investigator: Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)

This statement sets the official intellectual-property doctrine governing the scope of the contribution of manuscript **TPWRS-SENI-142-2026** and the treatment of the associated optimization engine, in response to the solver-code requests raised during the review correspondence. In line with the directives of the *IEEE PES Task Force on Benchmark Test Systems*, the following is declared:

---

### 1. Scope of the Contribution (Benchmark Paper)

The object of this article is the **physical network model** and its **open validation data**: the fully georeferenced 142-bus topology of the Dominican Republic interconnected national system (SENI), the 193 canonical branches (135 lines + 58 power transformers) with calibrated single-line CAD survey provenance from the official one-line diagram, the CSV censuses, the NPZ matrices, and the verification harness **verify_seni142_benchmark.py (41/41 checks PASS)**.

The benchmark is conceived to be **neutral and interoperable**: the scientific community can test **its own solvers** (MATPOWER, Pandapower, PyPSA, PowerFactory, PSS/E, or any other) on the released model. Reproducibility of every sealed structural quantity does not depend on proprietary software: the verification harness is restricted to `numpy` and `scipy`, and re-derives the partition residual, the block-diagonal Schur-complement structure, and the eight contingency balances directly from the released arrays.

### 2. Patent Protection (Patent-Pending)

The advanced multi-vector optimization engine developed within the author's doctoral program constitutes **protected intellectual property, subject to a Patent of Invention application and industrial secrecy**. Its release as a public open-source repository **would destroy the legal novelty** required by patent legislation; therefore the engine is **not part** of the open benchmark data package and will not be released during the patent grace period.

This reservation **does not affect** the reproducibility of the article: every quantity declared in the manuscript (border residual δ = 2.788×10⁻¹⁴ pu, κ₂(S) = 2,489.64, common-mode reserve sizing 752.00 MW, dispatch closure 687.40 + 58.50 + 6.10 = 752.00 MW) is sealed in the artifact `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json` and is verifiable with the open harness.

---

**Authorship declaration:** The benchmark, the manuscript, and this doctrine are entirely the work of the Principal Investigator **Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)**, sole author of submission TPWRS-SENI-142-2026.

*Custody status: document incorporated into the official upload package and sealed in `MANIFIESTO_SHA512_R5_DEFINITIVO.txt` (R9 refresh, 2026-10-19).*
