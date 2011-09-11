class IntHash < Hash
  def initialize
    super {|h, k| h[k] = 0}
  end
end

class Array
  def sum(s=0)
    self.inject(0, :*)
  end

  def product
    self.inject(1, :*)
  end

  def counts
    count_hash = IntHash.new
    self.each {|val| count_hash[val] += 1 }
    return Hash[count_hash]
  end

  def windows(window_length)
    (0..length - window_length).map do |i|
      slice(i, window_length)
    end
  end

  def cartesian_product(ary)
    self.map do |val1|
      ary.map do |val2|
        [val1, val2]
      end
    end.sum([])
  end
end

class String
  def palindrome?
    self == reverse
  end
  def to_a
    split('')
  end
end

class Integer
  def factorial
    (1..self).to_a.product
  end
end
