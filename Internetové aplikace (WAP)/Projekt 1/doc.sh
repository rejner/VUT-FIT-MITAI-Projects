#!/bin/bash

# Title:    WAP - Project 1 - Script for generating documentation
# Author:   Michal Rein (xreinm00)
# E-mail:   xreinm00@stud.fit.vutbr.cz
# Date:     27.02.2022

jsdoc -v &>/dev/null

# check if jsdoc is installed, install with npm if not
if [ $? != 0 ]; then
    npm install jsdoc
fi

# generate documentation into 'docs' directory from config file
jsdoc -c jsdoc.conf


