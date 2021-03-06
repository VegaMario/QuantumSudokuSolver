import math
import time
import nxn_generate, nxn_plot, nxn_QUBO, nxn_solver
import nxnxn_generate, nxnxn_plot, nxnxn_QUBO, nxnxn_solver
import sys
from hybrid.reference import KerberosSampler


# generate a sudoku puzzle
def generate(dim, nsize, blanks):
    # only 2D or 3D puzzles are allowed
    if dim == 2:
        nxn_generate.gen_nxn(nsize, blanks)
    elif dim == 3:
        nxnxn_generate.gen_nxnxn(nsize, blanks)
    else:
        print("Invalid")


# solve a sudoku puzzle
def solve(filename, qubotype, samplername, numreads, plot, dim):
    # use complex or simple QUBO?
    if qubotype:
        qtype = 'complex'
    else:
        qtype = 'simple'
    print("----------{}D Solver----------".format(dim))
    # Dimension can only be 2D or 3D
    if dim == 2:
        nxn_solver.solve_nxn(filename + ".txt", qtype, samplername, numreads, plot)
    elif dim == 3:
        nxnxn_solver.solve_nxnxn(filename + ".txt", qtype, samplername, numreads, plot)
    else:
        print("Invalid")


def main():
    # Make sure you are using Dwave ocean
    # python sudoku_main.py solve 9x9x9
    # python sudoku_main.py generate 9x9x9
    operation = sys.argv[1]
    filename = sys.argv[2]

    n = filename.split('x')
    c = filename.split(n[0])
    c = list(filter(None, c))
    # checking for some possible errors in the user input
    for i in c:
        if i != 'x':
            print('invalid input')
            exit()
    for i in n:
        if i != n[0]:
            print('invalid input')
            exit()
    if not(n[0].isdigit()):
        print('invalid input: n should be a number')
        exit()
    if not(math.sqrt(int(n[0])).is_integer()):
        print('invalid input: size of n is not valid')
        exit()
    dim = len(n)
    if not(dim == 2 or dim == 3):
        print('invalid input: incorrect dimensions')
        exit()
    if operation == 'solve' or operation == 'generate':
        # prepare to perform the operation
        if operation == 'solve':
            QUBO_type = -1
            make_plot = -1
            while QUBO_type != 1 and QUBO_type != 0:
                QUBO_type = int(input('QUBO Type? (1 for complex, 0 for simple): '))
            while make_plot != 1 and make_plot != 0:
                make_plot = int(input('Make Plots? (1 for yes, 0 for no): '))
            if make_plot:
                print('----------After viewing the plots, close them to allow the program to continue----------')
            num_samples = int(input('How many samples?: '))
            solve(filename, QUBO_type, "neal", num_samples, make_plot, dim)
        elif operation == 'generate':
            num = int(n[0])
            max_blanks = num ** dim
            blanks = int(input('Number of Blanks (max is {}):'.format(max_blanks)))
            generate(dim, num, blanks)
    else:
        print('invalid input')
        exit()


start_time = time.time()
main()
print("---------- %s seconds ----------" % (time.time() - start_time))
