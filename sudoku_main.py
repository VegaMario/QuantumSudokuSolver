import time
import nxn_generate, nxn_plot, nxn_QUBO, nxn_solver
import nxnxn_generate, nxnxn_plot, nxnxn_QUBO, nxnxn_solver
import sys
from hybrid.reference import KerberosSampler


# generate a sudoku puzzle
def generate(dim, nsize, blanks):
    if dim == 2:
        nxn_generate.gen_nxn(nsize, blanks)
    elif dim == 3:
        nxnxn_generate.gen_nxnxn(nsize, blanks)
    else:
        print("Invalid")


# solve a sudoku puzzle
def solve(filename, qubotype, samplername, numreads, plot):
    dim = 1
    for i in filename:
        if i == 'x':
            dim += 1
    print("----------{}D Solver----------".format(dim))
    if dim == 2:
        nxn_solver.solve_nxn(filename + ".txt", qubotype, samplername, numreads, plot)
    elif dim == 3:
        nxnxn_solver.solve_nxnxn(filename + ".txt", qubotype, samplername, numreads, plot)
    else:
        print("Invalid")
    dim = 1


def main():
    # print('Hello Cruel World!')
    # generate(3, 16, 1)

    # python sudoku_main.py solve 9x9x9
    # python sudoku_main.py generate 9x9x9
    operation = sys.argv[1]
    filename = sys.argv[2]

    if operation == 'solve':
        QUBO_type = input('QUBO Type (complex or simple): ').lower()
        make_plot = int(input('Make Plot? (1 or 0): '))
        solve(filename, QUBO_type, "neal", 10, make_plot)
    elif operation == 'generate':
        dim = 1
        for i in filename:
            if i == 'x':
                dim += 1
        num = ''
        for i in filename:
            if i != 'x':
                num += i
            else:
                break
        num = int(num)
        max_blanks = num ** dim
        blanks = int(input('Number of Blanks (max is {}):'.format(max_blanks)))
        generate(dim, num, blanks)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
