clear all
clc
close all


initCobraToolbox(false)

%%
cd 'G:\Mi unidad\Maestria\Tesis\03_Modelos_Metabolicos\Modelos'
fileName = '80_Reconstruccion_2.xlsx';

    

model = readCbModel(fileName);
writeCbModel(model,'mat','reconstruccion_mat.mat');
    
topo = networkTopology(model);
final = {model.mets topo};

xlswrite('final.xlsx',final)
%%
writeCbModel(model,'sbml','reconstruccion_sbml');

%%