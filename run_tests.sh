#!/bin/bash

NCORES=4
TIME=30
EXEC=$PWD/mmps
MAP_FILE=./map_file.txt


RUN()
{
    NCORES=$1
    TIME=$2
    COUNT=$3
    mkdir -p TEST_$NCORES
    pushd .
    cd TEST_$NCORES

    for i in $(seq 1 1 $COUNT)
    do
	echo "qsub -n $NCORES -t $TIME $EXEC"
        qsub -n $NCORES -t $TIME $EXEC
    done
    popd 
}


#RUN 2 30 5
#RUN 4 30 5
#RUN 8 30 5
#RUN 16 30 5
RUN 32 30 5





