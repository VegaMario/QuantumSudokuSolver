import neal
from dimod import BinaryQuadraticModel
from dwave.system import EmbeddingComposite, DWaveSampler
import math
import sys
from hybrid.reference import KerberosSampler
import greedy
from dwave_qbsolv import QBSolv
import nxnxn_QUBO
import nxnxn_plot


# generate variables in the form of layer,row,column_value

def var_generate(lay, row, col, val):
    return f"{lay},{row},{col}_{val}"


# This function is used to read a txt file to generate the sudoku puzzle
def scan_sudoku(filename):
    with open(filename, "r") as f:
        content = f.readlines()  # read each line

    lines = []  # store the lines in this list

    for line in content:
        new_line = line.rstrip()  # remove the blank space to the right of the line

        if new_line:  # if the line is non empty
            new_line = list(map(int, new_line.split("\t")))  # split from spaces and put into a list
            lines.append(new_line)  # add the line to the list of lines

    layers = lines_adjust(lines)  # we need some readjustments due to the three dimensions

    return layers  # return the lines


# Function to reorganize lines into a three dimensional list
def lines_adjust(lines):
    n = int(math.sqrt(len(lines)))
    layers = []  # store the layers of stacked sudoku puzzles

    for offset in range(n):
        layer = []  # individual layers will be stored here
        for row in range(n):
            layer.append(lines[row + offset * n])  # add the lines that belong to the layer
        layers.append(layer)  # add the layer to the list of layers

    return layers  # return the layers list


# generate a sudoku puzzle of size nxnxn
def generate_sudoku(n):
    layers = []  # store the layers
    lines = []  # stores the lines
    line = []  # stores each line

    # just filling in all of the lists
    for lay in range(n):
        for row in range(n):
            for col in range(n):
                line.append(0)
            lines.append(line)
            line = []
        layers.append(lines)
        lines = []

    return layers  # return the layer


# If there are some givens in the sudoku puzzle, then we adjust the BQM using this function
def givens_fill(bqm, sudoku):
    for layer in range(len(sudoku)):
        for row in range(len(sudoku)):
            for column in range(len(sudoku)):
                if sudoku[layer][row][column] != 0:  # If a cell in the sudoku puzzle is not empty
                    given_var = var_generate(layer, row, column, sudoku[layer][row][column])

                    bqm.fix_variable(given_var, 1)

    return bqm


# once we have obtained a sample, we use this function to print out the results in a way that is easier to understand
def print_result(sample, sudoku):
    flat = []  # Tempoorary list, flat because it is '1 dimensional'
    copy = sudoku  # make a copy of the sudoku puzzle
    n = int(len(copy))
    result = 'correct'

    for var, val in sample.items():  # if the variable was used, then add it to the flat list
        if val == 1:
            flat.append(var)

    # Read the variables in the flat list and add to the copy list of the sudoku puzzle on empty spots only
    for var in flat:
        cell, val = var.split('_')
        lay, row, col = map(int, cell.split(','))
        if copy[lay][row][col] == 0:
            copy[lay][row][col] = int(val)

    # print and check the layers in the x-direction planes
    print('----------X Direction layers----------')
    for i in range(n):
        lines = []
        for j in range(n):
            line = []
            for k in range(n):
                line.append(copy[i][j][k])
                sys.stdout.write(str(copy[i][j][k]) + "\t")
            print()
            lines.append(line)
        is_correct = check_solution(lines)
        if is_correct:
            print('good job')
        else:
            result = 'incorrect'
            print("incorrect")
        print()

    # print and check the layers in the y-direction planes
    print('----------Y Direction Layers----------')
    for k in range(n):
        lines = []
        for j in range(n):
            line = []
            for i in range(n):
                line.append(copy[i][j][k])
                sys.stdout.write(str(copy[i][j][k]) + "\t")
            print()
            lines.append(line)
        is_correct = check_solution(lines)
        if is_correct:
            print('good job')
        else:
            result = 'incorrect'
            print("incorrect")
        print()

    # print and check the layers in the z-direction planes
    print('----------Z Direction Layers----------')
    for j in range(n):
        lines = []
        for i in range(n):
            line = []
            for k in range(n):
                line.append(copy[i][j][k])
                sys.stdout.write(str(copy[i][j][k]) + "\t")
            print()
            lines.append(line)

        is_correct = check_solution(lines)

        if is_correct:
            print('good job')
        else:
            result = 'incorrect'
            print("incorrect")

        print()

    # nxnxn_plot.plot_3D_sudoku(copy, result)  # now plot the results
    print("\nThe Solution is {}".format(result))
    return copy, result


# check an individual layer of the 3D sudoku puzzle to see if it is correct
def check_solution(solved_sudoku):
    n = len(solved_sudoku)
    m = int(math.floor(int(math.sqrt(n))))
    values = set(range(1, n + 1))

    # checking for errors on the rows
    for row in range(n):
        row_vals = set()
        for val in solved_sudoku[row]:
            row_vals.add(val)
        if row_vals != values:
            print("error at row: {}".format(row + 1))
            return 0

    # checking for errors on the columns
    for col in range(n):
        col_vals = set()
        for row in range(n):
            col_vals.add(solved_sudoku[row][col])
        if col_vals != values:
            print("error at column: {}".format(col + 1))
            return 0

    # checking for errors on the subsquares
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


# function may be used for selecting the sampler
def select_sampler(keyword):
    if keyword.lower() == 'neal':
        return neal.SimulatedAnnealingSampler()
    elif keyword.lower() == 'kerberos':
        return KerberosSampler()
    elif keyword.lower() == 'dwavesampler':
        return EmbeddingComposite(DWaveSampler())
    elif keyword.lower() == 'greedy':
        return greedy.SteepestDescentSolver()
    elif keyword.lower() == 'qbsolv':
        return QBSolv()


# functioned used for converting a QUBO matrix into a BQM
def convert_to_bqm(Q, const):
    bqm = BinaryQuadraticModel.from_qubo(Q, offset=const)
    return bqm


# the main function
def solve_nxnxn(name, complexity, sampler_name, reads, plot):
    sudoku = scan_sudoku(name)
    n = len(sudoku)

    if complexity.lower() == "complex":
        nodes, edges = nxnxn_QUBO.gen_edges_nodes_complex(n)  # generate the nodes and edges of the sudoku based on
        # the size n
        QUBO, offset = nxnxn_QUBO.gen_QUBO_complex(sudoku, nodes, edges, 150)  # generate the QUBo, taking into
        # account the nodes and edges
    elif complexity.lower() == "simple":
        QUBO, offset = nxnxn_QUBO.gen_QUBO_simple(sudoku)

    bqm = convert_to_bqm(QUBO, offset)  # convert the QUBO matrix into a Binary Quadratic Mdoel
    bqm = givens_fill(bqm, sudoku)
    sampler = select_sampler(sampler_name.lower())  # select the sampler

    if sampler_name.lower() == "kerberos":
        sampleset = sampler.sample(bqm, max_iter=reads, convergence=3)
    else:
        sampleset = sampler.sample(bqm, num_reads=reads)  # sample the bqm to generate a sampleset

    print(sampleset)
    sample = sampleset.first.sample  # take the best solutin from the sampleset
    final_sudoku, result = print_result(sample, sudoku)  # print the results

    if plot:
        nxnxn_plot.plot_3D_sudoku(final_sudoku, result)
