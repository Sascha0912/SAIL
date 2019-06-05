#!/bin/sh
#PBS -N OpenFOAM_caseRunner
#PBS -q hpc1
#PBS -l nodes=1:ppn=32
#PBS -l walltime=72:00:00
#PBS -l vmem=180gb

# Necessary to pseudo-revert to old memory allocation behaviour
export MALLOC_ARENA_MAX=4

# Run experiment
cd $path
./Allclean && ./caseRunner.sh
