#!/bin/bash

#MAPPINGS=(linear_mapping.txt  random1_mapping.txt  random2_mapping.txt  random3_mapping.txt  regular_mapping.txt  reversed_mapping.txt)
#MAPPINGS=(random1_mapping.txt  random2_mapping.txt  random3_mapping.txt)
MAPPINGS=(linear_mapping.txt  random1_mapping.txt  random2_mapping.txt  regular_mapping.txt  reversed_mapping.txt  skewed1_mapping.txt  skewed2_mapping.txt  sliced_mappings.txt)
MAPPINGS=(best_mapping.txt)
for map in ${MAPPINGS[*]}
do
    echo "   qsub cobalt_script.sh $map"  >> qsub.log
    qsub cobalt_script.sh $map           &>> qsub.log
done
