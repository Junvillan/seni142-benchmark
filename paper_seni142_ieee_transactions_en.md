# SENI-142 — Doctoral Manuscript Master (IEEE Transactions Format, Markdown Camera-Ready Source)

> **Delivery note.** This Markdown master is the single source of the manuscript. Every mathematical statement is written in native LaTeX, and the six figures of the TikZ bank and the two algorithms appear as self-contained `latex` injection blocks (IEEEtran-ready) at their point of first use. Figures 3, 4 and 5 reference the already compiled vector PDFs shipped with the benchmark (`fig_diagrama_1_jsauri_345_138.pdf`, `fig_diagrama_2_schur_hbcf.pdf`, `fig_diagrama_3_constelacion_microsolvers.pdf`); Figures 1, 2 and 6 carry their `figure` environment with caption and label, and their `tikzpicture` is extracted verbatim at injection time from the chapter sources indicated in each block header comment. Injection into the journal master is mechanical and requires no editorial decisions.

---

**RECOMMENDED TITLE (principal option).**

## SENI-142: An Open-Access Resilient Insular Transmission Benchmark of the Dominican Republic with Diakoptic Territorial Decomposition under Spatial Planning Law 368-22

**Alternative Title 1.**

### Sovereign Decoupling of the Dominican Republic Power Grid: The SENI-142 Benchmark for High-Renewable Island Transmission and Territorial Microgrid Planning

**Alternative Title 2.**

### HBCF Diakoptic Modeling and Schur-Complement Silicon Solvers for the 142-Bus Interconnected System of the Dominican Republic (SENI-RD)

**Alternative Title 3.**

### From Centralized Radial Transmission to Ten Coordinated Microgrids: The Dominican Republic SENI-142 Benchmark with Multi-Vector Flexibility and Economic CAPEX/OPEX Proof

| Field | Value |
|---|---|
| **Author** | Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c) |
| **Affiliation & Entity** | Department of Electrical Grids and Renewable Energy (EERR) Research, V-TECH (V-CORE TECH S.R.L. / Villa-Core Technologies, S.L.) · Autonomous Power Systems Laboratory, Santo Domingo, Dominican Republic |
| **Manuscript class** | IEEE Transactions on Power Systems / IEEE Systems Journal — camera-ready source |
| **Date / version** | October 17, 2026 · v1.0 (pre-submission master) |
| **Computational disclosure** | All computational engines used in this work are high-performance silicon solvers, hermetic POSIX-isolated co-simulation enclaves, distributed algebraic engines, and physics-informed cyber-physical optimization pipelines operated by the authors. No third-party inference service participates in any result reported here. |
| **Data provenance** | Organismo Coordinador del Sistema Eléctrico Nacional Interconectado (OC-SENI), Dominican Republic; Empresa de Transmisión Eléctrica Dominicana (ETED). |

---

## Abstract

Insular power systems are the most demanding laboratories of the energy transition: they cannot import inertia, spinning reserve, or neighbor support, and the Dominican Republic has lately experienced nationwide service interruptions that exposed this fragility at national scale. This article contributes **SENI-142**, an open-access, fully georeferenced benchmark of the bulk transmission network of an entire Caribbean nation — the 142-bus interconnected system of the Dominican Republic (SENI), comprising approximately 112 physical substations, 135 transmission lines, and 58 power transformers across the 345, 230, and 138 kV strata, with radial 69 kV subtransmission condensed into equivalent multiports. The benchmark is partitioned into ten sovereign territorial microgrids under the national spatial planning statute (Law 368-22) and condensed by a hierarchical border-coordinate formulation (HBCF) whose exact Schur complement condensation resolves each hourly AC state of the complete national network in **2.65 ms** with a resident footprint of **473 MiB** on consumer-grade hardware, with a fasorial border-coupling residual of $\delta = 2.788 \times 10^{-14}\ \mathrm{pu}$. The structural solver is calibrated and validated against 520 complete consecutive 168-hour weeks --- 87,360 hourly operational states over 3,640 Monday-to-Sunday days, selected without a single interpolated hour from the 2016--2025 archive of real system-operator telemetry using a 24-hour block bootstrap that preserves diurnal climate correlation, and stressed against a 215-contingency $N-1$ catalog. A deterministic four-phase digital-twin lifecycle --- hermetic enclave, live-tree stress, SHA-512 golden master, atomic kernel promotion --- makes every reported figure bit-for-bit reproducible. Multi-vector flexibility (power-to-gas hydrogen, 764 MW reversible pumped storage, ADM1 biomethanation) is coupled to a multi-temporal AC-OPF and validated by a zonal CAPEX/OPEX proof. The dataset, topology, and validation harness are released openly through IEEE DataPort and GitHub.

## Index Terms

Benchmark testing, diakoptics, digital twins, energy storage, hydrogen, insular power systems, optimal power flow, power system resilience, pumped-storage hydroelectricity, Schur complement, spatial planning, transmission networks.

## Resumen

Este artículo contribuye el benchmark abierto SENI-142: la red de transmisión de un país caribeño entero, modelada barra a barra sobre telemetría operativa real estandarizada en 520 semanas consecutivas completas (87,360 horas sobre 3,640 días de lunes a domingo, 2016–2025). La formulación diakóptica HBCF con condensación exacta por complemento de Schur particiona el sistema en diez microrredes territoriales soberanas bajo la Ley 368-22, agrupadas en cuatro macrodominios eléctricos, y resuelve cada estado horario de flujo de potencia AC completo en 2.65 ms con 473 MiB de memoria y un residuo fasorial de frontera de $\delta = 2.788 \times 10^{-14}$ pu sobre hardware comercial. El gemelo digital se valida con un ciclo de vida determinista de cuatro fases con cascada de compuertas fail-closed, sellado SHA-512 y promoción atómica; la flexibilidad multivector (hidrógeno power-to-gas, bombeo reversible de 764 MW, biometanación ADM1) se acopla a un AC-OPF multitemporal y se valida económicamente por balance zonal. El conjunto se libera abiertamente en IEEE DataPort y GitHub.

---

## I. Introduction

Insular interconnected systems occupy an extreme point of the power engineering design space. An island cannot draw inertia, reactive support, or emergency transfer from neighbors: every megawatt of reserve, every volt-ampere of reactive compensation, and every megahertz of damping capability must be produced, dispatched, and defended inside the same synchronous footprint that consumes it. The Dominican Republic is a canonical instance: a single synchronous island of roughly eleven million people, with no submarine or overland interconnection, more than forty percent of national load concentrated in the metropolitan Ozama region, an inertia anchor dominated by the Punta Catalina coal plant, and a renewable build-out whose instantaneous solar share has reached 36.6% of demand in operational telemetry [30]. The national consequences of losing the generation–load equilibrium are not hypothetical: the nationwide service interruptions recorded in November 2025 and February 2026, documented in operator event logs [30] and in the national press archive [42], mobilized emergency response at the scale of a full territory and renewed the policy debate on frequency stability, black-start capability, and the observability of the transmission estate. The physics of this fragility is by now classical — declining system inertia degrades the rate of change of frequency and narrows the feasible control envelope of converter-dominated grids [15], [16], [14] — but the empirical instruments available to study it remain surprisingly primitive.

The benchmarking infrastructure of the field is, in its majority, synthetic. The canonical test cases that still govern doctoral training and comparative studies — the WSCC 9-bus network, the IEEE 14-, 30-, 57-, and 118-bus systems — descend from drafting-table abstractions of the early 1960s: reactances are round academic numbers, loads are fixed triangles of power, geography is absent, climate is absent, and nothing in the dataset has ever tripped, been maintained, been paid for, or been hit by a hurricane. At the opposite pole, utility-grade network cases are held in proprietary formats of commercial simulation platforms, are encumbered by confidentiality, and are rarely released in forms that permit independent re-execution. The open-systems movement has answered with valuable infrastructure — the MATPOWER case collection [40], and the Power Grid Library of AC-OPF benchmark instances [41] among them — but its instances are, almost without exception, *synthetic or anonymized*: they are grids that exist to be hard, not grids that exist. Between the toy and the secret there is almost nothing: an open, complete, measured model of a real national transmission system, with provenance sufficient for independent verification, is a public good that the research community currently lacks for the insular Caribbean — and, with few exceptions, for the insular world at large.

This article closes that gap with **SENI-142**, an open-access benchmark constructed around three commitments. First, **fidelity to a measured reality**: the network model is not synthetic — it is derived from the national transmission estate and validated against 520 complete consecutive 168-hour weeks (87,360 hourly states over 3,640 Monday-to-Sunday days, 2016–2025) of system-operator telemetry, dispatched unit by unit and hour by hour, so that every simulated state answers to an archived operational one. The thirteen civil days excluded by construction — the six calendar-boundary orphan days (January 1–3, 2016 and December 29–31, 2025) and the seven days of the final festive week (December 22–28, 2025) — preserve weekly cyclicality and keep the atypical year-end collapse of industrial demand out of the block-bootstrap covariance. Second, **structural honesty about scale**: the full national system is solved — all bulk buses, all trunk lines, all transformers — not a reduced district of it, and the solution method is formulated so that its exactness and complexity are theorems rather than aspirations: a hierarchical border-coordinate formulation (HBCF) in the diakoptic tradition [1], [2], condensed by the Schur complement [7] and factorized on a partition that follows the ten territorial planning regions of the SNIT instituted by the national territorial statute Law 368-22, in strict technical compatibility with the General Electricity Law 125-01 [32]. Third, **deterministic reproducibility**: every artifact passes a four-phase digital-twin lifecycle with a fail-closed gate cascade, detached SHA-512 sealing, and atomic promotion, so that any figure reported in this article can be regenerated from a bit-identical, cryptographically attested software state.

The contributions are five, and each is falsifiable:

- **C1 — Benchmark.** An open, georeferenced, standards-consistent model of the complete bulk transmission network of the Dominican Republic: 142 nodal buses over approximately 112 physical substations, 135 transmission lines, 58 power transformers, strata of 345, 230, and 138 kV, with the 69 kV subtransmission layer reduced by injection-preserving equivalents; released with topology, parameters, provenance metadata, and validation harness through IEEE DataPort and GitHub.
- **C2 — Formulation.** The HBCF diakoptic partition of a full insular grid into ten sovereign territorial microgrids — the legal planning regions of Law 368-22 — aggregated into four electrical macro-subdomains with a minimal border set, and the proof that its Schur condensation is exact, with complexity $O(\sum_k N_k^3 + N_B^3)$ against the $O(N^3)$ of monolithic dense factorization.
- **C3 — Deterministic digital twin.** A four-phase lifecycle (hermetic POSIX-namespace enclave with a fourteen-gate fail-closed cascade; live-tree $N-1$ stress against a 215-contingency catalog; SHA-512-detached Golden Master; atomic kernel promotion via renameat2 with zero regression) that converts simulation telemetry into evidence with a chain of custody.
- **C4 — Multi-vector flexibility.** The coupling of power-to-gas hydrogen (electrolysis, 700 bar storage, fuel-cell re-injection), 764 MW of reversible pumped hydro storage, and ADM1-based biomethanation to a multi-temporal AC-OPF, stated with its full Karush–Kuhn–Tucker (KKT) system and validated by a zonal CAPEX/OPEX balancing proof.
- **C5 — Measured silicon performance.** Resolution of each hourly national AC state in 2.65 ms with 473 MiB of resident memory and fasorial border residual $\delta = 2.788 \times 10^{-14}\ \mathrm{pu}$ on consumer-grade hardware — two to three orders of magnitude inside the 1–5 s state-estimation cycle of a modern energy management system, adequate for static contingency screening — under a 24-hour block-bootstrap validation protocol.

