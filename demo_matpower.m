%% DEMO_MATPOWER_SENI142.m
% Demostracion rapida para MATLAB / Octave con MATPOWER
% Benchmark Nacional SENI-142 (Republica Dominicana)
% Autor: Ing. Junior Alexis Villanueva Rosario, Ms.C., Ph.D.(c)
% Director: Dr. Manuel Alcazar Ortega (Universitat Politecnica de Valencia)

clear; clc;
fprintf('========================================================\n');
fprintf('  BENCHMARK NACIONAL SENI-142 · CASO MATPOWER ESTANDAR  \n');
fprintf('  Universitat Politecnica de Valencia (UPV)             \n');
fprintf('========================================================\n\n');

% 1. Cargar el caso canonico
mpc = case142_seni();
fprintf('-> Caso cargado exitosamente.\n');
fprintf('   - Barras nodales:     %d (115 transporte + 27 puertos 69 kV)\n', size(mpc.bus, 1));
fprintf('   - Ramas de red:       %d (135 lineas + 58 transformadores)\n', size(mpc.branch, 1));
fprintf('   - Parque generador:   %d unidades\n', size(mpc.gen, 1));
fprintf('   - Demanda pico total: %.1f MW | %.1f MVAR\n', sum(mpc.bus(:, 3)), sum(mpc.bus(:, 4)));
fprintf('   - Capacidad Pmax:     %.1f MW\n\n', sum(mpc.gen(:, 9)));

% 2. Ejecutar Flujo de Potencia DC
fprintf('-> Ejecutando Flujo de Potencia DC (rundcpf)...\n');
res_dc = rundcpf(mpc);
if res_dc.success
    fprintf('-> Flujo DC CONVERGIDO con exito!\n');
    fprintf('   - Perdidas activas: 0.00 MW (modelo DC sin perdidas)\n');
    fprintf('   - Rango de angulos: [%.2f°, %.2f°]\n\n', min(res_dc.bus(:, 9)), max(res_dc.bus(:, 9)));
else
    fprintf('-> Fallo en convergencia DC.\n\n');
end

% 3. Inspeccion de matriz de admitancias
fprintf('-> Calculando matriz de admitancias Ybus...\n');
[Ybus, Yf, Yt] = makeYbus(mpc);
fprintf('   - Dimension Ybus: %d x %d (dispersa)\n', size(Ybus, 1), size(Ybus, 2));
fprintf('   - Elementos no nulos (nnz): %d\n\n', nnz(Ybus));
fprintf('========================================================\n');
fprintf('  Demostracion completada con exito.                    \n');
fprintf('========================================================\n');
