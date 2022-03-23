% If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
%
% Find the sum of all the multiples of 3 or 5 below 1000.

applicable(N) :- 0 is N mod 3; 0 is N mod 5.

inc(N, Inc) :-
  (not(applicable(N)), Inc is 0);
  (applicable(N), Inc is N)
.

problem1(N, Solution) :-
  N > 0,
  inc(N, Inc),
  problem1(N-1, LastSolution),
  Solution is LastSolution + Inc,
  !
.

problem1(N, 0) :- N < 1.

% [problem1]. problem1(999, Solution).
:- initialization problem1(999, Solution), writeln(Solution), halt.
