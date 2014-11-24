#!/bin/bash

declare -a strings=("Sendrecv no delay" "Sendrecv wt delay" "Isend-recv no delay" "Isend-recv wt delay" "Isend-Irecv no delay" "Isend-Irecv wt delay" "12 at a time no delay" "12 at a time wt delay")

declare -a files=("regular_4.error" "odd_4.error" "regular_16.error" "odd_16.error" "regular_64.error" "odd_64.error" \
"regular_128.error" "odd_128.error" "regular_256.error" "odd_256.error" "regular_512.error" "odd_512.error" "regular_1024.error" "odd_1024.error"
"regular_10240.error" "odd_10240.error" "regular_102400.error" "odd_102400.error" "regular_1024000.error" "odd_1024000.error" )



for i in ${files[@]}
do
#    echo "$i"
    for search in "${strings[@]}"
    do
	#grep "$search" *error | awk '{print $(NF-1)}'
	echo -n "$i, $search, "
	grep "$search" $i | awk '{ total += $(NF-1) } END { print total/NR }'
    done 
done


