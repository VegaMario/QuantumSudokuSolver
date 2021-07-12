from collections import defaultdict
import math

'''About Complete'''


# generate variables in the form of layer,row,column_value
def var_generate(lay, row, col, val):
    return f"{lay},{row},{col}_{val}"


# generate variables in the form of variablename_value (primarily used for nodes and edges)
def var_generate2(var, val):
    return f"{var}_{val}"


# simple implementation of the graph representation of 3 dimensional sudoku
def gen_edges_nodes_simple(n):
    nodes = []  # will store the nodes
    edges = []  # will store the edges
    m = int(math.sqrt(n))

    # each cell in the sudoku is a node of the graph
    for i in range(n):
        for j in range(n):
            for k in range(n):
                nodes.append(str(i) + ',' + str(j) + ',' + str(k))

    # cells next to each other in the same row/column in the yz planes should have an edge
    for i in range(n):
        for j in range(n):
            for k in range(n - 1):
                edges.append((str(i) + ',' + str(j) + ',' + str(k), str(i) + ',' + str(j) + ',' + str(k + 1)))

    # cells next to each other in the same row/column in the xz planes should have an edge
    for i in range(n):
        for j in range(n):
            for k in range(n - 1):
                edges.append((str(k) + ',' + str(j) + ',' + str(i), str(k + 1) + ',' + str(j) + ',' + str(i)))

    # cells next to each other in the same row/column in the xy planes should have an edge
    for i in range(n):
        for j in range(n):
            for k in range(n - 1):
                edges.append((str(i) + ',' + str(k) + ',' + str(j), str(i) + ',' + str(k + 1) + ',' + str(j)))

    return nodes, edges  # return the nodes and the edges


# Complex implementation of the graph representation of a 3 dimensional sudoku puzzle
def gen_edges_nodes_complex(n):
    nodes = []  # store the nodes
    edges = []  # store the edges
    m = int(math.sqrt(n))

    # every cell in the sudoku puzzle is a node
    for i in range(n):
        for j in range(n):
            for k in range(n):
                nodes.append(str(i) + ',' + str(j) + ',' + str(k))

    # cells in a row in the yz planes should have an edge with all other cells in the same row
    for i in range(n):
        for j in range(n):
            for k in range(n - 1):
                for kk in range(k + 1, n):
                    edges.append((str(i) + ',' + str(j) + ',' + str(k), str(i) + ',' + str(j) + ',' + str(kk)))

    # cell in a row in the xz planes should have an edge with all other cells in the same row
    for i in range(n):
        for j in range(n):
            for k in range(n - 1):
                for kk in range(k + 1, n):
                    edges.append((str(k) + ',' + str(j) + ',' + str(i), str(kk) + ',' + str(j) + ',' + str(i)))

    # cells in a column in the xy planes should have an edge with all other cells in the same column
    for i in range(n):
        for j in range(n):
            for k in range(n - 1):
                for kk in range(k + 1, n):
                    edges.append((str(i) + ',' + str(k) + ',' + str(j), str(i) + ',' + str(kk) + ',' + str(j)))

    # cells in a subsqaure in the yz planes should have en edge with all other cells in the same sub square
    for i in range(n):
        for roff in range(m):
            for coff in range(m):
                for j in range(m):
                    for k in range(m):
                        for kk in range(k + 1, m):
                            edges.append(
                                (str(i) + ',' + str(j + roff * m) + ',' + str(k + coff * m),
                                 str(i) + ',' + str(j + roff * m) + ',' + str(kk + coff * m)))
                        for jj in range(j + 1, m):
                            for kk in range(m):
                                edges.append(
                                    (str(i) + ',' + str(j + roff * m) + ',' + str(k + coff * m),
                                     str(i) + ',' + str(jj + roff * m) + ',' + str(kk + coff * m)))

    # cells in a subsquare in the xz planes should have an edge with all other cells in the same subsquare
    for i in range(n):
        for roff in range(m):
            for coff in range(m):
                for j in range(m):
                    for k in range(m):
                        for kk in range(k + 1, m):
                            edges.append(
                                (str(k + coff * m) + ',' + str(j + roff * m) + ',' + str(i),
                                 str(kk + coff * m) + ',' + str(j + roff * m) + ',' + str(i)))
                        for jj in range(j + 1, m):
                            for kk in range(m):
                                edges.append(
                                    (str(k + coff * m) + ',' + str(j + roff * m) + ',' + str(i),
                                     str(kk + coff * m) + ',' + str(jj + roff * m) + ',' + str(i)))

    # cells in a subsquare in the xy planes should have an edge with all other cells in the same subsquare
    for i in range(n):
        for roff in range(m):
            for coff in range(m):
                for j in range(m):
                    for k in range(m):
                        for kk in range(k + 1, m):
                            edges.append(
                                (str(j + roff * m) + ',' + str(i) + ',' + str(k + coff * m),
                                 str(j + roff * m) + ',' + str(i) + ',' + str(kk + coff * m)))
                        for jj in range(j + 1, m):
                            for kk in range(m):
                                edges.append(
                                    (str(j + roff * m) + ',' + str(i) + ',' + str(k + coff * m),
                                     str(jj + roff * m) + ',' + str(i) + ',' + str(kk + coff * m)))

    return nodes, edges  # return the nodes and the edges


