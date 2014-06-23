require './primes'
require './fib'
require './eulerlib'
require './pythagoras'

P = Primes.new

def prob1(n)
  return (1...n).select {|i| (i % 3) * (i % 5) == 0  }.sum
end
puts prob1(1000)

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
puts prob2

def prob3(n=600851475143)
  return n.factors.max
end
puts prob3

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
puts prob4

def prob5(n=20)
  p_to_counts = IntHash.new
  (1..n).each do |i|
    i.factors.counts.each_pair do |p, count|
      p_to_counts[p] = [p_to_counts[p], count].max
    end
  end
  return p_to_counts.map {|p, count| p**count }.product
end
puts prob5(10)
puts prob5(20)

def prob6(n=100)
  return (1..n).to_a.sum ** 2 - ((1..n).map {|i| i**2}.sum)
end
puts prob6(10)
puts prob6(100)

# Problem 7
puts P.nth_prime(10001)

prob8_string = '7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450'

def prob8(window_length, s)
  return s.to_a.map(&:to_i).windows(window_length).map(&:product).max
end
puts prob8(5, prob8_string)


def prob9(sum=1000)
  Pythagoras.triples do |triple|
    return triple.product if triple.sum == sum
  end
end
puts prob9


def prob10(max_prime=2000000)
  sum = 0
  P.primes_iter do |p|
    return sum if p >= max_prime
    sum += p
  end
end
puts prob10(10) == 17
puts prob10
