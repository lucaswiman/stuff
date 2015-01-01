
first_nontrivial_odd_divisor(K, Div, Test) :-
  0 is K mod Test -> Div is Test;
  Test * Test > K -> false;
  Next is Test + 2, first_nontrivial_odd_divisor(K, Div, Next)
.

is_prime(K) :- 
  K is 2;
  not(0 is K mod 2), not(first_nontrivial_odd_divisor(K, _, 3));
  false
.
