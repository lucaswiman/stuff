#!/usr/bin/env problog explain
% https://www.math.hmc.edu/funfacts/ffiles/30002.6.shtml
% Suppose that you are worried that you might have a rare disease. You decide to get tested, and suppose that the testing methods for this disease are correct 99 percent of the time (in other words, if you have the disease, it shows that you do with 99 percent probability, and if you don't have the disease, it shows that you do not with 99 percent probability). Suppose this disease is actually quite rare, occurring randomly in the general population in only one of every 10,000 people.

% 0.99::edge(has_disease, tested_positive); 0.01::edge(has_disease, tested_negative).
% 0.01::edge(healthy, tested_positive); 0.99::edge(has_disease, tested_negative).
% path(X,Y) :- edge(X,Y).
% path(X,Y) :- edge(X,Z),
%              Y \== Z,
%          path(Z,Y).
%
% path(person, tested_positive).
% 1e-4::edge(person, has_disease); (1.0 - 1e-4)::edge(person, healthy).
%
% query(edge(person, has_disease)).


1e-4::has_disease(_).
tested_positive(Person) :- 0.99::has_disease(Person); 0.01::\+has_disease(Person).

tested_positive(john).
query(has_disease(john)).