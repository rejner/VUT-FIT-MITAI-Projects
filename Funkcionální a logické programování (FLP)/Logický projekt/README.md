# FLP Project 2 - Turing machine simulation (Prolog)
<pre>
Author:     Michal Rein (xreinm00)
Email:      xreinm00@stud.fit.vutbr.cz
Date:       25.04.2022
</pre>

Vaším úkolem je vytvořit simulátor nedeterministického
Turingova stroje. Na vstupu váš program obdrží pravidla pro Turingův stroj a vstupní obsah pásky. Výstupem bude
posloupnost konfigurací stroje.

## Project structure
```
Project_dir
│   README.md
│   Makefile
|   turing.pl <-- source file  
```

## How to run this project
Compile program with Makefile:

        make

Run program:

        ./flp21-log < [input\_file] > [output\_file] 

#### Získáno bodů: 6,5/8
Komentář: Program cyklí i když existuje řešení, problém s prací s prázdnými symboly.