#!/bin/bash

declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")

declare -a files=("regular_4B.error" "odd_4.error" "regular_1024.error"  "odd_1024.error" "regular_10240.error" "odd_10240.error")

for i in ${files[@]}
do
    echo "$i"
    for search in "${strings[@]}"
    do
	#grep "$search" *error | awk '{print $(NF-1)}'
	echo -n "$search in $i :  "
	grep "$search" $i | awk '{ total += $(NF-1) } END { print total/NR }'
    done 
done


