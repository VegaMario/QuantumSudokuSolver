import neal
from dimod import BinaryQuadraticModel
from dwave.system import EmbeddingComposite, DWaveSampler
import math
import sys
from hybrid.reference import KerberosSampler
from dwave_qbsolv import QBSolv
import nxn_QUBO

# By Mario Vega
# generate the variables
import nxn_plot


def var_generate(row, col, val):
    return f"{row},{col}_{val}"


# read the sudoku file and generate the sudoku puzzle
def get_sudoku_puzzle(filename):
    with open(filename, "r") as f:
        content = f.readlines()

    lines = []  # will store the rows of sudokus
    for line in content:
        new_line = line.rstrip()  # remove any blank space to the right

        if new_line:
            new_line = list(map(int, new_line.split('\t')))  # split into list from spaces
            lines.append(new_line)  # append the line to the lines list

    return lines


# If there are givens in the sudoku, then fill them in using this functions
def givens_fill(sudoku_puzzle, bqm):
    for row in range(len(sudoku_puzzle)):
        for col in range(len(sudoku_puzzle)):
            if int(sudoku_puzzle[row][col]) != 0:  # if there is a given, then adjust the BQM
                given_var = var_generate(row, col, sudoku_puzzle[row][col])
                bqm.fix_variable(given_var, 1)
    return bqm


# convert the QUBO matrix in to A binary Quadratic model
def convert_to_bqm(Q, const):
    bqm = BinaryQuadraticModel.from_qubo(Q, offset=const)
    return bqm


# Solve the Binary Quadratic Model
def solve_bqm(bqm, sampler, reads):
    sampleset = sampler.sample(bqm, num_reads=reads)
    return sampleset


# Select a sampler
def set_sampler(keyword):
    if keyword.lower() == "neal":
        return neal.SimulatedAnnealingSampler()
    elif keyword.lower() == "dwave":
        return EmbeddingComposite(DWaveSampler())
    elif keyword.lower() == "qbsolv":
        return QBSolv()
    elif keyword.lower() == "kerberos":
        return KerberosSampler()


# Print the result on the screen
def print_result(sample, sudoku_puzzle):
    flat = []
    copy = sudoku_puzzle
    result = "Correct"
    for var, val in sample.items():  # get the variable and value from the sample items
        if val == 1:
            flat.append(var)
    for var in flat:
        cell, val = var.split('_')
        row, col = map(int, cell.split(','))
        if copy[row][col] == 0:  # fill in the sudoku matrix
            copy[row][col] = int(val)

    for row in copy:  # print the results
        for val in row:
            sys.stdout.write(str(val) + "\t")
        print()

    is_correct = check_solution(copy)  # Check whether the solution is correct or not
    if is_correct:
        print('good job')
    else:
        print("incorrect")
        result = "Incorrect"

    # nxn_plot.plot_3D_sudoku(copy, result)
    print("\nThe Solution is {}".format(result))
    return copy, result


# check the solution and determine if it is correct or not.
def check_solution(solved_sudoku):
    n = len(solved_sudoku)
    m = int(math.floor(int(math.sqrt(n))))
    values = set(range(1, n + 1))

    # we will check to see that no rows have repeating values
    for row in range(n):
        row_vals = set()
        for val in solved_sudoku[row]:
            row_vals.add(val)
        if row_vals != values:
            print("error at row: {}".format(row + 1))
            return 0

    # check to see if that no cols have repeating values
    for col in range(n):
        col_vals = set()
        for row in range(n):
            col_vals.add(solved_sudoku[row][col])
        if col_vals != values:
            print("error at column: {}".format(col + 1))
            return 0

    # check to see that no sub squares have repeating values
    for r_delta in range(m):
        for c_delta in range(m):
            sub_vals = set()
            for row in range(m):
                for col in range(m):
                    sub_vals.add(solved_sudoku[row + r_delta * m][col + c_delta * m])
            if sub_vals != values:
                print("error at subsquare: {}".format((r_delta + 1, c_delta + 1)))
                return 0

    return 1


# If you have no puzzle to submit, then just try to generate an empty sudoku grid
def generate_sudoku(n):
    lines = []
    line = []
    for row in range(n):
        for col in range(n):
            line.append(0)
        lines.append(line)
        line = []
    return lines


# main function
def solve_nxn(name, complexity, sampler_name, reads, plot):
    sudoku_puzzle = get_sudoku_puzzle(name)  # read the file
    nn = len(sudoku_puzzle)  # used for either generating sudoku grids or generating nodes and edges
    sampler = set_sampler(sampler_name)  # we may select our sempler in this manner, or just do it the normal way
    gamma = 100  # you may need to play around with this value to give you good results

    n = len(sudoku_puzzle)  # generate the nodes and edges. In this case, we ue the
    # complex graph model
    if complexity.lower() == "complex":
        nodes, edges = nxn_QUBO.gen_nodes_edges_complex(nn)
        QUBO, const = nxn_QUBO.gen_QUBO_complex(sudoku_puzzle, nodes, edges, gamma)  # generate the QUBO, taking into
        # acccount the edges and nodes
    elif complexity.lower() == "simple":
        QUBO, const = nxn_QUBO.gen_QUBO_simple(sudoku_puzzle)

    # QUBO3 = gen_QUBO(sudoku_puzzle)
    bqm = convert_to_bqm(QUBO, const)  # convert the QUBO to a BQM
    bqm = givens_fill(sudoku_puzzle, bqm)  # for each given, adjust the BQM

    # sampleset = sampler.sample(bqm, max_iter=10, convergence=3)  # sample the BQM
    if sampler_name == "kerberos":
        sampleset = sampler.sample(bqm, max_iter=reads, convergence=3)
    else:
        sampleset = solve_bqm(bqm, sampler, reads)

    print(sampleset)
    sample = sampleset.first.sample  # get the best solution
    final_sudoku, result = print_result(sample, sudoku_puzzle)  # print the best solution found and check if correct

    if plot:
        nxn_plot.plot_2D_sudoku(final_sudoku, result)