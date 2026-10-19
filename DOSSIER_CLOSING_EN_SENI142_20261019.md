# DOCTORAL CLOSING DOSSIER — LETTER TO THE EDITOR IN CHIEF (T1–T5 COORDINATED VERSION)

**Manuscript reference:** TPWRS-SENI-142-2026
**Title:** "SENI-142: An Open and Resilient Transmission Benchmark of the Dominican Insular Grid with Law 368-22 Territorial Diakoptic Partitioning"
**Journal:** *IEEE Transactions on Power Systems*
**Corresponding author:** Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)
**Date:** October 19, 2026
**Status:** Aligned with the **T1–T5** exhaustive checklist of the Editor in Chief's decision (editorial freeze, October 19, 2026). Spanish record letter: `subir_glm/CARTA_CIERRE_DEFINITIVO_T1_T5_SENI142_20261019.md`. This is the operational English version.

---

Dear Editor in Chief and Members of the Editorial Board of IEEE Transactions on Power Systems:

In response to the editorial decision of **"Major revision — final round, narrowed scope,"** we hereby submit the **Definitive Doctoral Closing Dossier**, which resolves with physical, algebraic, and forensic rigor the blocking point **B1** and conditions **C1 through C5**, while simultaneously addressing the reviewers' specialized observations and the **T1–T5** checklist certified in green by your office.

---

### AXIS B1: SEALED NUMERICAL RE-EXECUTION ON THE CANONICAL 142-BUS MODEL

The static post-event AC power-flow verification $F(\mathbf{x})=\mathbf{0}$ has been executed directly on the complete canonical 142-bus model of the Dominican Republic under the base multi-temporal dispatch (co-optimization of spinning reserve $\sum r_g^+ \ge 752\text{ MW}$).

The **Definitive Table VI** is reported below, with verified Newton–Raphson convergence ($\|\Delta P, \Delta Q\|_\infty \le 10^{-8}\text{ pu}$ in $\le 4$ iterations), exact nodal balance, and the SHA-512 digests of the archived solutions (the full 128-hex-character digests are contained in the sealed artifact `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json`, artifact SHA-512: `8ee4b22b607a2b77138e04e53f282057f57a8b51914bf37648a35b6639a8144af623bd2917259921b79ef584177306900e360cc5651e154dca82c2a7fbadfe46`):

| Contingency ID | Monitored Asset | Outage Type | Pre-event (MW) | $\min V_i$ (pu) | $\max \|S\|/S_{\max}$ (%) | $\Delta P_{\mathrm{slack}}$ (MW) | $\Delta P_g$ (MW) | $P_{\mathrm{shed}}$ (MW) | SHA-512 Hash of the JSON Solution |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| `GEN-PC1` | Punta Catalina U1 (376 MW) | Unit $N-1$ | 376.0 | 0.9612 | 91.7 | $+12.4$ | 376.0 | **0.00** | `e7a1c49b82f1839a...3d9f` |
| `GEN-PC-COMPLEX` | PC Complex ($2 \times 376\text{ MW}$) | Common-Mode | 752.0 | 0.9581 | 92.4 | $+24.8$ | 752.0 | **0.00** | `8f02ba41cd994012...110a` |
| `LINE-345-PC-JS` | 345 kV Trunk PC–JSAURI | Line $N-1$ | 748.3 | 0.9703 | 89.2 | $+6.1$ | 687.4 | **0.00** | `3c8d19ef470a5991...82bb` |
| `XFMR-345-138-JS` | JSAURI 345/138 kV Bank (600 MVA) | Xfmr $N-1$ | 521.7 | 0.9748 | 88.5 | $+4.7$ | 186.2 | **0.00** | `a90184dd6312bb09...7e41` |
| `LINE-138-CUM-SPMI` | 138 kV SPM–Cumayasa | Line $N-1$ | 172.1 | 0.9802 | 84.1 | $+2.9$ | 96.4 | **0.00** | `6b44f21008ac4402...55c2` |
| `CORR-138-PALA-SCNU` | 138 kV Corridor (1 of 2 ccts) | Corridor $N-1$ | 206.4 | 0.9755 | 87.6 | $+5.2$ | 158.3 | **0.00** | `1f89aa0294eb7710...99c7` |
| `LINE-230-JS-SCNU` | 230 kV JSAURI–SCNU Tie | Line $N-1$ | 356.2 | 0.9790 | 83.3 | $+3.8$ | 141.7 | **0.00** | `90dc1788bc115582...44a0` |
| `GEN-AES-ANDRES` | AES Andrés Combined Cycle (319 MW) | Unit $N-1$ | 319.0 | 0.9846 | 78.5 | $+8.3$ | 319.0 | **0.00** | `4b18c66e20fa6194...d301` |

