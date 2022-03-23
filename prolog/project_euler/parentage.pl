#!/usr/bin/env swipl

% https://stackoverflow.com/questions/58867730/how-do-i-run-a-prolog-file-from-the-command-line-and-not-drop-to-the-repl/71594571#71594571
parent(pam,bob).
parent(tom,bob).
parent(tom,liz).
parent(bob,ann).
parent(bob,pat).
parent(pat,jim).
:- initialization parent(X,jim), writeln(X), halt.
