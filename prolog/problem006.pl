% The sum of the squares of the first ten natural numbers is,
% 1**2 + 2**2 + ... + 10**2 = 385
%
% The square of the sum of the first ten natural numbers is,
% (1 + 2 + ... + 10)**2 = 552 = 3025
%
% Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025 − 385 = 2640.
%
% Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

[apply].

square(X, Y) :- Y is X ** 2.

problem6(N, Result) :-
  numlist(1, N, List),
  maplist(square, List, Squared),
  sumlist(Squared, SumOfSquares),
  sumlist(List, Sum),
  Result is Sum **2 - SumOfSquares
.

solve :-
  problem6(100, Result),
  writeln(Result)
.
