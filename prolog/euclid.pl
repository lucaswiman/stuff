evaluated_gcd(A, B, Div) :-
  A < B -> gcd(B, A, Div)
  ; 0 is B -> Div is A
  ; Diff is A mod B, evaluated_gcd(Diff, B, Div)
.

gcd(A, B, Div) :-
  EvalA is A, EvalB is B, evaluated_gcd(EvalA, EvalB, Div)
.

lcm(A, B, LCM) :-
  gcd(A, B, Div),
  LCM is A * B / Div
.
