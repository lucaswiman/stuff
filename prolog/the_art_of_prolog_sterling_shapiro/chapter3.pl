% Section 3.3.1 Exercises

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (i) write a program for substitute(X,Y,L1,L2) where L2 is the result of
%     substituting Y for all occurrances of X in L1.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
substitute(_, _, [], []) :- !.
substitute(X, Y, [X|L1], [Y|L2]) :-
  substitute(X, Y, L1, L2),
  !
.

substitute(X, Y, [Z|L1], [Z|L2]) :-
  X \= Z,
  substitute(X, Y, L1, L2)
.
:- begin_tests(substitute).
test(substitute) :-
  substitute(1, 2, [1, 1, 3], [2, 2, 3])
.
test(substitute) :-
  substitute(1, 2, [], [])
.
:- end_tests(substitute).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (ii) What is the meaning of the variant of select:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
select_(X, [X|Xs], Xs).
select_(X, [Y|Ys], [Y|Zs]) :- X \= Y, select_(X, Ys, Zs).

% Answer: select(X, Y, Z) is true iff Z is the remainder of Y after the first occurrence of X.

:- begin_tests(select_).

  test(select_) :- select_(2, [2, 3], [3]), !.

  % \+/1 is the "cannot be proven" predicate.
  % "(mnemonic: + refers to provable and the backslash (\) is normally used to indicate negation in Prolog)."
  test(select_) :- \+(select_(2, [2, 3], [4])).

:- end_tests(select_).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (iii) Write a program for no_doubles(L1, L2) where L2 is the result of
%       removing all duplciate elements from L1,
%       e.g. no_doubles([a,b,c,b], [a,c,b]) (Hint: use member).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

no_doubles([], []).
no_doubles([X|Xs], [X|Ys]) :-
  \+(member(X, Xs)),
  no_doubles(Xs, Ys),
  !
.
no_doubles([X|Xs], Ys) :-
  member(X, Xs),
  no_doubles(Xs, Ys)
.

:- begin_tests(no_doubles).
  test(no_doubles) :- no_doubles([a,b,c,b], [a,c,b]).
  test(no_doubles) :- no_doubles([a,a], [a]).
:- end_tests(no_doubles).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (iv) write programs for even_permutations(Xs, Ys) and odd_permutations(Xs, Ys)
% that find Ys, the even and odd permutations of a list Xs. for example,
% even_permutations([1,2,3], [2,3,1]) and odd_permutations([1,2,3], [2,1,3]) are true.

% :- begin_tests(even_permutations).
% test(even_permutations) :-
%   even_permutations([1,2,3], [2,3,1])
% .
% :- end_tests(even_permutations).
% :- begin_tests(odd_permutations).
%   odd_permutations([1,2,3], [2,1,3]).
% :- end_tests(odd_permutations).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (v) write a program for merge_sort.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

merge_partition(_, [], [], []).
merge_partition(Split, [Y|Ys], LessEqual, Greater) :-
  ((Split >= Y) ->
    LessEqual = [Y|LessEquals],
    merge_partition(Split, Ys, LessEquals, Greater));
  ((Split < Y) ->
    Greater = [Y|Greaters],
    merge_partition(Split, Ys, LessEqual, Greaters)),
  !
.

merge_sort([], []).
merge_sort([X|Xs], Y) :-
  merge_partition(X, Xs, LessEqual, Greater),
  append(LessEqual, [X|Greater], Y)
.

:- begin_tests(merge_partition).
  test(merge_partition) :- merge_partition(1, [1,2], [1], [2]).
  test(merge_partition) :- merge_partition(1, [0,2, 2], [0], [2, 2]).
:- end_tests(merge_partition).

:- begin_tests(merge_sort).
  test(merge_sort) :- merge_sort([2,1,3], [1,2,3]).
:- end_tests(merge_sort).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (vi) Write a logic program for kth_largest(Xs, K) that implements the linear
% algorithm for finding the kth largest element K of a list Xs. The algorithm
% has the following steps:
% - Break the list into groups of five elements.
% - Efficiently find th median of each of the groups, which can be done with a
%   fixed number of comparisons.
% - Parition the original list iwth respect to the median of medians.
% - Recursively find the kth largest element in the appropriate smaller list.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (vii) Write a program for the relation better_poker_hand(Hand1, Hand2, Hand)
%       that succeeds if Hand is the better poker hand between Hand1 and Hand2.
%       For those unfamiliar with this card game, here are some rules of poker
%       necessary for answering this exercise:
%       (a) The order of cards is 2,3,4,5,6,7,8,9,J,Q,K,A.
%       (b) Each hand consists of five cards.
%       (c) The rank of hands in ascending order is:
%           no pairs < one par < two pairs < three of a kind < flush < straight < full house < four of a kind < straight flush
%       (d) Where two cards have the same rank, the higher denomination wins,
%           for example, a pair of kings beats a pair of 7s.
%
%       Hints: ...
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


