from operator import mod
from pyDatalog.pyDatalog import *

create_terms('fib, X, Y, is_even, mod')
fib[X] = fib[X-1] + fib[X-2]
fib[1] = 1
fib[2] = 2

is_even(X) <= (mod(X, 2) == 0)


