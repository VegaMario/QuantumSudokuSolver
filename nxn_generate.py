import random
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# credit for this sudoku generator goes to  Emma Hogan (https://github.com/roonil-wazlib)
# I only modified her code slightly to be able to generate sudoku puzzles of arbitrary size


def generate_ordered_2d_board(n):
    """ Generate an unshuffled 2d sudoku board """
    board = []

    for i in range(n):
        for j in range(n):
            board.append([((x + i) + n * j) % n ** 2 + 1 for x in range(n ** 2)])

    return board


def generate_shuffled_2d_board(n):
    """ Generate a 'random' 2D Sudoku board """

    ordered = generate_ordered_2d_board(n)
    columns_shuffled = shuffle_columns(ordered)
    # rows_shuffled = shuffle_rows(columns_shuffled)
    relabeled = relabel_values(columns_shuffled)

    return relabeled


def shuffle_columns(board):
    """ Shuffle the columns of a 2D board"""
    shuffled = []
    column_group_order = [n for n in range(int(math.sqrt(len(board))))]
    random.shuffle(column_group_order)
    for i in column_group_order:
        # shuffle columns within each of the 3 column groups
        column_order = [n for n in range(int(math.sqrt(len(board))))]
        random.shuffle([n for n in range(int(math.sqrt(len(board))))])
        for j in column_order:
            shuffled.append(board[int(math.sqrt(len(board))) * i + j])

    return shuffled


def relabel_values(board):
    """makes the board look more random but actually just produces the same board (isomorphic by relabelling)"""
    values = [n for n in range(1, len(board) + 1)]
    random.shuffle(values)

    output = []

    for x in board:
        col = []
        for y in x:
            col.append(values[y - 1])
        output.append(col)

    return output


# used for filling in the puzzle with empty spots, represented as 0s
def coordinate_map(sudoku, blanks_num):
    coord_list = []
    # make a list of coordinates
    n = len(sudoku)
    for i in range(n):
        for j in range(n):
            coord_list.append(var_gen(i, j))
    coord_map = set(coord_list)

    # empty random coordinates
    for i in range(blanks_num):
        coord = random.choice(coord_list)
        row, col = map(int, coord.split(','))
        sudoku[row][col] = 0
        coord_map.remove(coord)
        coord_list = list(coord_map)


# this formate will be used for the coordinates of the puzzle
def var_gen(row, col):
    return f"{row},{col}"


# Print the result on the screen
def print_result(sudoku_puzzle):
    copy = sudoku_puzzle
    for row in copy:  # print the results
        for val in row:
            sys.stdout.write(str(val) + "\t")
        print()


# create a txt file to store the puzzle
def write_file(name, sudoku):
    f = open(name + ".txt", "w+")
    for row in sudoku:  # print the results
        for val in row:
            f.write(str(val) + "\t")
        f.write("\n")


# generate a puzzle of size n with blanks_num number of blanks
def gen_nxn(n, blanks_num):
    name = "{}x{}".format(n, n)
    board = generate_shuffled_2d_board(int(math.sqrt(n)))
    coordinate_map(board, blanks_num)
    write_file(name, board)
    print('----------The following nxn sudoku game has been generated into the {}.txt file: ----------'.format(name))
    print_result(board)
    return name + ".txt"
