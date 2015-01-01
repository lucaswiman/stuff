:- dynamic
  consecutive_primes/2,
  is_prime/1
.

first_nontrivial_divisor(K, Div, Test) :-
  Test * Test > K -> false;
  0 is K mod Test -> Div is Test;
  consecutive_primes(Test, Next), first_nontrivial_divisor(K, Div, Next)
.

is_prime(K) :- 
  not(first_nontrivial_divisor(K, _, 2)),
  X is K,
  asserta(is_prime(X))
.

consecutive_primes_helper(Prime1, Prime2, Test) :-
  2 is Prime1 -> Prime2 is 3;
  is_prime(Test) -> Prime2 is Test, asserta(consecutive_primes(Prime1, Prime2) :- !);
  Next is Test + 2, consecutive_primes_helper(Prime1, Prime2, Next)
.

consecutive_primes(Prime1, Prime2) :-
  consecutive_primes_helper(Prime1, Prime2, Prime1 + 2)
.

primes_list_helper(X, Primes) :-
  freeze(Primes, (
      Primes=[Y|NextPrimes],
      consecutive_primes(X, Y),
      primes_list_helper(Y, NextPrimes)
    )
  )
.

primes_list([2|Primes]) :-
  primes_list_helper(2, Primes)
.
