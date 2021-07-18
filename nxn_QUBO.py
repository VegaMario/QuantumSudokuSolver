from collections import defaultdict
import math


def var_generate(row, col, val):
    return f"{row},{col}_{val}"


# generate the variables for the graph
def gen_graph_var(var, val):
    return f"{var}_{val}"


# Simple implementation of sudoku puzzle as a mathematical graph
# This is not used anymore, so this may be ignored
def gen_nodes_edges_simple(n):
    nodes = []
    edges = []

    for i in range(n):  # every cell in the sudoku is a node of the graph
        for j in range(n):
            nodes.append(str(i) + ',' + str(j))

    # row edges
    for i in range(n):  # nodes next to each other in the same row have an edge connecting them
        for j in range(n - 1):
            edges.append((str(i) + ',' + str(j), str(i) + ',' + str(j + 1)))

    # column edges
    for i in range(n):  # nodes next to each other in the same columns have an edge
        for j in range(n - 1):
            edges.append((str(j) + ',' + str(i), str(j + 1) + ',' + str(i)))

    return nodes, edges


# Complex implementation of sudoku puzzle as a mathematical graph
def gen_nodes_edges_complex(n):
    nodes = []
    edges = []
    m = int(math.sqrt(n))

    for i in range(n):  # every cell of the sudoku is a node
        for j in range(n):
            nodes.append(str(i) + ',' + str(j))

    # row edges
    for i in range(n):  # every cell in a row shares an edge with other cells in the same row
        for j in range(n - 1):
            for jj in range(j + 1, n):
                edges.append((str(i) + ',' + str(j), str(i) + ',' + str(jj)))

    # column edges
    for i in range(n):  # every cell in a col shares an edge with other cells in the same col
        for j in range(n - 1):
            for jj in range(j + 1, n):
                edges.append((str(j) + ',' + str(i), str(jj) + ',' + str(i)))

    for roff in range(m):  # every cell in the same subsqauare shares an edge with others in the same subsquare
        for coff in range(m):
            for i in range(m):
                for j in range(m):
                    for jj in range(j + 1, m):
                        edges.append(
                            (str(i + roff * m) + ',' + str(j + coff * m), str(i + roff * m) + ',' + str(jj + coff * m)))
                    for ii in range(i + 1, m):
                        for jj in range(m):
                            edges.append((str(i + roff * m) + ',' + str(j + coff * m),
                                          str(ii + roff * m) + ',' + str(jj + coff * m)))

    return nodes, edges


# generate the QUBO and take into account the nodes and edges
def gen_QUBO_complex(sudoku_puzzle, nodes, edges, gamma):
    n = len(sudoku_puzzle)
    m = int(math.floor(int(math.sqrt(n))))
    values = [i for i in range(1, n + 1)]
    Q = defaultdict(int)  # the QUBO matrix

    print("Nodes:{}".format(len(nodes)))
    print("Edges:{}".format(len(edges)))

    mn = 1.5

    offset = ((3 + mn) * n**2) * gamma + len(edges) * 2
    # the graph constraint
    for i in nodes:
        for j in range(len(values)):
            varj = gen_graph_var(i, j + 1)
            Q[(varj, varj)] += -1 * gamma * mn  # diagonal terms
            for jj in range(j + 1, len(values)):
                varjj = gen_graph_var(i, jj + 1)
                Q[(varj, varjj)] += 2 * gamma * mn  # off-diagonal

    # the graph objective
    for i in range(len(values)):
        for j, k in edges:
            varj = gen_graph_var(j, i + 1)
            vark = gen_graph_var(k, i + 1)
            Q[(varj, varj)] += -1  # diagonal
            Q[(vark, vark)] += -1  # diagonal
            Q[(varj, vark)] += 2  # off-diagonal

    # The constraints of Sudoku
    for i in range(n):  # no repeating numbers in rows
        for j in range(len(values)):
            for k in range(n):
                variable_k = var_generate(i, k, values[j])
                Q[(variable_k, variable_k)] += -1 * gamma  # diagonal terms
                for l in range(k + 1, n):
                    variable_l = var_generate(i, l, values[j])
                    Q[(variable_k, variable_l)] += 2 * gamma  # off-diagonal terms

    for i in range(n):  # no repeating numbers in cols
        for j in range(len(values)):
            for k in range(n):
                variable_k = var_generate(k, i, values[j])
                Q[(variable_k, variable_k)] += -1 * gamma  # diagonal
                for l in range(k + 1, n):
                    variable_l = var_generate(l, i, values[j])
                    Q[(variable_k, variable_l)] += 2 * gamma  # off-diagonal

    for r_delta in range(m):  # no repeating numbers in the sub squares
        for c_delta in range(m):
            for value in values:
                for i in range(m):
                    for j in range(m):
                        variable_k = var_generate(i + r_delta * m, j + c_delta * m, value)
                        Q[(variable_k, variable_k)] += -1 * gamma  # diagonal
                        for l in range(j + 1, m):
                            variable_l = var_generate(i + r_delta * m, l + c_delta * m, value)
                            Q[(variable_k, variable_l)] += 2 * gamma  # off-diagonal
                        for o in range(i + 1, m):
                            for p in range(m):
                                variable_l = var_generate(o + r_delta * m, p + c_delta * m, value)
                                Q[(variable_k, variable_l)] += 2 * gamma  # off-diagonal
    print("Qubo length: {}".format(len(Q)))
    return Q, offset


# Generate the QUBo matrix but don't take into account the nodes and edges of the graph
# it might just be that the simple case works best for the nxn sudokus
def gen_QUBO_simple(sudoku_puzzle):
    n = len(sudoku_puzzle)
    m = int(math.floor(int(math.sqrt(n))))
    values = [i for i in range(1, n + 1)]
    Q = defaultdict(int)  # the QUBO matrix

    offset = 4 * n**2

    # every cell must have exactly one value
    for i in range(n):
        for j in range(n):
            for k in range(len(values)):
                variable_k = var_generate(i, j, values[k])
                Q[(variable_k, variable_k)] += -1
                for l in range(k + 1, len(values)):
                    variable_l = var_generate(i, j, values[l])
                    Q[(variable_k, variable_l)] += 2

    # no repeating nubmers in rows
    for i in range(n):
        for j in range(len(values)):
            for k in range(n):
                variable_k = var_generate(i, k, values[j])
                Q[(variable_k, variable_k)] += -1
                for l in range(k + 1, n):
                    variable_l = var_generate(i, l, values[j])
                    Q[(variable_k, variable_l)] += 2

    # no repeating nubmers in cols
    for i in range(n):
        for j in range(len(values)):
            for k in range(n):
                variable_k = var_generate(k, i, values[j])
                Q[(variable_k, variable_k)] += -1
                for l in range(k + 1, n):
                    variable_l = var_generate(l, i, values[j])
                    Q[(variable_k, variable_l)] += 2

    # no repeating numbers in sub squares
    for r_delta in range(m):
        for c_delta in range(m):
            for value in values:
                for i in range(m):
                    for j in range(m):
                        variable_k = var_generate(i + r_delta * m, j + c_delta * m, value)
                        Q[(variable_k, variable_k)] += -1
                        for l in range(j + 1, m):
                            variable_l = var_generate(i + r_delta * m, l + c_delta * m, value)
                            Q[(variable_k, variable_l)] += 2
                        for o in range(i + 1, m):
                            for p in range(m):
                                variable_l = var_generate(o + r_delta * m, p + c_delta * m, value)
                                Q[(variable_k, variable_l)] += 2
    print("Qubo length: {}".format(len(Q)))
    return Q, offset