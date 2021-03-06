#!/bin/bash

declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")

for i in $(ls mmps*)
do
    echo $i
    for search in "${strings[@]}"
    do
	    #grep "$search" *error | awk '{print $(NF-1)}'
	    echo -n ${i#mmps_5D_} | sed 's/_/,\ /'
        echo -n ", $search, "
	    grep "$search" $i | awk '{ total += $(NF-1) } END { print total/NR }'
    done
done


