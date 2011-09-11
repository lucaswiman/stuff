class Pythagoras
  def self.triples
    m = 2
    while true
      (1...m).each do |n|
        yield [m ** 2 - n ** 2, 2 * m * n, m ** 2 + n ** 2]
      end
      m += 1
    end
  end
end