#!/bin/bash

#  PRL Project 2 - Implementation of order assignment to preorder vertices with Open MPI
#  Author:  Michal Rein (xreinm00)
#  File:    test.sh
#  Desc:    Script for compiling and running the program. Takes 1 parameter
#		    with string representing vertices of binary tree as an array.
#  Date:    22.04.2022


if [ $# -ne 1 ]; then 
    echo "Missing arguments..."
	exit 1;
fi;

tree=$1;
mpic++ pro.cpp -o pro -Wall
# CPU count: (2 * num_of_vertices) - 2
mpirun -np $(((2 * ${#1}) - 2)) --oversubscribe pro $tree #--prefix /usr/local/share/OpenMPI
rm -f pro 	
