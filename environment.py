import numpy as np

RED = 1
YELLOW = -1
ROWS = 6
COLS = 7 

class Connect4 ():
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.mat = np.zeros((self.rows, self.cols) , dtype=int)

    def print_board(self):
        print(self.mat)
    
    def isTerminal(self):
        return np.all(self.mat[0] != 0)

    def addPiece(self, piece, col):
        for row in range(self.rows - 1, -1, -1):
            if self.mat[row][col] == 0:
                self.mat[row][col] = piece
                return True
        return False

    def getChildren(self, type):
        children = []
        for i in range (self.cols):
            for j in range(self.rows-1 , -1 , -1):
                if self.mat[j][i] == 0:
                    child = Connect4()
                    child.mat = self.mat.copy()
                    if type == RED:
                        child.mat[j][i] = 1
                    else:
                        child.mat[j][i] = -1
                    children.append(child)
                    break
        return children