class Collatz
  def initialize
    @n_to_length = {1 => 1}
  end

  def step(n)
    if (n % 2) == 0
      return n / 2
    else
      return 3 * n + 1
    end
  end

  def length(n)
    return @n_to_length[n] if @n_to_length.key? n
    @n_to_length[n] = length(step(n)) + 1
    return @n_to_length[n] 
  end

  def steps(n)
    vals = []
    while n > 1
      vals << n
      n = step(n)
    end
    return vals
  end

  def print_steps(n)
    puts steps(n).join('=>')
  end
end