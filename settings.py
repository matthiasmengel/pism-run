import os
import pwd
import collections
import grids
import pwd

username = pwd.getpwuid(os.getuid()).pw_name

is_pikcluster = False
if username=="reese":
    is_pikcluster = True
    from pikcluster_settings import *
else:
    from supermuc_settings import *

# FIXME change code version
code_version = "dev"
#code_version = "pism1.1"
grid_id = "initmip16km"

experiment = code_version+"_063_"+grid_id+"_testing_small_ensemble_full_physics"

pism_experiments_dir = os.path.join(home_dir,"pism_experiments")
# FIXME change this to again to when using my own pism repo
#pismcode_dir = os.path.join(home_dir,"pism")
pismcode_dir = os.path.join(home_dir_mengel,"pism")


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

# Select the start year, this does only affect special runs - FIXME which?
startyear = 2300
length = 500
# The following choices apply only to the full_physics run 
# 'bootrstrapping' the file is bootstrapped, 
# 'regrid' bootrstrapping + regridding of certain variables
# '' if this is a restart run ?
init="" #"regrid" or "bootstrapping" or ""
# Select the run type. Possible choices are "nomass", "smoothing", "full_physics", "forcing"
# FIXME the order of the runs should be as ? 
#steps = ["smoothing","nomass", "full_physics", "forcing"]#["smoothing_nomass"] #,"full_physics", "forcing"]
steps = ["full_physics"]
# steps = ["continue"]

grid = grids.grids[grid_id]

bootstrapfile = os.path.join(input_data_dir,
                      "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc")
# infile = "no_mass.nc"

# use the smoothing file created with esia=essa=1
infile_smoothing = os.path.join(working_dir,"dev_061_initmip16km_testing_small_ensemble_dbeb47a0/",
                      "no_mass.nc")

# infile = bootstrapfile
# infile_full_physics = os.path.join(working_dir,"picobw_052_initmip4km_testing_tillphi_tw5/no_mass_tillphi_tillwatmod.nc")
# full file will be set in template
infile_full_physics = "/gss/scratch/pn69ru/di52cok/pism_out/dev_062_initmip16km_testing_small_ensemble_smoothing/smoothing_tillphi"
#infile_full_physics = "/gpfs/work/pr94ga/di36lav/pism_out/dev_058_initmip8km_resoensemble_nomass/no_mass_"
infile_forcing = "/gpfs/work/pn69ru/di36lav2/pism_store/dev_058_initmip4km_resoensemble5/dev_058_initmip4km_resoensemble5_"

atmfile = "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc"
ocean_opts = "-ocean pico -ocean_pico_file $oceanfile"

# ocean_data_dir = ""
oceanfile = os.path.join(ocn_data_dir,"schmidtko_"+grid_id+"_means.nc")
# oceanfile = os.path.join(ocn_data_dir,"schmidtko_"+grid_id+"_means_amundsen_m0p37.nc")

#ocean_data_dir = "/p/tmp/mengel/pycmip5/p003_testing"
ocean_data_dir = "/p/tmp/mengel/pycmip5/p003_testing"
# earlier settings overwritten by iterables
its = ["CSIRO-Mk3-6-0_historical+rcp85","GFDL-CM3_historical+rcp85","IPSL-CM5A-LR_historical+rcp85"]

iterables = {}
# FIXME include the ocean file iterables later on again
#iterables["oceanfile"] = { k : os.path.join(ocean_data_dir,
#   "thetao_Omon_"+k+"_r1i1p1/schmidtko_anomaly/thetao_Omon_"+k+"_r1i1p1_"+grid_id+"_100km.nc")
#   for k in its}

param_iterables = {}
param_iterables["stress_balance.sia.enhancement_factor"] = [1.0,2.0]
param_iterables["stress_balance.ssa.enhancement_factor"] = [1.0,0.4]
# param_iterables["basal_yield_stress.mohr_coulomb.till_effective_fraction_overburden"
#     ] = [0.03,0.025,0.04]
# param_iterables["basal_resistance.pseudo_plastic.q"] = [0.75,0.25,0.5]
# param_iterables["hydrology.tillwat_decay_rate"] = [2,5,8]
# special case topg_to_phi caught by if clause later:
# param_iterables["topg_to_phi"] = [
# [2.,20.,-700.,500.],
# [2.,50.,-500.,0.],
# [2.,20.,-500.,0.],
# [2.,50.,-500.,500.],
# [2.,20.,-500.,500.],
# [2.,30.,-500.,0.],
# [2.,50.,-500.,1000.]]
# param_iterables["ocean.pico.overturning_coefficent"] = [5e5,1e6]
#param_iterables["ocean.pico.heat_exchange_coefficent"] = [1e-5,2e-5,4e-5]

# iterables["oceanfile"].update({"base":oceanfile})

# for continue_set.py
# FIXME make sure to reset this value..
source_ensemble_table = "dev_060_initmip4km_testing_small_ensemble.txt"
# a subset of the hashes in ensemble_table, can also be "all".
runs_to_continue = "sets/dev_060_initmip4km_testing_small_ensemble.txt" #"data/lists_of_best/dev_058_initmip4km_resoensemble5best_20_amundsen_vel_gl.txt"


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



