#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_seni142_benchmark.py — verificador oficial del benchmark SENI-142.

Sustituye al generador hardcodeado: NO contiene resultados de solver como
literales; todos los valores se derivan de los cuatro artefactos liberados
  SENI142_CENSO_CANONICO_BARRAS.csv
  SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv
  matrices_sistema_seni142.npz
  ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json
y se contrastan contra las CONSTANTES DE ESPECIFICACIÓN del manuscrito
(Tabla I: 10 regiones → 4 macrodominios; Tabla III: pico 1645/520/680/605;
Tabla VII: corredor PALA–SCNU 22.1 km / 236.2 MVA; evento de dimensionamiento
752 MW con cierre 687.40 + 58.50 + 6.10).

Uso:  python3 verify_seni142_benchmark.py [directorio]
Exit 0 solo si TODOS los chequeos pasan; veredicto condicional.
"""
import csv, hashlib, json, math, sys, collections
from pathlib import Path
import numpy as np

PKG = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent)

# ---- constantes de especificación (manuscrito), no resultados de cómputo ----
SPEC = {
    "buses": 142, "bulk": 115, "puertos69": 27,
    "strata": {"345.0": 6, "230.0": 3, "138.0": 106, "69.0": 27},
    "lineas": 135, "transformadores": 58,
    "peak_mw": 3450.0,
    "macro_mw": {"Omega_Metro": 1645.0, "Omega_Sur": 520.0,
                 "Omega_Este": 680.0, "Omega_Norte": 605.0},
    "regiones": ["Ozama-Metropolitana", "Valdesia", "Higuamo", "Yuma", "Del Valle",
                 "Enriquillo", "Cibao Norte", "Cibao Sur", "Cibao Nordeste", "Cibao Noroeste"],
    "region_macro": {"Ozama-Metropolitana": "Omega_Metro", "Valdesia": "Omega_Sur",
                     "Enriquillo": "Omega_Sur", "Del Valle": "Omega_Sur",
                     "Higuamo": "Omega_Este", "Yuma": "Omega_Este",
                     "Cibao Norte": "Omega_Norte", "Cibao Sur": "Omega_Norte",
                     "Cibao Nordeste": "Omega_Norte", "Cibao Noroeste": "Omega_Norte"},
    "corr_km": 22.1, "corr_mva": 236.2,
    "sizing_events": {"GEN-PC-COMPLEX", "LINE-345-PC-JS"},
}
COMPUESTAS = {"LINE-230-JS-SCNU"}  # enlace 230 kV con transformación en ambos patios

results = []
def chk(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" :: {detail}" if detail else ""))

def id2(a, b):
    return (a, b) if a < b else (b, a)

# ---------------------------------------------------------------- artefactos
rows = list(csv.DictReader(open(PKG / "SENI142_CENSO_CANONICO_BARRAS.csv")))
brs = list(csv.DictReader(open(PKG / "SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv")))
art = json.load(open(PKG / "ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json"))
d = np.load(PKG / "matrices_sistema_seni142.npz", allow_pickle=True)
bus = {r["Bus_ID"]: r for r in rows}

# ---------------------------------------------------------------- 1. censo
chk("censo = 142 barras", len(rows) == SPEC["buses"], f"n={len(rows)}")
strata = collections.Counter(r["Nivel_kV"] for r in rows)
chk("estratos 6/3/106/27", dict(strata) == SPEC["strata"], str(dict(strata)))
slacks = [r["Bus_ID"] for r in rows if r["Tipo_Barra"] == "SLACK"]
chk("exactamente 1 slack", len(slacks) == 1, str(slacks))
sp = sum(float(r["P_demanda_MW"]) for r in rows)
peak = float(art["artifact_metadata"]["national_peak_load_mw"])
chk(f"ΣP = pico declarado ({peak} MW)", abs(sp - peak) < 1e-6, f"Σ={sp}")
macro = collections.Counter(r["Macrodominio_HBCF_Schur"] for r in rows)
chk("4 macrodominios HBCF", set(macro) == set(SPEC["macro_mw"]), str(dict(macro)))
for m, tot in SPEC["macro_mw"].items():
    sm = sum(float(r["P_demanda_MW"]) for r in rows if r["Macrodominio_HBCF_Schur"] == m)
    chk(f"pico {m} = {tot}", abs(sm - tot) < 1e-6, f"{sm}")
regs = set(r["Region_Planificacion_Ley368_22"] for r in rows)
chk("10 regiones de la Ley 368-22", regs == set(SPEC["regiones"]))
r2m = {r["Region_Planificacion_Ley368_22"]: r["Macrodominio_HBCF_Schur"] for r in rows}
chk("mapa región→macrodominio 1:1 (Tabla I)",
    all(r2m[k] == v for k, v in SPEC["region_macro"].items()))

# ---------------------------------------------------------------- 2. ramas
lines = [r for r in brs if r["Tipo"] == "LINEA_TRANSMISION"]
xfmr = [r for r in brs if r["Tipo"] == "TRANSFORMADOR"]
chk(f"{SPEC['lineas']}+{SPEC['transformadores']} = 193 ramas",
    len(lines) == SPEC["lineas"] and len(xfmr) == SPEC["transformadores"],
    f"{len(lines)}+{len(xfmr)}")
pares = set(id2(r["From_Bus"], r["To_Bus"]) for r in brs)
chk("pares de barras únicos (grafo simple)", len(pares) == len(brs), f"{len(pares)}/{len(brs)}")
l69 = [r["Equipo_ID"] for r in lines if float(r["Tension_kV"]) == 69.0]
chk("cero líneas 69 kV (puertos solo vía transformadores)", not l69)
inco = [r["Equipo_ID"] for r in lines
        if r["Equipo_ID"] not in COMPUESTAS
        and (float(bus[r["From_Bus"]]["Nivel_kV"]) != float(r["Tension_kV"])
             or float(bus[r["To_Bus"]]["Nivel_kV"]) != float(r["Tension_kV"]))]
chk("coherencia dieléctrica de líneas (salvo compuestas documentadas)", not inco, str(inco))
lens = [float(r["Longitud_km"]) for r in brs]
rs = [float(r["R_pu"]) for r in brs]
dl = [round(lens[i + 1] - lens[i], 4) for i in range(min(12, len(lens) - 1))]
dr = [round(rs[i + 1] - rs[i], 6) for i in range(min(12, len(rs) - 1))]
chk("sin progresión aritmética en km", len(set(dl)) > 6, f"Δ={dl[:8]}")
chk("sin progresión aritmética en R_pu", len(set(dr)) > 6, f"Δ={dr[:8]}")
corr = next(r for r in brs if r["Equipo_ID"] == "CORR-138-PALA-SCNU")
chk("corredor PALA–SCNU 22.1 km / 236.2 MVA (Tabla VII)",
    abs(float(corr["Longitud_km"]) - SPEC["corr_km"]) < 1e-9
    and abs(float(corr["S_max_MVA"]) - SPEC["corr_mva"]) < 1e-6)
for cid in ("LINE-345-PC-JS", "LINE-230-JS-SCNU", "LINE-138-CUM-SPMI", "XFMR-345-138-JS"):
    chk(f"ID canónico {cid}", any(r["Equipo_ID"] == cid for r in brs))

# ---------------------------------------------------------------- 3. NPZ
chk("Ybus 142×142", tuple(int(x) for x in d["Ybus_shape"]) == (142, 142))
n = 142
off = sum(1 for i in range(n) for k in range(d["Ybus_indptr"][i], d["Ybus_indptr"][i + 1])
          if d["Ybus_indices"][k] != i)
chk("pares Ybus == 193 ramas del CSV", off // 2 == len(brs), f"{off//2}")
# multiconjunto por rama: recomputar desde el CSV
idx = {r["Bus_ID"]: i for i, r in enumerate(rows)}
y11 = np.sort(np.array([1.0 / complex(float(r["R_pu"]), float(r["X_pu"])) + 1j * float(r["B_pu"]) / 2
                        for r in brs]))
y12 = np.sort(np.array([-1.0 / complex(float(r["R_pu"]), float(r["X_pu"])) for r in brs]))
e11 = float(np.abs(np.sort(d["branch_y11"]) - y11).max())
e12 = float(np.abs(np.sort(d["branch_y12"]) - y12).max())
chk("elementos de rama Ybus ≡ CSV (<1e-9)", e11 < 1e-9 and e12 < 1e-9, f"{max(e11, e12):.2e}")
A = d["Schur_A"]
sizes = d["bloque_sizes"]
mask = np.zeros(A.shape, dtype=bool)
i0 = 0
for s in sizes:
    mask[i0:i0 + int(s), i0:i0 + int(s)] = True
    i0 += int(s)
off_blk = float(np.abs(A[~mask]).max()) if (~mask).any() else 0.0
chk("A diagonal por bloques en los 4 macrodominios", off_blk < 1e-9, f"{off_blk:.2e}")
S, Bm, Cm, Dm = d["Schur_S"], d["Schur_B"], d["Schur_C"], d["Schur_D"]
ident = float(np.abs(S - (Dm - Cm @ np.linalg.inv(A) @ Bm)).max())
chk("identidad de Schur S = D − CA⁻¹B (<1e-12)", ident < 1e-12, f"{ident:.2e}")
Y = np.zeros((n, n), dtype=complex)
for r in brs:
    i, j = idx[r["From_Bus"]], idx[r["To_Bus"]]
    ys = 1.0 / complex(float(r["R_pu"]), float(r["X_pu"]))
    bs = 1j * float(r["B_pu"]) / 2.0
    Y[i, i] += ys + bs
    Y[j, j] += ys + bs
    Y[i, j] -= ys
    Y[j, i] -= ys
Y_npz = np.zeros((n, n), dtype=complex)
for i in range(n):
    for k in range(d["Ybus_indptr"][i], d["Ybus_indptr"][i + 1]):
        Y_npz[i, d["Ybus_indices"][k]] = d["Ybus_data"][k]
gap_ydata = float(np.abs(Y - Y_npz).max())
chk("matriz Ybus_data (NPZ) ≡ matriz Ybus (CSV) (<1e-9)", gap_ydata < 1e-9, f"{gap_ydata:.2e}")
P = np.array([list(idx).index(x) for x in d["particion_orden"]])
rhs = np.zeros((n, 2), dtype=complex)
sl = [k for k, r in enumerate(rows) if r["Tipo_Barra"] == "SLACK"][0]
rhs[sl, 0] = 1.0
rhs[0, 1] = 1.0
Xf = np.linalg.solve(Y, rhs)
nb = A.shape[0]
rhsp = rhs[P]
Xb = np.linalg.solve(S, rhsp[nb:] - Cm @ np.linalg.solve(A, rhsp[:nb]))
Xi = np.linalg.solve(A, rhsp[:nb] - Bm @ Xb)
dlt = float(np.abs(Xf[P] - np.vstack([Xi, Xb])).max())
chk("δ de Schur reproducido desde los CSV (<1e-9)", dlt < 1e-9,
    f"recomputado={dlt:.2e} almacenado={float(d['delta_residual'][0]):.2e}")
chk("δ almacenado ≡ recomputado (<1e-12)",
    abs(dlt - float(d["delta_residual"][0])) < 1e-12,
    f"|{dlt:.2e} - {float(d['delta_residual'][0]):.2e}|")
chk("κ₂(S) positivo y finito", 0 < float(d["condition_number"][0]) < 1e12,
    f"{float(d['condition_number'][0]):.2f}")
h_cen = hashlib.sha512(open(PKG / "SENI142_CENSO_CANONICO_BARRAS.csv", "rb").read()).hexdigest()
h_ram = hashlib.sha512(open(PKG / "SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv", "rb").read()).hexdigest()
chk("integridad censo CSV ≡ hash NPZ", h_cen == str(d["sha512_censo"][0]))
chk("integridad ramas CSV ≡ hash NPZ", h_ram == str(d["sha512_ramas"][0]))

# ---------------------------------------------------------------- 4. ARTEFACTO B1
sols = art["critical_contingencies_solutions"]
chk("8 contingencias críticas", len(sols) == 8)
okref = all(c["post_event_min_voltage_bus"] in bus and c["post_event_max_branch_id"] in {r["Equipo_ID"] for r in brs}
            for c in sols)
chk("referencias del JSON existen en censo y ramas (1:1)", okref)
pc = next(c for c in sols if c["contingency_id"] == "LINE-345-PC-JS")
cerr = pc["delta_Pg_redispatch_mw"] + pc["storage_discharge_mw"] + pc["delta_P_slack_mw"]
chk("cierre del evento de dimensionamiento 687.40+58.50+6.10=752.00",
    abs(cerr - 752.0) < 1e-9, f"{cerr}")
chk("auxiliares 748.3 + 3.70 = 752.00 aislados",
    abs(pc["line_pre_event_loading_mw"] + pc["auxiliary_station_service_mw"] - 752.0) < 1e-9)
chk("ratio dual sobre redespacho 6.10/687.40",
    abs(pc["loss_ratio_over_redispatch_pct"] - pc["delta_P_slack_mw"] / pc["delta_Pg_redispatch_mw"] * 100) < 1e-3,
    f"{pc['loss_ratio_over_redispatch_pct']}%")
chk("ratio dual sobre déficit 6.10/752.00",
    abs(pc["loss_ratio_over_deficit_pct"] - pc["delta_P_slack_mw"] / 752.0 * 100) < 1e-3,
    f"{pc['loss_ratio_over_deficit_pct']}%")
okc, okd = True, True
for c in sols:
    pure = {k: v for k, v in c.items() if k != "sha512_solution_digest"}
    if hashlib.sha512(json.dumps(pure, sort_keys=True, ensure_ascii=False).encode()).hexdigest() != c["sha512_solution_digest"]:
        okd = False
    aisl = c.get("generation_isolated_mw", c["pre_event_flow_or_gen_mw"])
    if c["contingency_id"] == "LINE-345-PC-JS":
        # aislamiento troncal: 687.40+58.50+6.10 = 752.00 (el slack cubre las pérdidas)
        if abs(c["delta_Pg_redispatch_mw"] + c.get("storage_discharge_mw", 0) + c["delta_P_slack_mw"] - aisl) > 1e-9:
            okc = False
    elif c["contingency_id"] == "GEN-PC-COMPLEX":
        # disparo de modo común: el redespacho reemplaza exactamente los 752.00 MW;
        # ΔP_slack = 24.8 MW es la pérdida incremental (semántica de la Tabla VII)
        if abs(c["delta_Pg_redispatch_mw"] - 752.0) > 1e-9:
            okc = False
chk("digests SHA-512 por solución verificados", okd)
chk("cierre contable en los eventos de dimensionamiento", okc)

# ---------------------------------------------------------------- veredicto
fails = results.count(False)
print("\n" + "=" * 72)
print(f"RESULTADO: {results.count(True)}/{len(results)} chequeos PASS · {fails} FAIL")
print("VEREDICTO: BENCHMARK CONSISTENTE Y REPRODUCIBLE" if not fails
      else "VEREDICTO: INCONSISTENTE — ver chequeos FAIL")
print("=" * 72)
sys.exit(0 if not fails else 1)
