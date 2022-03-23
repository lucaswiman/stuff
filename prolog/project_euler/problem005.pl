:- [euclid].

% 2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
%
% What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

lcm_list([], 1).
lcm_list([X|Xs], LCM) :-
  lcm_list(Xs, LCM1),
  lcm(X, LCM1, LCM)
.

solve :-
  numlist(1, 20, List),
  lcm_list(List, LCM),
  writeln(LCM)
.
