"""
DEMO_PYPOWER_SENI142.py
Demostracion rapida en Python para cargar y resolver SENI-142 con PyPower
Autor: Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)
Universitat Politecnica de Valencia (UPV)
"""
import numpy as np
from case142_seni import case142_seni
from pypower.rundcpf import rundcpf
from pypower.makeYbus import makeYbus

print("=" * 60)
print("  BENCHMARK NACIONAL SENI-142 · PYTHON / PYPOWER DEMO")
print("  Universitat Politecnica de Valencia (UPV)")
print("=" * 60)

# 1. Cargar caso
mpc = case142_seni()
print(f"-> Caso cargado: {len(mpc['bus'])} barras, {len(mpc['branch'])} ramas, {len(mpc['gen'])} generadores.")
print(f"   Demanda pico: {np.sum(mpc['bus'][:, 2]):.1f} MW, Capacidad Pmax: {np.sum(mpc['gen'][:, 8]):.1f} MW")

# 2. Convertir indices 1-based a 0-based para PyPower interno
b0 = mpc["bus"].copy(); b0[:, 0] -= 1
g0 = mpc["gen"].copy(); g0[:, 0] -= 1
br0 = mpc["branch"].copy(); br0[:, 0] -= 1; br0[:, 1] -= 1
ppc = {"baseMVA": mpc["baseMVA"], "bus": b0, "gen": g0, "branch": br0}

# 3. Flujo DC
res, success = rundcpf(ppc)
print(f"-> Flujo DC (rundcpf): {'CONVERGIDO CON EXITO' if success else 'FALLO'}")

# 4. Ybus
Ybus, Yf, Yt = makeYbus(mpc["baseMVA"], b0, br0)
print(f"-> Matriz Ybus calculada: {Ybus.shape[0]}x{Ybus.shape[1]}, {Ybus.nnz} elementos no nulos.")
print("=" * 60)
