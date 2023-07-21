#!/bin/bash

# Project:      FLP Project 1 - simplify-bkg
# Author:       Michal Rein (xreinm00)
# Date:         01.04.2022
# File:         test/test.sh
# Description:  Script for running basic tests

# USAGE:
# ./test.sh <TEST_DIR> <PATH_TO_EXECUTABLE>

TEST_DIR=$1
EXECUTABLE=$2
TESTS=${1}/test-*.in

PASSED=0
FAILED=0

RED="\033[1;31m"
GREEN="\033[1;32m"
RESET="\033[0m"


echo "Running tests..."
for test_file in $TESTS; do
	basename=${test_file%.*}
    num=${basename##*-}

    output_file=${basename}-i.out
    ./$EXECUTABLE -i $test_file > $output_file
    diff $test_file $output_file > /dev/null
    if [ $? != 0 ]; then
        echo -e "${RED}[FAIL]${RESET}: $test_file and $output_file DIFFER!"
        FAILED=$(($FAILED+1))
    else
        echo -e "${GREEN}[SUCCESS]${RESET}: $test_file and $output_file outputs equal."
        PASSED=$(($PASSED+1))
    fi

    output_file=${basename}-1.out
    ./$EXECUTABLE -1 $basename-1 > $output_file
    diff $basename-1 $output_file > /dev/null
    if [ $? != 0 ]; then
        echo -e "${RED}[FAIL]${RESET}: $basename-1 and $output_file DIFFER!"
        FAILED=$(($FAILED+1))
    else
        echo -e "${GREEN}[SUCCESS]${RESET}: $basename-1 and $output_file outputs equal."
        PASSED=$(($PASSED+1))
    fi

    output_file=${basename}-2.out
    ./$EXECUTABLE -2 $basename-2 > $output_file
    diff $basename-2 $output_file > /dev/null
    if [ $? != 0 ]; then
        echo -e "${RED}[FAIL]${RESET}: $basename-2 and $output_file DIFFER!"
        FAILED=$(($FAILED+1))
    else
        echo -e "${GREEN}[SUCCESS]${RESET}: $basename-2 and $output_file outputs equal."
        PASSED=$(($PASSED+1))
    fi

done

echo ""
echo "--------- Test results -----------"
echo -e "Passed: ${GREEN}${PASSED}x${RESET}"
echo -e "Failed: ${RED}${FAILED}x${RESET}"
