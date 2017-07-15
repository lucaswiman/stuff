
% (detection_rate = 0.9)
1.0-0.9::deleterious(Parent, Chromosome).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Facts
observed_deleterious_count(mother, 2).
observed_deleterious_count(father, 1).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

deleterious(mother, chr_X1) :- observed_deleterious_count(mother, Count), Count >= 1.
deleterious(mother, chr_X2) :- observed_deleterious_count(mother, Count), Count >= 2.
deleterious(father, chr_X) :- observed_deleterious_count(father, Count), Count >= 1.

affected :- passed_deleterious(mother), transmitted(father, chr_Y); passed_deleterious(mother), passed_deleterious(father).
passed_deleterious(father) :- deleterious(father, chr_X), transmitted(father, chr_X).
passed_deleterious(mother) :- deleterious(mother, chr_X1), transmitted(mother, chr_X1); deleterious(mother, chr_X2), transmitted(mother, chr_X2).
:- transmitted(father, chr_X), \+transmitted(father, chr_Y); \+transmitted(father, chr_X), transmitted(father, chr_Y).
:- transmitted(mother, chr_X1), \+transmitted(mother, chr_X2); \+transmitted(mother, chr_X1), transmitted(mother, chr_X2).

0.5::transmitted(father, chr_X).
0.5::transmitted(father, chr_Y).
0.5::transmitted(mother, chr_X1).
0.5::transmitted(father, chr_X2).


query(passed_deleterious(father)).
query(passed_deleterious(mother)).
query(affected).  % Should be 100%, not 0.375
