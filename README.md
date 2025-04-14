# N-Queens Problem Solver

This repository contains a Python implementation for solving the classic N-Queens problem. The goal is to place N non-attacking queens on an N×N chessboard, meaning no two queens can be in the same row, column, or diagonal.

This project includes:
* A core solver module.
* Unit tests for the solver.
* A demonstration script, focusing on performance.

The code was developed as part of an assignment for the course in AI Applications at the University of Pisa.

## Files

* `queens_solver.py`: Contains the main logic for finding solutions to the N-Queens problem for a given board size `N`. It uses a backtracking algorithm.
* `test_queen_solver.py`: Includes unit tests for the functions/classes defined in `queens_solver.py`. This helps ensure the solver's correctness for various inputs. Uses Python's `unittest` framework.
* `queens_performance_demo.py`: Demonstrates how to use the solver, showing how to find solutions for a specific `N`, count the number of solutions and the time taken for different values of `N`.