# generate the QUBO, but don't take into consideration the nodes and the edges of the graph
def gen_QUBO_simple(sudoku):
    n = len(sudoku)  # the length of the sudoku
    m = int(math.sqrt(n))  # the size of the sub square
    values = [i for i in range(1, n + 1)]  # the possible values that may go in each cell

    offset = 7 * n**3

    Q = defaultdict(int)  # the QUBO matrix

    # Every cell must have only one value
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(len(values)):
                    variable_l = var_generate(i, j, k, values[l])
                    Q[variable_l, variable_l] += -1
                    for o in range(l + 1, len(values)):
                        variable_o = var_generate(i, j, k, values[o])
                        Q[(variable_l, variable_o)] += 2

    # there should be no repeating values in the rows/columns in the yz plane layers
    for i in range(n):
        for j in range(n):
            for k in range(len(values)):
                for l in range(n):
                    variable_l = var_generate(i, j, l, values[k])
                    Q[(variable_l, variable_l)] += -1
                    for o in range(l + 1, n):
                        variable_o = var_generate(i, j, o, values[k])
                        Q[(variable_l, variable_o)] += 2

    # there should be no repeating values in the rows/columns in the xz plane layers
    for i in range(n):
        for j in range(n):
            for k in range(len(values)):
                for l in range(n):
                    variable_l = var_generate(i, l, j, values[k])
                    Q[(variable_l, variable_l)] += -1
                    for o in range(l + 1, n):
                        variable_o = var_generate(i, o, j, values[k])
                        Q[(variable_l, variable_o)] += 2

    # there should be no repeating values in the rows/columns in the xy plane layers
    for i in range(n):
        for j in range(n):
            for k in range(len(values)):
                for l in range(n):
                    variable_l = var_generate(l, i, j, values[k])
                    Q[(variable_l, variable_l)] += -1
                    for o in range(l + 1, n):
                        variable_o = var_generate(o, i, j, values[k])
                        Q[(variable_l, variable_o)] += 2

    # there should be no repeating layers in the subsquares of the yz plane layers
    for i in range(n):
        for r_delta in range(m):
            for c_delta in range(m):
                for j in values:
                    for k in range(m):
                        for l in range(m):
                            variable_l = var_generate(i, k + r_delta * m, l + c_delta * m, j)
                            Q[(variable_l, variable_l)] += -1
                            for p in range(l + 1, m):
                                variable_o = var_generate(i, k + r_delta * m, p + c_delta * m, j)
                                Q[(variable_l, variable_o)] += 2
                            for o in range(k + 1, m):
                                for p in range(m):
                                    variable_o = var_generate(i, o + r_delta * m, p + c_delta * m, j)
                                    Q[(variable_l, variable_o)] += 2

    # there should be no repeating layers in the subsquares of the xz plane layers
    for i in range(n):
        for r_delta in range(m):
            for c_delta in range(m):
                for j in values:
                    for k in range(m):
                        for l in range(m):
                            variable_l = var_generate(k + r_delta * m, l + c_delta * m, i, j)
                            Q[(variable_l, variable_l)] += -1
                            for p in range(l + 1, m):
                                variable_o = var_generate(k + r_delta * m, p + c_delta * m, i, j)
                                Q[(variable_l, variable_o)] += 2
                            for o in range(k + 1, m):
                                for p in range(m):
                                    variable_o = var_generate(o + r_delta * m, p + c_delta * m, i, j)
                                    Q[(variable_l, variable_o)] += 2

    # there should be no repeating layers in the subsquares of the xy plane layers
    for i in range(n):
        for r_delta in range(m):
            for c_delta in range(m):
                for j in values:
                    for k in range(m):
                        for l in range(m):
                            variable_l = var_generate(k + r_delta * m, i, l + c_delta * m, j)
                            Q[(variable_l, variable_l)] += -1
                            for p in range(l + 1, m):
                                variable_o = var_generate(k + r_delta * m, i, p + c_delta * m, j)
                                Q[(variable_l, variable_o)] += 2
                            for o in range(k + 1, m):
                                for p in range(m):
                                    variable_o = var_generate(o + r_delta * m, i, p + c_delta * m, j)
                                    Q[(variable_l, variable_o)] += 2
    print("Qubo length: {}".format(len(Q)))
    return Q, offset  # return the QUBo matrix


