#!/bin/bash
#COBALT -n 512
#COBALT -t 00:30:00
#COBALT -A ExM
#COBALT -q prod-short

MPI_RANKS=512
RANKS_PER_NODE=1
DIR=/home/yadunand/mira-halo/TEST_MAPPING_512_DATA

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_16
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_16
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_16
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_16
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_16
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_16
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_16
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_16
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_16
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_16
echo "done odd     ====================================================================="

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_64
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_64
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_64
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_64
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_64
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_64
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_64
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_64
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_64
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_64
echo "done odd     ====================================================================="

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_128
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_128
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_128
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_128
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_128
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_128
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_128
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_128
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_128
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_128
echo "done odd     ====================================================================="

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_256
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_256
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_256
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_256
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_256
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_256
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_256
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_256
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_256
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_256
echo "done odd     ====================================================================="

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_512
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_512
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_512
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_512
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_512
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_512
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_512
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_512
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_512
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_512
echo "done odd     ====================================================================="

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_102400
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_102400
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_102400
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_102400
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_102400
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_102400
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_102400
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_102400
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_102400
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_102400
echo "done odd     ====================================================================="

runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_1024000
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_1024000
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_1024000
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_1024000
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_1024000
echo "done regular ====================================================================="
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_1024000
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_1024000
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_1024000
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_1024000
runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/odd_map.txt : mmps_1024000
echo "done odd     ====================================================================="