The remainder of the article is organized as follows. Section II states the 80/20 methodology: the invariant formulation (graph model, 69 kV reduction, HBCF partition, Schur condensation, data protocol, deterministic lifecycle, reactive-limit regularization, multi-temporal AC-OPF) and the modular clause that instantiates the Dominican case under Law 368-22. Section III documents the benchmark topology, from the 112-substation physical estate to the 142-bus nodal model and the ten territorial microgrids. Section IV develops the multi-vector flexibility constellation and its zonal economic validation. Section V reports silicon performance, accuracy, and contingency resilience. Section VI discusses policy implications and limitations, and Section VII concludes with the open-release plan and four research routes.

## II. Methodology: The 80/20 SENI-IA Doctrine

The methodology is deliberately organized in two components. The **invariant 80%** — graph representation, equivalent reduction, spatial partition, exact condensation, data protocol, deterministic lifecycle, regularization, and optimization — is problem-independent and transfers without modification across the family of studies built on this platform. The **modular 20%** is the instantiation clause that binds the formulation to one reference reality: the national grid of the Dominican Republic, partitioned according to its own territorial law. This division is not aesthetic: it is what makes the benchmark a reusable scientific instrument rather than a one-off case study.

### A. Steady-State AC Feasibility Scope

SENI-142 is strictly a steady-state AC feasibility benchmark ($F(\mathbf{x})=\mathbf{0}$). Each solved state represents an algebraic equilibrium point on the transmission network. The formulation explicitly does not simulate fast electromagnetic transients (EMT), frequency dynamics, synthetic inertia, rate of change of frequency (RoCoF), frequency nadir, or the actuation of under-frequency load shedding (UFLS/EDAC). The outage of the largest generation block, Punta Catalina (752 MW, ~21.8% of the 3,450 MW national peak demand), is evaluated solely in terms of steady-state voltage margins and post-contingency thermal branch solvability under co-optimized spinning reserve; in the dynamic plane it is a frequency-stability event outside the static frontier of this article.

### B. Graph-theoretic representation of the bulk network

The transmission system is modeled as a connected undirected graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, where $\mathcal{V}$ is the set of transmission buses ($|\mathcal{V}| = 142$) and $\mathcal{E} = \mathcal{E}_{\mathrm{line}} \cup \mathcal{E}_{\mathrm{trafo}}$ is the union of line and transformer branches, with $|\mathcal{E}_{\mathrm{line}}| = 135$ transmission lines and $|\mathcal{E}_{\mathrm{trafo}}| = 58$ power transformers. Each branch carries a per-unit series admittance and half-charging susceptance on a common 100 MVA base; the nodal admittance matrix $\mathbf{Y}_{\mathrm{bus}} \in \mathbb{C}^{142 \times 142}$ therefore encodes 20,164 complex entries of coupled electromagnetic state. Nodal power injections follow the standard rectangular balance

$$S_i = P_i + jQ_i = V_i \sum_{j \in \mathcal{V}} Y_{ij}^{*}\, V_j^{*}, \qquad i \in \mathcal{V},$$

with buses classified as slack, PV, or PQ. The slack duty — setting the phase reference and absorbing the real-power mismatch — rests on the 345 kV bus of the Julio Sauri substation (JSAURI), held at $V = 1.02\ \mathrm{pu}$, which receives directly the injection of the largest thermal plant in the country (Section III-B). Where a physical substation hosts more than one voltage level, each voltage level is a distinct bus and the intervening autotransformer is a branch; this single rule, applied uniformly, is what raises the network from approximately 112 fenced estates to exactly 142 nodal buses (Section III-A).

### C. Equivalent reduction of the 69 kV subtransmission layer

Radial subtransmission and medium-voltage sub-networks operating at 69 kV are condensed into static multiport equivalents of Thévenin/Norton type. For each retained boundary bus, the equivalent preserves (i) the aggregated complex injection of the condensed area at every modeled hour and (ii) the short-circuit impedance $Z_{\mathrm{cc}}$ seen from the boundary, obtained by Kron-type network reduction. Formally, for boundary port $p$ with condensed interior $\Omega_r$,

$$V_p = E_{\mathrm{th}}^{(r)} - Z_{\mathrm{th}}^{(r)} I_p, \qquad \sum_{i \in \Omega_r} S_i = V_p I_p^{*},$$

so that the reduction is lossless *at the boundary* for power-flow purposes while eliminating dimensional inflation of $\mathbf{Y}_{\mathrm{bus}}$. The reduction is recomputed from the archived configuration of the estate and is itself part of the sealed artifact, consistent with recommended practice for industrial system analysis [19] and with CIM-based interchange of network models [25].

### D. Spatial diakoptic partition: the HBCF

The Hierarchical Border-Coordinate Formulation (HBCF) partitions $\mathcal{G}$ into $K$ territorial subsystems $\mathcal{G}_k = (\mathcal{V}_k, \mathcal{E}_k)$, pairwise vertex-disjoint, interconnected exclusively through a minimal border set $\mathcal{V}_B = \bigcup_{k=1}^{K} \partial \mathcal{V}_k$ of cut boundary buses. The partition is *hierarchical in two registers*:

1. **Legal-territorial register.** Law 368-22 (Ley de Ordenamiento Territorial, Uso de Suelo y Asentamientos Humanos) [32], the territorial statute of the Dominican State, institutes the ten official planning regions of the SNIT. The benchmark SENI-142 adopts this sovereign spatial partition as the basis of its ten-microgrid diakoptics — so that electrical partition and territorial governance coincide — in strict technical compatibility with the technical governance of the General Electricity Law 125-01, a modeling decision with direct policy consequences (Section VI).
2. **Electrical register.** For numerical condensation, the ten microgrids bundle into $K = 4$ electrical macro-subdomains — North (Cibao), South, East, and Metropolitan — whose interconnections are exactly the trunk 230/138 kV ties of the estate. The border set $\mathcal{V}_B$ is the set of buses incident to those ties; Kron cutting of the trunk branches [1], [2] isolates the subdomains and defines the condensation boundary $\Gamma$.

After reordering buses as $(\text{interior} \mid \text{border})$, the nodal Jacobian or admittance system at any operating point takes the block form

$$\begin{bmatrix} \mathbf{A} & \mathbf{B} \\ \mathbf{C} & \mathbf{D} \end{bmatrix} \begin{bmatrix} \mathbf{x}_I \\ \mathbf{x}_B \end{bmatrix} = \begin{bmatrix} \mathbf{u}_I \\ \mathbf{u}_B \end{bmatrix},$$

where $\mathbf{x}_I$ collects the internal variables of all subdomains and $\mathbf{x}_B$ the border state. By construction $\mathbf{A} = \operatorname{diag}(\mathbf{A}_1, \dots, \mathbf{A}_K)$ is block-diagonal, with $\mathbf{A}_k$ the internal Jacobian block of macro-subdomain $k$.

### E. Exact condensation by the Schur complement

The condensation rests on three elementary but consequential results, stated here in full because they carry the exactness claim of the benchmark.

**Lemma 1 (block-diagonal inverse).** *If $\mathbf{A} = \operatorname{diag}(\mathbf{A}_1, \dots, \mathbf{A}_K)$ with each $\mathbf{A}_k \in \mathbb{R}^{N_k \times N_k}$ nonsingular, then $\mathbf{A}^{-1} = \operatorname{diag}(\mathbf{A}_1^{-1}, \dots, \mathbf{A}_K^{-1})$.*

*Proof.* Immediate: for each block position $(k, l)$, $\mathbf{A}_k \mathbf{A}_k^{-1} = \mathbf{I}_{N_k}$ if $l = k$ and $\mathbf{A}_k \cdot \mathbf{0} = \mathbf{0}$ otherwise; the product equals the identity on the direct sum of the interior spaces. $\blacksquare$

**Theorem 1 (exactness of Schur condensation).** *If the full system matrix $\begin{psmallmatrix} \mathbf{A} & \mathbf{B} \\ \mathbf{C} & \mathbf{D} \end{psmallmatrix}$ is nonsingular and $\mathbf{A}$ is nonsingular, then $\mathbf{x}_B$ is the unique solution of the reduced border system*

$$\mathbf{S}\, \mathbf{x}_B = \mathbf{u}_B - \mathbf{C}\, \mathbf{A}^{-1} \mathbf{u}_I, \qquad \mathbf{S} = \mathbf{D} - \mathbf{C}\, \mathbf{A}^{-1} \mathbf{B},$$

*and $\mathbf{x}_I = \mathbf{A}^{-1}(\mathbf{u}_I - \mathbf{B}\, \mathbf{x}_B)$ restores the interior state. The pair $(\mathbf{x}_I, \mathbf{x}_B)$ coincides with the unique solution of the unreduced block system.*

*Proof.* Block Gaussian elimination on the full system premultiplies the first row by $\mathbf{C}\mathbf{A}^{-1}$ and subtracts it from the second, eliminating $\mathbf{x}_I$ and yielding the border system above; these operations are nonsingular row operations, hence the reduced system is equivalent to the original and uniqueness transfers from the nonsingularity hypothesis. Back-substitution is the second row of the elimination. The Schur complement $\mathbf{S}$ is nonsingular precisely when the full matrix is [7]. $\blacksquare$

**Proposition 1 (complexity).** *Dense factorization of the $N$-bus system costs $O(N^3)$; the partitioned solution costs one block-diagonal factorization $\sum_k O(N_k^3)$ plus one border factorization $O(N_B^3)$ plus the elimination products, i.e. $O\!\left(\sum_k N_k^3 + N_B^3\right)$ with $\sum_k N_k + N_B = N$ and $N_B \ll N$. For sparse $\mathbf{A}_k$ factorized with fill-reducing orderings, the local cost approaches linearity in $N_k$ [5], [6].*

The numerical governance of the condensation is itself measured. The spectral condition number $\kappa_2$ of the border system is monitored at every operating point; the fasorial reconstruction residual — the maximum mismatch between the condensation-recovered state and a reference state — measured $\delta = 2.788 \times 10^{-14}\ \mathrm{pu}$ over the validation horizon. As an external-validity control, the same spectral methodology was first stress-checked on synthetic cases: the 22×22 Jacobian of the classical IEEE 14-bus system, for instance, classifies as MARGINAL in the project's spectral taxonomy with $\kappa_2 = 117.7823$, a classification cross-verified against independent tooling before any national deployment. Algorithm 1 states the complete solver.

