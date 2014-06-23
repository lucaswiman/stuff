from itertools import chain
from pyDatalog.pyDatalog import *

create_terms('X, Y, mod, prob1')
mod[X, Y] = mod[X - Y, Y]
(mod[X, Y] == X) <= (X < Y)

prob1(X) <= (0 == mod[X, 3] * mod[X, 5])

print sum(chain(*(X.in_(range(1000)) & prob1(X))))

# Or in plain python
print sum(x for x in range(1000) if x % 3 == 0 or x % 5 == 0)
