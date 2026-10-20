# SENI-142: An Open-Access Resilient Transmission and Sovereign Decoupling Benchmark for the Dominican Republic Power Grid (IEEE TPWRS Submission Dataset & Verification Harness)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23484705.svg)](https://doi.org/10.5281/zenodo.23484705)

**Manuscript:** *TPWRS-SENI-142-2026* — IEEE Transactions on Power Systems
**Author:** Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)
**Benchmark:** SENI-142 — the 142-bus nodal model of the Dominican Republic bulk transmission system (115 bulk nodes at 345/230/138 kV + 27 retained 69 kV boundary ports; 135 transmission lines + 58 power transformers), partitioned into the ten territorial planning regions of Law 368-22 and condensed by the Hierarchical Border-Coordinate Formulation (HBCF) into four electrical macro-domains.

---

## Contents

| File | Description |
|---|---|
| `SENI142_CENSO_CANONICO_BARRAS.csv` | Canonical 142-bus census: one slack (`BUS-345-JULIO_SAURI`, 1.02 pu), regional assignment (Law 368-22), HBCF macro-domain, calibrated nodal peak (Σ = 3,450.0 MW). Names and coordinates with calibrated single-line CAD survey provenance from the official one-line-diagram extract. |
| `SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv` | 193 canonical branches (135 lines + 58 transformers) with calibrated single-line CAD survey provenance: circuit lengths and conductors from the drawing's own LT annotations, transformer Ucc/MVA/vector-group from the estate survey. Canonical IDs (`LINE-345-PC-JS`, `CORR-138-PALA-SCNU`, `LINE-230-JS-SCNU`, `LINE-138-CUM-SPMI`, `XFMR-345-138-JS`, …). |
| `matrices_sistema_seni142.npz` | System state: Ybus (142×142, 193 branch pairs), per-branch admittances, HBCF partition (block-diagonal A over the four macro-domains, minimal border set Γ), Schur complement S, measured decomposition residual δ and border condition number κ₂. Input hashes embedded. |
| `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json` | The eight canonical contingency solutions (215-element catalog screened), with per-solution SHA-512 digests, unit-level redispatch breakdown, station-service reconciliation for the 345 kV trunk (748.3 + 3.70 = 752.00 MW isolated), and the dual loss-ratio convention (0.887 % over redispatch / 0.811 % over total deficit). |
| `SENI142_CATALOGO_215_CONTINGENCIAS.csv` | Canonical N-1 screening catalog: 135 transmission lines + 58 power transformers + 22 major generating units = 215 single contingencies (identity, modeled bus where applicable, screening criterion; nameplate MW only where sealed by the release canon). |
| `verify_seni142_benchmark.py` | Official verification harness: loads the four artifacts and checks every structural, topological, matrix and accounting property from the data (no solver outputs are hardcoded). Exits non-zero on any failure. |
| `mutation_test_v3.py` | Adversarial mutation-robustness suite: 12 targeted corruptions (demand, admittance, residual, hashes, balances, metadata); the verifier must reject every one. |
| `paper_seni142_ieee_transactions_en.md` | Canonical master of the manuscript (bit-identical to the submission master). |
| `SENI142_IEEE_2col.pdf` / `SENI142_IEEE_1col.pdf` / `SENI142_IEEE_ES_1col.pdf` | Compiled manuscript (two-column, one-column, Spanish). |
| `CARTA_*`, `DOSSIER_*`, `MATRIZ_*` | Transmittal dossier and cross-reference matrix of the review correspondence. |
| `NOTA_PROPIEDAD_INTELECTUAL_SOLVER_ES_SENI142_20261019.md` / `IP_PATENT_SOLVER_STATEMENT_EN_SENI142_20261019.md` | Intellectual-property doctrine of the submission: benchmark-paper scope per IEEE PES Task Force practice (open model + open validation harness) versus the patent-pending multi-vector optimization solver. |

## Verification

```bash
python3 verify_seni142_benchmark.py          # 41 structural/physical checks, data-driven
```

Key invariants verified from the data: single slack; Σ P = 3,450.0 MW with the
1,645/520/680/605 macro-domain split; 193 unique branch pairs; zero 69 kV lines
(ports are fed exclusively by real 138/69 kV banks); no arithmetic progressions in
line parameters; Ybus ≡ branch table (<1e-9); block-diagonal A; Schur identity
‖S − (D − CA⁻¹B)‖∞ < 1e-12; 748.3 + 3.70 = 752.00 MW trunk isolation;
687.40 + 58.50 + 6.10 = 752.00 MW reserve-sizing closure (error 0.0000 MW).

The catalog `SENI142_CATALOGO_215_CONTINGENCIAS.csv` enumerates the 215 screened single contingencies; the release certifies the eight canonical contingency balances in `ARTEFACTO_B1`.

### Scope of the Verification Harness
The open verification harness (`verify_seni142_benchmark.py`) validates structural, topological, and algebraic consistency directly from the released bundle: nodal censuses, 193 branch parameters, exact Schur complement identity $\|\mathbf{S} - (\mathbf{D} - \mathbf{C}\mathbf{A}^{-1}\mathbf{B})\|_\infty < 10^{-12}$, unique slack assignment, and static contingency reserve accounting. Full non-linear AC Newton-Raphson iterations, multi-temporal OPF optimizations, and dynamic EMT simulations belong to the solver engine domain (the author's research C++/Sparse engine reports 2.65 ms / 473 MiB as an experimental baseline on an 8-thread workstation). The 87,360-state multi-temporal campaign and the 215-contingency screening are results of the author's patent-pending C++/Sparse engine; the released bundle certifies the network model, the condensed-solve invariants and the eight canonical contingency balances.

## Mutation robustness

```bash
python3 mutation_test_v3.py .                # 12/12 mutations detected (exit=1); clean control M00 passes (exit=0)
```

The suite applies twelve targeted corruptions to a temporary copy of the bundle
(load, coordinated intra-macro demand move, branch reactance, Ybus entries,
stored Schur residual, contingency balance, corridor metadata, rating, peak
load, coordinates, conductor records) and requires the verifier to exit
non-zero on every mutation while the intact control passes.

## Provenance

The data layer carries calibrated single-line CAD survey provenance from the official one-line-diagram database: 205 physical
busbars (`nivel_kv`, estate, drawing coordinates) --- from which the benchmark distills the 142 nodal compute buses (115 bulk buses at 345/230/138 kV plus 27 condensed 69 kV boundary ports) --- 511 transformer records with
declared Ucc/MVA/vector group, and 1,181 circuit annotations with real km, conductor
and circuit count (`LT_*kV: "27.5 km 559.5 MCM-AAAC 2C/F"`). The drawing scale is
calibrated with the three surveyed corridor anchors (JSAURI–PALAMARA 70.5 km,
PALAMARA–San Cristóbal 22.1 km, JSAURI–San Cristóbal 30.86 km route length).

## How to cite

Junior Alexis Villanueva Rosario, "SENI-142: An Open-Access Resilient Insular
Transmission Benchmark of the Dominican Republic with Diakoptic Territorial
Decomposition under Spatial Planning Law 368-22," submitted to
*IEEE Transactions on Power Systems* (TPWRS-SENI-142-2026).
