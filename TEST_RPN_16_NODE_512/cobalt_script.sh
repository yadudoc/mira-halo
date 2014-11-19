#!/bin/bash
#COBALT -n 512
#COBALT -t 01:59:00
#COBALT -A ExM
#COBALT -q prod-short

DIR=/home/yadunand/HALO/mira-halo/TEST_RPN_16_NODE_512
NP=8192
RANKSPERNODE=16
#mmps_array("mmps_5D_1" "mmps_5D_2")
MAPFILE=$1

echo "$MAPFILE"
#DATASIZE=(1 2 4 8 ) # 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 524288 1048576 2097152 4194304 8388608 16777216 33554432 67108864 134217728)
DATASIZE=(1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 524288 1048576 2097152 4194304 8388608 16777216 33554432 67108864 134217728)
for i in ${DATASIZE[*]}
do
    echo "runjob --cwd $DIR --block $COBALT_PARTNAME --np $NP -p $RANKSPERNODE --mapping $DIR/$MAPFILE : mmps $i"
    runjob --cwd $DIR --block $COBALT_PARTNAME --np $NP -p $RANKSPERNODE --mapping $DIR/$MAPFILE : mmps $i
    echo "done regular ======================================================================================="
done



#runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_4
#echo "done regular ====================================================================="
