#!/bin/bash


#ERRFILES=(362529.error 362530.error 362531.error 362532.error 362533.error 362534.error)

ERRFILES=(362529.error 362533.error 362534.error 363205.error 363206.error 363207.error)

for errfile in ${ERRFILES[*]}
do
    echo -n "$errfile  "
    cat ${errfile%.error}.cobaltlog | grep "qsub" | awk '{print $NF}'
    #grep "-q" ${errfile%.error}.cobaltlog | awk '{print $NF}'
    cat $errfile | grep microseconds | grep for > $errfile.data
    cat $errfile.data | grep "12 at a time no delay" | awk '{sum += $(NF-1)} (NR%50)==0{print sum/50; sum = 0;}'

done