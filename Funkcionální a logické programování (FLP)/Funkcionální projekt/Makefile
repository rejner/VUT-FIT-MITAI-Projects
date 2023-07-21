# Project:      FLP Project 1 - simplify-bkg
# Author:       Michal Rein (xreinm00)
# Date:         01.04.2022
# File:         Makefile
# Description:  Standard makefile
# Usage:		make [ clean | tests | zip ]

EXECUTABLE = flp21-fun
SOURCE = simplify-bkg.hs arguments.hs grammar.hs
SOURCE_DIR = src
ZIP_FILE = flp-fun-xreinm00.zip
FLAGS = -Wall

# Compile project
default: clean
	ghc $(FLAGS) $(SOURCE_DIR)/*.hs -o ${EXECUTABLE}

# Create zip file with project
zip:
	zip ${ZIP_FILE} ${SOURCE_DIR}/* doc/* test/* Makefile

# Clean folders from trash files
clean:
	rm -f $(EXECUTABLE)
	rm -f $(SOURCE_DIR)/*.hi $(SOURCE_DIR)/*.o
	rm -f $(ZIP_FILE)
	rm -f test/*.out

# Generate and run tests.
tests:
	./test/test.sh test $(EXECUTABLE)

