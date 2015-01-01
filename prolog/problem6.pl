squarelist([], []).
squarelist([X|Xs], [R|Rs]) :- R is X ** 2, squarelist(Xs, Rs).

problem6(N, Result) :-
  numlist(1, N, List),
  squarelist(List, Squares),
  sumlist(List, Sum),
  sumlist(Squares, SquareSum),
  writeln(Squares),
  writeln(SquareSum),
  Result is Sum ** 2 - SquareSum
.
