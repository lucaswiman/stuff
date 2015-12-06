% The prime factors of 13195 are 5, 7, 13 and 29.
%
% What is the largest prime factor of the number 600851475143 ?

remove_factor(N, Factor, Reduced) :-
  0 is N mod Factor -> remove_factor(N / Factor, Factor, Reduced)
  ; Reduced is N
.
largest_odd_prime_factor(N, Div, BiggestFactor) :-
  Next is Div + 2,
  (
    Div * Div > N -> BiggestFactor is N
    ; 0 is N mod Div ->
      writeln([N, Div]),
      remove_factor(N, Div, Reduced),
      (
        (Reduced is 1, BiggestFactor is Div);
        largest_odd_prime_factor(Reduced, Next, BiggestFactor)
      )
    ; largest_odd_prime_factor(N, Next, BiggestFactor)
  )
.

solve :-
  largest_odd_prime_factor(600851475143, 3, BiggestFactor),
  writeln(BiggestFactor)
.
