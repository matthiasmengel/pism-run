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

experiment = code_version+"_058_"+grid_id+"_resoensemble4"


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


startyear = 1850
length = 1000
boostrapping=False
# steps = ["smoothing_nomass","full_physics"]
steps = []
steps = ["nomass"]

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
oceanfile = os.path.join(ocn_data_dir,"schmidtko_"+grid_id+"_means_amundsen_m0p37.nc")

#ocean_data_dir = "/p/tmp/mengel/pycmip5/p003_testing"
# earlier settings overwritten by iterables
its = ["CSIRO-Mk3-6-0_historical+rcp85","GFDL-CM3_historical+rcp85","IPSL-CM5A-LR_historical+rcp85"]

iterables = {}
#iterables["oceanfile"] = { k : os.path.join(ocean_data_dir,
#    "thetao_Omon_"+k+"_r1i1p1/schmidtko_anomaly/thetao_Omon_"+k+"_r1i1p1_"+grid_id+"_100km.nc")
#    for k in its}

param_iterables = {}
param_iterables["stress_balance.sia.enhancement_factor"] = [1.0,2.0,3.0]
param_iterables["stress_balance.ssa.enhancement_factor"] = [0.4]#[1.0,0.4,0.7]
param_iterables["basal_yield_stress.mohr_coulomb.till_effective_fraction_overburden"] = [0.03]#,0.025,0.04]
param_iterables["basal_resistance.pseudo_plastic.q"] = [0.25]#[0.75,0.25,0.5]
param_iterables["hydrology.tillwat_decay_rate"] = [2,5,8]
#param_iterables["ocean.pico.overturning_coefficent"] = [5e5,1e6]
#param_iterables["ocean.pico.heat_exchange_coefficent"] = [1e-5,2e-5,4e-5]

# iterables["oceanfile"].update({"base":oceanfile})

# no edits below this line needed.
project_root = os.path.dirname(os.path.abspath(__file__))
user = pwd.getpwuid(os.getuid()).pw_name



