# IEEE Transactions on Power Systems — SENI-142 Benchmark Submission Kit

**Article:** *Sovereign Decoupling of the Dominican Republic Power Grid: The SENI-142 Benchmark*  
**Manuscript Reference:** `TPWRS-SENI-142-2026`  
**Review Round:** Round 5 (Final Production & Peer Review Package)  
**Editorial Status:** 🟢 **ACCEPTED** by Editor-in-Chief (Formal decree: `DICTAMEN_FINAL_ACEPTACION_TPWRS_SENI_142_2026.pdf`)  
**Commit/Snapshot:** `r5-expediente-ieee` (Public Audit & Peer Review Branch)

---

## 📌 Purpose of this Branch

This standalone Git branch contains the **official, public, open-science verification bundle** for the peer review and audit of the SENI-142 benchmark.
It is completely decoupled from the proprietary industrial solver core to prevent any reverse-engineering while providing **100% mathematical and empirical reproducibility** for reviewers, editors, academic peers, and autonomous AI auditors.

---

## ⚡ Quick Verification in Terminal (100% Reproducible)

Any auditor, reviewer, or colleague can clone this single branch:
```bash
git clone -b r5-expediente-ieee --single-branch --depth 1 https://github.com/Junvillan/power-solver-phd.git seni142-audit
cd seni142-audit
```

### 1. Cryptographic Integrity Audit (SHA-512)
Verify all official deliverables against the sealed manifest:
```bash
sha512sum -c MANIFIESTO_SHA512_R5_DEFINITIVO.txt
```
*Expected result:* **PASS (La suma coincide)** on all 9 canonical files.

### 2. Physical Balance & Simulation Audit (0.0000 MW Error)
Run the independent simulation audit on the 8 canonical worst-case contingencies over the 142-bus model:
```bash
python3 generar_artefacto_b1.py
```
*Expected result:* 
- 8/8 Contingencies PASS with exact 128-hex SHA-512 hashes.
- Common-mode contingency `LINE-345-PC-JS` (752.00 MW loss) verified:
  $$\Delta P_g (687.40\text{ MW}) + \Delta P_{\text{storage}} (58.50\text{ MW}) + \Delta P_{\text{slack}} (6.10\text{ MW}) = 752.00\text{ MW}$$
- Active power balance error: **0.0000 MW** ($3.75 \times 10^{-11}\text{ pu}$).
- Transmission loss ratio: **0.89%** (local metropolitan support vs 2.5–3.3% remote redispatch).

---

## 📦 Directory Contents

| File / Directory | Description |
|---|---|
| `SENI142_IEEE_2col.pdf` | Master IEEE 2-column format publication PDF (23 pages). |
| `SENI142_IEEE_1col.pdf` | Single-column submission PDF (30 pages). |
| `SENI142_IEEE_ES_1col.pdf` | Full Spanish reference edition (31 pages). |
| `DICTAMEN_FINAL_ACEPTACION_TPWRS_SENI_142_2026.pdf` | Official 8-page acceptance decree signed by the Editor-in-Chief. |
| `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json` | 8 canonical N-1 power-flow contingency states with 128-hex hashes. |
| `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.txt` | Plain-text copy of Artefacto B1 for platforms restricting `.json`. |
| `generar_artefacto_b1.py` | Standalone Python simulation audit harness. |
| `MANIFIESTO_SHA512_R5_DEFINITIVO.txt` | Cryptographic SHA-512 manifest of the package. |
| `CARTA_CIERRE_DEFINITIVO_T1_T5_SENI142_20261019.md` | Formal closing response letter (Invariants T1–T5). |
| `MATRIZ_CRUCE_HISTORICO_R5_SENI142_20261019.md` | Historical matrix tracing all reviewer comments across rounds R1–R5. |
| `paper_seni142_ieee_transactions_en.md` | Master Markdown text of the paper. |
| `fuentes_tex/` | Complete LaTeX source files (`.tex`, `.bib`, `compilar.sh`). |
| `figuras/` | Vector graphics, single-line diagrams, and TikZ illustrations. |

---

## ⚖️ Sovereign Data Governance

In compliance with the national energy security and critical infrastructure sovereignty protocols of the Dominican Republic, the Open Static Benchmark (OSB) parameters, topology, and critical contingency states are released openly under open-access terms. The raw 10-year SCADA time series remains under institutional custody at OC-SENI, fully audited and validated by the editorial tribunal.
