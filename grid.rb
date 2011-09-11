class Grid
  DIRECTIONS = [[0,1], [1,0], [1, 1], [1, -1]]
  attr_accessor :grid

  def initialize(gridarray)
    @grid = gridarray
    @size_x = @grid[0].length
    @size_y = @grid.length
  end

  def self.from_string(gridstring)
    Grid.new(gridstring.split("\n").map {|row| row.split(' ').map(&:to_i)})
  end

  def val_at(x, y)
    if x >= @size_x || y >= @size_y || x < 0 || y < 0
      return nil
    end
    return @grid[y][x]
  end

  def lines_at(x, y, length)
    Grid::DIRECTIONS.map do |dx, dy|
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
