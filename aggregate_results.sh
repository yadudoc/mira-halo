#!/bin/bash

declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")

for i in "TEST_2" "TEST_4" "TEST_8" "TEST_16" "TEST_32" "TEST_64" "TEST_128" "TEST_256" "TEST_512"
#for i in "TEST_MAPPING_512"
do
    cd $i
    #echo "$i"
    for search in "${strings[@]}"
    do
	#grep "$search" *error | awk '{print $(NF-1)}'
	echo -n "$i, $search, "
	grep "$search" *error | awk '{ total += $(NF-1) } END { print total/NR }'
    done
    cd ..
done


