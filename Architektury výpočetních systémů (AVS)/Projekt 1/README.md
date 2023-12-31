# Zadání

## Optimalizace sekvenčního kódu (vektorizace)

Cílem tohoto projektu je zrychlit výpočet tzv. Mandelbrotovy množiny. Její základní výpočet vektorizovatelný téměř není, ovšem šikovným přeskupením smyček a přidáním dalších parametrů je možné dosáhnout rozumného zrychlení. Profilovacím nástrojem bude Intel Advisor.

Projekt lze přeložit a spustit prakticky kdekoliv (vyžaduje CMake a kompilátor), budeme se ale spoléhat na optimalizační reporty poskytované Intel kompilátorem. Je žádoucí, aby cílový procesor disponoval podporou vektorového rozšíření AVX2. Referenčním strojem je výpočetní klastr Barbora s kompilátorem Intel (viz A), na jehož výpočetním uzlu provádějte všechna měření pro tento projekt. Kladení vašeho řešení můžete využít například i počítače v CVT (mimo serverů jako je Merlin, protože tam je omezená RAM na 1 GB) (viz B) nebo vlastní počítač, jestliže si nainstalujete nástroje od Intelu (jsou pro studenty zdarma). Pro první ladění funkcionality algoritmu je možné využít i překladač GCC.

#### Získáno bodů: 10/10