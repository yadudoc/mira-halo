#!/bin/bash
#COBALT -n 512
#COBALT -t 00:30:00
#COBALT -A ExM
#COBALT -q prod-short

MPI_RANKS=512
RANKS_PER_NODE=1
DIR=/home/yadunand/mira-halo/TEST_MAPPING_512_DATA

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_4
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_4
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_4
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_4
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_4
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_4
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_4
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_4
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_4
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_4
echo "done odd     ====================================================================="

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps
echo "done odd     ====================================================================="

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_10240
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_10240
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_10240
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_10240
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_10240
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_10240
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_10240
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_10240
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_10240
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_10240
echo "done odd     ====================================================================="