not(index_of(_, [], 0)).
index_of(Y, [X|Xs], Index) :-
  Y = X -> Index is 0;
  Y \= X -> (index_of(Y, Xs, Z), Index is Z+1)
.

card_values(Values) :- Values = [2, 3, 4, 5, 6, 7, 8, 9, 10, jack, queen, king, ace].
card_suites(Suites) :- Suites = [hearts, diamonds, clubs, spades].

card(Value, Suite) :-
  card_values(Values),
  card_suites(Suites),
  member(Value, Values),
  member(Suite, Suites)
.

suite(card(_, Suite), Suite).
card_value(card(Value, _), Value).

is_card(card(Suite, Value)) :- card(Suite, Value), !.
hand(Cards) :-
  length(Cards, 5),
  no_doubles(Cards, Cards),
  maplist(is_card, Cards)
.

% :- use_module(library(lists)).
flush(Cards) :-
  hand(Cards),
  maplist(suite, Cards, Suites),
  list_to_set(Suites, DistinctSuites),
  length(DistinctSuites, 1)
.

straight(Cards) :-
  hand(Cards),
  maplist(card_index, Cards, Indices),
  list_to_set(Indices, DistinctIndices),
  length(DistinctIndices, 5),
  min_list(Indices, Min),
  max_list(Indices, Max),
  4 is Max - Min
.

card_index(card(Value, _), Index) :-
  card_values(Values),
  index_of(Value, Values, Index),
  !
.

worse_card(Card1, Card2) :-
  card_index(Card1, Index1),
  card_index(Card2, Index2),
  Index1 < Index2
.
better_card(Card1, Card2) :- \+(worse_card(Card1, Card2)).

:- begin_tests(card).
  test(card) :- card(2, hearts), !.
  test(card) :- \+(card(1, hearts)).
  test(card) :- \+(card(2, something)).
  test(card) :-
    findall(card(X, Y), card(X, Y), Deck),
    length(Deck, 52)  % A deck should have 52 cards
  .
  test(card) :- \+(is_card(card(1, something))).
:- end_tests(card).

:- begin_tests(worse_card).
  test(worse_card) :- \+(worse_card(card(3, hearts), card(2, spades))).
  test(worse_card) :- worse_card(card(2, spades), card(3, hearts)).
  test(worse_card) :- worse_card(card(3, hearts), card(jack, spades)).
:- end_tests(worse_card).

:- begin_tests(better_card).
  test(better_card) :- \+(better_card(card(2, spades), card(3, hearts))).
  test(better_card) :- better_card(card(3, hearts), card(2, spades)).
  test(better_card) :- better_card(card(jack, spades), card(3, hearts)).
:- end_tests(better_card).

% :- begin_tests(hand).
%   test(hand) :-
% :- end_tests(hand).

:- begin_tests(flush).
  test(flush) :- flush([card(2, clubs), card(3, clubs), card(4, clubs), card(5, clubs), card(6, clubs)]).
  test(flush) :- \+(flush([card(2, hearts), card(3, clubs), card(4, clubs), card(5, clubs), card(6, hearts)])).
:- end_tests(flush).
:- begin_tests(straight).
  test(straight) :- straight([card(2, clubs), card(3, clubs), card(4, clubs), card(5, clubs), card(6, clubs)]).
  test(straight) :- \+(straight([card(2, clubs), card(3, clubs), card(4, clubs), card(5, clubs), card(5, hearts)])).
  test(straight) :- \+(straight([card(2, clubs), card(3, clubs), card(4, clubs), card(5, clubs), card(7, hearts)])).
:- end_tests(straight).

% :- begin_tests(better_hand).
% test(better_hand) :-
%   better_hand(
%     [card(2, hearts), card(3, hearts), card(4, hearts), card(5, hearts), card(6, hearts)]
%     [card(3, diamonds), card(4, diamonds), card(5, diamonds), card(6, diamonds), card(7, diamonds)]
%   )
% .
% :- end_tests(better_hand).
