lexicographic(<, [], [_|_]) :- !.
lexicographic(=, [], []) :- !.
lexicographic(>, [_|_], []) :- !.
lexicographic(Delta, [X|Xs], [Y|Ys]) :-
  compare(Op, X, Y),
  ((Op = (=) -> lexicographic(Delta, Xs, Ys), !);
   (Op = Delta)
  )
.


:- begin_tests(lexicographic).
  test(lexicographic) :- lexicographic((<), [1], [2]).
  test(lexicographic) :- lexicographic((>), [2], [1]).
  test(lexicographic) :- lexicographic((=), [2], [2]).
  test(lexicographic) :- lexicographic((<), [2], [2,3]).
  test(lexicographic) :- lexicographic((<), [2], [2,3]).
  test(lexicographic) :- lexicographic((<), [], [2,3]).
  test(lexicographic) :- lexicographic((>), [2], []).
  test(lexicographic) :- lexicographic((=), [], []).
:- end_tests(lexicographic).
