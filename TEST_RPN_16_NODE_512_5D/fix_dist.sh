#!/bin/bash


rm results.csv
for mapping in $(echo *txt)
do
    avgdist=$(./measure_mapping.py 8192 $mapping 8,8,8,8,2 | grep "Average" | awk '{print $NF}')
    maxdist=$(./measure_mapping.py 8192 $mapping 8,8,8,8,2 | grep "Max" | awk '{print $NF}')
    suffix=", $avgdist, $maxdist"

    cut -d "," -f -3  ${mapping%txt}csv | sed "s/$/$suffix/" >> results.csv
done
