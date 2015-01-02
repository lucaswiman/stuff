% The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
%
% Find the sum of all the primes below two million.

:- [primes].

prime_sum(Max, Sum, [P|Primes]) :-
  P > Max -> Sum is 0
  ; prime_sum(Max, SubSum, Primes), Sum is SubSum + P
.

% primes_list(Primes), prime_sum(10, Sum, Primes).
% primes_list(Primes), prime_sum(2000000, Sum, Primes).
