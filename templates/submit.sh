#!/bin/bash

#SBATCH --qos=short
#SBATCH --time=0-23:50:00
#SBATCH --job-name=pism
#SBATCH --account=ice
#SBATCH --output=./slurm_out.out
#SBATCH --error=./slurm_error.err
#SBATCH --ntasks=16
#SBATCH --tasks-per-node=16
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=mengel@pik-potsdam.de

runname=`echo $PWD | awk -F/ '{print $NF}'`
outdir=$working_dir/$runname

module purge
module load pism/stable08_srunpetsc

# make the PISM execution script aware that it is on compute nodes.
export PISM_ON_CLUSTER=1

./run_pism.sh $SLURM_NTASKS > $outdir/log/pism.out
