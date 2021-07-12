import time
import nxn_generate, nxn_plot, nxn_QUBO, nxn_solver
import nxnxn_generate, nxnxn_plot, nxnxn_QUBO, nxnxn_solver
from hybrid.reference import KerberosSampler

'''Maybe Complete'''


def generate(dim, nsize, blanks):
    if dim == 2:
        nxn_generate.gen_nxn(nsize, blanks)
    elif dim == 3:
        nxnxn_generate.gen_nxnxn(nsize, blanks)
    else:
        print("Invalid")


def solve(filename, qubotype, samplername, numreads, plot):
    dim = 1
    for i in filename:
        if i == 'x':
            dim += 1
    print("{}D Solver".format(dim))
    if dim == 2:
        nxn_solver.solve_nxn(filename + ".txt", qubotype, samplername, numreads, plot)
    elif dim == 3:
        nxnxn_solver.solve_nxnxn(filename + ".txt", qubotype, samplername, numreads, plot)
    else:
        print("Invalid")
    dim = 1


def main():
    # print('Hello Cruel World!')
    # generate(3, 9, 500)
    solve("4x4x4", "complex", "neal", 10, 1)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
