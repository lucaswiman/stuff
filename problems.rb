require './primes'
require './fib'
require './eulerlib'

P = Primes.new

def prob1(n)
  return (1...n).select {|i| (i % 3) * (i % 5) == 0  }.sum
end
# puts prob1(1000)

def prob2(max_fib=4000000)
  i = 1
  sum = 0
  while true
    fib = Fib.fib(i)
    if fib < max_fib
      if (fib % 2) == 0
        sum += fib 
        puts [i, fib].inspect
      end
    else
      break
    end
    i+=1 
  end
  return sum
end
# puts prob2

def prob3(n=600851475143)
  return P.max_prime_factor n
end
# puts prob3

def prob4(n=3)
  max_palindrome = 0
  biggest = nil
  biggest_factor = 10**n - 1
  smallest_factor = 10**(n-1)
  (smallest_factor...biggest_factor).each do |i|
    (i...biggest_factor).each do |j|
      prod = i * j
      if prod > max_palindrome && prod.to_s.palindrome?
        max_palindrome = prod
        biggest = [i, j]
      end
    end
  end
  return biggest
end
puts prob4