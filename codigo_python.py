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
        map_name = 'complete(3).json'
        
        
        model_path = 'Modelos'  ####SubCarpeta
        model_name = 'reconstruccion_mat.mat'
        
        restrictions_path = 'Restricciones'  ####SubCarpeta  
        restrictions_name = 'IAA_restrictions.xlsx'
        
        save_path = 'Soluciones'   ####SubCarpeta
        
        
        '''
        -----------------------------------------------------------------------------
        
        '''
        
        map_dir = join(data_dir,map_path)
        model_complete = join(model_path,model_name)
        model = cobra.io.load_matlab_model(model_complete)
        cobra.io.save_json_model(model, 'Modelos\\Reconstruccion.json')
        cobra.io.write_sbml_model(model, 'Modelos\\prueba_sbml')
        
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
        
        """
        Restricciones del modelo
        intake_flux
        """
        
        restrictions_complete = join(restrictions_path,restrictions_name)
        num_models = len(pandas.read_excel(restrictions_complete,   sheet_name=None, header = 0))
        models = pandas.ExcelFile(restrictions_complete)
        models_names = models.sheet_names
        del models
        webbrowser.open('https://escher.github.io/#/',0)
        time.sleep(3) # Sleep for 3 seconds
        
        for num in list(range(num_models)):
            model_id = num
            restrictions = pandas.read_excel(restrictions_complete,   sheet_name=model_id, header = 0)
            num_restrictions = len(restrictions)
            
            for i in list(range(num_restrictions)):
                react_id = restrictions.at[i,'Reaction']
                react_lb = restrictions.at[i,'Lb']
                react_ub = restrictions.at[i,'Ub']
                react_obj = restrictions.at[i,'Objective']
                model.reactions.get_by_id(react_id).upper_bound = 100
                model.reactions.get_by_id(react_id).lower_bound = -100
                model.reactions.get_by_id(react_id).upper_bound = react_ub
                model.reactions.get_by_id(react_id).lower_bound = react_lb
                model.reactions.get_by_id(react_id).objective_coefficient = react_obj
                
                
            print('Restricciones leidas correctamente')
            print(model.objective.expression)
            print(model.objective.direction) 
            print("exchanges", model.exchanges)
            print("demands", model.demands)
            print("sinks", model.sinks)
            name=models_names[num]
            ext = '.csv'
            file_name=name+ext
            model_save_path = join(model_path,(name + '.json'))
            solution_path = join(save_path,file_name)
            solution = model.optimize()
            Fluxes= solution.fluxes
            Fluxes.to_csv(path_or_buf=solution_path, sep=',',na_rep='', float_format=None, )
            print('Modelo ' + name + ' solucionado correctamente')
            map_file_path = join(map_dir,map_name)
            builder = Builder(map_json=map_file_path)
            builder.reaction_data = Fluxes
            builder.model_json = 'Modelos\\Reconstruccion.json'
            builder.save_html(join(map_dir,name +".html"))
            path_dir = join(map_dir,name+".html")
            file_dir = "file:\\" 
            final_dir = file_dir + path_dir 
            webbrowser.open(final_dir,0)
