import pygame
from random import shuffle
from board import board


def print_board(num_cb):
    for row in num_cb:
        print('\t', end='')
        for val in row:
            if val == 0:
                print('_', end=' ')
            if val == 1:
                print('Q', end=' ')
        print()

def is_safe(num_cb, row, col):
    N = len(num_cb)
    for i in range(N):
        if num_cb[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if num_cb[i][j] == 1:
            return False
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if num_cb[i][j] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, N, 1)):
        if num_cb[i][j] == 1:
            return False
    for i, j in zip(range(row, N, 1), range(col, N, 1)):
        if num_cb[i][j] == 1:
            return False
    
    return True

def solver(num_cb, cb, cols, col, seq):
    N = len(num_cb)
    if col == N:
        return True
    
    rows = [i for i in range(N)]
    shuffle(rows)

    col_index = str(cols[col]+1)
    if col == 0:
        seq += col_index
    else:
        seq += '-' + col_index

    print('\n >> placing queen in column {} \t\tsequence: {}'.format(cols[col]+1, seq))

    for row in rows:
        if is_safe(num_cb, row, cols[col]):
            num_cb[row][cols[col]] = 1
            cb.place_queen((cols[col], row))

            row_index = '(' + str(row+1) + ')'
            seq += row_index
            print('    ++ row {} selected \t\t\tsequence: {}'.format(row+1, seq))
            print_board(num_cb)

            if solver(num_cb, cb, cols, col+1, seq) == True:
                return True
            
            num_cb[row][cols[col]] = 0
            cb.remove_queen((cols[col], row))

            seq = seq[:-(len(row_index))]
            print('\n >> placing queen in column {} \t\tsequence: {}'.format(cols[col]+1, seq))
    
    seq = seq[:-(len(col_index)+1)]
    print('    -- no feasible place, backtracking \tsequence: {}'.format(seq))
    
    return False

def backtracking(num_cb, cb):
    N = len(num_cb)
    cols = [i for i in range(N)]
    shuffle(cols)

    seq = ''

    if solver(num_cb, cb, cols, 0, seq) == False:
        print('Solution does not exist!')
        return False
    
    print('\n********** final solution **********')
    print_board(num_cb)

    return True


if __name__ == "__main__":
    N = int(input("Enter the size of chess board\n"))
    cb = board(N)
    num_cb = [[0] * N for _ in range(N)]
    print_board(num_cb)

    finished = False

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        
        if not finished:
            if backtracking(num_cb, cb):
                finished = True
    
    pygame.quit()
