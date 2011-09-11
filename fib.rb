class Fib
  @@fibs = [1, 1]
  def self.fib(n)
    return @@fibs[n] if n < @@fibs.length 
    result = Fib.fib(n-1) + Fib.fib(n-2)
    @@fibs << result
    return result
  end
  
end