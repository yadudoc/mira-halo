#!/bin/bash
#COBALT -n 512
#COBALT -t 00:30:00
#COBALT -A ExM
#COBALT -q prod-short

MPI_RANKS=512
RANKS_PER_NODE=1
CWD=/home/yadunand/mira-halo/TEST_MAPPING_512

runjob --cwd $CWD --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping /home/yadunand/mira-halo/TEST_MAPPING_512/regular_map.txt : mmps
echo "done regular ====================================================================="
runjob --cwd $CWD --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping /home/yadunand/mira-halo/TEST_MAPPING_512/odd_map.txt : mmps
echo "done odd     ====================================================================="