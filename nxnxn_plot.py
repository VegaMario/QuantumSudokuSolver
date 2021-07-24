import matplotlib.pyplot as plt
import math


# function used for plotting the solution obtained, using matplotlib
def plot_3D_sudoku(sudoku, result):
    n = len(sudoku) # size of the sudoku puzzle
    values = [i for i in range(0, n + 1)] # the possible values that may go in a cell
    fig = plt.figure(figsize=(8, 8))  # figure
    fig.set_size_inches(8, 8)
    ax = fig.add_subplot(111, projection='3d') # 3d plot

    lays = [] # layers
    rows = [] # rows
    cols = [] # columns
    vals = [] # values

    # Filling in lists in such a way that allows me to plot the results in the orientation I want
    for i in range(n):
        for j in range(n):
            for k in range(n):
                lays.append(n - 1 - i) # reversing the order of layer coordinates
                rows.append(n - 1 - j) # reversing the order of row coordinates
                cols.append(k)
                vals.append(sudoku[i][j][k])

    for i in range(n**3):
        ax.text3D(x=cols[i], y=lays[i], z=rows[i], s=str(vals[i]))

    # just making some adjustments to the plot to make it easier to understand
    ax.set_xlim(0, n - 1)
    ax.set_ylim(0, n - 1)
    ax.set_zlim(0, n - 1)

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_zticks(range(n))
    if result == "":
        ax.set_title('The 3D solver will attempt to solve the {}x{}x{} Sudoku (close window)'.format(n, n, n), fontsize=16)
    else:
        ax.set_title("{} Solution of the {}x{}x{} Sudoku".format(result.capitalize(), n, n, n))
    ax.set_xlabel("Y")
    ax.set_ylabel("X")
    ax.set_zlabel("Z")

    ax.xaxis.set_ticklabels([i for i in range(n)])
    ax.yaxis.set_ticklabels([n - 1 - i for i in range(n)])
    ax.zaxis.set_ticklabels([n - 1 - i for i in range(n)])

    # show the plot
    plt.show()

    # make some new plots for individual 2d layers. n layers in yz, xz, and xy planes, making 3n in total
    m = int(math.sqrt(n))

    fig = plt.figure(figsize=(n, n)) # new plot
    fig.set_size_inches(8, 8)

    # generating the plot for showing the n layers in the yz planes (X direction)
    nlays, nrows, ncols, nvals = re_order(lays, rows, cols, vals, n, 1)
    for i in range(n):
        ax = fig.add_subplot(m, m, 1 + i)
        if n == 4:
            img = plt.imread("sudok4.png")
            ax.imshow(img, extent=[-0.5, n - 0.5, -0.5, n - 0.5])
        elif n == 9:
            img = plt.imread("sudok.png")
            ax.imshow(img, extent=[-1, n, -1, n])
        for j in range(n**2):
            ax.text(x=ncols[i][j], y=nrows[i][j], s=str(nvals[i][j]))
        ax.set_title("Layer X = {}".format(i), y=1.05, fontsize=8)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.axis('off')

    fig.suptitle('X direction layers: {} in total'.format(n), fontsize=16)

    plt.show() # show the plot

    fig = plt.figure(figsize=(n, n)) # new plot
    fig.set_size_inches(8, 8)

    # generating the plot for showing the n layers in the xz planes (Y direction)
    nlays, nrows, ncols, nvals = re_order(cols, rows, lays, vals, n, 0)

    for i in range(n):
        ax = fig.add_subplot(m, m, 1 + i)
        if n == 4:
            img = plt.imread("sudok4.png")
            ax.imshow(img, extent=[-0.5, n - 0.5, -0.5, n - 0.5])
        elif n == 9:
            img = plt.imread("sudok.png")
            ax.imshow(img, extent=[-1, n, -1, n])
        for j in range(n**2):
            ax.text(x=ncols[i][j], y=nrows[i][j], s=str(nvals[i][j]))
        ax.set_title("Layer Y = {}".format(i), y=1.05, fontsize=8)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.axis('off')

    fig.suptitle('Y direction layers: {} in total'.format(n), fontsize=16)

    plt.show() # show the plot

    fig = plt.figure(figsize=(n, n)) # new plot
    fig.set_size_inches(8, 8)

    # generating the plot for showing the n layers in the xy planes (Z direction)
    nlays, nrows, ncols, nvals = re_order(rows, lays, cols, vals, n, 1)

    for i in range(n):
        ax = fig.add_subplot(m, m, 1 + i)
        if n == 4:
            img = plt.imread("sudok4.png")
            ax.imshow(img, extent=[-0.5, n - 0.5, -0.5, n - 0.5])
        elif n == 9:
            img = plt.imread("sudok.png")
            ax.imshow(img, extent=[-1, n, -1, n])
        for j in range(n**2):
            ax.text(x=ncols[i][j], y=nrows[i][j], s=str(nvals[i][j]))
        ax.set_title("Layer Z = {}".format(i), y=1.05, fontsize=8)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.axis('off')

    fig.suptitle('Z direction layers: {} in total'.format(n), fontsize=16)

    plt.show() # show the plot


# used to reorder the solution lists in order to prepare for plotting
# I'm just manipulating the lists in order to allow me to implement a legend with colors
# What I'm trying to do is group coordinates together that share a common value.
def re_order(lays, rows, cols, vals, n, rev):
    nlays = [] # new layers
    nrows = [] # new rows
    ncols = [] # new columns
    nvals = [] # new values

    # make new lists that contains lists of individual layer coordinates
    for i in range(n):
        nl = []
        nr = []
        nc = []
        nv = []

        is_rev = i

        if rev:
            is_rev = n - 1 - i

        for j in range(n ** 3):
            if lays[j] == is_rev:
                nl.append(lays[j])
                nr.append(rows[j])
                nc.append(cols[j])
                nv.append(vals[j])

        nlays.append(nl)
        nrows.append(nr)
        ncols.append(nc)
        nvals.append(nv)

    ''' -- example
    -- original lists
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0]
    [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    -- n lists
    [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    [[3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0], [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0], [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0], [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0]]
    [[0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3], [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3], [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3], [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]]
    '''

    return nlays, nrows, ncols, nvals
