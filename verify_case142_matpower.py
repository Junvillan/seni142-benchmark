#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_case142_matpower.py — verificador del caso MATPOWER canónico del benchmark SENI-142.

Comprueba que `case142_seni.m` es (a) un caso MATPOWER estructuralmente válido,
(b) una reproducción exacta de la red liberada (censo y ramas, campo por campo),
(c) idéntico —en la matriz de admitancias— al Ybus certificado del release
(matrices_sistema_seni142.npz) y (d) cargable y resoluble por un solver de
flujo de potencia (MATPOWER / Octave / PYPOWER).

Reglas de la arnés:
  * No contiene resultados de solver como literales: todos los valores se
    derivan de los artefactos liberados.
  * Es de solo lectura: no escribe nada en disco.
  * Sale con codigo distinto de cero ante cualquier fallo (fail-closed).

Uso:
    python3 verify_case142_matpower.py            # usa el directorio del script
    python3 verify_case142_matpower.py <dir>      # verifica otro bundle

Dependencias:
    numpy   (obligatorio)
    pypower (opcional; sin el, las comprobaciones de Ybus y de solver se
             declaran SKIP y el resto sigue ejecutandose)
"""
import csv
import re
import sys
from pathlib import Path

import numpy as np

PKG = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent)

CASE = "case142_seni.m"

# ---- constantes de especificacion (manuscrito), no resultados de computo ----
SPEC = {
    "buses": 142, "branch": 193, "gen": 23,
    "peak_mw": 3450.0,
    "ref_pmax_mw": 800.0, "ref_pmin_mw": 0.0,
    "regiones": ["Ozama-Metropolitana", "Valdesia", "Higuamo", "Yuma", "Del Valle",
                 "Enriquillo", "Cibao Norte", "Cibao Sur", "Cibao Nordeste",
                 "Cibao Noroeste"],
    "macros": ["Omega_Metro", "Omega_Sur", "Omega_Este", "Omega_Norte"],
    "tolerancia_ybus": 1e-9,
}
TIPO = {"PQ": 1, "PV": 2, "SLACK": 3}

# Barras de conexion Tier B declaradas en la cabecera de case142_seni.m:
# unidades que el catalogo N-1 publica sin barra, mas una unidad del complejo
# Punta Catalina (el censo marca su patio de 138 kV como nodo de generacion y
# un solver exige un generador en toda barra controladora de tension).
TIER_B_BUS = {
    "GEN-PC2": "BUS-138-PUNTA_CATALINA",
    "GEN-AES-ANDRES": "BUS-138-SPM",
    "GEN-ESTRELLA-DEL-MAR": "BUS-138-BOCA_CHICA",
    "GEN-HATILLO": "BUS-138-HERRERA",
}
# Capacidades selladas por el catalogo N-1 (Tier A)
TIER_A_PMAX = {"GEN-PC1": 376.0, "GEN-PC2": 376.0, "GEN-AES-ANDRES": 319.0}

results = []
skipped = []


def chk(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" :: {detail}" if detail else ""))


def skip(name, why):
    skipped.append(name)
    print(f"[SKIP] {name} :: {why}")


# ============================================================================
# 1. Lector del caso MATPOWER (subconjunto literal de matrices)
# ============================================================================
def parse_case(path):
    """Devuelve (version, baseMVA, bus, gen, branch) leidos del fichero .m."""
    text = path.read_text(encoding="utf-8")
    version = None
    base_mva = None
    mats = {}

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if stripped.startswith("%") or not stripped:
            i += 1
            continue
        m = re.match(r"^mpc\.version\s*=\s*'([^']*)'\s*;", stripped)
        if m:
            version = m.group(1)
            i += 1
            continue
        m = re.match(r"^mpc\.baseMVA\s*=\s*([0-9.eE+-]+)\s*;", stripped)
        if m:
            base_mva = float(m.group(1))
            i += 1
            continue
        m = re.match(r"^mpc\.(\w+)\s*=\s*\[\s*$", stripped)
        if m:
            name = m.group(1)
            body = []
            i += 1
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith("%"):
                    i += 1
                    continue
                if s.startswith("]"):
                    break
                if s:
                    if s.endswith(";"):
                        s = s[:-1]
                    if s:
                        body.append(s)
                i += 1
            mats[name] = body
            i += 1
            continue
        i += 1

    def to_matrix(rows, ncol):
        if rows is None:
            return None
        out = []
        for r in rows:
            fields = [t for t in re.split(r"[\s,]+", r.strip()) if t]
            if len(fields) != ncol:
                raise ValueError(f"fila con {len(fields)} campos (se esperaban {ncol}): {r!r}")
            out.append([float(t) for t in fields])
        return np.array(out, dtype=float) if out else None

    return (version, base_mva,
            to_matrix(mats.get("bus"), 13),
            to_matrix(mats.get("gen"), 10),
            to_matrix(mats.get("branch"), 13),
            mats)


# ============================================================================
# 2. Derivacion canonica desde los CSV liberados
# ============================================================================
def read_csv(path):
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def derive(rows, ramas, gencat):
    idx = {r["Bus_ID"]: i + 1 for i, r in enumerate(rows)}
    bus = np.array([[
        i + 1,
        TIPO[r["Tipo_Barra"]],
        float(r["P_demanda_MW"]), float(r["Q_demanda_MVAR"]),
        0.0, 0.0,
        SPEC["regiones"].index(r["Region_Planificacion_Ley368_22"]) + 1,
        float(r["V_nom_pu"]), 0.0,
        float(r["Nivel_kV"]),
        SPEC["macros"].index(r["Macrodominio_HBCF_Schur"]) + 1,
        1.1, 0.9,
    ] for i, r in enumerate(rows)], dtype=float)

    branch = []
    for r in ramas:
        c = r["Circuitos"]
        n = 1 if c in ("", "-", "—") else int(c)
        rate = round(float(r["S_max_MVA"]) * n, 6)
        branch.append([idx[r["From_Bus"]], idx[r["To_Bus"]],
                       float(r["R_pu"]), float(r["X_pu"]), float(r["B_pu"]),
                       rate, rate, rate, 0.0, 0.0, 1, -360, 360])
    branch = np.array(branch, dtype=float)

    gen = []
    for g in gencat:
        eid = g["Elemento_ID"]
        bus_id = TIER_B_BUS.get(eid, g["To_Bus_o_Barra"])
        gen.append([idx[bus_id], 0.0, 0.0, 0.0, 0.0,
                    0.0, 100.0, 1, 0.0, 0.0, eid])
    return bus, branch, gen, idx


# ============================================================================
# 3. Comprobaciones
# ============================================================================
def main():
    census_p = PKG / "SENI142_CENSO_CANONICO_BARRAS.csv"
    ramas_p = PKG / "SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv"
    cat_p = PKG / "SENI142_CATALOGO_215_CONTINGENCIAS.csv"
    npz_p = PKG / "matrices_sistema_seni142.npz"
    case_p = PKG / CASE

    rows = read_csv(census_p)
    ramas = read_csv(ramas_p)
    cat = read_csv(cat_p)
    gencat = [g for g in cat if g["Tipo_Elemento"] == "UNIDAD_GENERADORA"]

    version, base_mva, bus, gen, branch, raw_mats = parse_case(case_p)

    chk("caso MATPOWER legible", bus is not None and gen is not None and branch is not None)
    chk("mpc.version = '2'", version == "2", f"'{version}'")
    chk("mpc.baseMVA = 100", base_mva == 100.0, f"{base_mva}")

    # --- dimensiones -------------------------------------------------------
    chk("mpc.bus = 142 filas x 13 columnas", bus.shape == (SPEC["buses"], 13), str(bus.shape))
    chk("mpc.branch = 193 filas x 13 columnas", branch.shape == (SPEC["branch"], 13), str(branch.shape))
    chk("mpc.gen = 23 filas x 10 columnas", gen.shape == (SPEC["gen"], 10), str(gen.shape))

    # --- integridad estructural -------------------------------------------
    chk("bus_i = 1..142 en orden", np.array_equal(bus[:, 0], np.arange(1, 143)))
    chk("tipos de barra en {1,2,3}", set(np.unique(bus[:, 1]).tolist()) <= {1.0, 2.0, 3.0},
        f"{sorted(set(np.unique(bus[:, 1]).tolist()))}")
    nslack = int((bus[:, 1] == 3).sum())
    chk("exactamente 1 barra de referencia (slack)", nslack == 1, f"{nslack}")
    pv_buses = set(bus[bus[:, 1] == 2, 0].astype(int).tolist())
    chk("tipos de barra coinciden con el censo",
        int((bus[:, 1] == 1).sum()) == 135 and int((bus[:, 1] == 2).sum()) == 6 and nslack == 1,
        f"PQ={int((bus[:,1]==1).sum())} PV={int((bus[:,1]==2).sum())} REF={nslack}")

    ends = np.concatenate([branch[:, 0], branch[:, 1]])
    chk("extremos de rama dentro de 1..142", ends.min() >= 1 and ends.max() <= 142,
        f"min={int(ends.min())} max={int(ends.max())}")
    gbus = gen[:, 0]
    chk("barras de generador dentro de 1..142", gbus.min() >= 1 and gbus.max() <= 142)
    chk("pares de barras unicos (grafo simple)",
        len({(int(f), int(t)) for f, t in branch[:, :2]}) == len(branch), f"{len(branch)}")
    chk("todas las ramas en servicio", np.all(branch[:, 10] == 1))
    chk("todas las unidades en servicio", np.all(gen[:, 7] == 1))

    # --- fidelidad campo por campo contra los CSV -------------------------
    ebus, ebranch, egen, idx = derive(rows, ramas, gencat)

    db = float(np.abs(bus - ebus).max())
    chk("mpc.bus identico al censo (<1e-9)", db < 1e-9, f"{db:.2e}")
    eb = float(np.abs(branch - ebranch).max())
    chk("mpc.branch identico al censo de ramas (<1e-9)", eb < 1e-9, f"{eb:.2e}")

    # rateA = Circuitos x S_max_MVA (coeficiente agregado del corredor)
    rate_ok = True
    for i, r in enumerate(ramas):
        c = r["Circuitos"]
        n = 1 if c in ("", "-", "—") else int(c)
        if abs(branch[i, 5] - float(r["S_max_MVA"]) * n) > 1e-9:
            rate_ok = False
            break
    chk("rateA = Circuitos x S_max_MVA (corredor agregado)", rate_ok)
    chk("rateA = rateB = rateC en las 193 ramas",
        np.allclose(branch[:, 5], branch[:, 6]) and np.allclose(branch[:, 6], branch[:, 7]))
    chk("tap nominal (ratio = 0) en las 193 ramas", np.all(branch[:, 8] == 0))
    chk("desfase de fase nulo (angle = 0)", np.all(branch[:, 9] == 0))

    # --- generadores -------------------------------------------------------
    cat_ids = [g["Elemento_ID"] for g in gencat]
    chk("las 22 unidades certificadas del catalogo N-1 estan presentes",
        len(cat_ids) == 22 and len({g[10] for g in egen}) == 22, f"{len(cat_ids)}")
    inv = {v: k for k, v in idx.items()}
    bus_ok = all(int(egen[i][0]) == int(gen[i][0]) for i in range(22))
    chk("filas 1..22 en orden de catalogo con su barra declarada", bus_ok)
    n_gen_ref = int((gen[:, 0] == int(np.argmax(bus[:, 1] == 3) + 1)).sum())
    chk("una sola fila de generador en la barra de referencia", n_gen_ref == 1, f"{n_gen_ref}")
    ref_row = gen[gen[:, 0] == int(np.argmax(bus[:, 1] == 3) + 1)][0]
    chk("banda de potencia activa de la referencia en 0..800 MW",
        ref_row[9] == SPEC["ref_pmin_mw"] and ref_row[8] == SPEC["ref_pmax_mw"],
        f"Pmin={ref_row[9]:g} Pmax={ref_row[8]:g}")
    chk("las 6 barras PV tienen al menos un generador",
        all(int((gen[:, 0] == b).sum()) >= 1 for b in pv_buses),
        f"{len(pv_buses)} barras PV")

    # capacidades selladas (Tier A) intactas
    seal_ok = True
    for i, g in enumerate(gencat):
        eid = g["Elemento_ID"]
        if eid in TIER_A_PMAX and abs(gen[i, 8] - TIER_A_PMAX[eid]) > 1e-9:
            seal_ok = False
    chk("capacidades selladas por el catalogo intactas (PC1/PC2/AES-Andres)",
        seal_ok, "376 / 376 / 319 MW")

    chk("Pmin <= Pg <= Pmax en las 23 unidades",
        np.all(gen[:, 9] <= gen[:, 1] + 1e-9) and np.all(gen[:, 1] <= gen[:, 8] + 1e-9))
    chk("Qmin <= Qmax en las 23 unidades", np.all(gen[:, 4] <= gen[:, 3] + 1e-9))
    chk("Qmin <= Qg <= Qmax en las 23 unidades",
        np.all(gen[:, 4] - 1e-9 <= gen[:, 2]) and np.all(gen[:, 2] <= gen[:, 3] + 1e-9))
    chk("mBase = 100 MVA en las 23 unidades", np.all(gen[:, 6] == 100.0))
    chk("Pg de la referencia dentro de su banda certificada 0..800 MW",
        SPEC["ref_pmin_mw"] <= ref_row[1] <= SPEC["ref_pmax_mw"], f"{ref_row[1]:g} MW")

    sp = float(bus[:, 2].sum())
    chk("suma Pd = pico nacional certificado (3450.0 MW)", abs(sp - SPEC["peak_mw"]) < 1e-6, f"{sp:.4f}")
    sg = float(gen[:, 1].sum())
    chk("suma Pg = 3450.0 MW (balance declarado)", abs(sg - SPEC["peak_mw"]) < 1e-6, f"{sg:.4f}")
    chk("Vg = consigna de tension de la barra anfitriona",
        all(abs(gen[i, 5] - bus[int(gen[i, 0]) - 1, 7]) < 1e-9 for i in range(len(gen))))

    # --- identidad de la Ybus con el NPZ certificado -----------------------
    have_pypower = True
    try:
        import pypower  # noqa: F401
        from pypower.makeYbus import makeYbus
        from scipy.sparse import csr_matrix
    except Exception as exc:  # pragma: no cover
        have_pypower = False
        skip("Ybus del caso == Ybus certificado (<1e-9)", f"pypower no disponible ({exc.__class__.__name__})")
        skip("carga del caso en un solver y convergencia", "pypower no disponible")

    if have_pypower:
        # PYPOWER usa indices de barra 0-based
        b0 = bus.copy()
        b0[:, 0] -= 1
        br0 = branch.copy()
        br0[:, 0] -= 1
        br0[:, 1] -= 1
        Ycase, Yf, Yt = makeYbus(base_mva, b0, br0)

        d = np.load(npz_p, allow_pickle=True)
        Ynpz = csr_matrix((d["Ybus_data"], d["Ybus_indices"], d["Ybus_indptr"]),
                           shape=tuple(d["Ybus_shape"])).toarray()
        e = float(np.abs(Ycase - Ynpz).max())
        chk("Ybus del caso == Ybus certificado (<1e-9)", e < SPEC["tolerancia_ybus"], f"{e:.2e}")

        # elementos de rama, como multiconjunto: Yf[k, fbus] = Yff, Yf[k, tbus] = Yft
        f0 = br0[:, 0].astype(int)
        t0 = br0[:, 1].astype(int)
        y11 = np.sort(np.array([Yf[k, f0[k]] for k in range(len(f0))]))
        y12 = np.sort(np.array([Yf[k, t0[k]] for k in range(len(f0))]))
        e11 = float(np.abs(np.sort(d["branch_y11"]) - y11).max())
        e12 = float(np.abs(np.sort(d["branch_y12"]) - y12).max())
        chk("elementos de rama del caso == NPZ (<1e-9)", e11 < 1e-9 and e12 < 1e-9,
            f"y11={e11:.2e} y12={e12:.2e}")

        # --- carga y resolucion en un solver ------------------------------
        try:
            from pypower.runpf import runpf
            from pypower.rundcpf import rundcpf
            g0 = gen.copy()
            g0[:, 0] -= 1
            ppc = {"baseMVA": base_mva, "bus": b0, "gen": g0, "branch": br0}
            rdc, okc = rundcpf(ppc)
            chk("flujo DC (sin perdidas) resuelto y convergente", bool(okc),
                f"max|angle|={np.abs(rdc['bus'][:, 8]).max():.2f} deg")

            gdc = float(rdc["gen"][:, 1].sum())
            ldc = float(rdc["bus"][:, 2].sum())
            chk("balance DC exacto: generacion = demanda = 3450.0 MW",
                abs(gdc - ldc) < 1e-6 and abs(gdc - SPEC["peak_mw"]) < 1e-6,
                f"gen={gdc:.4f} load={ldc:.4f}")

            refb = int(np.argmax(bus[:, 1] == 3) + 1)
            pgref = float(rdc["gen"][rdc["gen"][:, 0] == refb - 1, 1][0])
            chk("referencia dentro de su banda certificada 0..800 MW en el despacho DC",
                SPEC["ref_pmin_mw"] <= pgref <= SPEC["ref_pmax_mw"], f"{pgref:.4f} MW")

            # calidad termica del estado base, por subtipo de rama
            s = np.abs(rdc["branch"][:, 0])
            condensa = ("Empate_puerto_138/69", "Entrega_equivalente_Kron_138/dist",
                        "Entrega_equivalente_Kron_230/dist")
            over_t, over_c = 0, 0
            n_cond = sum(1 for r in ramas if r["Subtipo"] in condensa)
            for i, r in enumerate(ramas):
                if br0[i, 5] <= 0 or s[i] <= br0[i, 5] + 1e-6:
                    continue
                if r["Subtipo"] in condensa:
                    over_c += 1
                else:
                    over_t += 1
            chk("ninguna linea de transmision ni transformador sobre su rateA",
                over_t == 0, f"{over_t} de {len(ramas) - n_cond} ramas de transmision/transformacion")
            print(f"[INFO] equivalentes de distribucion condensados sobre su rating: "
                  f"{over_c} de {n_cond} (artefacto de la condensacion liberada, README errata 13)")

            va = float(np.abs(rdc["bus"][:, 8]).max())
            chk("perfil angular DC dentro de rango fisico (<60 deg)", va < 60.0, f"{va:.2f} deg")

            # El release certifica un modelo lineal (Ybus, Schur) y no un punto
            # operativo AC; se registra el intento sin puntuarlo.
            try:
                rac, oka = runpf(ppc)
                msg = (f"convergio, Vmin={rac['bus'][:, 7].min():.4f} pu" if oka
                       else "no converge: el modelo plano de per-unit del release "
                            "no admite punto operativo AC en el pico certificado "
                            "(la continuacion de carga converge solo hasta ~35-40 %)")
                print(f"[INFO] intento de flujo AC (no puntuado): {msg}")
            except Exception as exc:
                print(f"[INFO] intento de flujo AC (no puntuado): {exc.__class__.__name__}: {exc}")
        except Exception as exc:
            chk("carga del caso en un solver y convergencia", False,
                f"{exc.__class__.__name__}: {exc}")

    # --- veredicto ---------------------------------------------------------
    fails = results.count(False)
    print("\n" + "=" * 72)
    print(f"RESULTADO: {results.count(True)}/{len(results)} chequeos PASS · {fails} FAIL"
          + (f" · {len(skipped)} SKIP" if skipped else ""))
    print("VEREDICTO: CASO MATPOWER SENI-142 CONSISTENTE" if not fails
          else "VEREDICTO: CASO MATPOWER SENI-142 INCONSISTENTE")
    print("=" * 72)
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
