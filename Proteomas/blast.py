# -*- coding: utf-8 -*-
"""
Created on Mon May 10 18:50:34 2021

@author: Andy
"""

import os
from os.path import join
import pandas



data_dir = r'G:\Mi unidad\Maestria\Tesis\03_Modelos_Metabolicos\Proteomas'

os.chdir(data_dir)



db_file = 'DB_Enzimas.FASTA'
db_type = 'prot'
out = 'db_Enzimas'
db_command = 'makeblastdb -in ' + db_file +  ' -dbtype ' + db_type + " -out Bases_de_datos\\" + out

validation = os.path.exists("Bases_de_datos\\"+ out + ".pdb")

if validation == False:
    os.popen(db_command)



db = out
query = 'Prot_Shewanella.FASTA'
num_treads = '8'
out_blast = "Prot_Shewanella.txt"
outfmt = '"6 qseqid pident evalue qcovs mismatch score stitle" -max_target_seqs 1 -subject_besthit -qcov_hsp_perc 80  -evalue 1'

blastn_c = 'blastp -db Bases_de_datos\\' + db + ' -query Querys\\' + query + ' -num_threads ' +  num_treads + ' -out Resultados\\' + out_blast + " -outfmt " + outfmt 
os.system(blastn_c)
os.system('copy ' + 'Resultados\\' + out_blast + "  C:\\Users\\Andy\\Documents\\Blast\\Resultados\\" + out_blast)



    
