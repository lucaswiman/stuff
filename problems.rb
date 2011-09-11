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
puts prob3