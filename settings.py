import os
import pwd
import collections
import grids
import pwd

username = pwd.getpwuid(os.getuid()).pw_name

is_pikcluster = False
if username=="mengel":
    is_pikcluster = True
    from pikcluster_settings import *
else:
    from supermuc_settings import *

code_version = "dev"
grid_id = "initmip4km"

experiment = code_version+"_058_"+grid_id+"_resoensemble7warmamund"


pism_experiments_dir = os.path.join(home_dir,"pism_experiments")
pismcode_dir = os.path.join(home_dir,"pism")

input_data_dir = os.path.join(input_root_dir,"merged")
atm_data_dir = os.path.join(input_root_dir,"merged")
ocn_data_dir = os.path.join(input_root_dir,"schmidtko")

pism_config_file = os.path.join(pismcode_dir,code_version,"src/pism_config.cdl")

# override parameters that deviate from default.
override_params = collections.OrderedDict([
# "ocean.pico.continental_shelf_depth", -2000,
("stress_balance.sia.enhancement_factor",1.0),
("stress_balance.ssa.enhancement_factor",1.0),
("stress_balance.model","ssa+sia"),
("time_stepping.skip.enabled", "yes"),
("basal_yield_stress.mohr_coulomb.till_effective_fraction_overburden", 0.03),
("basal_resistance.pseudo_plastic.q", 0.75),
("basal_yield_stress.mohr_coulomb.topg_to_phi.enabled",  "yes"),
("basal_yield_stress.mohr_coulomb.topg_to_phi.phi_min", 5.0),
("basal_yield_stress.mohr_coulomb.topg_to_phi.phi_max", 50.0),
("basal_yield_stress.mohr_coulomb.topg_to_phi.topg_min", -700.0),
("basal_yield_stress.mohr_coulomb.topg_to_phi.topg_max", 500.0),
("basal_resistance.pseudo_plastic.enabled","true"),
("hydrology.tillwat_decay_rate", 5.0),
# grounding line interpolations
("energy.basal_melt.use_grounded_cell_fraction", "false"),
("calving.methods", "eigen_calving,thickness_calving"),
("calving.eigen_calving.K", 1e17),
("calving.thickness_calving.threshold", 200),
# the following four options are equivalent to command line option -pik
# if all set to true
("stress_balance.calving_front_stress_bc", "true"),
("geometry.part_grid.enabled", "true"),
("geometry.remove_icebergs", "true"),
("geometry.grounded_cell_fraction", "true"),

("ocean.pico.exclude_ice_rises", "yes"),
])

startyear = 2300
length = 500
init="regrid" # or "bootstrapping" or ""
# steps = ["smoothing_nomass","full_physics", "forcing"]
steps = ["continue"]

grid = grids.grids[grid_id]

bootstrapfile = os.path.join(input_data_dir,
                      "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc")
# infile = "no_mass.nc"

infile_smoothing = os.path.join(working_dir,"picobw_050_initmip4km_testing1",
                      "no_mass_tillphi.nc")

# infile = bootstrapfile
# infile_full_physics = os.path.join(working_dir,"picobw_052_initmip4km_testing_tillphi_tw5/no_mass_tillphi_tillwatmod.nc")
# full file will be set in template
infile_full_physics = "/gpfs/work/pr94ga/di36lav/pism_out/dev_058_initmip8km_resoensemble_nomass/no_mass_"

atmfile = "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc"
ocean_opts = "-ocean pico -ocean_pico_file $oceanfile"

# ocean_data_dir = ""
oceanfile = os.path.join(ocn_data_dir,"schmidtko_"+grid_id+"_means.nc")
# oceanfile = os.path.join(ocn_data_dir,"schmidtko_"+grid_id+"_means_amundsen_m0p37.nc")

#ocean_data_dir = "/p/tmp/mengel/pycmip5/p003_testing"
# earlier settings overwritten by iterables
its = ["CSIRO-Mk3-6-0_historical+rcp85","GFDL-CM3_historical+rcp85","IPSL-CM5A-LR_historical+rcp85"]

iterables = {}
#iterables["oceanfile"] = { k : os.path.join(ocean_data_dir,
#    "thetao_Omon_"+k+"_r1i1p1/schmidtko_anomaly/thetao_Omon_"+k+"_r1i1p1_"+grid_id+"_100km.nc")
#    for k in its}

param_iterables = {}
param_iterables["stress_balance.sia.enhancement_factor"] = [1.0,2.0,3.0]
param_iterables["stress_balance.ssa.enhancement_factor"] = [1.0,0.4,0.7]
param_iterables["basal_yield_stress.mohr_coulomb.till_effective_fraction_overburden"
    ] = [0.03,0.025,0.04]
param_iterables["basal_resistance.pseudo_plastic.q"] = [0.75,0.25,0.5]
param_iterables["hydrology.tillwat_decay_rate"] = [2,5,8]
# special case topg_to_phi caught by if clause later:
# param_iterables["topg_to_phi"] = [
# [2.,20.,-700.,500.],
# [2.,50.,-500.,0.],
# [2.,20.,-500.,0.],
# [2.,50.,-500.,500.],
# [2.,20.,-500.,500.],
# [2.,30.,-500.,0.],
# [2.,50.,-500.,1000.]]
#param_iterables["ocean.pico.overturning_coefficent"] = [5e5,1e6]
#param_iterables["ocean.pico.heat_exchange_coefficent"] = [1e-5,2e-5,4e-5]

# iterables["oceanfile"].update({"base":oceanfile})

# for continue_set.py
source_ensemble_table = "dev_058_initmip4km_resoensemble5.txt"
# a subset of the hashes in ensemble_table, can also be "all".
runs_to_continue = "data/lists_of_best/dev_058_initmip4km_resoensemble5best_20_amundsen_vel.txt"


# ensemble hash is inserted between infile_continue[0] and infile_continue[1]
# infile_continue = ["/gpfs/work/pn69ru/di36lav2/pism_store/dev_058_initmip4km_resoensemble5/dev_058_initmip4km_resoensemble5_",
# "snapshots_2300.000.nc"]
def get_infile_to_continue(ehash, year):
    pre = "/gpfs/work/pn69ru/di36lav2/pism_store/dev_058_initmip4km_resoensemble5/dev_058_initmip4km_resoensemble5_"
    fle = ["snapshots_",".000.nc"]
    return os.path.join(pre+ehash,fle[0]+str(year)+fle[1])


# no edits below this line needed.
project_root = os.path.dirname(os.path.abspath(__file__))
user = pwd.getpwuid(os.getuid()).pw_name



