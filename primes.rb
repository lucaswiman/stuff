require 'set'

class Primes
  attr_accessor :primes, :prime_set, :cur_n
  def initialize
    @primes = [2, 3]
    @prime_set = Set.new(@primes)
    @cur_n = 5
  end

  def prime?(n)
    if @prime_set.include? n
      return true
    end
    sqrt = Math.sqrt(n)
    primes_iter do |prime|
      if prime > sqrt
        break
      end
      return false if n % prime == 0
    end
    return true
  end

  def primes_iter
    i = 0
    while true
      yield next_prime(i)
      i += 1
    end 
  end

  def next_prime(i)
    if i < @primes.length
      return @primes[i]
    else
      while !prime? @cur_n
        @cur_n += 2
      end
      @primes << @cur_n
      @prime_set << @cur_n
      @cur_n += 2
      return @primes[-1]
    end
  end

  def factorize(n)
    factors = [1]
    primes_iter do |prime|
      return factors if n == 1
      while n % prime == 0
        factors << prime
        n /= prime
      end
    end
  end

  def max_prime_factor(n)
    return factorize(n).max
  end

  def nth_prime(n)
    i = 1
    primes_iter do |prime|
      return prime if i == n
      i += 1
    end
  end

  def num_divisors(n)
    factors = factorize(n) - [1]
    return factors.counts.values.map {|prime_pow| prime_pow + 1}.product
  end

  def divisors(n)
    factors = factorize(n) - [1, n]
    divisors = Set.new [1]
    factors.counts.each_pair do |p, pow|
      (1..pow).each do |cur_pow|
        divisors.merge(divisors.map {|d| d * p })
      end
    end
    return divisors.to_a.sort!
  end

  def proper_divisors(n)
    return divisors(n) - [n]
  end

  def amicable?(n)
    divisor_sum = proper_divisors(n).sum
    return divisor_sum != n && proper_divisors(divisor_sum).sum == n
  end
end

