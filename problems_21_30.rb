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

def problem23(max_n=28123)
  abundants = (1..max_n).select(&P.method(:abundant?))
  abundant_set = Set.new abundants
  is_abundant_sum = lambda do |k|
    abundants.each do |abundant|
      return false if abundant >= k
      return true if abundant_set.include? (k - abundant)
    end
    return false
  end
  (1..max_n).select {|k| !is_abundant_sum.call(k) }.sum
end

# puts problem23

