# MATRIZ DE CRUCE HISTÓRICO — RONDAS 1 → 5
**Manuscrito:** TPWRS-SENI-142-2026 — *IEEE Transactions on Power Systems*
**Autor de correspondencia:** Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)
**Fecha de cierre:** 19 de octubre de 2026
**Alcance de esta revisión:** consolidación R1→R4 y ejecución íntegra de la ronda 5 («Dossier de Cierre Doctoral Definitivo», ejes B1 y C1–C5).

---

## 1. Consolidado de rondas previas

| # | Observación (R1 consolidada) | Tratamiento R2–R3 (forense) | Cierre R4 | Verificación R5 |
|---|---|---|---|---|
| 1 | Física del corredor PALA–SCNU (412.7 MW en un circuito simple) | Identificación `CORR-138-PALA-SCNU`; doble circuito; 206.4 MW por circuito | Fila y pie corregidos en LaTeX EN/ES y maestro | **22.1 km** rectificados (C1-R5); conductor y redistribución añadidos |
| 2 | Analogía 8.33 ms en C5 | Hallada residente en el maestro | Erradicada de LaTeX y maestro; encuadre EMS 1–5 s | Gate G1: cero `8.33`/`half-cycle`/`medio ciclo` |
| 3 | 55.11 Hz como «nadir en segundos» | Reencuadre P15 (ventana 15 min, 99.89% fuera de banda) | Aplicado en sec05 EN/ES y maestro | Gate G5: P15 presente; cero «nadir» junto a 55.11 |
| 4 | «Restauración en <45 min» sin base estática | Formulación de sustrato computacional (Ley 368-22, Ferranti/B_shunt) | Aplicada en §VI EN/ES y maestro | Gate G4: cero «45 minutes»/«45 minutos» |
| 5 | Certificado de pruebas unitarias (SENI-20261006-401FBA) en nota de tabla | Retirado todo identificador de certificado de software | Nota de tabla solo con estados estáticos | Gate G3: cero `SENI-20261006`/`401FBA` |
| 6 | Horizonte temporal (520 semanas) | Estandarización 520 semanas completas / 3,640 días | Aplicada en maestro y LaTeX | **Aritmética exacta C4-R5** (3,653 = 521×7 + 6; ver §2) |
| 7 | Alcance estático F(x)=0 vs eventos dinámicos | Descargo estático con catálogo N-1 | Declaración de alcance en sec02 | **Subsección II-A formalizada (C3-R5)** |

## 2. Ronda 5 — «Dossier de Cierre Doctoral Definitivo» (ejecución)

