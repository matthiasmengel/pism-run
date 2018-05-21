"""
Submit the ensemble of PISM runs, as created with
create_set.py, to the batch system of cluster PIK or SUPERMUC.
"""

import os
import pandas as pd
import subprocess
import settings; reload(settings)

ensemble_table = pd.read_csv(os.path.join("sets",settings.experiment+".txt"),
                             sep='\s+',index_col=0)

for exp_hash in ensemble_table.index[0:1]:

    ens_member_name = settings.experiment+"_"+exp_hash
    ens_member_path = os.path.join(settings.pism_experiments_dir,ens_member_name)
    print ens_member_path
    subprocess.check_call("cd "+ens_member_path+" && "+settings.submit_command,
                          shell=True)


