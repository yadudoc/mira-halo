#!/bin/bash

declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")

DATA=(368005.error  368007.error  368006.error  368008.error  368009.error  368010.error  368011.error  368012.error  370055.error  370054.error)
DATA=(376884.error)
for d in ${DATA[*]}
do
    grep "for" $d > $d.data
    errfile="$d.data"
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


