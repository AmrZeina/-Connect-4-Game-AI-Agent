import environment
import Heuristic
import numpy as np

def Expectimax(state, depth):
    best_child, _ = MaxNode(state, depth)
    return best_child

def MaxNode(state, depth):
    if depth == 0 or state.isTerminal():
        return None, Heuristic.heuristic(state.mat, 1, -1)
    max_child = None
    max_eval  = -float('inf')
    valid_cols = get_valid_columns(state)
    for col in valid_cols:
        eval, _ = ChanceNode(state, col, depth, environment.RED)
        if eval > max_eval:
            max_eval  = eval
            max_child = generate_child(state,  environment.RED, col)
    return max_child, max_eval

def MinNode(state, depth):
    if depth == 0 or state.isTerminal():
        return None, Heuristic.heuristic(state.mat, 1, -1)

    min_child = None
    min_eval  = float('inf')
    valid_cols = get_valid_columns(state)
    for col in valid_cols:
        eval, _ = ChanceNode(state, col, depth,  environment.YELLOW)
        if eval < min_eval:
            min_eval  = eval
            min_child = generate_child(state,  environment.YELLOW, col)
    return min_child, min_eval

def ChanceNode(state, chosen_col, depth, piece):
    """
    This node handles randomness:
        - chosen: 0.6
        - left:   0.2
        - right:  0.2
    """
    probabilities = []

    top = state.mat[0]  
    if top[chosen_col] == 0:
        probabilities.append((chosen_col, 0.6))
    # Check left and right
    leftAvailable  = (chosen_col - 1 >= 0 and top[chosen_col - 1] == 0)
    rightAvailable = (chosen_col + 1 < state.cols and top[chosen_col + 1] == 0)

    if leftAvailable and rightAvailable:
        probabilities.append((chosen_col - 1, 0.2))
        probabilities.append((chosen_col + 1, 0.2))

    elif leftAvailable and not rightAvailable:
        probabilities.append((chosen_col - 1, 0.4))

    elif rightAvailable and not leftAvailable:
        probabilities.append((chosen_col + 1, 0.4))

    elif not leftAvailable and not rightAvailable and top[chosen_col] != 0:
        #EVERYTHING is blocked 
        return Heuristic.heuristic(state.mat, 1, -1), None

    expected_value = 0

    for col, prob in probabilities:
        #Create child after piece drops in this column
        child = generate_child(state, piece, col)
        if child is None:  
            val = Heuristic.heuristic(state.mat, 1, -1)
        else:
            next_player =  environment.RED if piece ==  environment.YELLOW else  environment.YELLOW
            if next_player ==  environment.RED:
                _, val = MaxNode(child, depth - 1)
            else:
                _, val = MinNode(child, depth - 1)

        expected_value += prob * val

    return expected_value, None

def generate_child(state, piece, col):
    """Return a NEW child board with piece dropped in col."""
    child = Connect4_clone(state)
    success = child.addPiece(piece, col)
    if not success:
        return None
    return child

def get_valid_columns(state):
    """Return columns that are not full."""
    return [c for c in range(state.cols) if state.mat[0][c] == 0]

def Connect4_clone(state):
    """Deep copy of the Connect4 object."""
    new_state = environment.Connect4()
    new_state.mat = state.mat.copy()
    return new_state
