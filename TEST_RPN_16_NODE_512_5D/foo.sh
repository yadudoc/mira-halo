#!/bin/bash


for i in $(seq 0 1 3)
do
    for j in $(seq 0 1 3)
    do
        for k in $(seq 0 1 3)
        do
            grep "^$i $j $k" random3_mapping.txt >> random4_mapping.txt
        done
    done
done
