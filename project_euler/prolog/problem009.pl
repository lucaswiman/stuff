% A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
%
% a2 + b2 = c2
% For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.
%
% There exists exactly one Pythagorean triplet for which a + b + c = 1000.
% Find the product abc.

pythagorean_triple_sum(Sum, Pair) :-
  Pair=[A,B],
  between(1, Sum, A),
  between(A, Sum, B),
  C is round(sqrt(A*A + B*B)),
  0 is A*A + B*B - C*C,
  Sum is A + B + C
.

problem9(Sum, Result) :-
  findall(Pair, pythagorean_triple_sum(Sum, Pair), [[A,B]]),
  C is round(sqrt(A*A + B*B)),
  Result is A*B*C,
  writeln([A, B, C]),
  writeln(Result)
.

solve :- problem9(1000, Result), writeln(Result).
