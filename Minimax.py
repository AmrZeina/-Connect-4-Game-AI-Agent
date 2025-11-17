import environment
import Heuristic

#Function to calculate max from children
def Maximize(state, depth): 
    #Check if reached final depth or leave node
    if depth == 0 or state.isTerminal():
        return None, Heuristic.heuristic(state.mat, 1, -1) 

    maxChild, maxEval = None, -float('inf') #Set max to - infinity

    #For every child calculate the heuristic and get max child
    for child in state.getChildren(environment.RED):
        _, eval = Minimize(child, depth-1)
        if eval > maxEval:
            maxChild, maxEval = child, eval
    return maxChild, maxEval


#Function to calculate Min from children
def Minimize(state, depth):
    #Check if reached final depth or leave node
    if depth == 0 or state.isTerminal():
        return None, Heuristic.heuristic(state.mat, 1, -1)

    minChild, minEval = None, float('inf')

    #For every child calculate the heuristic and get min child
    for child in state.getChildren(environment.YELLOW):
        _, eval = Maximize(child, depth-1)
        if minEval > eval:
            minChild, minEval = child, eval
    return minChild, minEval

#The main function which returns the final move
def minimax(state, depth):
    child,_ = Maximize(state, depth)
    return child