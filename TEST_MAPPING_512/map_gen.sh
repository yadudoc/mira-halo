#!/bin/bash

DIM_A=4
DIM_B=4
DIM_C=4
DIM_D=4
DIM_E=4
DIM_T=1

for T in $(seq 0 1 $(($DIM_T-1)) )
do
    for E in $(seq 0 1 $(($DIM_E-1)) )
    do
	echo "$E $T"
    done
    


done