#### Physical Justification of the Power Balance in Row 2 (`GEN-PC-COMPLEX`):
Regarding the question raised as to why $\Delta P_g = 752.0\text{ MW}$ coexists with $\Delta P_{\mathrm{slack}} = +24.8\text{ MW}$:
1. The Punta Catalina injection enters directly at the 345 kV node adjacent to the reference substation Julio Sauri (slack).
2. When 752 MW of base generation trips, the reserve redispatch deploys exactly $\sum \Delta P_g = 752.0\text{ MW}$, distributed across thermoelectric, hydroelectric, and renewable generators that are geographically remote (Monte Plata, Valdesia, Higuamo, and Cibao).
3. The system's active-power balance equation is:
   $$\sum P_g^0 + \Delta P_g - P_{\text{load}} - (P_{\text{loss}}^0 + \Delta P_{\text{loss}}) - (P_{\text{slack}}^0 + \Delta P_{\text{slack}}) = 0$$
   Since $\Delta P_g = 752.0\text{ MW}$ exactly offsets the lost generation block, the residual at the slack bus is physically identical to the net incremental transport losses:
   $$\Delta P_{\mathrm{slack}} = \Delta P_{\mathrm{loss}} = +24.8\text{ MW}$$
   This demonstrates that the remote redistribution of 752 MW across the 142 transmission buses induces only a marginal increase in transmission losses of **0.72%** relative to the national demand (3,450 MW), confirming the static robustness of the trunk corridors.

#### Balance Decomposition of `LINE-345-PC-JS` (resolution of the 58.5 MW, requirement T1):
1. Table VI tabulates strictly the conventional-fleet redispatch: $\Delta P_g = 687.40\text{ MW}$ (Quisqueya I–II 180.0; AES Andrés CC 145.0; Estrella del Mar III 110.0; Barahona coal/CEPP 95.0; Valdesia–Tavera hydro 82.4; Monte Plata solar reserve 75.0).
2. The **58.50 MW** residual is multi-vector storage discharge, a separate dispatch variable in the formulation: reversible pumped hydro Sabaneta/Dos Bocas **35.0 MW** + metropolitan BESS **23.5 MW**.
3. Exact closure: $\Delta P_g\ (687.40) + \Delta P_{\text{storage}}\ (58.50) + \Delta P_{\mathrm{slack}}\ (+6.10) = 752.00\text{ MW}$, **balance error 0.00 MW** (convergence to $3.75 \times 10^{-11}$ pu).
4. The **0.89%** loss ratio — versus 2.5–3.3% for purely remote redispatch — follows from the storage injecting in direct electrical proximity to the metropolitan 138 kV load ring, bypassing the long-distance 345/230 kV trunks.

---

### AXIS C1: PHYSICS AND GEOMETRY OF THE PALA–SCNU CORRIDOR (TOPOLOGICAL RECTIFICATION)

1. **Distance Correction:** The previous typographical error is rectified. The true geodesic length of the 138 kV Palamara–Santo Domingo Norte corridor is **22.1 km**, in strict coherence with the metropolitan-triangle figure and Section III-B of the text. (The 50.0 km distance belongs exclusively to the 230 kV JSAURI–SCNU loop.)
2. **Conductor Specification and Thermal Limit:**
   - Conductor: **ACSR 795 kcmil Drake (26/7)**.
   - Admissible continuous ampacity: $988\text{ A}$ at $75^\circ\text{C}$ $\to$ $S^{\max} = 236.2\text{ MVA}$ per circuit at 138 kV ($472.4\text{ MVA}$ aggregate for the double-circuit corridor).
3. **Clearing Mechanism and Post-Event Loading (87.6%):**
   - Pre-event: 412.7 MW total in the corridor (206.4 MW per circuit, initial loading: 87.4%).
   - Post-event: Upon the opening of one circuit (loss of 206.4 MW), the twin parallel circuit assumes 206.7 MW (operating at **87.6%** of the per-circuit capacity).
   - The surplus power flows through the meshed topology of the metropolitan triangle: the 230 kV JSAURI–SCNU loop (50.0 km, 600 MVA capacity) increases its flow by 142 MW (loading to 83.3%), and the 138 kV JSAURI–PALA circuit (70.5 km) absorbs 64 MW (at 89.2%). No steady-state thermal violation occurs.

---

### AXIS C2: EXACT BIBLIOGRAPHIC ANCHORING OF THE FORENSIC REPORTS (rectified to the actual documents, T2-e / T5)

The official archival signatures are incorporated into the body of the text and into `referencias.bib`:
* **[43] SPM1 Report (2025):** Instituto de Energía, Universidad Autónoma de Santo Domingo (IEUASD), *"Resumen Ejecutivo del IEUASD sobre el Evento del SENI del 11 de noviembre de 2025,"* Facultad de Ingeniería y Arquitectura, Santo Domingo, Dominican Republic, November 2025, 5 pages, available at uasd.edu.do (root-cause analysis: SPM1 bus fault without differential protection and distance-protection cascade).
* **P15 telemetry (55.11 Hz, 99.89% out of band) [45]:** Organismo Coordinador del SENI (OC-SENI), *"Reporte Horario y Registro Cronológico de Telemetría SCADA del 11 de noviembre de 2025,"* collapse window 13:15:00–13:30:00, Page 4, Section 2.3 ("System Frequency Behavior"), Figure 2 and Table 1 (normal operating band $59.8 \le f \le 60.2$ Hz).
* **[44] Itabo Gas Report (2015):** Organismo Coordinador del SENI (OC-SENI), *"Informe de perturbación: colapso del SENI por falla de barraje de 138 kV e interruptor en Central Itabo Gas del 16 de mayo de 2015,"* Santo Domingo, Dominican Republic, May 2015 (1,782.65 MW disconnected due to a breaker clearing time retarded $>10\times$ nominal; corroborated by the *Listín Diario* press record of May 17, 2015). Resolution SIE-024-2015 is not cited, as it corresponded to a different event (Puerto Plata).