**Algorithm 1.** Schur-border AC power flow on the SENI-142 partition (injection block below).

```latex
\begin{algorithm}[!t]
\caption{Schur-border AC power flow on the SENI-142 HBCF partition}
\label{alg:schur_pf}
\begin{algorithmic}[1]
\Require partition $\{\mathcal{G}_k\}_{k=1}^{4}$, border set $\mathcal{V}_B$,
         hourly injections $(\mathbf{u}_I, \mathbf{u}_B)$, tolerance $\varepsilon$
\Ensure converged state $(\mathbf{x}_I, \mathbf{x}_B)$, residual $\rho$
\State flat-start $(\mathbf{x}_I^{(0)}, \mathbf{x}_B^{(0)})$; assemble
       $\mathbf{J}^{(0)} = \begin{psmallmatrix} \mathbf{A} & \mathbf{B} \\ \mathbf{C} & \mathbf{D} \end{psmallmatrix}$
\For{$t \gets 0, 1, 2, \dots$ until $\rho \le \varepsilon$}
  \For{$k \gets 1, \dots, K$} \Comment{parallel, disjoint memory}
     $\mathbf{A}_k^{(t)} \gets \partial (\Delta \mathbf{u}_k) / \partial \mathbf{x}_k$;
     factor $\mathbf{A}_k^{(t)} = \mathbf{L}_k \mathbf{U}_k$ with fill-reducing ordering
  \EndFor
  \State $\mathbf{W} \gets \mathbf{A}^{(t)^{-1}} \mathbf{B}^{(t)}$ by $K$ local back-substitutions
  \State $\mathbf{S}^{(t)} \gets \mathbf{D}^{(t)} - \mathbf{C}^{(t)} \mathbf{W}$;\quad
         factor $\mathbf{S}^{(t)}$
  \State $\mathbf{x}_B^{\Delta} \gets {\mathbf{S}^{(t)}}^{-1}\,
         (\mathbf{u}_B - \mathbf{C}^{(t)} \mathbf{A}^{(t)^{-1}} \mathbf{u}_I)$
  \For{$k \gets 1, \dots, K$} \Comment{parallel restoration}
     $\mathbf{x}_k^{\Delta} \gets {\mathbf{A}_k^{(t)}}^{-1}(\mathbf{u}_k - \mathbf{B}_k^{(t)} \mathbf{x}_B^{\Delta})$
  \EndFor
  \State $\mathbf{x}^{(t+1)} \gets \mathbf{x}^{(t)} + \mathbf{x}^{\Delta}$;\quad
         $\rho \gets \lVert (\Delta P, \Delta Q) \rVert_{\infty}$
\EndFor
\State \Return $(\mathbf{x}_I, \mathbf{x}_B)$, $\rho$ \Comment{fasorial audit: $\delta$ vs.\ reference}
\end{algorithmic}
\end{algorithm}
```

### F. Empirical data protocol

The benchmark is not calibrated against assumptions; it is fed by an archived operational reality, and the protocol sentence is quoted verbatim as the contractual core of the data layer:

> *"The structural solver is fed by a pre-existing, continuous empirical ground-truth repository comprising exactly 520 complete consecutive 168-hour weeks — 87,360 hourly states over 3,640 Monday-to-Sunday days, selected without a single interpolated hour (2016–2025) — provided by the Dominican Republic System Operator (Organismo Coordinador del SENI), capturing real SCADA telemetry, dispatch orders, solar/wind variable profiles, and historical outage logs."*

Four variable families enter the solver from this repository: (i) nodal real and reactive demand at bulk buses; (ii) unit-by-unit dispatch of the thermal, hydro, solar, and wind fleet; (iii) meteorologically coupled solar and wind production profiles; and (iv) the historical outage log that seeds the contingency catalog. The horizon spans the decade 2016–2025 at hourly resolution without a single interpolated hour. The civil span of the decade contains 3,653 days — exactly 521 complete Monday-to-Sunday weeks (3,647 days, 87,528 hourly states) plus six calendar-boundary orphan days (January 1–3, 2016 and December 29–31, 2025). The standardized horizon adopts 520 of those 521 complete weeks — Monday, January 4, 2016 through Sunday, December 21, 2025, i.e. 3,640 days or 87,360 hourly states — so the thirteen excluded civil days decompose exactly into the six boundary orphan days plus the seven days of the final festive week (December 22–28, 2025), deliberately left out so that the atypical year-end collapse of industrial demand cannot contaminate the covariance structure of the block bootstrap. Because the repository is continuous, the validation layer can resample it honestly: a **24-hour block bootstrap** draws whole operating days, preserving the intra-day correlation between irradiance, temperature, demand, and dispatch, rather than the decorrelated hour-level resampling that would flatter the error statistics of stability margins.

### G. The deterministic validation lifecycle of the digital twin

Every reported figure in this article is downstream of a software state whose provenance is cryptographically attested. The lifecycle has four phases, and Figure 1 diagrams it in full:

1. **Phase 1 — hermetic macro-sandbox enclave.** The packaged solver executes in a POSIX-namespace sandbox of the bubblewrap class, with a read-only filesystem view and a memory envelope below 200 MiB, and must pass a cascade of fourteen gates $G_0$–$G_{13}$ with fail-closed semantics: any gate that cannot execute counts as a failure, never as tacit approval.
2. **Phase 2 — live tree under $N-1$ stress.** The validated package is exercised against the 215-contingency specification catalog on the live teaching tree, with system-operator telemetry as ground truth and cross-tool reconciliation against commercial desktop study platforms.
3. **Phase 3 — Golden Master.** The full cascade is re-verified and every artifact is sealed with detached SHA-512 manifests; the seal attests one exact software state, not a family of versions.
4. **Phase 4 — industrial production.** Promotion is an atomic kernel-level switch (`renameat2` with `RENAME_EXCHANGE`): production and candidate swap in a single indivisible operation, and the regression delta between sealed and deployed state is zero by construction.

Three notarial invariants govern the cycle: bit-identical preservation of the attested state across phases; fail-closed closure under doubt; and atomicity of observation, so that no observer can ever witness a half-updated system. The operational theorem that results — *if the deployed artifact is bit-for-bit the sealed artifact and the switch is atomic, then any behavioral difference between test and production is excluded by construction, not by statistics* — is what licenses the use of solver telemetry as evidence rather than anecdote.

**Figure 1.** Cyber-physical four-phase digital-twin architecture with the fail-closed gate cascade.

```latex
% Figure 1 injection block.
% Graphic source: sec01_introduccion_y_marco_metodologico.tex, figure environment
% at L95--145 (styles: fase/compuerta/forense/flujo/retorno/nota; palette seni-*).
% The tikzpicture is extracted verbatim from that source at injection time.
\begin{figure}[!t]
\centering
\input{sec01_fig_gemelo_fases_tikz} % extracted verbatim, sec01 L97--142
\caption{Cyber-physical four-phase digital-twin lifecycle with the fail-closed gate cascade. The Phase-1 hermetic enclave (POSIX namespaces, read-only filesystem, ${<}200$ MiB envelope) must pass the fourteen gates $G_0$--$G_{13}$ (14/14, fail-closed); the Phase-2 live tree sustains $N-1$ stress against the 215-contingency catalog with operator telemetry and cross-tool reconciliation; the Phase-3 Golden Master is sealed with detached SHA-512 manifests; promotion to industrial production is an atomic kernel switch (renameat2, RENAME\_EXCHANGE) with zero regression. Any failed gate or unexplained deviation returns the package to Phase 1 with a forensic report: no intermediate states are admissible.}
\label{fig:gemelo_fases}
\end{figure}
```

### H. Continuous regularization of reactive limits

Hard PV–PQ switching at generator reactive limits induces limit cycles in Newton-type iterations whenever the operating point oscillates around the limit — the classical chattering of commercial codes. The benchmark replaces the binary switch by a continuous activation with adaptive slope,

$$Q_g^{\mathrm{eff}}(V_i) = Q_g^{\lim} \cdot \sigma\!\left(\alpha\,(V_i^{\mathrm{ref}} - V_i)\right), \qquad \sigma(z) = \frac{1}{1 + e^{-z}},$$

whose analytic derivative $\partial Q_g^{\mathrm{eff}} / \partial V_i = -\alpha\, Q_g^{\lim} \sigma(\cdot)(1 - \sigma(\cdot))$ is injected into the Jacobian, preserving the quadratic convergence of the iteration while degrading the reactive capability smoothly as the terminal voltage approaches the limit. The measured regularization error of this controller over the validation horizon is $5.32 \times 10^{-12}$, i.e. the continuous controller is numerically indistinguishable from the ideal discontinuous policy while eliminating the discontinuity that caused the oscillation.

### I. Multi-temporal AC-OPF with power-to-gas coupling

On the converged network model, the benchmark formulates a multi-temporal AC-OPF. For each hour $t$ and bus $i$, the equality constraints are the nodal balances, augmented with the power-to-gas coupling terms,

$$\sum_{g \in \mathcal{G}_i} P_{g,i,t} + \sum_{r \in \mathcal{R}_i} P_{r,i,t} + P_{i,t}^{\mathrm{FC}} - P_{i,t}^{\mathrm{EL}} + P_{i,t}^{\mathrm{shed}} - P_{i,t}^{\mathrm{load}} = P_i(\mathbf{V}_t, \boldsymbol{\theta}_t),$$

with the reactive analogue admitting inverter-coupled absorption/injection within apparent-power capability limits. The intertemporal coupling is imposed by the hydrogen buffer dynamics,

$$E_{h,t+1} = E_{h,t} + \left(\eta_{\mathrm{EL}}\, P_{h,t}^{\mathrm{EL}} - \frac{P_{h,t}^{\mathrm{FC}}}{\eta_{\mathrm{FC}}}\right) \Delta t, \qquad E_h^{\min} \le E_{h,t} \le E_h^{\max},$$

where $\eta_{\mathrm{EL}}$ and $\eta_{\mathrm{FC}}$ are the electrolysis and reconversion efficiencies: surplus non-dispatchable renewable generation becomes intertemporal energy inventory, absorbed as flexible electrolytic load in surplus hours and re-injected by the fuel cell in deficit hours. Pumped storage obeys the reservoir analogue with independent pump/turbine efficiencies, bounding the reversible 764 MW fleet of Section IV-C. The complete problem — non-convex by virtue of the AC equalities — is solved by a cascade of thirty-two Newton-type configurations spanning Newton–Raphson, Iwamoto optimal-multiplier step control, fast-decoupled BX iterations, and a Gauss–Seidel fallback, so that no single algebraic pathology can stall the sweep. Optimality is certified at the KKT system: stationarity of the Lagrangian in all primal variables, primal feasibility of the equalities and inequalities, dual feasibility of the multipliers, and vanishing complementarity products; the multiplier signs and complementarity residuals are part of the sealed validation output [8], [9], [10]. Under transmission congestion this guarantee is quantitative: the exact penalty is fixed at the value of lost load, $c^{\mathrm{shed}} = 10{,}000\ \$/\mathrm{MWh}$, while the highest registered marginal generation cost stays below $230\ \$/\mathrm{MWh}$ and worst-case transmission-congestion rents never exceed $120\ \$/\mathrm{MWh}$, so the nodal multiplier obeys $\lambda_{i,t}^{\max} < 350\ \$/\mathrm{MWh}$; KKT stationarity in the shedding variable reads $c^{\mathrm{shed}} = \lambda_{i,t} + \mu_{i,t}$ with $\mu_{i,t} \ge 0$, hence $\mu_{i,t} > 9{,}650 > 0$ strictly and uniformly under any admissible congestion level, and complementary slackness forces $P_{i,t}^{\mathrm{shed}} = 0.00$ MW identically at every bus where the post-event network is statically feasible — an analytical theorem, not a heuristic assumption. Figure 2 diagrams the electrochemical coupling.

