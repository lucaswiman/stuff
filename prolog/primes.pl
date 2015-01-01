:- dynamic
  consecutive_primes/2
.

first_nontrivial_odd_divisor(K, Div, Test) :-
  0 is K mod Test -> Div is Test;
  Test * Test > K -> false;
  consecutive_primes(Test, Next), first_nontrivial_odd_divisor(K, Div, Next)
.

is_prime(K) :- 
  K is 2;
  not(0 is K mod 2), not(first_nontrivial_odd_divisor(K, _, 3));
  false
.

consecutive_primes_helper(Prime1, Prime2, Test) :-
  2 is Prime1 -> Prime2 is 3;
  is_prime(Test) -> Prime2 is Test, asserta(consecutive_primes(Prime1, Prime2) :- !);
  Next is Test + 2, consecutive_primes_helper(Prime1, Prime2, Next)
.

consecutive_primes(Prime1, Prime2) :-
  consecutive_primes_helper(Prime1, Prime2, Prime1 + 2)
.
