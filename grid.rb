class BaseGrid
  attr_accessor :grid
  def self.from_string(gridstring)
    self.new(gridstring.split("\n").map {|row| row.split(' ').map(&:to_i)})
  end
end

class Grid < BaseGrid
  DIRECTIONS = [[0,1], [1,0], [1, 1], [1, -1]]

  def initialize(gridarray)
    @grid = gridarray
    @size_x = @grid[0].length
    @size_y = @grid.length
  end

  def val_at(x, y)
    if x >= @size_x || y >= @size_y || x < 0 || y < 0
      return nil
    end
    return @grid[y][x]
  end

  def lines_at(x, y, length)
    self::DIRECTIONS.map do |dx, dy|
      (0...length).map do |i|
        val_at(x + i * dx, y + i * dy) 
      end
    end.select {|path| path.all? {|val| !val.nil? } }
  end

  def lines(length)
    (0...@size_x).to_a.
      cartesian_product((0...@size_y)).
      map {|x, y| lines_at(x, y, length) }.
      sum([])
  end
end

class TriangleGrid < BaseGrid
  attr_accessor :grid
  def initialize(gridarray)
    @grid = gridarray
    @height = @grid.length
    @base = @grid[-1].length
    @pos_to_max_sum_below = Hash.new {|h, k| h[k] = _max_sum_path(*k) }
  end
  def _max_sum_path(x, y)
    max_sum = @grid[y][x]
    if y != @height - 1
      max_sum += [@pos_to_max_sum_below[[x, y + 1]], @pos_to_max_sum_below[[x + 1, y + 1]]].max
    end
    return max_sum
  end
  def max_sum
    return @pos_to_max_sum_below[[0, 0]]
  end
end
