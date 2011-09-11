require 'open-uri'
require 'linguistics'

require './primes'
require './fib'
require './eulerlib'
require './pythagoras'
require './grid'
require './triangle'
require './collatz'

P = Primes.new

def problem21(n=10000)
  (2...n).select(&P.method(:amicable?)).sum
end
# puts problem21


def problem22(url="http://projecteuler.net/project/names.txt")
  names = open(url).
    read.split(',').sort.
    map(&:letter_sum).
    enum_for(:each_with_index).
    map {|letter_sum, idx| letter_sum * (idx + 1) }.sum
end
# puts problem22

