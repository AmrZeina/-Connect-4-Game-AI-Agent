import numpy as np

RED = 1
YELLOW = -1

class Connect4 ():
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.mat = np.zeros((self.rows, self.cols) , dtype=int)

    def print_board(self):
        print(self.mat)

