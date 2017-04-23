#!/usr/bin/python

#SIZE = 9
SIZE = 19

def copy_list(L):
    M = []
    for item in L:
        M.append(item)
    return M

def copy_board(board):
    newbrd = []
    for row in board:
        newbrd.append(copy_list(row))
    return newbrd

def make_board():
    board = []
    for i in range(SIZE):
        row = [0]*SIZE
        board.append(row)
    return board

def get_neighbors(i,j):
    assert i>=0 and i<SIZE and j>=0 and j<SIZE
    neighbors = [pair for pair in \
            [(i-1,j), (i+1,j), (i,j-1), (i,j+1)] \
            if pair[0] >= 0 and pair[0] < SIZE and \
            pair[1] >= 0 and pair[1] < SIZE]
    return neighbors

def get_group(board_master, i,j):
    # Make a copy... (because I'm going to be messing with it)
    board = copy_board(board_master)

    if board[i][j] == 0:
        return [], []
    color = board[i][j]
    grp = []

    # Liberties
    libs = []

    # Start with a single point
    neighbors = [(i,j)]

    # DEPTH FIRST SEARCH!!!!
    # Assume that everything that makes it into neighbors is the right color
    while neighbors:
        # Pop off the last element
        a,b = neighbors.pop()

        # Put it into grp
        grp.append((a,b))

        # Mark it on the board
        board[a][b] = 0

        # Find the neighbors
        nbd = get_neighbors(a,b)

        # Loop through the neighbors and find the ones of the right color
        for nbr in nbd:
            # The following line would let us find ALL visible adjacencies
            #grp.append(nbr)
            
            # Let's also find the liberties... (neighbors that are 0)
            # Note: Should check board_master rather than board
            #   b/c board gets changed
            if not board_master[nbr[0]][nbr[1]]:
                libs.append(nbr)

            # This will let us continue finding the group
            elif board[nbr[0]][nbr[1]] == color:
                neighbors.append(nbr)

    # Eliminate duplicates from libs
    libs = set(libs)

    return grp, libs

# Define a unique way to produce a group representative
# Steps:
#   Take the top row (lowest y value)
#   Take the leftmost cell in the top row (lowest x value)
def group_rep(grp):
    ymin = 100
    for cell in grp:
        if cell[1] < ymin:
            ymin = cell[1]
    xmin = 100
    for cell in grp:
        if cell[0] < xmin and cell[1] == ymin:
            xmin = cell[0]
    return xmin, ymin

# Gather all the group representatives
def get_all_reps(board_master):
    board = copy_board(board_master)

    reps = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j]:
                grp,libs = get_group(board, i,j)
                for node in grp:
                    board[node[0]][node[1]] = 0
                rep = group_rep(grp)
                reps.append(rep)
    return reps






def test():
    B = make_board()
    B[3][4] = 1
    B[4][4] = 1
    B[5][4] = 1

    print get_group(B, 3, 4)



if __name__ == '__main__':
    test()
