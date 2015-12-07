:- use_module(library(clpfd)).

is_card(card(Value, Suite)) :-
  Value #>= 0, Value #< 12,
  Suite #>= 0, Suite #< 4,
  writeln([Value, Suite])
.

hand(Cards) :-
  sort(Cards, Cards),
  length(Cards, 5),
  maplist(is_card, Cards)
.