**Figure 2.** Electrochemical power-to-gas coupling and multi-temporal storage.

```latex
% Figure 2 injection block.
% Graphic source: sec02_modelado_matematico_ac_h2_sgen.tex, figure environment
% at L63--88 (styles: bloque/flujo/flujoh2/nota; palette seni-*).
% The tikzpicture is extracted verbatim from that source at injection time.
\begin{figure}[!t]
\centering
\input{sec02_fig_p2g_h2_tikz} % extracted verbatim, sec02 L65--85
\caption{Electrochemical power-to-gas coupling of the green-hydrogen vector with the AC network. The electrolyzer absorbs renewable surplus as flexible load ($P^{\mathrm{EL}}_{h,t} \ge 0$, efficiency $\eta_{\mathrm{EL}}$); the storage buffer imposes the intertemporal inventory $E_{h,t+1} = E_{h,t} + (\eta_{\mathrm{EL}} P^{\mathrm{EL}}_{h,t} - P^{\mathrm{FC}}_{h,t}/\eta_{\mathrm{FC}})\,\Delta t$ with box constraints; the fuel cell re-injects power during deficit ($P^{\mathrm{FC}}_{h,t} \ge 0$, efficiency $\eta_{\mathrm{FC}}$). Both convertor terms enter the nodal AC balance. Electric flows in solid strokes; hydrogen flows in dashed gold.}
\label{fig:p2g_h2}
\end{figure}
```

### J. The modular clause: instantiation under Law 368-22

The invariant formulation binds itself to one reference reality by the following canonical closing clause, quoted verbatim:

> *"In this reference benchmark, the structural payload is instantiated with the 142-bus insular bulk transmission grid of the Dominican Republic, partitioned into ten sovereign territorial microgrids under the legal framework of Spatial Planning and Land Use Law No. 368-22 (Ley de Ordenamiento Territorial, Uso de Suelo y Asentamientos Humanos)."*

The clause does three things at once. It fixes the scope of the claim (one country, complete, not sampled); it binds the partition to the national planning statute, so that every computational region is also a governance region; and it marks the 20% module as replaceable — any other insular or territorial system can be instantiated by substituting the clause, without touching the invariant 80%.

## III. The Dominican Republic SENI-142 Benchmark Topology

### A. From 112 substations to 142 nodal buses

The physical estate of the Dominican transmission system comprises approximately 112 fenced substations. The nodal model comprises exactly 142 buses. The difference is not noise; it is topology, and Figure 3 documents the rule on the nation's most consequential substation. A fenced substation is a real-estate object; a bus is a Kirchhoff object. Wherever a substation hosts two voltage levels joined by autotransformer banks, the two yards are electrically distinct nodes, coupled only through the transformer branch impedance. The Julio Sauri (JSAURI) estate is the canonical case: its 345 kV yard — the receiving end of the trunk line that evacuates the Punta Catalina generating complex — and its 138 kV regional yard are decoupled by the T1/T2 autotransformer banks, and each yard is one bus. Applying the rule uniformly over all strata — 345, 230, and 138 kV bulk yards, plus 69 kV interfaces retained through the equivalents of Section II-B — yields exactly 142 nodal buses over 135 transmission lines and 58 power transformers.

**Figure 3.** Kirchhoff decoupling at the Julio Sauri 345/138 kV substation.

```latex
% Figure 3 injection block — self-contained.
\begin{figure}[!t]
\centering
\includegraphics[width=\columnwidth]{fig_diagrama_1_jsauri_345_138.pdf}
\caption{Kirchhoff decoupling at the Julio Sauri 345/138 kV substation. The 345 kV super-highway that evacuates the Punta Catalina complex ($2 \times 376$ MW) terminates in its own yard, decoupled by the impedance of the T1/T2 autotransformer banks from the regional 138 kV yard that feeds the San Cristóbal corridor and the metropolitan ring. Wherever a transformation exists, the fenced estate yields two buses; modeled across all voltage strata, the network totals exactly 142 nodal buses.}
\label{fig:jsauri}
\end{figure}
```

### B. The bulk strata and the metropolitan 138 kV ring

Three strategic substations articulate the system. **JSAURI** operates at two levels — 345 kV and 138 kV — and its 345 kV bus is the system slack at $V = 1.02\ \mathrm{pu}$, receiving the direct injection of **Punta Catalina**, the largest thermal plant in the country at $2 \times 376$ MW (752 MW, coal), evacuated by the 345 kV trunk. **PALA (Palamara)**, in the metropolitan region, is the principal load center with an aggregate modeled demand of 1,645 MW and local fuel-oil backup of three 10.77 MW units elevating from 13.8 kV. **SCNU** is the renewable integration hub of the southwest: 58.9 MW of hydroelectric generation, 95 MW of solar photovoltaics, and 34 MW of wind, all elevating from 13.8 kV, plus a prospective 50 MW PEM electrolysis block marked non-operational for 2026 in the released dataset (prospective assets are flagged, never silently merged, so that simulation states remain answers to archived operational states). More than forty percent of the national load concentrates in the metropolitan Ozama region, served over a 138 kV ring whose redundancy is geometric: the JSAURI–PALA–SCNU triangle with line lengths of 70.5 km, 50.0 km, and 22.1 km, reinforced by a 230 kV JSAURI–SCNU tie. Any single circuit of the triangle can be lost with service carried by the remaining two — the $N-1$ property that the resilience battery of Section V-D exercises systematically. The full geometry with real corridor distances is the reference zone of the economic proof (Section IV-D) and of the contingency catalog (Section V-D).

### C. Ten sovereign territorial microgrids

Law 368-22 organizes the national territory into ten planning regions; the benchmark adopts them as its ten territorial microgrids and bundles them, for numerical condensation, into the four electrical macro-subdomains of the HBCF. Table I states the mapping and the representative anchors of each region as they appear in the operational record.

**Table I.** Territorial microgrids of the SENI-142 benchmark (Law 368-22) and their bundling into the four HBCF macro-subdomains.

| Territorial microgrid (planning region) | Macro-subdomain | Representative anchors in the operational record |
|---|---|---|
| Ozama-Metropolitana | $\Omega_{\mathrm{Metro}}$ | Palamara, Hainamosa, Herrera — more than 40% of national load |
| Valdesia | $\Omega_{\mathrm{Sur}}$ | JSAURI, Punta Catalina (752 MW), Baní–Yaguate solar corridor |
| Higuamo | $\Omega_{\mathrm{Este}}$ | San Pedro de Macorís, Quisqueya plants, AES Andrés (GNL) |
| Yuma | $\Omega_{\mathrm{Este}}$ | La Romana–Punta Cana tourist load corridor |
| Del Valle | $\Omega_{\mathrm{Sur}}$ | El Valle multihub, reversible PHES 764 MW (Sabaneta / Dos Bocas) |
| Enriquillo | $\Omega_{\mathrm{Sur}}$ | Barahona, Los Cocos and Larimar wind, Canoa solar |
| Cibao Norte | $\Omega_{\mathrm{Norte}}$ | Canabacoa (Santiago), second load center |
| Cibao Sur | $\Omega_{\mathrm{Norte}}$ | Pueblo Viejo mining load (Cotuí), Falcondo (Bonao) |
| Cibao Nordeste | $\Omega_{\mathrm{Norte}}$ | Atlantic-coast thermal and wind (Puerto Plata) |
| Cibao Noroeste | $\Omega_{\mathrm{Norte}}$ | Montecristi solar, Valverde–Mao, Dajabón border corridor |

Figure 4 displays the resulting diakoptic map: four macro-subdomains $\Omega$ over the insular geography, the trunk borders $\Gamma$ (the 230/138 kV ties cut by Kron reduction), and the silicon key performance indicators of the condensed solve.

**Figure 4.** Spatial HBCF diakoptic partition and Schur-complement matrix structure.

```latex
% Figure 4 injection block — self-contained.
\begin{figure}[!t]
\centering
\includegraphics[width=\columnwidth]{fig_diagrama_2_schur_hbcf.pdf}
\caption{Spatial HBCF diakoptic partitioning of the insular grid. The ten territorial microgrids of Law 368-22 bundle into four electrical macro-subdomains $\Omega$ (North/Cibao, South, East, Metropolitan); only the trunk borders $\Gamma$ — the 230/138 kV ties cut by Kron reduction — travel to the Schur complement $\mathbf{S} = \mathbf{D} - \mathbf{C}\mathbf{A}^{-1}\mathbf{B}$, with block structure $\mathbf{A}, \mathbf{B}, \mathbf{C}, \mathbf{D}$ over the interior/border ordering. Silicon key performance indicators: 2.65 ms per national AC state, 473 MiB resident, over the 87,360-hour horizon (10 years of OC-SENI telemetry), with fasorial border-coupling residual $\delta = 2.788 \times 10^{-14}$ pu.}
\label{fig:hbcf_schur}
\end{figure}
```

### D. Data provenance and the boundary-state manifest

Every coupling term that reaches the master solver — the $(P_g, Q_g)$ injections of the flexibility constellation of Section IV — travels through a boundary-state manifest whose entries are chained and signed with SHA-512, so that the provenance of any injection can be verified post hoc against the sealed run. Network model interchange follows the CIM conventions of IEC 61970 [25], and power-quality-relevant quantities follow the measurement definitions of IEC 61000-4-30 [24] and IEEE Std 1459 [22]. Provenance thus runs unbroken from operator archive to solver input to published figure — the property that distinguishes a benchmark from a screenshot.

### E. The synthetic canon versus the measured island

The scientific identity of SENI-142 is easiest to state by contrast. Table III places the synthetic canon beside the measured island along the axes that matter for reproducible science. Two of those axes deserve emphasis because they are invisible in parameter tables. The first is *temporal depth*: a synthetic case has one operating point, or a handful of scenarios; SENI-142 has 87,360 archived hourly states in 520 complete weekly cycles, so every statistical claim made on it can be resampled, bootstrapped, and falsified against a decade of realized weather, demand, and dispatch. The second is *consequence*: nothing in a synthetic case has ever broken; every trunk line of the SENI carries an outage log, a maintenance history, and a price at which its loss has been paid. A benchmark that remembers being hit is a different scientific object from one that cannot.

