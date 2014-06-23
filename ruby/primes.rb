require 'set'

class Primes
  attr_accessor :primes, :prime_set, :cur_n
  def initialize
    @primes = [2, 3]
    @prime_set = Set.new(@primes)
    @cur_n = 5
  end

  def primes_iter(max=nil)
    i = 0
    while true
      p = next_prime(i)
      yield p
      i += 1
      if max && p >= max
        break
      end
    end 
  end

  def next_prime(i)
    if i < @primes.length
      return @primes[i]
    else
      while !@cur_n.prime?
        @cur_n += 2
      end
      @primes << @cur_n
      @prime_set << @cur_n
      @cur_n += 2
      return @primes[-1]
    end
  end

  def nth_prime(n)
    i = 1
    primes_iter do |prime|
      return prime if i == n
      i += 1
    end
  end

end

class Integer
  Primes = Primes.new

  def prime?
    return false if self < 2
    if Integer::Primes.prime_set.include? self
      return true
    end
    sqrt = Math.sqrt(self)
    Integer::Primes.primes_iter do |prime|
      if prime > sqrt
        break
      end
      return false if self % prime == 0
    end
    return true
  end

  def num_divisors
    nontrivial_factors = factors - [1]
    return nontrivial_factors.counts.values.map {|prime_pow| prime_pow + 1}.product
  end

  def divisors
    proper_factors = self.factors - [1, self]
    divisor_set = Set.new [1]
    factors.counts.each_pair do |p, pow|
      (1..pow).each do |cur_pow|
        divisor_set.merge(divisor_set.map {|d| d * p })
      end
    end
    return divisor_set.to_a.sort!
  end

  def proper_divisors
    return divisors - [self]
  end

  def amicable?
    divisor_sum = proper_divisors.sum
    return divisor_sum != self && divisor_sum.proper_divisors.sum == self
  end

  def abundant?
    return proper_divisors.sum > self
  end

  def factors
    facts = [1]
    n = self
    Integer::Primes.primes_iter do |prime|
      return facts if n == 1
      while n % prime == 0
        facts << prime
        n /= prime
      end
    end
  end
end