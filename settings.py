import os
import pwd
import collections
import grids

# machine-dependent settings
pism_experiments_dir = "/home/mengel/pism_experiments/"
script_name = "run_pism.sh"
pismcode_dir = "/home/mengel/pism"
working_dir = "/p/tmp/mengel/pism_out"
pism_exec = "./bin/pismr"
pism_mpi_do = "srun -n"

input_data_dir = "/p/projects/pism/mengel/pism_input/merged"
atm_data_dir = "/p/projects/pism/mengel/pism_input/merged"
ocean_data_dir = "/p/tmp/mengel/pycmip5/p003_testing"

pism_config_file = os.path.join(pismcode_dir,"github/src/pism_config.cdl")

# override parameters that deviate from default.
override_params = collections.OrderedDict([
# "ocean.pico.continental_shelf_depth", -2000,
("stress_balance.sia.enhancement_factor",2.0),
("stress_balance.model","ssa+sia"),
("time_stepping.skip.enabled", "yes"),
("basal_yield_stress.mohr_coulomb.till_effective_fraction_overburden", 0.04),
("basal_resistance.pseudo_plastic.q", 0.5),
# grounding line interpolations
("geometry.grounded_cell_fraction", "true"),
("energy.basal_melt.use_grounded_cell_fraction", "false"),

("calving.methods", "eigen_calving,thickness_calving"),
("calving.eigen_calving.K", 1e17),
("calving.thickness_calving.threshold", 200),

# the follwing are equivalent to command line option -pik
("stress_balance.calving_front_stress_bc", "true"),
("geometry.part_grid.enabled", "true"),
("geometry.remove_icebergs", "true"),
("geometry.grounded_cell_fraction", "true"),
])

startyear = 2000
length = 100

grid_id = "initmip8km"
experiment = "pismpik_047_"+grid_id+"_testing"
grid = grids.grids[grid_id]
start_from_pism_file = False
infile = os.path.join(input_data_dir,
                      "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc")

# infile = os.path.join(working_dir,"pismpik_044_initmip16km_1263_gfdlcm3rcp85",
#                       "no_mass_tillphi.nc")

atmfile = "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc"
oceanfile = os.path.join(input_data_dir,"schmidtko_"+grid_id+".nc")

# earlier settings overwritten by iterables
iterables = {"oceanfile":{
"CSIRO-Mk3-6-0_rcp85":"thetao_Omon_CSIRO-Mk3-6-0_rcp85_r1i1p1/schmidtko_anomaly/thetao_Omon_CSIRO-Mk3-6-0_rcp85_r1i1p1_"+grid_id+"_100km.nc",
"GFDL-CM3_rcp85":"thetao_Omon_GFDL-CM3_rcp85_r1i1p1/schmidtko_anomaly/thetao_Omon_GFDL-CM3_rcp85_r1i1p1_"+grid_id+"_100km.nc",
"IPSL-CM5A-LR_rcp85":"thetao_Omon_IPSL-CM5A-LR_rcp85_r1i1p1/schmidtko_anomaly/thetao_Omon_IPSL-CM5A-LR_rcp85_r1i1p1_"+grid_id+"_100km.nc"
}}

# no edits below this line needed.
project_root = os.path.dirname(os.path.abspath(__file__))
user = pwd.getpwuid(os.getuid()).pw_name