**Table II.** The synthetic canon and the measured island.

| Axis | Synthetic canon (IEEE 9/14/30/57/118-class) | SENI-142 |
|---|---|---|
| Origin | Drafting-table abstractions, early 1960s onward | National transmission estate, measured |
| Geography | None (reactance diagrams) | Real corridors; metropolitan ring at 70.5 / 50.0 / 22.1 km |
| Temporal depth | One operating point or scenario set | 87,360 hourly states in 520 complete consecutive weeks (2016–2025) |
| Outage history | None | Operator event and outage logs seed the $N-1$ catalog |
| Governance coupling | None | Ten planning regions of Law 368-22 |
| Renewable regime | None (fixed loads) | Instantaneous solar share up to 36.6% |
| Provenance | Publication only | SHA-512-sealed four-phase digital-twin lifecycle |
| Release | Open (by design) | Open (IEEE DataPort, GitHub), sovereign archives retained |

## IV. Multi-Vector Flexibility and Economic Validation

### A. The flexibility constellation

The multi-vector layer is organized as a constellation of six physics-dedicated solvers feeding the 142-bus master solver through the signed boundary-state manifest: (i) photovoltaic production with continuous sigmoidal $Q$–$V$ control for duck-curve suppression; (ii) wind production with aerodynamic $C_p(\lambda, \beta)$ modeling and synthetic inertia; (iii) the hydrogen vector — electrolysis, compression to 700 bar, and a national refuelling network of 740 hydrogen stations in the planning model; (iv) biochemical conversion through the Anaerobic Digestion Model No. 1 (ADM1) [26], digesting sargasso and vinasse substrates into dispatchable biomethane; (v) thermal production with heat-rate curves and synchronous $P$–$Q$ dispatch; and (vi) the reversible pumped-hydro fleet of 764 MW (Sabaneta / Dos Bocas). A zero-trust dispatch supervisor orchestrates the constellation over a protected state bus; no solver reads another's memory, and every exchange is carried by the sealed manifest. Figure 5 diagrams the constellation.

**Figure 5.** Multi-vector flexibility constellation (hydrogen, biomethanation, and 764 MW PHES).

```latex
% Figure 5 injection block — self-contained.
\begin{figure}[!t]
\centering
\includegraphics[width=\columnwidth]{fig_diagrama_3_constelacion_microsolvers.pdf}
\caption{Multi-vector flexibility constellation. Six physics-dedicated solvers — photovoltaic (sigmoidal $Q$--$V$ control), wind ($C_p(\lambda,\beta)$ with synthetic inertia), hydrogen (electrolysis, 700 bar compression, 740 refuelling stations), biochemical (ADM1 digestion of sargasso and vinasse), thermal (heat-rate dispatch), and reversible PHES (764 MW, Sabaneta/Dos Bocas) — deliver their net injections $(P_g, Q_g)$ through a zero-trust dispatch supervisor and a SHA-512-signed boundary-state manifest to the 142-bus master solver of the national network.}
\label{fig:constellation}
\end{figure}
```

### B. Electrochemical power-to-gas operation

Operationally, the power-to-gas block of Section II-H behaves as a pair of opposing flexible loads with memory. In surplus hours — the growing regime in which instantaneous solar penetration reaches 36.6% and midday prices collapse — the electrolyzer absorbs what the network would otherwise curtail, converting it into pressurized inventory; in deficit hours the fuel cell returns firm energy at the efficiency ratio $\eta_{\mathrm{EL}} \cdot \eta_{\mathrm{FC}}$. The buffer constraints make the intertemporal opportunity set explicit and auditable, and the coupling terms enter the AC balances without any relaxation of network physics. Interconnection of the coupled assets follows the inverter-based-resource requirements of IEEE Std 2800-2022 [23] and the distributed-energy interface of IEEE Std 1547-2018 [21].

### C. Pumped storage and biomethanation buffers

The reversible 764 MW pumped-storage fleet of the El Valle multihub (Sabaneta / Dos Bocas plants) plays the complementary role at system scale: it converts nocturnal and surplus energy into synchronized inertia-bearing capacity for the deficit hours, with reservoir dynamics analogous to the hydrogen buffer and dispatch subject to the same KKT-certified optimality. The ADM1 biochemical layer adds a third buffer with a different time constant: digester state dynamics convert sargasso and vinasse inflows into biomethane that enters the thermal dispatch as a storable, renewable fuel — closing a nutrient-and-energy loop with direct land-use relevance under the same territorial statute that defines the partition.

Following the standard practice of IEEE Power & Energy Society benchmarks (e.g., RTS-GMLC, Texas-2000), SENI-142 decouples the validated historical operational base of the conventional fleet from the standardized energy-transition storage portfolio — the reversible pumped-hydro plants of Sabaneta/Dos Bocas and the metropolitan battery energy storage system (BESS) — modeled as a prospective buffer for multi-temporal AC-OPF studies under the expansion plans of the CNE and EGEHID. In the 215-single-contingency $N-1$ catalog, storage remains inactive ($\Delta P_{\mathrm{storage}} = 0$); only in the canonical common-mode reserve-sizing event — the complex trip or its evacuation-trunk trip, LINE-345-PC-JS (Section V-D) — does the 58.5 MW fast discharge vector participate.

### D. The zonal CAPEX/OPEX economic proof

The economic layer validates the flexibility stack by zonal balancing: for the reference zone (the metropolitan 138 kV triangle of Section III-B), the released harness accounts, per hour and per flexibility asset, four terms of the zonal welfare identity,

$$\Delta C^{\mathrm{zone}}_t = \underbrace{c^{\mathrm{curt}} E^{\mathrm{abs}}_t}_{\text{curtailment avoided}} + \underbrace{c^{\mathrm{fuel}} E^{\mathrm{displ}}_t}_{\text{fuel displaced}} + \underbrace{c^{\mathrm{ss}} N^{\mathrm{avoid}}_t}_{\text{start-stop avoided}} + \underbrace{\big(R^{\mathrm{base}}_t - R^{\mathrm{flex}}_t\big)}_{\text{loss differential}},$$

where $E^{\mathrm{abs}}_t$ is the renewable energy absorbed by electrolysis and pumping instead of being curtailed, $E^{\mathrm{displ}}_t$ the thermal energy displaced by fuel-cell and biomethane re-injection, $N^{\mathrm{avoid}}_t$ the avoided thermal unit start-stop events, and $R^{\mathrm{base}}_t - R^{\mathrm{flex}}_t$ the network-loss differential between the flexible and inflexible dispatches; the identity is enforced per zone and per hour so that every economic conclusion reconciles with a physical state. Unit costs and capital charges are parameterized transparently from national planning and international hydrogen references [31], [34], [35], and the balancing identity is closed against the bootstrap envelope of the operational record. The qualitative findings are stable across the envelope: the flexibility stack absorbs a material fraction of otherwise-curtailed solar surplus, reduces thermal start-stop cycling on the coal anchor, and defers firm-capacity additions in the reference zone — with all quantities reproducible from the released dataset rather than asserted.

## V. Silicon Performance, Accuracy and Numerical Benchmarking

### A. Measurement validity through digital-twin determinism

Section II-F established that promotion to the production state is atomic and bit-identical to a SHA-512-sealed Golden Master. The consequence for this section is epistemic: every number below is a property of a frozen, attestable software state, re-runnable by any reader who obtains the released artifact. This is the operational meaning of "verified in silicon" — not a rhetorical flourish but a chain of custody. Algorithm 2 states the resilience-and-sealing pipeline that produced the performance record.

**Algorithm 2.** $N-1$ resilience sweep with block-bootstrap envelope and cryptographic sealing (injection block below).

```latex
\begin{algorithm}[!t]
\caption{$N$--$1$ resilience sweep with 24-hour block bootstrap and SHA-512 sealing}
\label{alg:n1_seal}
\begin{algorithmic}[1]
\Require sealed solver state $\Sigma$, contingency catalog $\mathcal{C}$
         ($|\mathcal{C}| = 215$), horizon $\mathcal{H}$ (87,360 h)
\Ensure resilience record $\mathcal{R}$, seal $\sigma$
\State $\mathcal{R} \gets \emptyset$
\For{$c \in \mathcal{C}$} \Comment{deterministic order, fail-closed}
   \For{$b \in \text{bootstrap}(\mathcal{H}, 24\,\mathrm{h})$} \Comment{whole-day blocks}
      \State inject contingency $c$ on block $b$; run Algorithm 1 at every hour
      \State record $\rho$, $\kappa_2$, voltage/frequency margins into $\mathcal{R}[c, b]$
   \EndFor
\EndFor
\State aggregate margins over the bootstrap envelope per contingency
\State $\sigma \gets \mathrm{SHA512}\text{-chain}(\Sigma, \mathcal{C}, \mathcal{R})$ \Comment{detached manifest}
\State \Return $\mathcal{R}$, $\sigma$
\end{algorithmic}
\end{algorithm}
```

### B. Convergence speed and memory

On consumer-grade commercial hardware (an 8-thread laptop of the Dell Inspiron 5570 class), the partitioned solver converges each hourly AC state of the complete 142-bus national network in **2.65 ms** with a resident footprint of **473 MiB** holding the standardized validation horizon of 520 complete weeks (87,360 hourly states over 3,640 Monday-to-Sunday days). The sweep completes in minutes, where monolithic campaigns of the same horizon on the same class of hardware demand hours to days, consistent with the $O(N^3)$-to-$O(\sum_k N_k^3 + N_B^3)$ asymptotics of Proposition 1 and with fill-reducing sparse practice [5], [6]. The 2.65 ms execution time sits two to three orders of magnitude inside the standard 1--5 s cycle of modern Energy Management System (EMS) state estimators, enabling real-time static contingency screening over thousands of concurrent operating states.

Three operational consequences follow from this envelope and are worth stating explicitly, because they change who can use the benchmark, not merely how fast. First, *study cadence*: a ten-year-scale national sweep is no longer a campaign to be scheduled but a question to be asked; parameter studies, bootstrap envelopes, and contingency catalogs re-execute interactively, which changes the scientific workflow from batch archaeology to live experimentation. Second, *deployment class*: the hardware requirement is a consumer laptop, not a computing cluster — a property with direct consequences for regulatory bodies, universities, and utilities in developing insular systems, for whom the alternative platforms carry license and infrastructure costs of a different order [19], [40]. Third, *pedagogical simultaneity*: a classroom can re-execute the national power flow of the hour being taught while it is being taught, collapsing the distance between the textbook operating point and the operating point on the actual system.

### C. Accuracy and numerical conditioning

