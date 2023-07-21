#!/bin/bash

# Title:    WAP - Project 1 - Script for running tests
# Author:   Michal Rein (xreinm00)
# E-mail:   xreinm00@stud.fit.vutbr.cz
# Date:     27.02.2022

# Parameters:
#   install : install dependencies for Jest framework
#   (if none or illegal parameters are given, run tests)

if [ "$1" == "install" ]; then
        echo "Installing Jest dependencies..."
        npm install jest --save-dev
    else
        npm test
fi

