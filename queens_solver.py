"""
8-Queens Problem Solver

This module implements functions to solve the classic 8-queens problem.
"""

import functools

def is_safe(board, row, col):
    """
    Check if a queen can be placed at position (row, col) without being threatened.
    
    A queen threatens another queen if they share the same row, column, or diagonal.
    
    Parameters:
        board (list): A 1D array where board[i] represents the column position 
                     of the queen in row i
        row (int): The row to check
        col (int): The column to check
    
    Returns:
        bool: True if it's safe to place a queen at position (row, col), False otherwise
    """

    if len(board) == 0:
        return True

    # Dictionary representing the major diagonals (difference between column and row)
    major_diag = dict()

    # Dictionary representing the minor diagonals (sum between column and row)
    minor_diag = dict()

    for r, c in enumerate(board):
        if row == r or col == c:
            return False
        major_diag[c-r] = 1
        minor_diag[c+r] = 1

    major_index = col-row
    minor_index = col+row

    # if there is a queen on the same diagonal return False
    if (major_index in major_diag and major_diag[col-row] != -1) or (minor_index in minor_diag and minor_diag[col+row] != -1):
        return False
    return True

# Dictionary to cache the last checked square for each row so that subsequent calls don't recheck the same squares
cache_unplaceable=dict()

def solve_queens(n=8):
    """
    Solve the n-queens problem and return a solution if one exists.
    
    Parameters:
        n (int): The size of the board and number of queens to place
        
    Returns:
        list or None: A 1D array representing a solution, where solution[i] is the 
                     column position of the queen in row i, or None if no solution exists
    """
    rows = [-1 for _ in range(n)]
    cols = [-1 for _ in range(n)]
    major_diag = {i: -1 for i in range(-n, n)}
    minor_diag = {i: -1 for i in range(((2*n)-1))}

    # recursive_function is not called because the iterative one has slightly better performance 
    solution = iterative_backtracking(rows=rows, cols=cols, major_diag=major_diag, minor_diag=minor_diag, unplaceable=None)

    # if there was no solution (n < 4) clear the cache
    if not solution:
        global cache_unplaceable
        cache_unplaceable = dict()
        return None

    return solution


def recursive_backtracking(rows, cols, major_diag, minor_diag, unplaceable, row=0, solutions=None):
    """
    Solves the N-Queens problem recursively using a backtracking approach.

    Parameters:
        rows (list): A list representing the rows of the board, where the index is the row number and the value is the column number of the queen.
        cols (list): A list representing the columns of the board, where the index is the column number and the value is the row number of the queen.
        major_diag (dict): A dictionary representing the major diagonals (difference between column and row). In this case sets are slower.
        minor_diag (dict): A dictionary representing the minor diagonals (sum of column and row). In this case sets are slower.
        unplaceable (dict, optional): A dictionary to keep track of columns where queens cannot be placed for each row. Defaults to an empty dictionary.
        row (int, optional): The current row to place a queen. Defaults to 0.
        first_call (bool, optional): A flag to indicate if this is the first call to the function. Defaults to False.
        solutions (set, optional): A set of solutions to avoid duplicate solutions. Defaults to None.

    Returns:
        list or bool: Returns the list of rows with queen placements if a solution is found, otherwise returns False.
    """
    if unplaceable is None:
        global cache_unplaceable
        unplaceable = cache_unplaceable

    length = len(rows)
    
    # if all queens have been placed return rows
    if row >= length:
        return rows
    
    # if the backtracking reached the root return False; there is no solution
    if row < 0:
        return False

    # start searching the position from the first unchecked squares
    first_col = unplaceable[row]+1 if row in unplaceable and unplaceable[row] != -1 else 0
    for col in range(first_col, length):

        # check if safe without calling is_safe for better performance
        if rows[row] == -1 and cols[col] == -1 and major_diag[col-row] == -1 and minor_diag[col+row] == -1:

            # place the queen on (row, col)
            rows[row] = col

            # if the solution is already been found unplace the queen and continue the search
            if solutions is not None and tuple(rows) in solutions:
                rows[row] = -1
                continue
            cols[col] = row
            major_diag[col-row] = 1
            minor_diag[col+row] = 1

            # try and place the next queen
            ret = recursive_backtracking(rows=rows, cols=cols, major_diag=major_diag, minor_diag=minor_diag, row=row+1, unplaceable=unplaceable, solutions=solutions)
            if ret:
                return ret
            else:
                # unplace the queen if the next queen couldn't be placed
                unplaceable_col = rows[row] 
                rows[row] = -1
                cols[unplaceable_col] = -1
                major_diag[unplaceable_col-row] = -1
                minor_diag[unplaceable_col+row] = -1
                unplaceable[row] = unplaceable_col    
                unplaceable[row+1] = -1
    
    return False


