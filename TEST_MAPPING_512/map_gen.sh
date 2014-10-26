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
	for D in $(seq 0 1 $(($DIM_D-1)) )
	do
	    for C in $(seq 0 1 $(($DIM_C-1)) )
	    do
		for B in $(seq 0 1 $(($DIM_B-1)) )
		do
		    for A in $(seq 0 1 $(($DIM_A-1)) )
		    do
			echo "$A $B $C $D $E $T"
		    done
		done
	    done
	done
    done
done