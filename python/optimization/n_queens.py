# http://stackoverflow.com/questions/41131644/n-queens-symmetry-breaking-google-or-tools
from ortools.constraint_solver import pywrapcp

N = 12
solver = pywrapcp.Solver("n-queens")
# Creates the variables.
# The array index is the column, and the value is the row.
queens = (
    [solver.IntVar(0, (N // 2) + 1)] +  # require the first row to be on the "left half" of the board
    [solver.IntVar(0, N - 1, "x%i" % i) for i in range(1, N)])
# Creates the constraints.
# All rows must be different.
solver.Add(solver.AllDifferent(queens))
# All columns must be different because the indices of queens are all different.
# No two queens can be on the same diagonal.
solver.Add(solver.AllDifferent([queens[i] + i for i in range(N)]))
solver.Add(solver.AllDifferent([queens[i] - i for i in range(N)]))

# TODO: add symmetry breaking constraints

db = solver.Phase(queens, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
solver.NewSearch(db)
num_solutions = 0
while solver.NextSolution():
  num_solutions += 1
solver.EndSearch()
print()
print("Solutions found:", num_solutions)
print("Time:", solver.WallTime(), "ms")