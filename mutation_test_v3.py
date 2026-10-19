#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BATERÍA DE MUTATION TESTING DEL VERIFICADOR v3 (verify_seni142_benchmark.py)
Revisor #1 — Ronda 3. 20-oct-2026.

Objetivo: comprobar empíricamente la afirmación del autor de que "si usted muta
o corrompe deliberadamente cualquier valor de inyección, rama o balance, el
arnés ya NO da PASS ciego: falla inmediatamente con código de salida no nulo".

Cada mutación se aplica sobre una COPIA LIMPIA del bundle y se ejecuta el
verificador oficial. Se registra el exit code y el veredicto.
"""
import json, os, shutil, subprocess, sys, tempfile
import numpy as np
from pathlib import Path

BUNDLE = Path(sys.argv[1] if len(sys.argv) > 1 else "/workspace/seni142_v3").resolve()
results = []


def run_mut(name, mutate, expect_fail=True, note=""):
    tmp = Path(tempfile.mkdtemp())
    dst = tmp / "b"
    shutil.copytree(BUNDLE, dst, ignore=shutil.ignore_patterns(".git"))
    try:
        mutate(dst)
        r = subprocess.run([sys.executable, "verify_seni142_benchmark.py", str(dst)],
                           cwd=dst, capture_output=True, text=True, timeout=600)
        out = r.stdout
        failed_checks = [l.strip() for l in out.splitlines() if l.startswith("[FAIL]")]
        passed = "PASS" in out and "FAIL" not in out.replace("0 FAIL", "")
        verdict_ok = (r.returncode != 0) if expect_fail else (r.returncode == 0)
        results.append((name, expect_fail, verdict_ok, r.returncode, failed_checks[:3], note))
        print(f"\n{'='*100}\n[{name}]  exit={r.returncode}  detectado={verdict_ok}  (esperado: {'FALLO' if expect_fail else 'PASS'})")
        if failed_checks:
            for f in failed_checks[:4]:
                print(f"    -> {f[:150]}")
        if note:
            print(f"    nota: {note}")
    except Exception as e:
        results.append((name, expect_fail, False, -1, [str(e)], note))
        print(f"\n[{name}] ERROR: {e}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- mutaciones
def m_demanda(d):
    p = d / "SENI142_CENSO_CANONICO_BARRAS.csv"
    lines = p.read_text(encoding="utf-8").splitlines()
    f = lines[1].split(",")
    f[5] = str(float(f[5]) + 1.0)          # P_demanda_MW +1 MW
    lines[1] = ",".join(f)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def m_demanda_por_macro(d):
    """Corrupcion COORDINADA: se mueve 1 MW entre dos barras del mismo macrodominio.
       Suma total y total por macro se conservan -> el arnés deberia NOTARLO (o no)."""
    p = d / "SENI142_CENSO_CANONICO_BARRAS.csv"
    rows = p.read_text(encoding="utf-8").splitlines()
    hdr = rows[0].split(",")
    iP, iM = hdr.index("P_demanda_MW"), hdr.index("Macrodominio_HBCF_Schur")
    data = [r.split(",") for r in rows[1:]]
    same = [r for r in data if r[iM] == data[0][iM]]
    a, b = same[0], same[1]
    a[iP] = str(float(a[iP]) + 1.0); b[iP] = str(float(b[iP]) - 1.0)
    p.write_text("\n".join([rows[0]] + [",".join(r) for r in data]) + "\n", encoding="utf-8")


def m_impedancia(d):
    p = d / "SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv"
    lines = p.read_text(encoding="utf-8").splitlines()
    f = lines[1].split(",")
    f[7] = str(float(f[7]) * 1.05)         # X_pu +5 %
    lines[1] = ",".join(f)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def m_ybus(d):
    p = d / "matrices_sistema_seni142.npz"
    z = np.load(p, allow_pickle=True)
    dat = z["Ybus_data"].copy()
    dat[0] = dat[0] * 1.01
    np.savez(p, **{k: z[k] for k in z.files} | {"Ybus_data": dat})
    z.close()


def m_delta_npz(d):
    p = d / "matrices_sistema_seni142.npz"
    z = np.load(p, allow_pickle=True)
    kw = {k: z[k] for k in z.files}
    kw["delta_residual"] = np.array([9.99e-12])
    np.savez(p, **kw)
    z.close()


def m_balance_json(d):
    p = d / "ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json"
    j = json.loads(p.read_text(encoding="utf-8"))
    for c in j["critical_contingencies_solutions"]:
        if c["contingency_id"] == "LINE-345-PC-JS":
            c["delta_Pg_redispatch_mw"] = 600.0
    p.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding="utf-8")


def m_ref_fantasma(d):
    p = d / "ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json"
    j = json.loads(p.read_text(encoding="utf-8"))
    j["critical_contingencies_solutions"][0]["post_event_min_voltage_bus"] = "BUS-138-INEXISTENTE_XYZ"
    p.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding="utf-8")


def m_corrida_km(d):
    p = d / "SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv"
    lines = p.read_text(encoding="utf-8").splitlines()
    for i, l in enumerate(lines):
        if "22.1" in l:
            f = l.split(",")
            f[10] = "22.2"
            lines[i] = ",".join(f)
            break
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def m_smax(d):
    p = d / "SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv"
    lines = p.read_text(encoding="utf-8").splitlines()
    f = lines[1].split(",")
    f[9] = "9999.0"
    lines[1] = ",".join(f)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def m_peak_json(d):
    p = d / "ARTEFACTO_B1_8_CONTINGENCIAS_CANONICAS_142BARRAS.json"
    j = json.loads(p.read_text(encoding="utf-8"))
    j["artifact_metadata"]["national_peak_load_mw"] = 3451.0
    p.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding="utf-8")


def m_coordinada(d):
    """Corrupcion COORDINADA: se desplaza una coordenada 40 km sin tocar longitudes.
       Si el arnés no valida geometria contra coordenadas, NO lo detectara."""
    p = d / "SENI142_CENSO_CANONICO_BARRAS.csv"
    lines = p.read_text(encoding="utf-8").splitlines()
    f = lines[1].split(",")
    f[11] = str(float(f[11]) + 40.0)
    lines[1] = ",".join(f)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def m_conductor(d):
    p = d / "SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv"
    lines = p.read_text(encoding="utf-8").splitlines()
    f = lines[1].split(",")
    f[11] = "conductor inventado X"
    lines[1] = ",".join(f)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def m_ninguno(d):
    pass


MUTS = [
    ("M01 demanda de una barra +1 MW", m_demanda, True, "inyección individual"),
    ("M02 demanda movida dentro del mismo macrodominio (coordinada)", m_demanda_por_macro, True,
     "conserva ΣP y el total por macrodominio"),
    ("M03 impedancia X_pu +5 %", m_impedancia, True, "parámetro de rama"),
    ("M04 entrada de la Ybus (npz) +1 %", m_ybus, True, "matriz"),
    ("M05 delta_residual del npz", m_delta_npz, True, "residuo almacenado"),
    ("M06 balance del JSON: 687.4 -> 600.0", m_balance_json, True, "el que rompía el verificador v2"),
    ("M07 referencia fantasma en el JSON", m_ref_fantasma, True, "ID inexistente"),
    ("M08 longitud del corredor 22.1 -> 22.2 km", m_corrida_km, True, "geometría declarada"),
    ("M09 ampacidad S_max_MVA", m_smax, True, "rating térmico"),
    ("M10 pico declarado en el JSON 3450 -> 3451", m_peak_json, True, "metadato"),
    ("M11 coordenada desplazada 40 km (coordinada)", m_coordinada, True, "geometría vs longitudes"),
    ("M12 conductor declarado", m_conductor, True, "metadato de equipo"),
    ("M00 bundle intacto (control positivo)", m_ninguno, False, "debe dar 41/41 PASS"),
]

print("# BATERÍA DE MUTATION TESTING — verificador v3 (verify_seni142_benchmark.py)")
print(f"# bundle: {BUNDLE}")
for name, fn, expect_fail, note in MUTS:
    run_mut(name, fn, expect_fail, note)

print("\n" + "=" * 100)
print("RESUMEN")
print("=" * 100)
detectadas = sum(1 for _, ef, ok, _, _, _ in results if ef and ok)
esperadas = sum(1 for _, ef, _, _, _, _ in results if ef)
print(f"  mutaciones que el arnés DEBÍA detectar : {detectadas}/{esperadas}")
for name, ef, ok, rc, fc, note in results:
    if ef:
        print(f"    [{'DETECTADA ' if ok else '*** NO DETECTADA ***'}] {name:52s} exit={rc}")
    else:
        print(f"    [control    ] {name:52s} exit={rc}")
undet = [n for n, ef, ok, *_ in results if ef and not ok]
print("\n  VEREDICTO: el arnés es ROBUSTO" if not undet else
      f"\n  VEREDICTO: el arnés NO detecta: {undet}")
