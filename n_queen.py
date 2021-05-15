import pygame
import numpy as np
from random import shuffle

class board:
    def __init__(self, N):
        self.N = N
        self.colors = [(255,255,255), (255,153,204)]
        self.surface_sz = 640
        self.grid_sz = self.surface_sz // self.N
        self.surface_sz = self.N * self.grid_sz
        self.surface = None
        self.queen = pygame.image.load("queen.png")
        self.queen = pygame.transform.scale(self.queen, (self.grid_sz, self.grid_sz))
        self.offset = (self.grid_sz-self.queen.get_width()) // 2

        self.create_board()
    
    def create_board(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.surface_sz, self.surface_sz))

        for row in range(self.N):
            color_ind = row % 2
            for col in range(self.N):
                grid = (col*self.grid_sz, row*self.grid_sz, self.grid_sz, self.grid_sz)
                self.surface.fill(self.colors[color_ind], grid)
                color_ind = (color_ind + 1) % 2
        
        pygame.display.flip()
    
    def place_queen(self, pos):
        x1 = pos[0] * self.grid_sz
        y1 = pos[1] * self.grid_sz
        x2 = (pos[0] + 1) * self.grid_sz
        y2 = (pos[1] + 1) * self.grid_sz

        self.surface.blit(self.queen, (x1+self.offset,y1+self.offset))
        pygame.display.update(x1,y1,x2,y2)
        pygame.event.pump()
        pygame.time.delay(500)
    
    def remove_queen(self, pos):
        x1 = pos[0] * self.grid_sz
        y1 = pos[1] * self.grid_sz
        x2 = (pos[0] + 1) * self.grid_sz
        y2 = (pos[1] + 1) * self.grid_sz
        color_ind = (pos[0] + pos[1]) % 2

        grid = (x1, y1, self.grid_sz, self.grid_sz)
        self.surface.fill(self.colors[color_ind], grid)
        pygame.display.update(x1,y1,x2,y2)
        pygame.event.pump()
        pygame.time.delay(500)

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
