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
end

class String
  def palindrome?
    self == reverse
  end
end