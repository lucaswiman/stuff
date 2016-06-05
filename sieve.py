"""
Lazy sieve of Eratosthenes, loosely based off https://www.cs.hmc.edu/~oneill/papers/Sieve-JFP.pdf
"""
from __future__ import print_function, division

import itertools as it
from collections import defaultdict

def sieve():
    yield 2
    n_to_divisor_iterators = defaultdict(list)
    for n in it.count(3, step=2):
        divisor_iterators = n_to_divisor_iterators.pop(n, [])
        if not divisor_iterators:
            # n hasn't been sieved by anything, so is prime.
            yield n
            divisor_iterators.append(itertools.count(
                # Start counting at p**2, which is the next multiple not already sieved
                # by some other sieve.
                n ** 2,
                # Step by 2 * p, since we're special-casing evens to speed everything up by 2x.
                step=2 * n))
        for divisor_iterator in divisor_iterators:
            next_composite = next(divisor_iterator)
            n_to_divisor_iterators[next_composite].append(divisor_iterator)


if __name__ == '__main__':
    import math
    for i, p in enumerate(sieve()):
        if i % 5000 == 0:
            # Compare actual prime counts to prime number theorem.
            # The third column should asymptotically approach 1.
            print(i+1, p, ((i+1) / (p / math.log(p))))