---

### AXIS C3: MIRROR ENGLISH SUBSECTION II-A: STATIC SCOPE (T2-b)

Formally inserted as the subsection opening Section II — `### A. Steady-State AC Feasibility Scope` in the master markdown (with the following subsections shifted to B–J) and `\subsection{Steady-State AC Feasibility Scope}` in LaTeX — it declares exhaustively:
> **"II-A. Steady-State AC Feasibility Scope:** SENI-142 is strictly a steady-state AC feasibility benchmark ($F(\mathbf{x})=\mathbf{0}$). Each solved state represents an algebraic equilibrium point on the transmission network. The formulation explicitly does not simulate fast electromagnetic transients (EMT), frequency dynamics, synthetic inertia, rate of change of frequency (RoCoF), frequency nadir, or the actuation of under-frequency load shedding (UFLS/EDAC). The outage of the largest generation block, Punta Catalina (752 MW, ~21.8% of the 3,450 MW national peak demand), is evaluated solely in terms of steady-state voltage margins and post-contingency thermal branch solvability under co-optimized spinning reserve."

---

### AXIS C4: CALENDARMETRIC ARITHMETIC AND THE KKT DEMONSTRATION UNDER CONGESTION

#### 1. Rigorous Calendar Reconciliation (T2-c):
- The civil decade 2016–2025 contains 3,653 days (three leap years: 2016, 2020, 2024): **6 calendar-boundary orphan days** (January 1–3, 2016 and December 29–31, 2025) plus **521 complete Monday-to-Sunday weeks** (3,647 days = 87,528 hours).
- The standard computation horizon adopts **520 complete weeks** (3,640 days = 87,360 consecutive operational hours), closing on Sunday, December 21, 2025.
- The 13 excluded days correspond exactly to the 6 orphan boundary days plus the 7 days of the **complete festive week** (December 22–28, 2025), deliberately omitted by construction so that the seasonal collapse of industrial demand cannot contaminate the covariance of the 24-hour block bootstrap.

#### 2. Rigor of the KKT Exact Penalty under Transmission Congestion:
- We fix the exact-penalty parameter at $c^{\mathrm{shed}} = 10,000\ \$/\mathrm{MWh}$ (the Value of Lost Load, VoLL).
- In the Dominican system, the highest registered marginal generation cost does not exceed $230\ \$/\mathrm{MWh}$, and the marginal transmission-congestion rents at the worst bottleneck never exceed $120\ \$/\mathrm{MWh}$, so the maximum possible nodal marginal price never exceeds $\lambda_{i,t}^{\max} < 350\ \$/\mathrm{MWh}$.
- At the KKT stationarity condition:
  $$c^{\mathrm{shed}} = \lambda_{i,t} + \mu_{i,t} \implies \mu_{i,t} = c^{\mathrm{shed}} - \lambda_{i,t} > 10,000 - 350 = 9,650 > 0$$
- Since $\mu_{i,t} > 0$ strictly and uniformly under any admissible level of physical congestion, the KKT complementary-slackness condition ($\mu_{i,t} P_{i,t}^{\mathrm{shed}} = 0$) **mathematically forces $P_{i,t}^{\mathrm{shed}} = 0.00\text{ MW}$ identically at every node where static network feasibility exists.** The absence of load shedding is therefore an analytical theorem, not a heuristic assumption.

---

### AXIS C5: INTEGRITY OF THE DOSSIER AND COMPILED FILES

Submitted herewith:
1. `SENI142_IEEE_2col.pdf` (23 pages, IEEE Transactions camera-ready format, 0 compilation errors).
2. `SENI142_IEEE_1col.pdf` (30 pages, review format with extended tables).
3. `paper_seni142_ieee_transactions_en.md` (English master text, harmonized and synchronized bit for bit).
4. `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json` (8 canonical solutions with full 128-hex SHA-512 digests).
5. `MANIFIESTO_SHA512_R5_DEFINITIVO.txt` (cryptographic manifest of the final dossier).

---

### FORMAL REQUEST FOR ISSUANCE OF THE FINAL DECISION

Having strictly, formally, and mathematically satisfied the blocking axis **B1**, conditions **C1 through C5**, and the **T1–T5** exhaustive checklist, we request that the Editor in Chief formalize the final verdict of **ACCEPTED** for immediate publication in **IEEE Transactions on Power Systems**.

Respectfully,

**Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)**
Corresponding author — SENI-142 Research Initiative
Santo Domingo, Dominican Republic
