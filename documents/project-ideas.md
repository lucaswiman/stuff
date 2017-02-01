### Generate examples from `parsimonious` grammars
References:
- [Issue to implement in `revex`](https://github.com/lucaswiman/revex/issues/5)
- ["Detecting Ambiguity in Programming Language Grammars"](http://soft-dev.org/pubs/pdf/vasudevan_tratt__detecting_ambiguity_in_programming_language_grammars.pdf).
  Describes using Boltzmann samplers on programming language grammars, then doing a sort of "mutation testing" of the grammars.
- ["A CALCULUS FOR THE RANDOM GENERATION OF COMBINATORIAL STRUCTURES"](http://algo.inria.fr/flajolet/Publications/RR-1830.pdf) Describes a way of constructing combinatorial objects via a "grammar" of simpler combinatorial objects.
- ["Boltzmann Samplers for the Random Generation of Combinatorial Structures"](http://algo.inria.fr/flajolet/Publications/DuFlLoSc04.pdf) A more efficient way of sampling from the above constructions using Boltzmann distributions.

### Python 3 import checker
- flake8-tidy-imports
- Comprehensive list of removed/moved imports https://github.com/lucaswiman/legacy-python-upgrade-guide/blob/master/imports/build_banned_imports.py


### Railroad diagrams for `parsimonious`

https://github.com/erikrose/parsimonious/issues/104
