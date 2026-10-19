# NOTA DE PROPIEDAD INTELECTUAL DEL SOLVER
## Expediente TPWRS-SENI-142-2026 — IEEE Transactions on Power Systems
### Fecha: 2026-10-19 · Autor e Investigador Principal: Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)

La presente nota fija la doctrina oficial de propiedad intelectual que gobierna el alcance de la contribución del manuscrito **TPWRS-SENI-142-2026** y el tratamiento del motor de optimización asociado, en respuesta a las solicitudes de código del solver formuladas durante la correspondencia de revisión. Conforme a las directrices de la *IEEE PES Task Force on Benchmark Test Systems*, se declara lo siguiente:

---

### 1. Alcance de la Contribución (Benchmark Paper)

El objeto de este artículo es el **modelo de red física** y sus **datos abiertos de validación**: la topología georreferenciada de 142 barras del Sistema Eléctrico Nacional Interconectado de la República Dominicana (SENI), los 193 ramos canónicos (135 líneas + 58 transformadores de potencia) con procedencia 1:1 del unifilar oficial (DWG), los censos CSV, las matrices NPZ y el arnés de verificación **verify_seni142_benchmark.py (41/41 checks PASS)**.

El benchmark está concebido para ser **neutral e interoperable**: la comunidad científica puede probar **sus propios solvers** (MATPOWER, Pandapower, PyPSA, PowerFactory, PSS/E, o cualquier otro) sobre el modelo liberado. La reproducibilidad de todas las cantidades estructurales selladas no depende de software propietario: el arnés de verificación está restringido a `numpy` y `scipy`, y reproduce el residuo de partición, la estructura bloque-diagonal del complemento de Schur y los ocho balances de contingencia directamente desde los arreglos liberados.

### 2. Protección por Patente de Invención (Patent-Pending)

El motor de optimización multivectorial avanzado desarrollado en el programa doctoral del autor constituye **propiedad intelectual protegida, sujeta a Solicitud de Patente de Invención y secreto industrial**. Su liberación en código abierto como repositorio público **vulneraría la novedad jurídica** exigida por la legislación de patentes, por lo que dicho motor **no forma parte** del paquete de datos abierto del benchmark ni será liberado durante el período de gracia patentario.

Esta reserva **no afecta** la reproducibilidad del artículo: todos los resultados declarados en el manuscrito (residuo de frontera δ = 2.788×10⁻¹⁴ pu, κ₂(S) = 2,489.64, dimensionamiento de reserva de modo común 752.00 MW, cierre de despacho 687.40 + 58.50 + 6.10 = 752.00 MW) están sellados en el artefacto `ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json` y son verificables con el arnés abierto.

---

**Declaración de autoría:** La totalidad del benchmark, del manuscrito y de la presente doctrina es obra del Investigador Principal **Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)**, autor único de la sumisión TPWRS-SENI-142-2026.

*Estado de custodia: documento incorporado al expediente oficial de subida y sellado en `MANIFIESTO_SHA512_R5_DEFINITIVO.txt` (refresco R9, 2026-10-19).*
