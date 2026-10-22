# SENI-142: An Open-Access Resilient Transmission and Sovereign Decoupling Benchmark for the Dominican Republic Power Grid (IEEE TPWRS Submission Dataset & Verification Harness)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23484704.svg)](https://doi.org/10.5281/zenodo.23484704)

**Manuscript:** *TPWRS-SENI-142-2026* — IEEE Transactions on Power Systems
**Author:** Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)
**Benchmark:** SENI-142 — the 142-bus nodal model of the Dominican Republic bulk transmission system (115 bulk nodes at 345/230/138 kV + 27 retained 69 kV boundary ports; 135 transmission lines + 58 power transformers), partitioned into the ten territorial planning regions of Law 368-22 and condensed by the Hierarchical Border-Coordinate Formulation (HBCF) into four electrical macro-domains.

---

## Contents

| File | Description |
|---|---|
| `SENI142_CENSO_CANONICO_BARRAS.csv` | Canonical 142-bus census: one slack (`BUS-345-JULIO_SAURI`, 1.02 pu), regional assignment (Law 368-22), HBCF macro-domain, calibrated nodal peak (Σ = 3,450.0 MW). Names and coordinates with calibrated single-line CAD survey provenance from the official one-line-diagram extract. |
| `SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv` | 193 canonical branches (135 lines + 58 transformers) with calibrated single-line CAD survey provenance: circuit lengths and conductors from the drawing's own LT annotations, transformer Ucc/MVA/vector-group from the estate survey. Canonical IDs (`LINE-345-PC-JS`, `CORR-138-PALA-SCNU`, `LINE-230-JS-SCNU`, `LINE-138-CUM-SPMI`, `XFMR-345-138-JS`, …). |
| `matrices_sistema_seni142.npz` | System state: Ybus (142×142, 193 branch pairs), per-branch admittances, HBCF partition (block-diagonal A over the four macro-domains, trunk-induced boundary set Γ), Schur complement S, measured decomposition residual δ and border condition number κ₂. Input hashes embedded. |
| `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json` | The eight canonical contingency solutions (215-element catalog screened), with per-solution SHA-512 digests, unit-level redispatch breakdown, station-service reconciliation for the 345 kV trunk (748.3 + 3.70 = 752.00 MW isolated), and the dual loss-ratio convention (0.887 % over redispatch / 0.811 % over total deficit). |
| `SENI142_CATALOGO_215_CONTINGENCIAS.csv` | Canonical N-1 screening catalog: 135 transmission lines + 58 power transformers + 22 major generating units = 215 single contingencies (identity, modeled bus where applicable, screening criterion; nameplate MW only where sealed by the release canon). |
| `verify_seni142_benchmark.py` | Official verification harness: loads the four artifacts and checks every structural, topological, matrix and accounting property from the data (no solver outputs are hardcoded). Exits non-zero on any failure. |
| `mutation_test_v3.py` | Adversarial mutation-robustness suite: 12 targeted corruptions (demand, admittance, residual, hashes, balances, metadata); the verifier must reject every one. |
| `paper_seni142_ieee_transactions_en.md` | Canonical master of the manuscript (bit-identical to the submission master). |
| `SENI142_IEEE_2col.pdf` / `SENI142_IEEE_1col.pdf` / `SENI142_IEEE_ES_1col.pdf` | Compiled manuscript (two-column, one-column, Spanish). |
| `CARTA_*`, `DOSSIER_*`, `MATRIZ_*` | Transmittal dossier and cross-reference matrix of the review correspondence. |
| `NOTA_PROPIEDAD_INTELECTUAL_SOLVER_ES_SENI142_20261019.md` / `IP_PATENT_SOLVER_STATEMENT_EN_SENI142_20261019.md` | Intellectual-property doctrine of the submission: benchmark-paper scope per IEEE PES Task Force practice (open model + open validation harness) versus the patent-pending multi-vector optimization solver. |

## Errata and clarifications (2026-10-22)

Auditor-driven clarifications on branch-rating semantics and modeling conventions. None of
them alters any data artifact: the four sealed artifacts (census CSV, branch CSV, NPZ,
ARTEFACTO B1 JSON) and the verifier are untouched, and `verify_seni142_benchmark.py`
still reports 41/41 PASS.

1. **`S_max_MVA` is a per-circuit rating.** The aggregate thermal capability of a
   multi-circuit branch is `S_max_MVA × Circuitos`:
   `LINE-345-PC-JS` 421.3 MVA × 3 (3C/F, three 559.5 MCM AAAC per phase) = 1,263.9 MVA;
   `CORR-138-PALA-SCNU` 236.2 × 2 = 472.4 MVA; `LINE-138-CUM-SPMI` 168.5 × 2 = 337.0 MVA.
