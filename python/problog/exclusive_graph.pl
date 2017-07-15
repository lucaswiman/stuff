0.5::transmitted(fatherX).
0.5::transmitted(fatherY).
% detection_rate = 0.9
1.0-0.9::undetected_deleterious(fatherX).
0.0::observed_deleterious(fatherX).

affected(child) :- passed_deleterious(mother), passed_deleterious(father).
passed_deleterious(father) :- (observed_deleterious(fatherX); undetected_deleterious(fatherX)), transmitted(fatherX).
:- transmitted(fatherX), \+transmitted(fatherY); \+transmitted(fatherX), transmitted(fatherY).

query(passed_deleterious(father)).