Three measured quantities bound the numerical fidelity of the condensed solution. First, the fasorial border-coupling residual — the mismatch between the Schur-recovered state and an independent reference state — measures $\delta = 2.788 \times 10^{-14}\ \mathrm{pu}$ across the validation horizon, sitting more than an order of magnitude below the global rounding floor scaled by the worst border conditioning ($\varepsilon_{\mathrm{mach}}\kappa_2(\mathbf{S}) = 2.22 \times 10^{-16} \times 2{,}489.64 \approx 5.53 \times 10^{-13}$~pu) --- the small nonzero residue, the signature of two distinct factorization trajectories, is a direct benefit of the orthogonal and well-conditioned structure of the $\Gamma = 30$ boundary partition --- and nearly six orders of magnitude below the $10^{-8}$~pu stopping tolerance of the cascade. Second, the sigmoidal reactive-limit controller of Section II-G contributes a regularization error of $5.32 \times 10^{-12}$ while eliminating the PV–PQ limit cycle. Third, the spectral condition number $\kappa_2$ of every reduced border system is monitored and archived; the governance threshold machinery was validated on synthetic references before national deployment (the IEEE 14-bus 22×22 Jacobian classifies MARGINAL at $\kappa_2 = 117.7823$), so that a degradation of conditioning on the real grid would be detected against a calibrated scale rather than an ad-hoc one.

### D. Contingency resilience on the reference topology

The resilience battery evaluates the 215-contingency $N-1$ catalog — the transmission operator's own outage list, screened under the automatic branch-selection doctrine of [35] — on the live reference topology, concentrated on the metropolitan 138 kV ring whose real corridor distances (70.5 km, 50.0 km, 22.1 km) fix the electrical geometry, as shown in Figure 6. The outage of the Punta Catalina complex ($2 \times 376 = 752$~MW), the largest common contingency in the system, is solved under the preventive criterion of Section II-J: the active power deficit is covered through the redispatch of co-optimized spinning reserve ($\sum r_g^+ \ge 752$~MW), preserving post-event steady-state voltage and power-flow feasibility without load shedding ($P_{\mathrm{shed}} = 0$). The campaign's anomaly log also records severe voltage depression with reactive-margin depletion — $\lambda_{\min}(\mathbf{J}_R) < 10^{-2}$ on the reduced reactive block — in the JSAURI–Palamara–Haina 138 kV loop under specific $N-1$ states; these findings were added to the contingency catalog and drive the shunt-support bisection. All margins are reported under the 24-hour block-bootstrap envelope of Algorithm 2.

The four-clause PASS is a reportable numerical result, not a narrative claim. Table IV reports, for the eight most severe elements of the catalog — ranked by post-event voltage margin and thermal loading — the complete dispatch and verification row: pre-event flow or generation, worst post-event voltage, worst post-event branch loading, slack deviation after reserve deployment, co-optimized reserve redispatched, and unserved load. The unit-level trip (GEN-PC1, 376 MW) is the worst unitary $N-1$; the complex-level trip (GEN-PC-COMPLEX, $2 \times 376 = 752$~MW) is the worst common-mode event of the island, covered preventively by the reserve sizing; both rows close with every retained bus inside $[0.95, 1.05]$~pu, worst branch loading below 92.4% of thermal rating, bounded slack deviation, and zero unserved load ($P_{\mathrm{shed}} = 0.00$~MW).

LINE-138-CUM-SPMI is the corridor whose 2025 in-service failure is documented in the national press record [42]; its catalog row demonstrates that the modeled transmission grid carries the loss of that circuit without shedding ($P_{\mathrm{shed}} = 0$) under static AC feasibility. This analytical decoupling between steady-state deliverability and historical national blackouts is corroborated by primary forensic records: independent engineering investigations of the November 11, 2025 collapse [43] established that the blackout was initiated by maintenance switching in S/E SPM1, which lacked bus differential protection, triggering an uncoordinated cascade of distance protections that tripped 10 transmission circuits in 680 ms; the primary forensic reports of the Universidad Autónoma de Santo Domingo (UASD) and the System Operator record a 15-minute (P15) window mean frequency of 55.11 Hz during the collapse, with 99.89% of the window outside the normal operating band, per the Operator's hourly SCADA telemetry record of the 13:15–13:30 collapse window [45]. Similarly, the May 16, 2015 national blackout (1,782.65 MW disconnected) originated in a 138 kV busbar fault at Itabo Gas compounded by circuit breaker failure with clearing times exceeding $10\times$ nominal [44]. The empirical benchmark confirms that the Dominican transmission estate possesses sufficient post-contingency thermal and voltage deliverability under $N-1$; historical vulnerabilities are transient, dynamic, and protection-coordination failures that belong strictly to the dynamic domain.

The two most scrutinized rows admit an explicit physical reading. For the PALA–SCNU double-circuit corridor (ACSR 795 kcmil Drake conductor, 26/7 stranding, 988 A continuous at 75 °C, $S^{\max} = 236.2$ MVA per circuit and 472.4 MVA for the aggregate corridor), the pre-event state carries 412.7 MW — 206.4 MW per circuit, an 87.4% initial loading; after one circuit trips, the surviving twin assumes 206.7 MW, the reported 87.6% loading, while the surplus redistributes through the meshed metropolitan ring: the 30.86 km (route length) 230 kV JSAURI–SCN tie picks up about 142 MW (83.3% loading) and the 70.5 km JSAURI–PALA 138 kV circuit absorbs about 64 MW (89.2%), with no steady-state thermal violation. For the complex-level Punta Catalina trip, the co-optimized reserve redispatch replaces the lost injection exactly ($\Delta P_g = 752.0$ MW, deployed across geographically remote thermal, hydroelectric, and renewable units), so the residual deviation at the reference bus is physically the incremental transport loss of rerouting 752 MW across the 142-bus estate: $\Delta P_{\mathrm{slack}} = \Delta P_{\mathrm{loss}} = +24.8$ MW, a 0.72% increase over the 3,450 MW reference national demand. In the LINE-345-PC-JS row, the 752 MW deficit closes exactly through two separate dispatch variables of the multi-vector formulation: $\Delta P_g = 687.40$ MW of conventional thermal/hydro redispatch (Quisqueya I–II 180.0, AES Andrés CC 145.0, Estrella del Mar III 110.0, Barahona coal/CEPP 95.0, Valdesia–Tavera hydro 82.4, Monte Plata solar reserve 75.0) and $\Delta P_{\mathrm{storage}} = 58.50$ MW of fast storage discharge (reversible PHES Sabaneta/Dos Bocas 35.0 MW; metropolitan BESS 23.5 MW), with the residual $\Delta P_{\mathrm{slack}} = +6.10$ MW of marginal transport losses closing the balance at exactly 752.00 MW (zero error). The resulting 0.89% loss ratio — versus 2.5–3.3% for purely remote redispatch — follows from injecting the storage in direct electrical proximity to the metropolitan load ring, bypassing the long-distance 345/230 kV trunks. The LINE-345-PC-JS corridor is the sole bulk-evacuation trunk of the Punta Catalina thermal complex ($2 \times 376 = 752$ MW); its physical trip isolates the full complex injection at the SENI trunk node, configuring the canonical common-mode reserve-sizing event. Newton–Raphson convergence was verified at $\|\Delta P, \Delta Q\|_{\infty} \le 10^{-8}$ pu in at most four iterations per state, with exact nodal balance, inside the sealed validation output of the canonical suite.

**Table IV.** Worst-Case Critical Contingencies: Dispatch and Post-Event Static Verification Report.

| Contingency ID | Monitored Asset | Outage Type | Pre-event Flow/Gen (MW) | $\min V_i$ (pu) | $\max \|S\|/S_{\max}$ (%) | $\Delta P_{\mathrm{slack}}$ (MW) | $\Delta P_g$ (MW) | $P_{\mathrm{shed}}$ (MW) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `GEN-PC1` | Punta Catalina Unit 1 (376 MW) | Unit $N-1$ | 376.0 | 0.9612 | 91.7 | $+12.4$ | 376.0 | **0.00** |
| `GEN-PC-COMPLEX` | Punta Catalina Complex ($2 \times 376\text{ MW}$) | Common-Mode | 752.0 | 0.9581 | 92.4 | $+24.8$ | 752.0 | **0.00** |
| `LINE-345-PC-JS` | 345 kV Trunk Punta Catalina–JSAURI | Line $N-1$ | 748.3 | 0.9703 | 89.2 | $+6.1$ | 687.4 | **0.00** |
| `XFMR-345-138-JS` | JSAURI 345/138 kV Bank (600 MVA) | Xfmr $N-1$ | 521.7 | 0.9748 | 88.5 | $+4.7$ | 186.2 | **0.00** |
| `LINE-138-CUM-SPMI` | 138 kV SPM–Cumayasa Line | Line $N-1$ | 172.1 | 0.9802 | 84.1 | $+2.9$ | 96.4 | **0.00** |
| `CORR-138-PALA-SCNU` | 138 kV PALA–SCNU double-circuit corridor, 22.1 km (one circuit loss) | Corridor $N-1$ | 206.4 | 0.9755 | 87.6 | $+5.2$ | 158.3 | **0.00** |
| `LINE-230-JS-SCNU` | 230 kV JSAURI–SCNU Tie | Line $N-1$ | 356.2 | 0.9790 | 83.3 | $+3.8$ | 141.7 | **0.00** |
| `GEN-AES-ANDRES` | AES Andrés Combined Cycle (319 MW) | Unit $N-1$ | 319.0 | 0.9846 | 78.5 | $+8.3$ | 319.0 | **0.00** |

*Note: All rows satisfy the four-clause PASS of Section II-J: convergence $\|\Delta P, \Delta Q\|_{\infty} \le 10^{-8}$ pu; $V_i \in [0.95, 1.05]$ pu; $|S_\ell| \le S_\ell^{\max}$; $|\Delta P_{\mathrm{slack}}| \le \varepsilon_{\mathrm{slack}}$ with $P_{\mathrm{shed}} = 0$. Static post-contingency AC feasibility verification states computed on the complete canonical 142-bus transmission model under the multi-temporal dispatch baseline. The outage GEN-PC-COMPLEX ($2 \times 376 = 752$~MW) represents the common-mode benchmark reference for spinning reserve dimensioning ($R^{\mathrm{req}}$), treated as an external sizing event beyond the 215 single outage ($N-1$) catalog. The LINE-345-PC-JS trunk is the sole bulk-evacuation path of the complex ($2 \times 376 = 752$~MW); its loss constitutes the canonical common-mode reserve-sizing event. For the PALA–SCNU double-circuit corridor, the pre-event flow is the 206.4 MW carried by the tripped circuit within a 412.7 MW aggregate corridor flow; the reported 87.6% post-event loading refers to the surviving circuit and adjacent ties, within actual conductor thermal ratings. Conductor: ACSR 795 kcmil Drake (26/7), 988 A continuous at 75 °C, $S^{\max} = 236.2$ MVA per circuit (472.4 MVA aggregate).*

**Figure 6.** Real subtransmission triangle of the SENI 138 kV ring.

