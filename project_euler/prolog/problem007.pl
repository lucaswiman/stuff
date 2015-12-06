% By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.
%
% What is the 10,001st prime number?

:- [primes].

problem7(Num) :-
  primes_list(Primes),
  nth1(Num, Primes, X),
  writeln(X)
.

solve :- problem7(10001).