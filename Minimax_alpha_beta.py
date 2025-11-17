import environment
import Heuristic

def Maximize(state, depth, alpha, beta):
    if depth == 0 or state.isTerminal():
        return None, Heuristic.heuristic(state.mat, 1, -1)

    maxChild, maxEval = None, -float('inf')

    for child in state.getChildren(environment.RED):
        _, eval = Minimize(child, depth-1, alpha, beta)
        if eval > maxEval:
            maxChild, maxEval = child, eval

        if maxEval >= beta:
            break
        if maxEval > alpha:
            alpha = maxEval
            
    return maxChild, maxEval


def Minimize(state, depth, alpha, beta):
    if depth == 0 or state.isTerminal():
        return None, Heuristic.heuristic(state.mat, 1, -1)

    minChild, minEval = None, float('inf')

    for child in state.getChildren(environment.YELLOW):
        _, eval = Maximize(child, depth-1, alpha, beta)
        if minEval > eval:
            minChild, minEval = child, eval
        
        if minEval <= alpha:
            break
        if minEval < beta:
            beta = minEval

    return minChild, minEval

def minimax(state, depth):
    child,_ = Maximize(state, depth, -float('inf'), float('inf'))
    return child