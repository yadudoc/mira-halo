#!/bin/bash

NCORES=4
TIME=30
EXEC=./mmps
MAP_FILE=./map_file.txt


qsub -n $NCORES -t $TIME --env RUNJOB_MAPPING=$MAP_FILE $EXEC