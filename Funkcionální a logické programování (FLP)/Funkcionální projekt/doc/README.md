# FLP - Projekt 1: simplify-bkg

#### Autor: &nbsp; &nbsp; &nbsp;    Michal Rein (xreinm00)
#### Email: &nbsp; &nbsp; &nbsp;    xreinm00@stud.fit.vutbr.cz
#### Datum: &nbsp; &nbsp;           02.04.2022

## Struktura projektu:

```
flp-fun-xreinm00
│   
|   Makefile
│
└───doc
│   │   README.md
│   
└───src
│   │   arguments.hs      -- modul pro zpracování argumentů
│   │   grammar.hs        -- modul pro zpracování gramatiky
│   |   simplify-bkg.hs   -- main programu
│   
└───test
    │   test.sh           -- skript pro spuštění testů
    │   test-XY.in        -- testovací vstupní soubor
    |   test-XY-1         -- referenční výstup po 1. kroku algoritmu
    |   test-XY-2         -- referenční výstup po 2. kroku algoritmu

```

## Spuštění a překlad

Program lze přeložit pomocí přiloženého souboru Makefile a příkazu make:

    make


Samotný program je spustitelný v kořenovém adresáři tohoto projektu:

    ./flp21-fun [-i|-1|-2|-h] <INPUT>

    Argumenty:
    -h: vypíše nápovědu na stdout.

    -i: vypíše se pouze načtená a do vnitřní reprezentace převedená BKG na stdout.

    -1: vypíše se BKG G¯ (po prvním kroku algoritmu 4.3 z opory TIN) na stdout.

    -2: na stdout se vypíše BKG, která generuje stejný jazyk jako vstupní gramatika, ale neobsahuje žádné zbytečné symboly.

    <INPUT>: je jméno vstupního souboru (pokud není specifikováno, program čte standardní vstup) obsahujícího BKG.

Program reaguje na chybnou cestu ke vstupnímu souboru chybovou hláškou. Neznámé argumenty rovněž způsobí přerušení vykonávání programu.

## Testy

K programu jsou přiloženy testy v adresáři test.
Testovací skript *test/test.sh* lze buď spustit přímo: 

    ./test.sh <TEST_DIR> <PATH_TO_EXECUTABLE>

    Argumenty:
    <TEST_DIR>: adresář obsahující testy
    <PATH_TO_EXECUTABLE>: cesta k binárnímu spustitelnému souboru programu
 
 případně k provedení testů v nijak nemodifikovaném projektu lze využít i příkaz:

    make tests

## Ostatní

Příkaz na vygenerování výsledného .zip souboru s projektem:

    make zip

Příkaz na vyčištění adresářů od zbytečných souborů (po kompilaci + generování výstupů testů)

    make clean