# Fuentes LaTeX del Manuscrito SENI-142

Esta carpeta reúne la totalidad de los archivos fuente `.tex`, `.bib` y subsecciones modulares del artículo científico **SENI-142** para IEEE Transactions, organizado bajo el **Protocolo Scout**:

## 1. Archivos Maestros de Compilación
- `SENI142_IEEE_1col.tex`: Manuscrito completo en formato monográfico (1 columna, 11pt) en inglés.
- `SENI142_IEEE_2col.tex`: Manuscrito completo en formato camera-ready oficial IEEE (2 columnas, 10pt) en inglés.
- `SENI142_IEEE_ES_1col.tex`: Manuscrito completo en español (1 columna).
- `SENI142_IEEE_ZH_1col.tex`: Manuscrito completo en chino simplificado (XeLaTeX + xeCJK).
- `SECCION_II_METODOLOGIA_EN.tex`: Documento autónomo de 8 páginas con la Sección II (Metodología) en inglés.
- `SECCION_II_METODOLOGIA_ES.tex`: Documento autónomo de 8 páginas con la Sección II (Metodología) en español.

## 2. Subcarpetas de Secciones Modulares
- `secciones/`: Secciones I a VII en inglés técnico IEEE.
- `secciones_es/`: Secciones I a VII en español académico riguroso.
- `secciones_zh/`: Secciones I a VII en chino simplificado.

## 3. Figuras TikZ Nativas
- `sec01_fig_gemelo_fases_tikz.tex` / `_es.tex`: Diagrama del Gemelo Digital en 4 fases.
- `sec02_fig_p2g_h2_tikz.tex` / `_es.tex`: Diagrama del vector electroquímico Power-to-Gas e hidrógeno.
- `sec03_fig_topologia_seni_tikz.tex` / `_es.tex`: Diagrama topológico de la red SENI-142.

## 4. Bibliografía
- `referencias.bib`: Base de datos BibTeX unificada con las 41 citas de literatura revisada por pares.

## 5. Compilación Rápida
Ejecute el script reproducible:
```bash
./compilar.sh {1col|2col|es1col|zh1col|sec2_es|sec2_en|all}
```
El script compila con marca temporal determinista (`SOURCE_DATE_EPOCH`), deposita los PDFs directamente en la raíz de `PAPER_SENI_142_IEEE_TRANSACTIONS/` y traslada los archivos volátiles a `auxiliares/`.
