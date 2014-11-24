#!/bin/bash


#ERRFILES=(362529.error 362530.error 362531.error 362532.error 362533.error 362534.error)

ERRFILES=(362529.error 362533.error 362534.error 363205.error 363206.error 363207.error)
declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")

echo "" > results.csv
for i in ${ERRFILES[*]}
do
    echo $i
    for search in "${strings[@]}"
    do
        MAPPING_FILE=$(cat ${i%.error}.cobaltlog | grep "qsub" | awk '{print $NF}')
        FOO=${MAPPING_FILE%.txt}
	    #grep "$search" *error | awk '{print $(NF-1)}'
	    prefix="$FOO, $search, "
	    grep "$search" $i | awk '{print $(NF-1)}' | sed -e "s/^/$prefix/" >> results.csv
    done
done

exit

for errfile in ${ERRFILES[*]}
do
    echo  "$errfile  "
    MAPPING_FILE=$(cat ${errfile%.error}.cobaltlog | grep "qsub" | awk '{print $NF}')
    FOO=${MAPPING_FILE%.txt}
    #grep "-q" ${errfile%.error}.cobaltlog | awk '{print $NF}'
    cat $errfile | grep microseconds | grep for | sed 's/\ for.*pclks\,\   /, /' | sed -e "s/^/$FOO, /" > $FOO.csv
    #cat $errfile.data | grep "12 at a time no delay" | awk '{sum += $(NF-1)} (NR%50)==0{print sum/50; sum = 0;}'

done
