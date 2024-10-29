"""

Name:João Pedro
Surname: REGAZZI FERREIRA DA SILVA
Email: joao-pedro.regazzi-ferreira-da-silva@student-cs.fr


There are three functions in this solution:

lectureGrille(filename):
    - Reads a Minesweeper grid from a file.
    - Returns number of columns in the grid, number of lines in the grid and a 2D list representing the grid

display_solution(grid, solution, lines, cols):
    - Clue numbers are displayed as they are
    - Mines are displayed as 'X'
    - Empty cells are displayed as spaces

solve_minesweeper(filename):
    - Reads the grid from the file
    - Sets up the CSP problem
    - Adds variables and constraints
    - Solves the problem
    - Displays the solution

    
Usage:
To run this script, ensure Python is installed with the constraint module available.
Execute the script from the command line using at least one grid to be read.


Examples:

python ./minesweeper_solver.py "/path/to/gid1.txt"

python ./minesweeper_solver.py "/path/to/gid1.txt" "/path/to/gid2.txt" "/path/to/gid3.txt"


"""


import sys, os
from constraint import Problem, ExactSumConstraint

def lectureGrille(filename):
    with open(filename, mode='r') as file:
        lines = int(file.readline())
        cols = int(file.readline())
        grid = [[0]*cols for i in range(lines)]
        for i in range(lines):
            line = file.readline()
            for j in range(cols):
                if line[j]!='0':
                    grid[i][j] = int(line[j])
        return (lines, cols, grid)

    
lines, cols, grille = lectureGrille(r'grille1.txt')

def solve_minesweeper(filename):

    lines, cols, grid = lectureGrille(filename)

    # Initialize the CSP problem
    problem = Problem()
    
    unknown_cells = []
    # Create variables for unknown cells
    for row in range(lines):
        for col in range(cols):
            if grid[row][col] == 0:
                var_name = 'cell_{}_{}'.format(row, col)
                # 0 means empty and 1 means mine
                problem.addVariable(var_name, [0, 1])
                unknown_cells.append((row, col))
    
    # Add constraints based on clues
    for row in range(lines):
        for col in range(cols):
            clue = grid[row][col]
            if clue > 0:
                # Get the list of adjacent unknown cells
                adjacent_vars = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        # Skip the clue cell is itself
                        if i == 0 and j == 0:
                            continue  
                        adj_row = row + i
                        adj_col = col + j
                        if 0 <= adj_row < lines and 0 <= adj_col < cols:
                            if grid[adj_row][adj_col] == 0:
                                var_name = 'cell_{}_{}'.format(adj_row, adj_col)
                                adjacent_vars.append(var_name)
                # Add a constraint that the sum of adjacent mines equals the clue
                problem.addConstraint(ExactSumConstraint(clue), adjacent_vars)
    
    # Force cells not adjacent to any clues to be empty
    for row in range(lines):
        for col in range(cols):
            if grid[row][col] == 0:
                # Check if adjacent to any clue cell
                adjacent_to_clue = False
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        adj_row = row + i
                        adj_col = col + j
                        if 0 <= adj_row < lines and 0 <= adj_col < cols:
                            if grid[adj_row][adj_col] > 0:
                                adjacent_to_clue = True
                                break
                    if adjacent_to_clue:
                        break
                if not adjacent_to_clue:
                    # Cell is not adjacent to any clue, must be empty
                    var_name = 'cell_{}_{}'.format(row, col)
                    problem.addConstraint(lambda v: v == 0, [var_name])

    # Solve the CSP
    solutions = problem.getSolutions()
    
    # Handle the results
    if len(solutions) == 0:
        print("No solution found.")
    elif len(solutions) == 1:
        solution = solutions[0]
        print("Solution:")
        display_solution(grid, solution, lines, cols)
    else:
        print("Multiple solutions found. Displaying one of them:")
        solution = solutions[0]
        display_solution(grid, solution, lines, cols)

def display_solution(grid, solution, lines, cols):

    # Colors for numbers and mines
    colors = {
        '1': '\033[34m',  # Blue
        '2': '\033[32m',  # Green
        '3': '\033[31m',  # Red
        '4': '\033[35m',  # Purple
        '5': '\033[33m',  # Yellow
        '6': '\033[36m',  # Cyan
        '7': '\033[37m',  # White
        '8': '\033[90m',  # Bright Black (Gray)
        'X': '\033[91m',  # Bright Red for mines
        'reset': '\033[0m'
    }

    # Create a display grid with the solution
    display_grid = [[' ' for _ in range(cols)] for _ in range(lines)]
    for row in range(lines):
        for col in range(cols):
            if grid[row][col] > 0:
                # Clue cell
                display_grid[row][col] = str(grid[row][col])
            elif grid[row][col] == 0:
                # Unknown cell, check the solution
                var_name = f'cell_{row}_{col}'
                if solution[var_name] == 1:
                    display_grid[row][col] = 'X'
                else:
                    display_grid[row][col] = ' '

    # Build the display string using box-drawing characters
    horizontal_line = '═══'
    top_border = '╔' + ('╦'.join([horizontal_line] * cols)) + '╗'
    bottom_border = '╚' + ('╩'.join([horizontal_line] * cols)) + '╝'
    middle_border = '╠' + ('╬'.join([horizontal_line] * cols)) + '╣'

    print(top_border)
    for row_idx, row in enumerate(display_grid):
        row_str = '║'
        for cell in row:
            color = colors.get(cell, '')
            reset = colors['reset'] if color else ''
            cell_content = f'{color}{cell}{reset}'
            # Center the cell content
            row_str += f' {cell_content} ║'
        print(row_str)
        if row_idx < lines - 1:
            print(middle_border)
    print(bottom_border)
    

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please provide at least one grid file.")
    else:
        for grid_file_name in sys.argv[1:]:
            grid_path = os.path.abspath(grid_file_name)
            print(f"Solving {grid_file_name}:")
            solve_minesweeper(grid_path)