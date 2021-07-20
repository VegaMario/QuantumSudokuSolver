import matplotlib.pyplot as plt
import math


# function used for plotting the solution obtained, using matplotlib
def plot_2D_sudoku(sudoku, result):
    n = len(sudoku)  # size of the sudoku puzzle
    values = [i for i in range(0, n + 1)]  # the possible values that may go in a cell

    rows = []  # rows
    cols = []  # columns
    vals = []  # values

    # Filling in lists in such a way that allows me to plot the results in the orientation I want
    for j in range(n):
        for k in range(n):
            rows.append(n - 1 - j)  # reversing the order of row coordinates
            cols.append(k)
            vals.append(sudoku[j][k])

    fig = plt.figure(figsize=(n, n))  # new plot
    fig.set_size_inches(8, 8)
    # place a sudoku grid on a subplot and fill in the digits in the cells
    ax = fig.add_subplot(111)
    if n == 4:
        img = plt.imread("sudok4.png")
        ax.imshow(img, extent=[-0.5, n-0.5, -0.5, n-0.5])
    elif n == 9:
        img = plt.imread("sudok.png")
        ax.imshow(img, extent=[-1, n, -1, n])
    elif n == 16:
        img = plt.imread("sudok16.png")
        ax.imshow(img, extent=[-1.5, n+1.2, -1.5, n+0.9])
    elif n == 25:
        img = plt.imread("sudok25.png")
        ax.imshow(img, extent=[-0.3, n, -0.3, n])
    # filling in the digits into the cells of the plot
    for j in range(n ** 2):
        ax.text(x=cols[j], y=rows[j], s=str(vals[j]))
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.axis('off')

    fig.suptitle('{} Solution of the {}x{} Sudoku'.format(result, n, n), fontsize=16)

    plt.show()  # show the plot
