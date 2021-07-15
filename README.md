# QuantumSudokuSolver
    solves both 2D and 3D sudoku puzzles using quantum annealing based on the QUBO model

I have designed a quantum sudoku solver that can solve both 2D and 3D sudoku puzzles using the programming language of python along with Dwave’s Ocean sdk. This was implemented in the remaining 3 weeks of my Quantum Computing course.

My solver is successfully able to solve 2D and 3D Sudoku puzzles of varying size and emptiness using the approach of quantum annealing, a branch of quantum computing in which a quantum system attempts to solve a user-designed BQM by finding the lowest energy state.

My approach to implementing the quantum sudoku solver involved formulating Quadratic Unconstrained Binary Optimization equations for both 2-dimensional and 3-dimensional Sudoku puzzles and using the equations to write a program which can generate QUBO matrices based on arbitrary user-submitted Sudoku puzzles. The QUBO matrix would then be converted into BQM to be inputted into the sampler to obtain a solution. As an additional feature, I utilized the matplotlib tool to generate plots of solutions to assist with the visualization of the results. 

## My 2D sudoku QUBO Equation
![Picture4](https://user-images.githubusercontent.com/74283978/125514349-82697311-185d-42c6-9a65-37cdd60c7938.png)

## My 3D sudoku QUBO Equation
![Picture1](https://user-images.githubusercontent.com/74283978/125513782-3b855fcd-c196-4d49-8a72-8440951f275b.png)

## Explaining my 2D QUBO equation
In my equations, each variable is represented by a pair of c and d letters. c represents a particular cell of the sudoku puzzle using coordinates (i, j), and d represents the particular kth digit being used out of the n possible digits. I group these two properties as one variable in order to allow me to differentiate which part of the variable represents the cell and which part represents the digit. The indices i, j, and k also represent the order in which the values will be cycled through. Generally, the index that is cycled through first is the one that is enclosed by the innermost parentheses and so on. 

## Explaining my 3D QUBO equation
My equations for the 3D sudoku solver are similar to those of the 2D sudoku. However, for these equations, there is one more index as a consequence of the additional dimension. So, we now have indices i, j, k, and l. 

Each variable is represented by a pair of c and d letters. c represents a particular cell of the sudoku puzzle using coordinates (i, j, k), and d represents the particular lth digit being used out of the n possible digits.


