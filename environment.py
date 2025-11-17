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

    def addPeice(self, type, row, col):
        if self.mat[row][col] == 0:
            if type == RED:
                self.mat[row][col] = 1
            else :
                self.mat[row][col] = -1
        else :
            print("Error: Slot is not empty!")

    def getChildren(self, type):
        children = []
        for i in range (self.cols):
            for j in range(self.rows-1 , -1 , -1):
                if self.mat[j][i] == 0:
                    child = self.mat.copy()
                    if type == RED:
                        child[j][i] = 1
                    else:
                        child[j][i] = -1
                    children.append(child)
                    break
        return children