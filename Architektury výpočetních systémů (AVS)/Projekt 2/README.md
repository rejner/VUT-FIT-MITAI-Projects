# Zadání

## Paralelizace s OpenMP

Primárním cílem tohoto projektu je vyzkoušet si přechod od sekvenčního k paralelnímu algoritmu a jeho praktickou implementaci a optimalizaci. Druhotným cílem je pak osvojit si metriky používané při hodnocení efektivity paralelních algoritmů. Vaším prvním úkolem bude paralelizace naivního algoritmu pro rekonstrukci polygonálního povrchu ze skalárního pole ve 3D prostoru (tzv. "Marching Cubes") a vyhodnocení vlastností tohoto řešení. Druhým úkolem bude optimalizace tohoto řešení na úrovni algoritmu pomocí hierarchického dělení prostoru (tzv. "Octree") a rychlé eliminace prázdného prostoru.

Veškeré paralelizace budou tvořeny pomocí OpenMP pragma pro vícevláknovou aplikaci se sdílenou pamětí - neboli sekce #pragma omp parallel.

Přístup k překladu a ladění je podobný, jako v prvním projektu. Jen namísto Intel Advisor budete využívat Intel VTune. Projekt lze přeložit a spustit prakticky kdekoliv (vyžaduje CMake a kompilátor), budeme se ale spoléhat na optimalizační reporty poskytované Intel kompilátorem. Referenčním strojem je výpočetní klastr Barbora s kompilátorem Intel (viz A), na jehož výpočetním uzlu provádějte veškerá měření pro tento projekt. K ladění vašeho řešení můžete využít například i počítače v CVT (mimo servery jako je Merlin, protože tam je omezená RAM na 1 GB a nepojede tam VTune) (viz B) nebo vlastní počítač, jestliže si nainstalujete nástroje od Intelu (jsou pro studenty zdarma). Pro prvotní ladění funkcionality algoritmu je možné využít i překladač GCC.

#### Získáno bodů: 20/20