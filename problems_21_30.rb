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

def problem24(lst=[0,1,2,3,4,5,6,7,8,9], size=1000000)
  count = 0
  lst.lexicographic_permutations do |perm|
    count += 1
    if count == size
      return perm.join('')
    end
  end
end

# puts problem24

def problem25(digits=1000)
  i = 0
  while true
    i += 1
    return i + 1 if Fib.fib(i).to_s.length >= digits
  end
end

# puts problem25

