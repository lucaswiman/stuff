require './primes'
require './fib'
require './eulerlib'
require './pythagoras'
require './grid'
require './triangle'
require './collatz'
require 'linguistics'

P = Primes.new

def problem21(n=10000)
  (2...n).select(&P.method(:amicable?)).sum
end
puts problem21