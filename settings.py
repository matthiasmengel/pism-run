###
# Set basic settings here,e.g., adjust path to input files, 
# select the run type, ensemble parameters...
# runscripts are created via create_run.py or create_set.py
# more options are set in templates/pism_run.sh.jinja2

import os
import pwd
import collections
import grids
import pwd


# import settings including path to input, output directories
username = pwd.getpwuid(os.getuid()).pw_name
is_pikcluster = False
if username=="reese":
    is_pikcluster = True
    from pikcluster_settings import *
else:
    from supermuc_settings import *

# select pism code version
code_version = "pism1.1" #"dev" # "pism1.1"
# select resolution of the run
grid_id = "initmip16km"

# ATTENTION: make sure to adjust this, otherwise, files will be overwritten
# a useful approach is to have one number (_061_) for a suite of runs that get a
# common name (_small_ensemble_) and an additional identifies for the current 
# run step (_forcing_) 
experiment = code_version+"_070_"+grid_id+"_ensemble_bedmap2_nomass_adjtillwat"

# directories
pism_experiments_dir = os.path.join(home_dir,"pism_experiments")
pismcode_dir = os.path.join(home_dir,"pism")
#pismcode_dir = os.path.join(home_dir_mengel,"pism")

input_data_dir = os.path.join(input_root_dir,"merged")
atm_data_dir = os.path.join(input_root_dir,"merged")
ocn_data_dir = os.path.join(input_root_dir,"schmidtko")


# set pism parameters that apply to all runs (unless part of the ensemble)
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
# Include limit for the nomass runs! FIXME nomass only!
("stress_balance.ssa.fd.max_speed", 10e3),
("stress_balance.sia.limit_diffusivity", "yes"),
("stress_balance.sia.max_diffusivity", 10),
])


# select the run steps, possible are "smoothing","nomass", "full_physics", "forcing"
# "continue"
# smoothing: optionally run 1-year sia only to smooth the fields
# nomass: no_mass run for temperature evolution (could be run with sia or sia+ssa advection, in the latter
# case you might want to limit sia-diffusivity and ssa velocities using config_override)
# full_physics: run with full physics, select start year and input type below, select parametes for ensemble below
# forcing: run forcing experiment, select forcing files below, FIXME this does not exist yet!
steps = ["nomass"]


# Only full_physics, forcing: select the start year and duration
startyear = 2300
length = 500

# Only full_physics: select the init type
# "bootrstrapping": the file is bootstrapped, 
# "regrid": bootrstrapping + regridding of certain variables
# "": -i option
init="" 


grid = grids.grids[grid_id]

bootstrapfile = os.path.join(input_data_dir,
                      "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc")
# regrid only the tillwat variable from a fit with rignot velocities
regridfile_tillwat = "/gpfs/work/pn69ru/di52cok/pism_store/dev_061_initmip16km_testing_small_ensemble/dev_062_initmip16km_testing_small_ensemble_smoothing/smoothing_tillphi_adjtillwat.nc"
# infile = "no_mass.nc"

# use the smoothing file created with esia=essa=1
infile_smoothing = os.path.join(working_dir,"dev_061_initmip16km_testing_small_ensemble_dbeb47a0/",
                      "no_mass.nc")

# infile = bootstrapfile
# infile_full_physics = os.path.join(working_dir,"picobw_052_initmip4km_testing_tillphi_tw5/no_mass_tillphi_tillwatmod.nc")
infile_full_physics = "/gpfs/work/pn69ru/di52cok/pism_store/dev_061_initmip16km_testing_small_ensemble/dev_062_initmip16km_testing_small_ensemble_smoothing/smoothing_tillphi_adjtillwat"

infile_forcing = "/gpfs/work/pn69ru/di52cok/pism_store/dev_061_initmip16km_testing_small_ensemble/dev_063_initmip16km_testing_small_ensemble_full_physics_dbeb47a0"
# test this..
runs_for_forcing = "data/lists_of_best/dev_063_initmip16km_testing_small_ensemble_full_physics_forcing.txt"


atmfile = "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc"
ocean_opts = "-ocean pico -ocean_pico_file $oceanfile"

# ocean_data_dir = ""
oceanfile = os.path.join(ocn_data_dir,"schmidtko_"+grid_id+"_means.nc")
# oceanfile = os.path.join(ocn_data_dir,"schmidtko_"+grid_id+"_means_amundsen_m0p37.nc")

# forcing: ocean data iterables
ocean_data_dir = "/gpfs/work/pn69ru/di52cok/pism_input/pycmip5/p003_testing"
its = ["CSIRO-Mk3-6-0_historical+rcp85","GFDL-CM3_historical+rcp85","IPSL-CM5A-LR_historical+rcp85"]

iterables = {}
# FIXME include the ocean file iterables for "forcing" runs: 
#iterables["oceanfile"] = { k : os.path.join(ocean_data_dir,
#   "thetao_Omon_"+k+"_r1i1p1/schmidtko_anomaly/thetao_Omon_"+k+"_r1i1p1_"+grid_id+"_100km.nc")
#   for k in its}

# "full_physics": to create parameter ensemble
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
# This allows to continue a number of runs as specifies in runs_to_continue from the full_physics ensemble
# it is not useful to create forcing runs, since the iterables are not taken into account
source_ensemble_table = "dev_063_initmip16km_testing_small_ensemble_full_physics.txt"
# a subset of the hashes in ensemble_table, can also be "all".
runs_to_continue = "data/lists_of_best/dev_063_initmip16km_testing_small_ensemble_full_physics.txt" #"data/lists_of_best/dev_058_initmip4km_resoensemble5best_20_amundsen_vel_gl.txt"


# ensemble hash is inserted between infile_continue[0] and infile_continue[1]
# infile_continue = ["/gpfs/work/pn69ru/di36lav2/pism_store/dev_058_initmip4km_resoensemble5/dev_058_initmip4km_resoensemble5_",
# "snapshots_2300.000.nc"]
def get_infile_to_continue(ehash, year):
    pre = "/gpfs/work/pn69ru/di52cok/pism_store/dev_061_initmip16km_testing_small_ensemble/dev_063_initmip16km_testing_small_ensemble_full_physics_"
    fle = ["snapshots_",".000.nc"]
    return os.path.join(pre+ehash,fle[0]+str(year)+fle[1])


# no edits below this line needed.
project_root = os.path.dirname(os.path.abspath(__file__))
user = pwd.getpwuid(os.getuid()).pw_name



