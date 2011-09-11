class IntHash < Hash
  def initialize
    super {|h, k| h[k] = 0}
  end
end

class Array
  def sum
    s = 0
    self.each do |a|
      s += a
    end
    return s
  end
  def product
    p = 1
    self.each do |a|
      p *= a
    end
    return p
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
end

class String
  def palindrome?
    self == reverse
  end
  def to_a
    split('')
  end
end