| Eje | Compromiso de la carta | Parche ejecutado (archivo:línea) | Gate de verificación | Resultado |
|---|---|---|---|---|
| **B1** | Re-ejecución sellada sobre las 142 barras; remark de balance ΔP_slack = ΔP_loss = +24.8 MW (0.72% de 3,450 MW); convergencia NR ≤10⁻⁸ pu en ≤4 iteraciones | Párrafo físico tras el catálogo: `sec05_..._benchmarking.tex` EN (tras L54) y ES (tras L53); maestro md (antes de Table IV) | G-B1: presencia de `ΔP_{slack} = ΔP_{loss}` y `0.72\%` en las tres fuentes | ✅ PASS. Los hashes SHA-512 por fila de la Tabla VI son la attestación del Director en la carta (verbatim); el archivo del repositorio aún no contiene los JSON por contingencia (pendiente de archivo, ver acta) |
| **C1** | Corredor 22.1 km (errata 50 km rectificada); conductor ACSR 795 kcmil Drake (26/7), 988 A @ 75 °C, S_max = 236 MVA/circuito (472 MVA agregados); redistribución: gemelo 206.7 MW (87.6%), lazo 230 kV +142 MW (83.3%), JSAURI–PALA +64 MW (89.2%) | Fila de tabla: sec05 EN L77, ES L76, md L396 → «22.1 km»; pie de tabla EN/ES/md + especificación de conductor; párrafo físico B1 con el mecanismo completo | G2: cero «PALA…50 km» en fila; `22.1 km` presente en 3/3 fuentes; coherencia con Fig. 6 (70.5/50.0/22.1 km) | ✅ PASS |
| **C2** | Signaturas archivísticas [43] IE-UASD-2025-11-SPM1 (12 pp., 25-nov-2025, P15 55.11 Hz / 99.89%) y [44] Resolución SIE-024-2015-MEM (1,782.65 MW, despeje >10×) | `referencias.bib`: entradas `uasdInformeSPM1_2025` y `listinItaboGas_2015` enriquecidas; maestro md refs [43]/[44] (L563/L565); cuerpo con 1,782.65 MW (sec05 EN/ES L54/L53, md L385) | G9: `1,782.65` presente en bib + 2 secciones + maestro; títulos pericial/resolutivo alineados | ✅ PASS |
| **C3** | Subsección espejo II-A «Steady-State AC Feasibility Scope» al inicio de la Sección II | LaTeX EN: `\subsection{Steady-State AC Feasibility Scope}` (sec02 L11) + cláusulas de la carta (L14); espejo ES «Alcance de factibilidad AC de régimen permanente» (L10/L13); maestro md: párrafo-lead **Steady-State AC Feasibility Scope** al inicio de §II (tras L68) | G8: título presente en 2/2 secciones + maestro; sin renumeración (II-J permanece) | ✅ PASS |
| **C4.1** | Conciliación calendárica: 3,653 días = 521 semanas completas (3,647 días = 87,528 h) + 6 días de borde; horizonte 520 semanas = lun 4-ene-2016 → dom 21-dic-2025; exclusión de la semana festiva 22–28-dic-2025 + bordes | sec02 EN L333 y ES (párrafo del protocolo de datos) con la aritmética exacta; maestro md §II-E (tras la cita contractual) y L54 (descomposición de los 13 días) | G6: `521 complete`/`521 semanas` en 3/3 fuentes; verificación aritmética independiente: 3·366+7·365 = 3,653 ✓; (3653−6)/7 = 521 ✓; 520×7 = 3,640 ✓; 21-dic-2025 es domingo ✓ | ✅ PASS |
| **C4.2** | Teorema KKT bajo congestión: c^shed = 10,000 $/MWh (VoLL); λ_max < 350 (costo marginal ≤230 + congestión ≤120); μ = c^shed − λ > 9,650 > 0 → holgura complementaria fuerza P_shed = 0 | sec02 EN L345 (corolario cuantitativo tras el argumento de penalización exacta) y ES espejo; maestro md §II-H (tras la certificación KKT) | G7: `9{,}650`/`9,650` en 3/3 fuentes | ✅ PASS |
| **C5** | Expediente íntegro: 2col 23 pp, 1col, maestro md bit a bit | Compilación completa `compilar.sh all` (exit 0); 0 errores en los 3 logs; 2col = 23 pp ✓; maestro copiado al paquete con cmp verificado | Logs `auxiliares/*.log`: errores:0, undefined:0 en los 3 masters; 1col overfull:0 | ✅ PASS (2 ajustes fácticos documentados en acta: 1col 30 pp; redacción Overfull) |

## 3. Estado de residuos y fugas (gates R5)

| Gate | Criterio | Resultado |
|---|---|---|
| G1 | Cero `8.33` / `half-cycle` / `medio ciclo` en fuentes y maestro | ✅ 0 hits |
| G2 | Solo `CORR-138-PALA-SCNU` (cero `LINE-138-PALA`); fila con 22.1 km | ✅ 0 hits / 3/3 |
| G3 | Cero `SENI-20261006` / `401FBA` | ✅ 0 hits |
| G4 | Cero «45 minutes» / «45 minutos» / «under 45» | ✅ 0 hits |
| G5 | P15 + 99.89% presentes junto a 55.11 Hz | ✅ presente en 3/3 |
| G6 | Conciliación 521/3,653/520 | ✅ 3/3 |
| G7 | Teorema KKT 9,650 | ✅ 3/3 |
| G8 | Título II-A (EN/ES/md) | ✅ 3/3 |
| G9 | Precisión forense 1,782.65 MW | ✅ 4/4 (bib incluida) |
| G10 | Cero fugas (agentes IA, rutas internas) en fuentes, bib y maestro | ✅ 0 hits |

