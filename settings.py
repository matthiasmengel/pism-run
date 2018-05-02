import os
import pwd
import collections
import grids

# machine-dependent settings
pism_experiments_dir = "/home/mengel/pism_experiments/"
pismcode_dir = "/home/mengel/pism"
working_dir = "/p/tmp/mengel/pism_out"
pism_exec = "./bin/pismr"
pism_mpi_do = "srun -n"
pik_partition="broadwell"
submit_command="sbatch submit.sh"

input_data_dir = "/p/projects/pism/mengel/pism_input/merged"
atm_data_dir = "/p/projects/pism/mengel/pism_input/merged"
ocn_data_dir = "/p/projects/pism/mengel/pism_input/schmidtko"

pism_config_file = os.path.join(pismcode_dir,"picobw/src/pism_config.cdl")

# override parameters that deviate from default.
override_params = collections.OrderedDict([
# "ocean.pico.continental_shelf_depth", -2000,
("stress_balance.sia.enhancement_factor",2.0),
("stress_balance.model","ssa+sia"),
("time_stepping.skip.enabled", "yes"),
("basal_yield_stress.mohr_coulomb.till_effective_fraction_overburden", 0.04),
("basal_resistance.pseudo_plastic.q", 0.5),
("basal_yield_stress.mohr_coulomb.topg_to_phi.enabled",  "no"),
# ("basal_yield_stress.mohr_coulomb.topg_to_phi.phi_min", 5.0),
# ("basal_yield_stress.mohr_coulomb.topg_to_phi.phi_max", 15.0),
# ("basal_yield_stress.mohr_coulomb.topg_to_phi.topg_min", -1000.0),
# ("basal_yield_stress.mohr_coulomb.topg_to_phi.topg_max", 1000.0),

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
length = 450
grid_id = "initmip4km"
boostrapping=False
# steps = ["smoothing_nomass","full_physics"]
# steps = ["smoothing_nomass"]
steps = ["full_physics"]

experiment = "picobw_052_"+grid_id+"_testing_tillphi"
grid = grids.grids[grid_id]

bootstrapfile = os.path.join(input_data_dir,
                      "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc")
# infile = "no_mass.nc"

infile = os.path.join(working_dir,"picobw_050_initmip4km_testing1",
                      "no_mass_tillphi.nc")

# infile = bootstrapfile

atmfile = "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc"
ocean_opts = "-ocean pico -ocean_pico_file $oceanfile"

# ocean_data_dir = ""
oceanfile = os.path.join(ocn_data_dir,"schmidtko_"+grid_id+"_means.nc")

ocean_data_dir = "/p/tmp/mengel/pycmip5/p003_testing"
# earlier settings overwritten by iterables
its = ["CSIRO-Mk3-6-0_historical+rcp85","GFDL-CM3_historical+rcp85","IPSL-CM5A-LR_historical+rcp85"]

iterables = {}
iterables["oceanfile"] = { k : os.path.join(ocean_data_dir,
    "thetao_Omon_"+k+"_r1i1p1/schmidtko_anomaly/thetao_Omon_"+k+"_r1i1p1_"+grid_id+"_100km.nc")
    for k in its}

param_iterables = {}
# param_iterables["ocean.pico.overturning_coefficent"] = [1e5,2e5,5e5]
# param_iterables["ocean.pico.heat_exchange_coefficent"] = [5e-6,1e-5,5e-5]

iterables["oceanfile"].update({"base":oceanfile})

# no edits below this line needed.
project_root = os.path.dirname(os.path.abspath(__file__))
user = pwd.getpwuid(os.getuid()).pw_name



