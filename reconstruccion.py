# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import cobra
import os
from os.path import join
import pandas
import webbrowser
from escher import Builder
import time



data_dir = r'G:\Mi unidad\Maestria\Tesis\03_Modelos_Metabolicos'
os.chdir(data_dir)

map_path = 'Mapas_graficos'  ####Subcarpeta
map_name = 'e_coli_core.Core metabolism.json'

model_path = 'Modelos'  ####SubCarpeta
model_name = 'reconstruccion_mat.mat'

restrictions_path = 'Restricciones'  ####SubCarpeta  
restrictions_name = 'restrictions.xlsx'

save_path = 'Soluciones'   ####SubCarpeta


'''
-----------------------------------------------------------------------------

'''

map_dir = join(data_dir,map_path)
model_complete = join(model_path,model_name)
model = cobra.io.load_matlab_model(model_complete)



print(f'{len(model.reactions)} reactions')
print(f'{len(model.metabolites)} metabolites')
print(f'{len(model.genes)} genes')


print("Reactions")
print("---------")
for x in model.reactions:
    print("%s : %s" % (x.id, x.reaction))

print("")
print("Metabolites")
print("-----------")
for x in model.metabolites:
    print('%9s : %s' % (x.id, x.formula))

print("")
print("Genes")
print("-----")
for x in model.genes:
    associated_ids = (i.id for i in x.reactions)
    print("%s is associated with reactions: %s" %
          (x.id, "{" + ", ".join(associated_ids) + "}"))


print(model.objective.expression)
print(model.objective.direction)

print("exchanges", model.exchanges)
print("demands", model.demands)
print("sinks", model.sinks)


"""
Para solucionar el modelo
"""
model.reactions.get_by_id('EX_glc__D_e').lower_bound = -1
model.reactions.get_by_id('EX_glc__D_e').upper_bound = -1
model.objective = 'GLCt1'



file_name = 'prueba'
solution_path = join(save_path,file_name)
name=file_name

solution = model.optimize()
Fluxes= solution.fluxes

Fluxes.to_csv(path_or_buf=solution_path, sep=',',na_rep='', float_format=None, )
print('Modelo ' + name + ' solucionado correctamente')
map_file_path = join(map_dir,map_name)
builder = Builder(map_json=map_file_path)
builder.reaction_data = Fluxes
cobra.io.save_json_model(model,'prueba.json')
builder.model = cobra.io.load_json_model('prueba.json')
builder.save_html(join(map_dir,name +".html"))
path_dir = join(map_dir,name+".html")
file_dir = "file:\\" 
final_dir = file_dir + path_dir 
webbrowser.open(final_dir,0)


