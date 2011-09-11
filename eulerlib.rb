class Array
  def sum
    s = 0
    self.each do |a|
      s += a
    end
    return s
  end
end
