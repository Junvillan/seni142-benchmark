#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates fig_hd4_grafo_completo_seni142.tex — full canonical graph of the
SENI-142 benchmark (142 buses, 193 branches) as a high-definition TikZ
standalone, drawn from the real normalized DWG one-line coordinates.

Sources (sealed, dossier TPWRS-SENI-142-2026):
  SENI142_CENSO_CANONICO_BARRAS.csv
  SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv

Usage:  python3 generar_grafo_completo_seni142_hd.py [data_directory]
"""
from __future__ import annotations

import csv
import collections
import datetime
import hashlib
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DEFECTO = AQUI / ".." / ".." / "opinion_ia_cloud" / "ronda_5" / "expediente_oficial_subida"
DATOS = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFECTO.resolve()

CENSO = DATOS / "SENI142_CENSO_CANONICO_BARRAS.csv"
RAMAS = DATOS / "SENI142_RAMAS_LINEAS_Y_TRANSFORMADORES.csv"

# ------------------------------------------------------------------ paleta
PREAMBULO = r"""\documentclass[tikz,border=12pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usetikzlibrary{arrows.meta,positioning,calc}
\definecolor{seniNavy}{RGB}{26,54,93}
\definecolor{seniRed}{RGB}{155,44,44}
\definecolor{seniBlue}{RGB}{43,108,176}
\definecolor{seniGold}{RGB}{190,140,40}
\definecolor{seniGreen}{RGB}{39,103,73}
\tikzset{>={Stealth[length=2.5mm,width=1.8mm]}}
\begin{document}
"""

COLOR_MACRO = {
    "Omega_Metro": "seniRed!75",
    "Omega_Sur": "seniGold!75",
    "Omega_Este": "seniGreen!75",
    "Omega_Norte": "seniBlue!75",
}
NOMBRE_MACRO = {
    "Omega_Metro": r"$\Omega_{\text{Metro}}$",
    "Omega_Sur": r"$\Omega_{\text{Sur}}$",
    "Omega_Este": r"$\Omega_{\text{Este}}$",
    "Omega_Norte": r"$\Omega_{\text{Norte}}$",
}
RADIO_KV = {"345.0": 0.130, "230.0": 0.100, "138.0": 0.065, "69.0": 0.050}
ESTILO_LINEA = {
    "345.0": r"seniRed,line width=1.5pt",
    "230.0": r"seniBlue,line width=0.9pt",
    "138.0": r"seniGold,line width=0.4pt",
}
ETIQUETAS = {  # bid -> (text, dx, dy, anchor): curated anti-collision labels
    "BUS-345-JULIO_SAURI": ("JULIO SAURI", 0.20, 0.12, "south west"),
    "BUS-345-PUNTA_CATALINA": ("PUNTA CATALINA", 0.20, -0.30, "north west"),
    "BUS-345-GUERRA": ("GUERRA", 0.20, -0.06, "west"),
    "BUS-345-BONAO_3": ("BONAO 3", 0.18, 0.14, "south west"),
    "BUS-345-EL_NARANJO": ("EL NARANJO", 0.0, -0.24, "north"),
    "BUS-345-MANZANILLO_POWER_LAND": ("MANZANILLO", 0.20, -0.06, "west"),
    "BUS-138-SAN_CRISTOBAL_NORTE": ("S. CRISTÓBAL N. (SCN)", -0.18, 0.12, "south east"),
    "BUS-138-PALAMARA": ("PALAMARA", -0.18, -0.24, "north east"),
}

def sha512_de(p: Path) -> str:
    return hashlib.sha512(p.read_bytes()).hexdigest()

def main() -> None:
    buses = list(csv.DictReader(open(CENSO, encoding="utf-8")))
    ramas = list(csv.DictReader(open(RAMAS, encoding="utf-8")))
    assert len(buses) == 142, f"censo={len(buses)}"
    assert len(ramas) == 193, f"ramas={len(ramas)}"

    macro = {b["Bus_ID"]: b["Macrodominio_HBCF_Schur"] for b in buses}
    xs = [float(b["Coord_X"]) for b in buses]
    ys = [float(b["Coord_Y"]) for b in buses]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    dx, dy = xmax - xmin, ymax - ymin
    esc = 22.0 / dx  # 22 cm wide canvas
    alto = dy * esc
    # orientation calibration: north (Cibao, Omega_Norte) must point up
    yn = [float(b["Coord_Y"]) for b in buses if macro[b["Bus_ID"]] == "Omega_Norte"]
    ysu = [float(b["Coord_Y"]) for b in buses if macro[b["Bus_ID"]] == "Omega_Sur"]
    invertir = sum(yn) / len(yn) < sum(ysu) / len(ysu)

    def px(b):
        return (float(b["Coord_X"]) - xmin) * esc

    def py(b):
        v = (float(b["Coord_Y"]) - ymin) * esc
        return alto - v if invertir else v

    def uv(bid):
        b = por_id[bid]
        return f"{px(b):.4f}", f"{py(b):.4f}"

    por_id = {b["Bus_ID"]: b for b in buses}

    lineas = [r for r in ramas if r["Tipo"] == "LINEA_TRANSMISION"]
    trafos = [r for r in ramas if r["Tipo"] == "TRANSFORMADOR"]
    por_tier = collections.Counter(r["Tension_kV"] for r in lineas)
    macro_n = collections.Counter(macro.values())
    kv_n = collections.Counter(b["Nivel_kV"] for b in buses)

    out = []
    out.append(f"% Generado por generar_grafo_completo_seni142_hd.py — {datetime.date.today().isoformat()}")
    out.append(f"% Censo: {CENSO.name} sha512={sha512_de(CENSO)[:32]}…")
    out.append(f"% Ramas: {RAMAS.name} sha512={sha512_de(RAMAS)[:32]}…")
    out.append(PREAMBULO)
    out.append(rf"\begin{{tikzpicture}}[x=1cm,y=1cm]%")
    out.append(rf"% canvas: {22.0:.1f} x {alto:.2f} cm · DWG dx={dx:.1f} dy={dy:.1f} units · north up={not invertir}")

    # ------------------------------------------------- branches: transformers
    out.append("% --- transformers (dashed stroke) ---")
    for r in trafos:
        ax, ay = uv(r["From_Bus"])
        bx, by = uv(r["To_Bus"])
        out.append(rf"\draw[seniNavy,line width=0.55pt,dash pattern=on 2.2pt off 1.6pt] ({ax},{ay}) -- ({bx},{by});")
    # ------------------------------------------------- branches: lines per tier
    for tier in ("138.0", "230.0", "345.0"):
        out.append(f"% --- {tier} kV lines ---")
        for r in lineas:
            if r["Tension_kV"] != tier:
                continue
            ax, ay = uv(r["From_Bus"])
            bx, by = uv(r["To_Bus"])
            out.append(rf"\draw[{ESTILO_LINEA[tier]}] ({ax},{ay}) -- ({bx},{by});")

    # --------------------------------------------------------------- buses
    orden = ["69.0", "138.0", "230.0", "345.0"]
    out.append("% --- buses (color per HBCF macro-domain) ---")
    for tier in orden:
        for b in buses:
            if b["Nivel_kV"] != tier:
                continue
            x, y = px(b), py(b)
            rad = RADIO_KV[tier]
            relleno = COLOR_MACRO[b["Macrodominio_HBCF_Schur"]]
            out.append(rf"\draw[seniNavy,line width=0.3pt,fill={relleno}] ({x:.4f},{y:.4f}) circle ({rad});")
            if b["Tipo_Barra"] == "SLACK":
                out.append(rf"\draw[seniRed,line width=0.7pt] ({x:.4f},{y:.4f}) circle ({rad + 0.055:.3f});")
    # curated labels (white halo for legibility)
    out.append("% --- curated labels ---")
    for bid, (nombre, dxl, dyl, ancla) in ETIQUETAS.items():
        if bid in por_id:
            x, y = uv(bid)
            out.append(
                rf"\node[font=\tiny,anchor={ancla},inner sep=1pt,seniNavy,"
                rf"fill=white,fill opacity=0.7,text opacity=1] "
                rf"at ({float(x)+dxl:.4f},{float(y)+dyl:.4f}) {{{nombre}}};")

    # -------------------------------------------------------------- legend
    lx = 22.0 + 1.1   # panel to the right of the graph
    ly = alto
    out.append("% --- technical legend ---")
    out.append(rf"\draw[seniNavy,thick,rounded corners=3pt,fill=white] ({lx:.2f},{ly - 9.4:.2f}) rectangle ({lx + 5.6:.2f},{ly:.2f});")
    tx = lx + 0.25
    ty = ly - 0.55
    out.append(rf"\node[font=\small\bfseries,seniNavy,anchor=north west] at ({tx:.2f},{ty:.2f}) {{SENI-142 — Canonical graph}};")
    ty -= 0.55
    out.append(rf"\node[font=\scriptsize,seniNavy,anchor=north west] at ({tx:.2f},{ty:.2f}) {{142 buses · 193 branches}};")
    ty -= 0.50
    for mk in ("Omega_Metro", "Omega_Sur", "Omega_Este", "Omega_Norte"):
        out.append(rf"\draw[seniNavy,line width=0.3pt,fill={COLOR_MACRO[mk]}] ({tx + 0.14:.2f},{ty - 0.14:.2f}) circle (0.14);")
        out.append(rf"\node[font=\scriptsize,anchor=west] at ({tx + 0.45:.2f},{ty - 0.14:.2f}) {{{NOMBRE_MACRO[mk]} — {macro_n[mk]} buses}};")
        ty -= 0.42
    out.append(rf"\node[font=\scriptsize,anchor=north west,seniNavy] at ({tx:.2f},{ty:.2f}) {{buses: 6$\times$345 · 3$\times$230 · 106$\times$138}};")
    ty -= 0.42
    out.append(rf"\node[font=\scriptsize,anchor=north west,seniNavy] at ({tx:.2f},{ty:.2f}) {{27 buses 69 kV (border ports)}};")
    ty -= 0.52
    for tier, desc in (("345.0", "345 kV lines"), ("230.0", "230 kV lines"), ("138.0", "138 kV lines")):
        out.append(rf"\draw[{ESTILO_LINEA[tier]}] ({tx:.2f},{ty - 0.12:.2f}) -- ({tx + 0.85:.2f},{ty - 0.12:.2f});")
        out.append(rf"\node[font=\scriptsize,anchor=west] at ({tx + 1.0:.2f},{ty - 0.12:.2f}) {{{desc}: {por_tier[tier]}}};")
        ty -= 0.40
    out.append(rf"\draw[seniNavy,line width=0.55pt,dash pattern=on 2.2pt off 1.6pt] ({tx:.2f},{ty - 0.12:.2f}) -- ({tx + 0.85:.2f},{ty - 0.12:.2f});")
    out.append(rf"\node[font=\scriptsize,anchor=west] at ({tx + 1.0:.2f},{ty - 0.12:.2f}) {{transformers: {len(trafos)}}};")
    ty -= 0.46
    out.append(rf"\draw[seniNavy,line width=0.3pt,fill=seniRed!75] ({tx + 0.14:.2f},{ty - 0.10:.2f}) circle (0.13);")
    out.append(rf"\draw[seniRed,line width=0.7pt] ({tx + 0.14:.2f},{ty - 0.10:.2f}) circle (0.185);")
    out.append(rf"\node[font=\scriptsize,anchor=west] at ({tx + 0.45:.2f},{ty - 0.10:.2f}) {{slack JULIO SAURI (1.02 pu)}};")
    ty -= 0.46
    out.append(rf"\node[font=\scriptsize,seniNavy!75,anchor=north west,align=left] at ({tx:.2f},{ty:.2f}) {{DWG one-line coordinates,\\ normalized ({dx:.0f}$\times${dy:.0f} units);\\ schematic plan geometry.}};")

    out.append(r"\end{tikzpicture}")
    out.append(r"\end{document}")

    destino = AQUI / "fig_hd4_grafo_completo_seni142.tex"
    destino.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"buses={len(buses)} branches={len(ramas)} (lines={len(lineas)} {dict(por_tier)}, trafos={len(trafos)})")
    print(f"macro={dict(macro_n)} kv={dict(kv_n)}")
    print(f"canvas=22.0 x {alto:.2f} cm  north_up={not invertir}")
    print(f"written: {destino} ({destino.stat().st_size} B)")

if __name__ == "__main__":
    main()
