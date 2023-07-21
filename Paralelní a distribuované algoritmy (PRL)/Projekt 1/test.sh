#!/bin/bash
numbers=8
#preklad zdrojaku
mpicc --prefix /usr/local/share/OpenMPI -o oems oems.c
#vyrobeni souboru s random cisly
dd if=/dev/random bs=1 count=$numbers of=numbers > /dev/null 2>&1
#spusteni
mpirun --prefix /usr/local/share/OpenMPI --np 19 --oversubscribe oems
#uklid
rm -f oems numbers