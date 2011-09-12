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

def find_period(s)
  s = s.to_s
  p = 1
  while p < s.length / 2
    if s[0, p] == s[p, p]
      return p
    end
    p += 1
  end
  return -1
end

def problem26(n=1000)
  # HACK assume arbitrarily that 1/i cannot have a period bigger than i (is this true?)
  best = 7
  best_period = 6
  ((best + 1)..n).each do |i|
    period = find_period((10 ** (10 * n)) / i)
    if period > best_period
      best_period = period
      best = i
    end
  end
  return [best, best_period]
end

puts problem26.inspect