def iterative_backtracking(rows, cols, major_diag, minor_diag, unplaceable, solutions=None):
    """
    Solves the N-Queens problem iteratively using a backtracking approach.
    
    Parameters:
        rows (list): A list representing the rows of the board, where the index is the row number and the value is the column number of the queen.
        cols (list): A list representing the columns of the board, where the index is the column number and the value is the row number of the queen.
        major_diag (dict): A dictionary representing the major diagonals (difference between column and row). In this case sets are slower.
        minor_diag (dict): A dictionary representing the minor diagonals (sum of column and row). In this case sets are slower.
        unplaceable (dict, optional): A dictionary to keep track of columns where queens cannot be placed for each row. Defaults to an empty dictionary.
        solutions (set, optional): Set of solutions to avoid duplicates. Defaults to None.
        first_call (bool, optional): Flag indicating if this is the first call to the function. Defaults to False.
    
    Returns:
        list: A list representing the board with queens placed if a solution is found.
        bool: False if no solution is found.
    """
    if unplaceable is None:
        global cache_unplaceable
        unplaceable = cache_unplaceable

    length = len(rows)
    row = 0
    replace = False
    while True:
        placed = False
        
        # unplace the queen if the next queen couldn't be placed
        if replace:
            unplaceable_col = rows[row] 
            rows[row] = -1
            cols[unplaceable_col] = -1
            major_diag[unplaceable_col-row] = -1
            minor_diag[unplaceable_col+row] = -1
            unplaceable[row] = unplaceable_col    
            unplaceable[row+1] = -1
            replace = False

        # start searching the position from the first unchecked squares
        first_col = unplaceable[row]+1 if row in unplaceable and unplaceable[row] != -1 else 0
        for col in range(first_col, length):

            # check if safe without calling is_safe for better performance
            if rows[row] == -1 and cols[col] == -1 and major_diag[col-row] == -1 and minor_diag[col+row] == -1:

                # place the queen on (row, col)
                rows[row] = col
                
                # if the solution is already been found unplace the queen and continue the search
                if solutions is not None and tuple(rows) in solutions:
                    rows[row] = -1
                    continue
                cols[col] = row
                major_diag[col-row] = 1
                minor_diag[col+row] = 1
                row += 1

                # if all queens have been placed return rows
                if row == length:
                    return rows
                placed = True
                break
        
        # if queen couldn't be placed must backtrack
        if not placed:
            row -= 1

            # if the first queen couldn't be place return False; there is no solution
            if row < 0:
                return False
            
            # in the next iteration the queen on (row, rows[row]) must be moved
            replace = True

def find_all_solutions(n=8):
    """
    Find all solutions to the n-queens problem.
    
    Parameters:
        n (int): The size of the board and number of queens to place
        
    Returns:
        list: A list of solutions, where each solution is a 1D array where
              solution[i] is the column position of the queen in row i
    """
    
    # set to save found solutions
    solutions = set()
    unplaceable = dict()
    while True:
        rows = [-1 for _ in range(n)]
        cols = [-1 for _ in range(n)]
        major_diag = {i: -1 for i in range(-n, n)}
        minor_diag = {i: -1 for i in range(((2*n)-1))}
        
        # find a new solution
        solution = iterative_backtracking(rows=rows, cols=cols, major_diag=major_diag, minor_diag=minor_diag, unplaceable=unplaceable, solutions=solutions) 
        
        # if no new solution found -> all solutions have already been found
        if not solution:
            break 

        # add found solution to solutions set
        solutions.add(tuple(solution))
    return [list(sol) for sol in solutions]

def board_to_string(board):
    """
    Convert a board configuration to a string representation.
    
    Parameters:
        board (list): A 1D array where board[i] represents the column position 
                     of the queen in row i
                     
    Returns:
        str: A string representation of the board with 'Q' for queens and '.' for empty squares
    """
    length = len(board)
    board_string = []
    for r, c in enumerate(board):
        if c == -1:
            board_string += ['.' * length]
        else:
            board_string += ['.' * c]
            board_string += ['Q']
            board_string += ['.' * (length - 1 - c)]
        board_string += ['\n']
    return ''.join(board_string)

@functools.cache
def count_solutions(n=8):
    """
    Count the number of solutions to the n-queens problem.
    
    Parameters:
        n (int): The size of the board and number of queens to place
        
    Returns:
        int: The number of solutions
    """
    return len(find_all_solutions(n))

def is_valid_solution(board):
    """
    Check if a board configuration is a valid solution to the n-queens problem.
    
    Parameters:
        board (list): A 1D array where board[i] represents the column position 
                     of the queen in row i
                     
    Returns:
        bool: True if the board is a valid solution, False otherwise
    """
    lenght = len(board)
    for r, c in enumerate(board):
        if c >= lenght or not is_safe(board=board[:r], row=r, col=c):
            return False
    return True
