#!/bin/bash

declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")

for i in ("regular_4B.error" "regular_1024.error" "regular_10240.error" "odd_4.error" "odd_1024.error" "odd_10240.error")
do
    cd $i
    echo "$i"
    for search in "${strings[@]}"
    do
	#grep "$search" *error | awk '{print $(NF-1)}'
	echo -n "$search in $i :  "
	grep "$search" *error | awk '{ total += $(NF-1) } END { print total/NR }'
    done
    cd ..
done


