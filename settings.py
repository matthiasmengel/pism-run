import os
import pwd
import grids

# machine-dependent settings
pism_experiments_dir = "/home/mengel/pism_experiments/"
experiment = "pismpik_046_initmip16km_testing"
script_name = "run_pism.sh"
pismcode_dir = "/home/mengel/pism"
working_dir = "/p/tmp/mengel/pism_out"
input_data_dir = "/p/projects/pism/mengel/pism_input/merged"
pism_exec = "./bin/pismr"
pism_mpi_do = "srun -n"

pism_config_file = os.path.join(pismcode_dir,"github/src/pism_config.cdl")

# override parameters that deviate from default.
pism_override_params = {"ocean.pico.continental_shelf_depth": -900}

startyear = 2000
length = 100

grid = grids.grids["initmip16km"]
start_from_pism_file = False
infile = os.path.join(input_data_dir,
                      "bedmap2_albmap_racmo_wessem_tillphi_pism_initmip16km.nc")

# infile = os.path.join(working_dir,"pismpik_044_initmip16km_1263_gfdlcm3rcp85",
#                       "no_mass_tillphi.nc")

atmfile = "bedmap2_albmap_racmo_wessem_tillphi_pism_initmip16km.nc"
oceanfile = "schmidtko_initmip16km.nc"

# no edits below this line needed.
project_root = os.path.dirname(os.path.abspath(__file__))
user = pwd.getpwuid(os.getuid()).pw_name



