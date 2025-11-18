import copy

RED = 1
YELLOW = -1
ROWS = 6
COLS = 7 

class Connect4 ():
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.mat = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def print_board(self):
        print(self.mat)
    
    def isTerminal(self):
        return all(self.mat[0][c] != 0 for c in range(self.cols))

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
                    child.mat = copy.deepcopy(self.mat)
                    child.mat[j][i] = type
                    children.append(child)
                    break
        return children