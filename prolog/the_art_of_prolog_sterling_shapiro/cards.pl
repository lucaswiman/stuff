:- use_module(library(clpfd)).

is_card([Value, Suite]) :-
  between(1, 13, Value),
  between(1, 4, Suite)
.

hand(Cards) :-
  length(Cards, 5),
  maplist(is_card, Cards),
  sort(Cards, Cards)
.

value_groups([V1, S1], [1, V1, [[V1, S1]]]).
value_groups([[V1, S1], [V1, S2]|Xs], )

:- begin_tests(is_card).
  test(is_card) :-
    findall(X, is_card(X), Deck),
    length(Deck, 52)  % A deck should have 52 cards
  .
:- end_tests(is_card).

:- begin_tests(hand).
  test(hand) :- hand([[1,2], [2,2], [3,2], [4,2], [5,2]]).
:- end_tests(hand).