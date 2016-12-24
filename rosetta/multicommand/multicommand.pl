#!/usr/bin/env swipl -f -q

% http://stackoverflow.com/questions/25467090/how-to-run-swi-prolog-from-the-command-line

library(process).  % http://www.swi-prolog.org/pldoc/man?predicate=process_create/3

:- initialization main.

main :-
  current_prolog_flag(argv, Argv),
  format('Hello World, argv:~w\n', [Argv]),
  halt(0)
.
