import random
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import nxn_generate

# credit for this sudoku generator goes to  Emma Hogan (https://github.com/roonil-wazlib)
# I only modified her code slightly to be able to generate sudoku puzzles of arbitrary size


def shuffle_cube(cube):
    """shuffle the columns around within the 3D implementation"""
    shuffled = []
    column_group_order = [n for n in range(int(math.sqrt(len(cube))))]
    random.shuffle(column_group_order)
    for i in column_group_order:
        # shuffle columns within each of the 3 column groups
        column_order = [n for n in range(int(math.sqrt(len(cube))))]
        random.shuffle([n for n in range(int(math.sqrt(len(cube))))])
        for j in column_order:
            shuffled.append(cube[int(math.sqrt(len(cube))) * i + j])

    return shuffled


def generate_3d_board(n):
    """generate 3D cube from 2D board"""
    layer = nxn_generate.generate_shuffled_2d_board(n)
    cube = []
    for i in range(len(layer)):
        new_layer = []
        for column in layer:
            new_column = []
            # this nested mess is to ensure that none of the sub 3x3 squares violates sudoku rules from any x y or z
            # perspective (also the Latin Square rules but the subsquares are trickier and the cause of more mess)
            for j in range(int(math.sqrt(len(layer)))):
                for k in range(int(math.sqrt(len(layer)))):
                    # lot of 3 = (i+j) % 3
                    # index within lot = (i + k + (i//3)) % 3
                    new_column.append(column[int(math.sqrt(len(layer))) * ((i + j) % int(math.sqrt(len(layer)))) + (
                            i + k + (i // int(math.sqrt(len(layer))))) % int(math.sqrt(len(layer)))])
            new_layer.append(new_column)
        cube.append(new_layer)

    return shuffle_cube(cube)


def print_result(sudoku):
    copy = sudoku  # make a copy of the sudoku puzzle
    n = int(len(copy))

    # print and check the layers in the x-direction planes
    for i in range(n):
        for j in range(n):
            for k in range(n):
                sys.stdout.write(str(copy[i][j][k]) + "\t")
            print()
        print()

# store the sudoku puzzle into a txt file
def write_file(name, sudoku):
    n = len(sudoku)
    f = open(name + ".txt", "w+")

    for i in range(n):
        for j in range(n):
            for k in range(n):
                f.write(str(sudoku[i][j][k]) + "\t")
            f.write("\n")
        f.write("\n")


# used for placing a number empty spots on the sudoku puzzle
def coordinate_map(sudoku, blanks_num):
    coord_list = []
    # making a list of coordinates
    n = len(sudoku)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                coord_list.append(var_gen(i, j, k))
    coord_map = set(coord_list)

    # filling random spots in the sudoku puzzle with empty spots, represented as 0s
    for i in range(blanks_num):
        coord = random.choice(coord_list)
        lay, row, col = map(int, coord.split(','))
        sudoku[lay][row][col] = 0
        coord_map.remove(coord)
        coord_list = list(coord_map)


# format that will be used for the coordinates
def var_gen(lay, row, col):
    return f"{lay},{row},{col}"


# generate a puzzle of size n with blanks_num number of blanks
def gen_nxnxn(n, blanks_num):
    name = "{}x{}x{}".format(n, n, n)
    board = generate_3d_board(int(math.sqrt(n)))
    coordinate_map(board, blanks_num)
    write_file(name, board)
    print('The following nxnxn sudoku game has been generated into the {}.txt file: '.format(name))
    print_result(board)
    return name + ".txt"
