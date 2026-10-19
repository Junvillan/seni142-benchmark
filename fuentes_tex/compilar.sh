#!/usr/bin/env bash
# ==============================================================================
# compilar.sh — Compilador unificado y protocolo Scout para fuentes LaTeX (SENI-142)
# Workspace: PAPER_SENI_142_IEEE_TRANSACTIONS
# ==============================================================================
set -eu

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(dirname "$DIR")"
AUX="$WS/auxiliares"
mkdir -p "$AUX"

export SOURCE_DATE_EPOCH=1760659200
export FORCE_SOURCE_DATE=1

TARGET="${1:-all}"

compilar_job() {
  local JOB="$1"
  local ENGINE="${2:-pdflatex}"
  echo "==> Compilando $JOB con $ENGINE..."
  
  cd "$DIR"
  nice -n 19 "$ENGINE" -interaction=nonstopmode "$JOB.tex" > /dev/null 2>&1 || true
  if [ -f "$JOB.aux" ]; then
    bibtex "$JOB" > /dev/null 2>&1 || true
  fi
  nice -n 19 "$ENGINE" -interaction=nonstopmode "$JOB.tex" > /dev/null 2>&1 || true
  nice -n 19 "$ENGINE" -interaction=nonstopmode "$JOB.tex" > /dev/null 2>&1 || true

  if [ -f "$JOB.pdf" ]; then
    cp -f "$JOB.pdf" "$WS/$JOB.pdf" && rm -f "$JOB.pdf"
    echo "    [OK] PDF depositado en $WS/$JOB.pdf"
  else
    echo "    [ERROR] No se generó $JOB.pdf"
    exit 1
  fi

  # Protocolo Scout: mover todos los volátiles a auxiliares/
  for ext in aux log out bbl blg toc lof lot xdv fdb_latexmk fls; do
    [ -f "$DIR/$JOB.$ext" ] && mv -f "$DIR/$JOB.$ext" "$AUX/" || true
    [ -f "$WS/$JOB.$ext" ] && [ "$ext" != "pdf" ] && mv -f "$WS/$JOB.$ext" "$AUX/" || true
  done
}

case "$TARGET" in
  1col|en1col)
    compilar_job "SENI142_IEEE_1col" "pdflatex"
    ;;
  2col|en2col)
    compilar_job "SENI142_IEEE_2col" "pdflatex"
    ;;
  es|es1col)
    compilar_job "SENI142_IEEE_ES_1col" "pdflatex"
    ;;
  zh|zh1col)
    compilar_job "SENI142_IEEE_ZH_1col" "xelatex"
    ;;
  sec2_es)
    compilar_job "SECCION_II_METODOLOGIA_ES" "pdflatex"
    ;;
  sec2_en)
    compilar_job "SECCION_II_METODOLOGIA_EN" "pdflatex"
    ;;
  all)
    compilar_job "SENI142_IEEE_1col" "pdflatex"
    compilar_job "SENI142_IEEE_2col" "pdflatex"
    compilar_job "SENI142_IEEE_ES_1col" "pdflatex"
    compilar_job "SENI142_IEEE_ZH_1col" "xelatex"
    compilar_job "SECCION_II_METODOLOGIA_ES" "pdflatex"
    compilar_job "SECCION_II_METODOLOGIA_EN" "pdflatex"
    echo "==> [SCOUT PROTOCOL PASS] Todos los PDFs compilados y depositados en raíz."
    ;;
  *)
    echo "Uso: $0 {1col|2col|es1col|zh1col|sec2_es|sec2_en|all}"
    exit 2
    ;;
esac
