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
  (smallest_factor..biggest_factor).each do |i|
    (i..biggest_factor).each do |j|
      prod = i * j
      if prod > max_palindrome && prod.to_s.palindrome?
        max_palindrome = prod
        biggest = [i, j]
      end
    end
  end
  return biggest
end
# puts prob4

def prob5(n=20)
  p_to_counts = IntHash.new
  (1..n).each do |i|
    P.factorize(i).counts.each_pair do |p, count|
      p_to_counts[p] = [p_to_counts[p], count].max
    end
  end
  return p_to_counts.map {|p, count| p**count }.product
end
# puts prob5(10)
# puts prob5(20)

def prob6(n=100)
  return (1..n).to_a.sum ** 2 - ((1..n).map {|i| i**2}.sum)
end
# puts prob6(10)
# puts prob6(100)

# Problem 7
# puts P.nth_prime(10001)
