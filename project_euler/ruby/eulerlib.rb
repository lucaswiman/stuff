class Count
  def self.iter(min=0)
    i = min
    while true
      yield i
      i += 1
    end
  end
end

class IntHash < Hash
  def initialize
    super {|h, k| h[k] = 0}
  end
end

class Array
  def sum(s=0)
    self.inject(s, :+)
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

  def lexicographic_permutations
    if empty?
      yield []
    else
      first = sort
      first.each do |elem|
        (first - [elem]).lexicographic_permutations do |perm|
          yield [elem] + perm
        end
      end
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

  def letter_sum
    a = 'a'.bytes.first
    return self.downcase.gsub(/[^a-z]/, '').bytes.map {|byte| byte - a + 1 }.sum
  end
end

class Integer
  def factorial
    (1..self).to_a.product
  end
end