```latex
% Figure 6 injection block.
\begin{figure}[!t]
\centering
\input{sec03_fig_topologia_seni_tikz}
\caption{Real subtransmission triangle of the SENI 138 kV ring. JSAURI--PALA--SCNU with geodesic line lengths of 70.5, 50.0, and 22.1 km, the 230 kV JSAURI--SCNU reinforcement (dashed), the 345 kV transmission bar decoupled to the left as system slack ($V = 1.02$ pu) receiving Punta Catalina ($2 \times 376$ MW), the SCNU renewable hub (58.9 MW hydro, 95 MW solar, 34 MW wind) and the prospective 50 MW PEM electrolysis block (non-operational, 2026, asterisked), and the PALA load center (1,645 MW aggregate). The 215-contingency $N-1$ catalog of the validation battery is defined on this topology.}
\label{fig:topologia_seni}
\end{figure}
```

**Table V.** Silicon telemetry of the SENI-142 digital twin (all values from sealed validation runs).

| Metric | Value | Condition |
|---|---|---|
| Convergence time per hourly national AC state | 2.65 ms | 142-bus full model, consumer laptop (8 threads) |
| Resident memory, full horizon | 473 MiB | 87,360 hourly states (520 complete weeks) |
| Fasorial border-coupling residual $\delta$ | $2.788 \times 10^{-14}$ pu | Schur reconstruction vs. reference state |
| Reactive-limit regularization error | $5.32 \times 10^{-12}$ | Sigmoidal controller, analytic Jacobian injection |
| Static screening capacity (EMS) | 2.65 ms / state | Inside 1--5 s EMS state estimation cycle |
| Contingency catalog | 215 $N-1$ scenarios | Phase-2 static post-event verification |
| Spectral cross-check (IEEE 14-bus, 22×22) | $\kappa_2 = 117.7823$ (MARGINAL) | External validity control |
| Largest single contingency | Punta Catalina trip, 752 MW | Feasible in steady state with spinning reserve ($P_{\mathrm{shed}} = 0$) |

## VI. Discussion and Policy Implications

**Deterministic resilience for hurricane-exposed islands.** Caribbean insular systems plan not against statistical weather but against named storms. A benchmark whose $N-1$ margins carry correlation-honest bootstrap envelopes, whose largest credible contingency is exercised explicitly, and whose state resolution sits comfortably inside the 1--5 s EMS screening cycle converts resilience from an aspiration into a scheduled computation. For a country that has twice in twelve months mobilized around nationwide interruptions [30], [46], and where post-collapse restoration historically exceeds 10 to 14 hours due to Ferranti overvoltages ($B_{\mathrm{shunt}}$) on unloaded lines tripping black-start units, the difference between hours-long legacy studies and 2.65 ms diakoptic states is profound: Law 368-22 territorial partitioning provides the steady-state computational substrate for bottom-up modular restoration through concurrent territorial microgrids, mitigating the Ferranti-effect overvoltages associated with no-load line energization and accelerating national re-synchronization.

**Planning law as a computational boundary.** The partition of this benchmark is not an optimization artifact: it is the national territorial statute [32]. When the electrical partition coincides with the planning regions of Law 368-22, every simulation result is already expressed in the units in which permits, land use, and microgrid autonomy are decided — and the autonomy question (which territory can stand alone after a trunk loss?) becomes a property of the model rather than a separate study. The renewable incentive framework [33] and the national expansion planning cycle [31] acquire, in consequence, a common evidentiary substrate.

**Standards alignment and data sovereignty.** The benchmark speaks the standards it must interoperate with: CIM-consistent model interchange [25], measurement-grade power-quality definitions [24], [22], harmonic practice [20], study-method recommended practice [19], and inverter-based-resource interconnection [23], [21]. At the same time, the underlying operational archives remain under national custody: the released benchmark carries structure, parameters, and validation harness, while the sovereign telemetry layer is governed by national institutions. This separation — open science on structure, sovereign custody on archives — is a deliberate policy architecture, not an omission.

**Capacity building.** A national grid that can be simulated openly is a national grid that can be taught openly. The same artifact that serves this article serves university laboratories: doctoral and undergraduate exercises execute against the real estate — its distances, its outages, its anchors — instead of the drafting-table abstractions of 1962, closing the gap between the classroom and the control room.

**Limitations.** The honest boundaries of the present release are: (i) the 69 kV layer enters through static equivalents, exact at the boundary for power flow but not for short-circuit transients inside condensed areas; (ii) the formulation is phasor-domain — electromagnetic transient studies require an EMT extension; (iii) telemetry arrives at operational latency, so the twin is causal but not clairvoyant; and (iv) market settlement is out of scope of the present release, though the hourly resolution of the horizon is settlement-grade.

**Replication for other island systems.** Finally, the methodology is deliberately portable, and the porting protocol is part of the contribution. Because the invariant formulation touches no geography, replicating SENI-142 for another insular system requires only the territorial clause to be re-instantiated: (1) the network estate assembled to the same nodal rule (one bus per voltage level per substation, transformers as branches); (2) the operational horizon ingested under the same data-protocol sentence with the substitutable system operator named; (3) the partition declared from the governing territorial statute of the jurisdiction, whatever it is, with the legal layer bundled into electrical macro-subdomains by trunk-tie topology; and (4) the deterministic lifecycle re-sealed from the first gate. The Republic's benchmark thus functions simultaneously as artifact and as template — an instrument for its own country and a reproducibility contract for the insular world.

## VII. Conclusion and Future Work

This article contributed SENI-142: an open-access, measured, and deterministically reproducible benchmark of an entire national transmission system — 142 buses, approximately 112 substations, 135 lines, 58 transformers, ten territorial microgrids under Law 368-22 — with an exact diakoptic condensation that resolves each hourly national AC state in 2.65 ms and 473 MiB at fasorial residual $\delta = 2.788 \times 10^{-14}\ \mathrm{pu}$, validated against a decade of continuous operational telemetry and sealed by a four-phase digital-twin lifecycle; the benchmark, the validation harness, and the resilience record are openly released as stated in the Data Availability statement.

Four research routes follow directly. First, **sub-second physics-informed neural surrogates**: the 87,360-state horizon (520 complete weekly cycles) is the training ground for learned accelerators of the classical sweep, with the exact solver retained as the falsification oracle [18]. Second, **grid-forming EMT co-simulation**: embedding converter control-level dynamics of grid-forming resources [17], [23] inside the partitioned envelope to study frequency formation, not only frequency containment. Third, **electrolyzer membrane degradation under transient dispatch**: the power-to-gas block's intertemporal operation is the natural load profile for aging studies of PEM stacks [34], [35]. Fourth, **distributed hourly settlement in silicon**: the settlement-grade hourly horizon, the signed manifests, and the Merkle-style provenance chain [27], [28] outline a settlement architecture in which every priced hour reconciles against a cryptographically attested physical state. The island that could not import inertia has, in its own measured image, produced something exportable: a public instrument for the engineering of energy autonomy.

## Nomenclature

| Symbol | Definition |
|---|---|
| $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ | Connected undirected graph of the transmission network |
| $\mathcal{V}$, $|\mathcal{V}| = 142$ | Set of transmission buses |
| $\mathcal{E}_{\mathrm{line}}$, $\mathcal{E}_{\mathrm{trafo}}$ | Line branches (135), transformer branches (58) |
| $\mathbf{Y}_{\mathrm{bus}}$ | Nodal admittance matrix, $\mathbb{C}^{142 \times 142}$ |
| $S_i = P_i + j Q_i$ | Complex power injection at bus $i$ |
| $Z_{\mathrm{cc}}$ | Short-circuit impedance of a reduced area |
| $\mathcal{G}_k$, $\Omega_k$ | Territorial microgrid $k$ and its macro-subdomain |
| $\mathcal{V}_B$, $\Gamma$ | Border bus set and condensation boundary |
| $\mathbf{A}, \mathbf{B}, \mathbf{C}, \mathbf{D}$ | Interior/border blocks of the reordered system matrix |
| $\mathbf{S} = \mathbf{D} - \mathbf{C}\mathbf{A}^{-1}\mathbf{B}$ | Schur complement of the interior block |
| $\mathbf{x}_I$, $\mathbf{x}_B$, $\mathbf{u}_I$, $\mathbf{u}_B$ | Interior/border states and right-hand sides |
| $N$, $N_k$, $N_B$ | System, subdomain, and border dimensions |
| $\kappa_2(\cdot)$ | Spectral condition number |
| $\delta$ | Fasorial border-coupling residual (pu) |
| $P_i(\mathbf{V}_t, \boldsymbol{\theta}_t)$ | Nodal real-power injection from the network state |
| $P^{\mathrm{EL}}_{h,t}$, $P^{\mathrm{FC}}_{h,t}$ | Electrolyzer / fuel-cell electrical power of unit $h$ |
| $\eta_{\mathrm{EL}}$, $\eta_{\mathrm{FC}}$ | Electrolysis / reconversion efficiencies |
| $E_{h,t}$, $E_h^{\min}$, $E_h^{\max}$ | Hydrogen buffer inventory and bounds |
| $\Delta t$ | Time-step duration (1 h) |
| $C_p(\lambda, \beta)$ | Wind turbine power coefficient |
| $\sigma(\cdot)$, $\alpha$ | Sigmoidal activation and its adaptive slope |
| $Q_g^{\lim}$, $Q_g^{\mathrm{eff}}$ | Generator reactive limit and regularized capability |
| PHES | Pumped-storage hydroelectricity (764 MW reversible fleet) |
| ADM1 | Anaerobic Digestion Model No. 1 |
| PEM | Proton-exchange membrane (electrolysis) |

**Data Availability.** The SENI-142 benchmark dataset, network parameters, provenance metadata, validation harness, and sealed resilience record are openly available at https://github.com/Junvillan/seni142-benchmark, with a mirrored archival deposit on IEEE DataPort.

## References

[1] G. Kron, *Diakoptics: The Piecewise Solution of Large-Scale Systems*. London, U.K.: MacDonald, 1963.

[2] H. H. Happ, *Diakoptics and Networks*. New York, NY, USA: Academic Press, 1971.

[3] W. F. Tinney and C. E. Hart, "Power flow solution by Newton's method," *IEEE Transactions on Power Apparatus and Systems*, vol. PAS-86, no. 11, pp. 1449–1460, Nov. 1967.

[4] B. Stott and O. Alsac, "Fast decoupled load flow," *IEEE Transactions on Power Apparatus and Systems*, vol. PAS-93, no. 3, pp. 859–869, May/Jun. 1974.

[5] A. George, "Nested dissection of a regular finite element mesh," *SIAM Journal on Numerical Analysis*, vol. 10, no. 2, pp. 345–363, 1973.

[6] Y. Saad, *Iterative Methods for Sparse Linear Systems*, 2nd ed. Philadelphia, PA, USA: SIAM, 2003.

[7] F. Zhang, Ed., *The Schur Complement and Its Applications* (Numerical Methods and Algorithms, vol. 4). New York, NY, USA: Springer, 2005.

[8] J. Nocedal and S. J. Wright, *Numerical Optimization*, 2nd ed. New York, NY, USA: Springer, 2006.

[9] H. W. Dommel and W. F. Tinney, "Optimal power flow solutions," *IEEE Transactions on Power Apparatus and Systems*, vol. PAS-87, no. 10, pp. 1866–1876, Oct. 1968.

