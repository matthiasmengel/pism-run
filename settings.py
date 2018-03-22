import os
import pwd

startyear = 2000
length = 100


# machine-dependent settings
pism_experiments_dir = "/home/mengel/pism_experiments/"
experiment = "pismpik_046_initmip16km_testing"
script_name = "run_pism.sh"
pismcode_dir = "/home/mengel/pism"
working_dir = "/p/tmp/mengel/pism_out"
input_data_dir = "/p/projects/pism/mengel/pism_input/merged"
pism_exec = "./bin/pismr"
pism_mpi_do = "srun -n"

# no edits below this line needed.
project_root = os.path.dirname(os.path.abspath(__file__))
user = pwd.getpwuid(os.getuid()).pw_name