2. **Base-case loading of the 345 kV Punta Catalina trunk.** Under the bundle rating
   above, the pre-event flow of 748.3 MW over `LINE-345-PC-JS` is a 59.2% bundle loading
   (plus 3.70 MW of local station service, i.e. 752.00 MW of gross isolated injection,
   as sealed in ARTEFACTO B1).
3. **Terminals of `LINE-138-CUM-SPMI`.** The canonical census terminals are
   `BUS-138-CUMAYASA` → `BUS-138-JUAN_DOLIO` (the San Pedro de Macorís corridor; the
   "SPMI" suffix refers to the SPM1 substation estate where the November 2025 collapse
   initiated). Earlier prose glosses such as "SPM–Cumayasa" must be read against the
   canonical `From_Bus`/`To_Bus` columns.
4. **`LINE-230-JS-SCNU` is the benchmark's single composite branch** (census subtipo
   `Linea_transmision_compuesta`): it links the 345 kV JSAURI bar to the 138 kV
   San Cristóbal Norte bus through integrated port autotransformation, with the branch
   impedance referenced to the 230 kV trunk base. The verifier whitelists it explicitly
   in its dielectric-coherence check.
5. **Double-circuit corridors are archived as a single equivalent branch** (column
   `Circuitos` = 2). A "one circuit out of service" contingency is screened at corridor
   level; post-event flows are determined by the corrective stage (automatic
   corrective-overload control and fast topological redispatch deployed with the
   co-optimized reserve), not by the passive impedance split alone.
6. **Inertia constants (H) and per-unit synchronous ratings are not yet published.**
   Community RoCoF/frequency-nadir computation requires them; their addition is a
   planned dynamic extension of the release.
7. **Manuscript-notation alignment pending.** The reactive-limit regularization is
   reformulated in the two-part manuscript suite as a two-sided smoothed
   Fischer–Burmeister complementarity on [Q_min, Q_max] whose limit recovers the rigid
   PV→PQ characteristic. The master markdown still carries the earlier centered
   sigmoidal notation; it will be aligned in the next release.

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

### Recommended clean execution environment

The harness depends only on `numpy`. On macOS — or in any Conda-preloaded shell where older
scientific packages may already shadow the interpreter — run from a fresh standard virtual
environment:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install numpy
python3 verify_seni142_benchmark.py
```

The verifier is strictly read-only: it opens the four data artefacts, prints
`RESULTADO: 41/41 chequeos PASS`, and writes nothing to disk.

### Scope of the Verification Harness: Consistency vs. Field Provenance

To guarantee deterministic, license-free reproducibility — no commercial power-flow solver
(PSS/E, PowerFactory) or proprietary environment required — this release states its
verification boundary in three explicit layers.

**1. What the open harness rigorously validates.** `verify_seni142_benchmark.py`
recomputes the 41 structural, topological and algebraic invariants listed above directly
from the canonical arrays, with no solver output hardcoded and a fail-closed non-zero exit
on any failure. This is an internal-consistency proof: it certifies that the released
arrays are mutually coherent under the declared electrical identities — not that they are
physically correct.

**2. Where field accuracy comes from.** The physical grounding of the calibrated
3,450.0 MW system peak, the 1,645 / 520 / 680 / 605 MW macro-domain demand split, and the
ten-region partition under Spatial Planning Law 368-22 derive from 520 complete
consecutive 168-hour weeks — 87,360 hourly operational states over 3,640
Monday-to-Sunday days — selected without a single interpolated hour from the 2016–2025
archive of Dominican system-operator telemetry (OC-SENI / ETED), against which the
calibrated CAD network reconstruction is validated. Thirteen civil days are excluded by
construction (six calendar-boundary orphan days and the seven days of the final festive
week) so that the atypical year-end collapse of industrial demand cannot contaminate the
covariance structure of the block bootstrap.

**3. What is deliberately not in this repository.** Full non-linear AC Newton-Raphson
iterations, multi-temporal AC-OPF optimization and dynamic EMT simulation belong to the
solver-engine domain, together with the 2.65 ms / 473 MiB execution figures — an
experimental reference measurement of the author's patent-pending C++/Sparse research engine
on an 8-thread Linux workstation, which this open harness does **not** and cannot
reproduce. That engine is protected as industrial secret under a pending patent
application; access to it is available to reviewers under confidential peer-review
agreement per the IEEE PES Data Availability policy. This release certifies the network
model, the condensed-solve invariants and the eight canonical contingency balances, and
nothing beyond them.

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
