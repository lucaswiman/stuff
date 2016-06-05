# -*- coding: utf-8 -*-
# Grammar for Datalog. Based off the BNF grammar from
# http://docs.racket-lang.org/datalog/datalog.html
# The original BNF is reproduced below:
#
#
# ‹program› ::= ‹statement›*
#
# ‹statement› ::= ‹assertion› | ‹retraction› | ‹query›
#
# ‹assertion› ::= ‹clause› .
#
# ‹retraction› ::= ‹clause› ~
#
# ‹query› ::= ‹literal› ?
#
# ‹clause›::= ‹literal› :- ‹body› | ‹literal›
#
# ‹body› ::= ‹literal› , ‹body› | ‹literal›
#
# ‹literal› ::= ‹predicate-sym› ( ) | ‹predicate-sym› ( ‹terms› ) | ‹predicate-sym› | ‹term› = ‹term› | ‹term› != ‹term›
#
# ‹predicate-sym› ::= ‹IDENTIFIER› | ‹STRING›
#
# ‹terms› ::= ‹term› | ‹term› , ‹terms›
#
# ‹term› ::= ‹VARIABLE› | ‹constant›
#
# ‹constant› ::= ‹IDENTIFIER› | ‹STRING›