# Generate the QUBO, but do take into consideration the nodes and edges of the graph
def gen_QUBO_complex(sudoku, nodes, edges, gamma):
    n = len(sudoku)  # the size of the SUdoku puzzle
    m = int(math.sqrt(n))  # the size of each subsquare
    values = [i for i in range(1, n + 1)]  # the possible values that may go inside each cell of the sudoku

    print("nodes: {}".format(len(nodes)))
    print("edges: {}".format(len(edges)))

    offset = ((6 + 1.5) * n ** 3) * gamma + len(edges) * 2

    Q = defaultdict(int)  # the QUBO matrix

    # there can only be one value in each cell of the sudoku
    for i in nodes:
        for j in range(len(values)):
            vari = var_generate2(i, j + 1)
            Q[(vari, vari)] += -1 * gamma * 1.5
            for k in range(j + 1, len(values)):
                varj = var_generate2(i, k + 1)
                Q[(vari, varj)] += 2 * gamma * 1.5

    # For every pair of cells/nodes that share an edge, they must not have the same value
    for i in range(len(values)):
        for j, k in edges:
            varj = var_generate2(j, i + 1)
            vark = var_generate2(k, i + 1)
            Q[(varj, varj)] += -1
            Q[(vark, vark)] += -1
            Q[(varj, vark)] += 2

    # there should be no repeating values in the rows/columns in the yz plane layers
    for i in range(n):
        for j in range(n):
            for k in range(len(values)):
                for l in range(n):
                    variable_l = var_generate(i, j, l, values[k])
                    Q[(variable_l, variable_l)] += -1 * gamma
                    for o in range(l + 1, n):
                        variable_o = var_generate(i, j, o, values[k])
                        Q[(variable_l, variable_o)] += 2 * gamma

    # there should be no repeating values in the rows/columns in the xz plane layers
    for i in range(n):
        for j in range(n):
            for k in range(len(values)):
                for l in range(n):
                    variable_l = var_generate(i, l, j, values[k])
                    Q[(variable_l, variable_l)] += -1 * gamma
                    for o in range(l + 1, n):
                        variable_o = var_generate(i, o, j, values[k])
                        Q[(variable_l, variable_o)] += 2 * gamma

    # there should be no repeating values in the rows/columns in the xy plane layers
    for i in range(n):
        for j in range(n):
            for k in range(len(values)):
                for l in range(n):
                    variable_l = var_generate(l, i, j, values[k])
                    Q[(variable_l, variable_l)] += -1 * gamma
                    for o in range(l + 1, n):
                        variable_o = var_generate(o, i, j, values[k])
                        Q[(variable_l, variable_o)] += 2 * gamma

    # there should be no repeating layers in the subsquares of the yz plane layers
    for i in range(n):
        for r_delta in range(m):
            for c_delta in range(m):
                for j in values:
                    for k in range(m):
                        for l in range(m):
                            variable_l = var_generate(i, k + r_delta * m, l + c_delta * m, j)
                            Q[(variable_l, variable_l)] += -1 * gamma
                            for p in range(l + 1, m):
                                variable_o = var_generate(i, k + r_delta * m, p + c_delta * m, j)
                                Q[(variable_l, variable_o)] += 2 * gamma
                            for o in range(k + 1, m):
                                for p in range(m):
                                    variable_o = var_generate(i, o + r_delta * m, p + c_delta * m, j)
                                    Q[(variable_l, variable_o)] += 2 * gamma

    # there should be no repeating layers in the subsquares of the xz plane layers
    for i in range(n):
        for r_delta in range(m):
            for c_delta in range(m):
                for j in values:
                    for k in range(m):
                        for l in range(m):
                            variable_l = var_generate(k + r_delta * m, l + c_delta * m, i, j)
                            Q[(variable_l, variable_l)] += -1 * gamma
                            for p in range(l + 1, m):
                                variable_o = var_generate(k + r_delta * m, p + c_delta * m, i, j)
                                Q[(variable_l, variable_o)] += 2 * gamma
                            for o in range(k + 1, m):
                                for p in range(m):
                                    variable_o = var_generate(o + r_delta * m, p + c_delta * m, i, j)
                                    Q[(variable_l, variable_o)] += 2 * gamma

    # there should be no repeating layers in the subsquares of the xy plane layers
    for i in range(n):
        for r_delta in range(m):
            for c_delta in range(m):
                for j in values:
                    for k in range(m):
                        for l in range(m):
                            variable_l = var_generate(k + r_delta * m, i, l + c_delta * m, j)
                            Q[(variable_l, variable_l)] += -1 * gamma
                            for p in range(l + 1, m):
                                variable_o = var_generate(k + r_delta * m, i, p + c_delta * m, j)
                                Q[(variable_l, variable_o)] += 2 * gamma
                            for o in range(k + 1, m):
                                for p in range(m):
                                    variable_o = var_generate(o + r_delta * m, i, p + c_delta * m, j)
                                    Q[(variable_l, variable_o)] += 2 * gamma
    print("Qubo length: {}".format(len(Q)))

    return Q, offset  # return the QUBO matrix