[10] A. J. Wood, B. F. Wollenberg, and G. B. Sheblé, *Power Generation, Operation, and Control*, 3rd ed. Hoboken, NJ, USA: Wiley, 2013.

[11] P. Kundur, *Power System Stability and Control*. New York, NY, USA: McGraw-Hill, 1994.

[12] T. Van Cutsem and C. Vournas, *Voltage Stability of Electric Power Systems*. New York, NY, USA: Springer, 1998.

[13] G. C. Ejebe and B. F. Wollenberg, "Automatic contingency selection," *IEEE Transactions on Power Apparatus and Systems*, vol. PAS-98, no. 1, pp. 97–109, Jan./Feb. 1979.

[14] N. Hatziargyriou, J. V. Milanović, C. Rahmann, V. Ajjarapu, C. Cañizares, I. Erlich, D. Hill, I. Hiskens, I. Kamwa, B. Pal, and V. Vittal, "Definition and classification of power system stability — revisited & extended," *IEEE Transactions on Power Systems*, vol. 36, no. 4, pp. 3271–3281, Jul. 2021.

[15] P. Tielens and D. Van Hertem, "The relevance of inertia in power systems," *Renewable and Sustainable Energy Reviews*, vol. 55, pp. 999–1009, Mar. 2016.

[16] F. Milano, F. Dörfler, G. Hug, D. J. Hill, and G. Verbič, "Foundations and challenges of low-inertia systems," in *Proc. 20th Power Systems Computation Conference (PSCC)*, Dublin, Ireland, 2018, pp. 1–25.

[17] R. Rosso, X. Wang, M. Liserre, F. Lu, and S. Engelken, "Grid-forming converters: Control approaches, grid-synchronization, and future trends — a review," *IEEE Open Journal of Industry Applications*, vol. 2, pp. 93–109, 2021.

[18] G. S. Misyris, A. Venzke, and S. Chatzivasileiadis, "Physics-informed neural networks for power systems," in *Proc. 21st Power Systems Computation Conference (PSCC)*, Porto, Portugal, 2020, pp. 418–425.

[19] IEEE Std 399-1997, *IEEE Recommended Practice for Industrial and Commercial Power System Analysis* (IEEE Brown Book), IEEE, New York, NY, USA, 1998.

[20] IEEE Std 519-2022, *IEEE Standard for Harmonic Control in Electric Power Systems*, IEEE, New York, NY, USA, 2022.

[21] IEEE Std 1547-2018, *IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces*, IEEE, New York, NY, USA, 2018.

[22] IEEE Std 1459-2010, *IEEE Standard Definitions for the Measurement of Electric Power Quantities Under Sinusoidal, Nonsinusoidal, Balanced, or Unbalanced Conditions*, IEEE, New York, NY, USA, 2010.

[23] IEEE Std 2800-2022, *IEEE Standard for Interconnection Requirements for Inverter-Based Resources Interconnecting with Transmission and Subtransmission Systems*, IEEE, New York, NY, USA, 2022.

[24] IEC 61000-4-30, *Electromagnetic Compatibility (EMC) — Part 4-30: Testing and Measurement Techniques — Power Quality Measurement Methods*, International Electrotechnical Commission, Geneva, Switzerland, 2015.

[25] IEC 61970 (series), *Energy Management System Application Program Interface (EMS-API) — Common Information Model (CIM)*, International Electrotechnical Commission, Geneva, Switzerland.

[26] D. J. Batstone, J. Keller, I. Angelidaki, S. S. Kalyuzhnyi, S. G. Pavlostathis, A. Rozzi, W. T. M. Sanders, H. Siegrist, and V. A. Vavilin, "The IWA anaerobic digestion model no 1 (ADM1)," *Water Science and Technology*, vol. 45, no. 10, pp. 65–73, 2002.

[27] R. C. Merkle, "A digital signature based on a conventional encryption function," in *Advances in Cryptology — CRYPTO '87*, Lecture Notes in Computer Science, vol. 293. Berlin, Germany: Springer, 1988, pp. 369–378.

[28] National Institute of Standards and Technology, *Secure Hash Standard (SHS)*, FIPS PUB 180-4, Gaithersburg, MD, USA, Aug. 2015.

[29] U.S.–Canada Power System Outage Task Force, *Final Report on the August 14, 2003 Blackout in the United States and Canada: Causes and Recommendations*, Apr. 2004.

[30] Organismo Coordinador del Sistema Eléctrico Nacional Interconectado (OC-SENI), *Operational telemetry, dispatch archives, and event logs of the Dominican interconnected system*, Santo Domingo, Dominican Republic, 2016–2025.

[31] Comisión Nacional de Energía (CNE), *Plan de Expansión de la Generación Eléctrica 2022–2036*, Santo Domingo, Dominican Republic, 2022.

[32] Congreso Nacional de la República Dominicana, *Ley No. 368-22 de Ordenamiento Territorial, Uso de Suelo y Asentamientos Humanos*, Gaceta Oficial, Santo Domingo, Dominican Republic, 2022.

[33] Congreso Nacional de la República Dominicana, *Ley No. 57-07 sobre Incentivo a las Energías Renovables y Regímenes Especiales*, Santo Domingo, Dominican Republic, 2007.

[34] International Renewable Energy Agency (IRENA), *Green Hydrogen Cost Reduction: Scaling up Electrolysers to Meet the 1.5°C Climate Goal*, Abu Dhabi, United Arab Emirates, 2020.

[35] International Energy Agency (IEA), *Global Hydrogen Review 2023*, Paris, France, 2023.

[36] M. E. J. Newman, *Networks: An Introduction*. Oxford, U.K.: Oxford University Press, 2010.

[37] Empresa de Transmisión Eléctrica Dominicana (ETED), *Technical documentation of the national transmission estate*, Santo Domingo, Dominican Republic.

[38] F. Dörfler, M. Chertkov, and F. Bullo, "Synchronization in complex oscillator networks and smart grids," *Proceedings of the National Academy of Sciences*, vol. 110, no. 6, pp. 2005–2010, 2013.

[39] D. K. Molzahn and I. A. Hiskens, "A survey of relaxations and approximations for optimal power flow," *Foundations and Trends in Electric Energy Systems*, vol. 4, no. 1–2, pp. 1–221, 2019.

[40] R. D. Zimmerman, C. E. Murillo-Sánchez, and R. D. Thomas, "MATPOWER: Steady-state operations, planning, and analysis tools for power systems research and education," *IEEE Transactions on Power Systems*, vol. 26, no. 1, pp. 12–19, Feb. 2011.

[41] S. Babaeinejadsarookolaee *et al.*, "The Power Grid Library for benchmarking AC optimal power flow algorithms," arXiv preprint, 2019.

[42] Y. Crespo, "SENI: registro hemerográfico de 89 apagones nacionales y cronología de la salida del 11 de noviembre de 2025 en la subestación 138/69 kV SPMI y la línea de 138 kV SPM--Cumayasa," *Listín Diario*, Santo Domingo, Dominican Republic, Nov. 13, 2025.

[43] Instituto de Energía, Universidad Autónoma de Santo Domingo (IEUASD), "Resumen Ejecutivo del IEUASD sobre el Evento del SENI del 11 de noviembre de 2025," Facultad de Ingeniería y Arquitectura, Santo Domingo, Dominican Republic, Nov. 2025, 5 pp., available at uasd.edu.do (analyzes SPM1 bus fault without differential protection and distance cascade; P15 window-mean frequency of 55.11 Hz with 99.89% outside band recorded in Organismo Coordinador OC-SENI hourly metrology log, window 13:15–13:30).

[44] Organismo Coordinador del SENI (OC-SENI), "Informe de perturbación: colapso del SENI por falla de barraje de 138 kV e interruptor en Central Itabo Gas del 16 de mayo de 2015," Santo Domingo, Dominican Republic, May 2015 (1,782.65 MW disconnected; breaker clearing time exceeding 10× nominal; see also *Listín Diario*, May 17, 2015).

[45] Organismo Coordinador del Sistema Eléctrico Nacional Interconectado (OC-SENI), "Reporte Horario y Registro Cronológico de Telemetría SCADA del 11 de noviembre de 2025," Santo Domingo, Dominican Republic, Nov. 2025 (collapse window 13:15:00–13:30, P15; p. 4, §2.3, Fig. 2 and Table 1: P15 window-mean frequency 55.11 Hz with 99.89% of the window outside the normal operating band, 59.8 ≤ f ≤ 60.2 Hz).

[46] Diario Libre, "Apagón general por falla en circuito troncal de 138 kV Hainamosa--Villa Duarte," Santo Domingo, Dominican Republic, Feb. 24, 2026.

## Appendix A — IEEEtran Injection Map

For the camera-ready assembly, the following table is the complete mapping between this master's figures, the vector bank of the project, and the injection action required. Blocks for Figures 3, 4, and 5 are already self-contained; blocks for Figures 1, 2, and 6 reference the chapter sources whose `tikzpicture` is extracted verbatim (the extraction is mechanical: the figure environments in the sources are self-contained and idempotent, with palette definitions safe to re-define).

| Manuscript figure | Bank source | Injection action |
|---|---|---|
| Figure 1 (digital-twin lifecycle) | `sec01_introduccion_y_marco_metodologico.tex`, figure environment (tikzpicture at L97–142) | Extract `tikzpicture` to `sec01_fig_gemelo_fases_tikz.tex`; block ready |
| Figure 2 (power-to-gas coupling) | `sec02_modelado_matematico_ac_h2_sgen.tex`, figure environment (tikzpicture at L65–85) | Extract to `sec02_fig_p2g_h2_tikz.tex`; block ready |
| Figure 3 (JSAURI 345/138 decoupling) | `fig_diagrama_1_jsauri_345_138.pdf` (compiled) | None — `\includegraphics` wired |
| Figure 4 (HBCF partition and Schur structure) | `fig_diagrama_2_schur_hbcf.pdf` (compiled) | None — `\includegraphics` wired |
| Figure 5 (flexibility constellation) | `fig_diagrama_3_constelacion_microsolvers.pdf` (compiled) | None — `\includegraphics` wired |
| Figure 6 (138 kV reference triangle) | `sec03_topologia_redes_ieee_y_seni_tikz.tex`, figure environment (tikzpicture at L155–213) | Extract to `sec03_fig_topologia_seni_tikz.tex`; block ready |

Algorithms 1 and 2 use the standard `algorithm`/`algorithmic` pairing of the IEEEtran toolchain and inject without modification. All mathematics in this master is native LaTeX and migrates verbatim; the two verbatim protocol clauses (Section II-E and Section II-I) must be preserved character-for-character in the camera-ready text, as they are contractual.

---

*Manuscript master v1.0 — SENI-142, October 17, 2026. Sealed companion artifacts: SHA-512 sidecar and mission manifest in this folder; the deterministic audit record (structure, confidentiality, canonical figures, verbatim clauses, figures and algorithms, seals) is maintained in the project session records and referenced from the delivery report.*
