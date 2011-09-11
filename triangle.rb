class Triangle
  def self.nth(n)
    ((n + 1) * n) / 2
  end

  def self.numbers
    i = 1
    s = 0
    while true
      s += i
      i += 1
      yield s
    end
  end
end