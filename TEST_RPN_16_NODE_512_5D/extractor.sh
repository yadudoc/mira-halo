#!/bin/bash

declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")


#ERRFILES=(368005.error.data) # 368006.error.data  368007.error.data  368008.error.data  368009.error.data  368010.error.data  368011.error.data  368012.error.data)
ERRFILES=(368005.error.data  368006.error.data  368007.error.data  368008.error.data  368009.error.data  368010.error.data  368011.error.data  368012.error.data)
for errfile in ${ERRFILES[*]}
do
    mapping="$(cat ${errfile%.error.data}.cobaltlog | grep "qsub" | awk '{print $NF}')"
    CSV=${mapping%.txt}.csv
    avgdist=$(./measure_mapping.py 8192 $mapping 8,8,8,8,2 | grep "Average" | awk '{print $NF}')
    maxdist=$(./measure_mapping.py 8192 $mapping 8,8,8,8,2 | grep "Max" | awk '{print $NF}')
    suffix=", $avgdist, $maxdist"
    rm $CSV
    for search in "${strings[@]}"
    do
        FOO="${mapping%.txt}, $search"
        #grep "$search" $errfile | awk '{sum += $(NF-1)} (NR%50)==0{print sum/50; sum = 0;}' | sed -e "s/^/$FOO,\ /" | sed -e "s/$/$suffix/" >> $CSV
        grep "$search" $errfile | awk '{print $(NF-1)}' | sed -e "s/^/$FOO,\ /" | sed -e "s/$/$suffix/" >> $CSV
    done
done


