from logpy.tests.test_sudoku import *
example_board = (
    0, 0, 8, 0, 0, 6, 0, 0, 0,
    0, 0, 4, 3, 7, 9, 8, 0, 0,
    5, 7, 0, 0, 1, 0, 3, 2, 0,
    0, 5, 2, 0, 0, 7, 0, 0, 0,
    0, 6, 0, 5, 9, 8, 0, 4, 0,
    0, 0, 0, 4, 0, 0, 5, 7, 0,
    0, 2, 1, 0, 4, 0, 0, 9, 8,
    0, 0, 9, 6, 2, 3, 1, 0, 0,
    0, 0, 0, 9, 0, 0, 7, 0, 0,
)
variables = vars(example_board)
rows = get_rows(variables)
cols = get_columns(rows)
sqs = get_squares(rows)
run(1, variables, (everyg, all_numbers, cols + rows + sqs))
c_sols = set(run(0, variables, everyg(all_numbers, cols)))
r_sols = set(run(0, variables, everyg(all_numbers, rows)))
s_sols = set(run(0, variables, everyg(all_numbers, sqs)))
assert len(c_sols) == len(r_sols) == len(s_sols)
assert len(c_sols & r_sols & s_sols) == 2


from logpy.tests.test_sudoku import *
example_board = (
   5, 3, 4, 6, 7, 8, 9, 1, 2,
   6, 7, 2, 1, 9, 5, 3, 4, 8,
   1, 9, 8, 3, 4, 2, 5, 6, 7,
   8, 5, 9, 7, 6, 1, 4, 2, 3,
   4, 2, 6, 8, 5, 3, 7, 9, 1,
   7, 1, 3, 9, 2, 4, 8, 5, 6,
   9, 6, 1, 5, 3, 7, 2, 8, 4,
   2, 8, 7, 4, 1, 9, 6, 3, 5,
   3, 4, 5, 2, 8, 6, 0, 7, 9
    )

get_rows(sudoku_solver(example_board))

example_board_2 = (
        5, 3, 0, 0, 7, 0, 0, 0, 0,
        6, 0, 0, 1, 9, 5, 0, 0, 0,
        0, 9, 8, 0, 0, 0, 0, 6, 0,
        8, 0, 0, 0, 6, 0, 0, 0, 3,
        4, 0, 0, 8, 0, 3, 0, 0, 1,
        7, 0, 0, 0, 2, 0, 0, 0, 6,
        0, 6, 0, 0, 0, 0, 2, 8, 0,
        0, 0, 0, 4, 1, 9, 0, 0, 5,
        0, 0, 0, 0, 8, 0, 0, 7, 9)
get_rows(sudoku_solver(example_board_2))


example_board_3 = (
   5, 3, 4, 6, 7, 8, 9, 0, 0,
   6, 7, 0, 0, 9, 5, 3, 4, 8,
   0, 9, 8, 3, 4, 0, 5, 6, 7,
   8, 5, 9, 7, 6, 0, 4, 0, 3,
   4, 0, 6, 8, 5, 3, 7, 9, 0,
   7, 0, 3, 9, 0, 4, 8, 5, 6,
   9, 6, 0, 5, 3, 7, 0, 8, 4,
   0, 8, 7, 4, 0, 9, 6, 3, 5,
   3, 4, 5, 0, 8, 6, 0, 7, 9
    )
get_rows(sudoku_solver(example_board_3))


from logpy.tests.test_sudoku import *
example_board_3 = (
   5, 3, 4, 6, 7, 8, 9, 0, 0,
   6, 7, 0, 0, 9, 5, 3, 4, 8,
   0, 9, 8, 3, 4, 0, 5, 6, 7,
   8, 5, 9, 7, 6, 0, 4, 0, 3,
   4, 0, 6, 8, 5, 3, 7, 9, 0,
   7, 0, 3, 9, 0, 4, 8, 5, 6,
   9, 6, 0, 5, 3, 7, 0, 8, 4,
   0, 8, 7, 4, 0, 9, 6, 3, 5,
   3, 4, 5, 0, 8, 6, 0, 7, 9
    )

variables = vars(example_board_3)
