#!/bin/bash


#ERRFILES=(362529.error 362530.error 362531.error 362532.error 362533.error 362534.error)

DATA=(368013.error  368015.error  368014.error  368016.error  368017.error  368018.error  368019.error  368020.error  373058.error  373055.error  373057.error  373054.error  373059.error)
DATA=(368013.error  368014.error  368017.error  368019.error  373058.error  373057.error  373059.error 368015.error  368016.error  368018.error  368020.error  373055.error  373054.error  376883.error)
declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")


for d in ${DATA[*]}
do
    grep "for" $d > $d.data
done

#ERRFILES=(368005.error.data) # 368006.error.data  368007.error.data  368008.error.data  368009.error.data  368010.error.data  368011.error.data  368012.error.data)                           
#ERRFILES=(368005.error.data  368006.error.data  368007.error.data  368008.error.data  368009.error.data  368010.error.data  368011.error.data  368012.error.data)                             
for data in ${DATA[*]}
do
    errfile="$data.data"
    mapping="$(cat ${errfile%.error.data}.cobaltlog | grep "qsub" | awk '{print $NF}')"
    CSV=${mapping%.txt}.csv
    avgdist=$(./measure_mapping.py 8192 $mapping 32,32,8 | grep "Average" | awk '{print $NF}')
    maxdist=$(./measure_mapping.py 8192 $mapping 32,32,8 | grep "Max" | awk '{print $NF}')
    suffix=", $avgdist, $maxdist"
    rm $CSV
    for search in "${strings[@]}"
    do
        FOO="${mapping%.txt}, $search"
        #grep "$search" $errfile | awk '{sum += $(NF-1)} (NR%50)==0{print sum/50; sum = 0;}' | sed -e "s/^/$FOO,\ /" | sed -e "s/$/$suffix/" >> $CSV                                           
        grep "$search" $errfile | awk '{print $(NF-1)}' | sed -e "s/^/$FOO,\ /" | sed -e "s/$/$suffix/" >> $CSV
    done
done