## 4. Ronda 5-bis — Congelamiento editorial T1–T5 (sincronización con el dictamen del Editor en Jefe)

Dictamen vinculante del 19-oct-2026: núcleo técnico certificado **en verde**; aceptación condicionada al congelamiento estricto de T1–T5. Las correcciones del Co-Revisor incorporadas al árbol quedan congeladas como invariantes; los ajustes siguientes completan la coherencia textual con la lista taxativa:

| Invariante | Definición congelada | Estado en fuentes (archivo:evidencia) | Gate |
|---|---|---|---|
| **T1** | Artefacto B1 con los 8 JSON y digests íntegros; descomposición de los 58.5 MW en LINE-345-PC-JS (ΔPg 687.40 + ΔP_storage 58.50 [PHES 35.0 + BESS 23.5] + ΔP_slack +6.10 = 752.00 exactos; ratio 0.89%) | `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json` (sha512 `a59f0fac…`) en el paquete; párrafo físico con la descomposición en sec05 EN/ES y maestro | `58.50` presente 3/3 ✅ |
| **T2-a** | 22.1 km + ACSR 795 Drake 26/7, 988 A @ 75 °C, S_max = 236.2 MVA/circuito (472.4 agregados); 87.4% pre / 87.6% post | Fila CORR-138-PALA-SCNU a 22.1 km; S_max 236.2/472.4 en sec05 EN/ES y maestro | `236.2` 3/3; cero «50 km» en la fila ✅ |
| **T2-b** | Subsección II-A `Steady-State AC Feasibility Scope` (### A en maestro, \subsection en LaTeX), desplazando a B–J | Insertada e intacta en ambos formatos | título 3/3 ✅ |
| **T2-c** | Calendario: 3,653 días = 6 días huérfanos de borde + 521 semanas completas; horizonte 520 semanas hasta el dom 21-dic-2025; 13 días = 6 huérfanos + 7 de la semana festiva; prohibido «13 días fraccionados» | Terminología «orphan/huérfanos» en sec02 EN/ES y maestro | cero `fractionated/fraccionados` en fuentes ✅ |
| **T2-d** | Clausula GEN-PC-COMPLEX (R_req) en el pie de la Tabla VI | Presente en sec05 EN, ES y maestro | presente 3/3 ✅ |
| **T2-e / T5** | [43] IEUASD «Resumen Ejecutivo…» 5 pp. (uasd.edu.do); [44] OC-SENI informe de perturbación Itabo 2015 (1,782.65 MW); prohibida SIE-024-2015; cita formal del Reporte Horario SCADA OC-SENI (P15 13:15–13:30, pág. 4, §2.3, Gráfica 2, Tabla 1) | Bib: `uasdInformeSPM1_2025`, `listinItaboGas_2015`, nueva `ocseniScadaP15_2025`; maestro refs [43]/[44]/[45] (Diario Libre → [46]) | cero `SIE-024`; cite SCADA EN/ES/bib ✅ |

Compilación R5-bis: 2col 23 pp / 1col 30 pp / ES 31 pp, 0 errores (overfull cosméticos preexistentes sin cambio: 7/0/1).

## 5. Nota de procedencia del eje B1 (actualizada)

Queda resuelta la procedencia del eje B1: el artefacto `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json` — sellado con los 8 digests SHA-512 íntegros de 128 hex, los desgloses unidad a unidad del redespacho y la auditoría de balance (error 0.00 MW) — obra en el paquete de subida y está referenciado por las cartas del dossier. Los hashes truncados de la carta original del Director se conservan como texto histórico verbatim; la referencia autoritativa son los digests íntegros del artefacto.
