#!/bin/bash
#COBALT -n 512
#COBALT -t 00:59:00
#COBALT -A ExM
#COBALT -q prod-short

DIR=/home/yadunand/mira-halo/TEST_RPN_2_NODE_512

mmps_array=("mmps_5D_1" "mmps_5D_2" "mmps_5D_4" "mmps_5D_8" "mmps_5D_16" "mmps_5D_32" "mmps_5D_64" "mmps_5D_128" \
    "mmps_5D_256" "mmps_5D_512" "mmps_5D_1024" "mmps_5D_2048" "mmps_5D_4096" "mmps_5D_8192" "mmps_5D_10240" "mmps_5D_16384" \
    "mmps_5D_24576" "mmps_5D_32768" "mmps_5D_65536" "mmps_5D_131072" "mmps_5D_262144" "mmps_5D_524288" "mmps_5D_1048576" \
    "mmps_5D_2097152" "mmps_5D_4194304" "mmps_5D_8388608")

#mmps_array("mmps_5D_1" "mmps_5D_2")

for i in ${mmps_array[*]}
do
    
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/regular_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/regular_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/regular_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/regular_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/regular_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/odd_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/odd_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/odd_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/odd_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/odd_map.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/max_dist.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/max_dist.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/max_dist.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/max_dist.txt : $i
    runjob --cwd $DIR --block $COBALT_PARTNAME --np 1024 -p 2 --mapping $DIR/max_dist.txt : $i
    echo "done regular ======================================================================================="

done



#runjob --cwd $DIR --block $COBALT_PARTNAME --np $MPI_RANKS -p $RANKS_PER_NODE --mapping $DIR/regular_map.txt : mmps_4
#echo "done regular ====================================================================="