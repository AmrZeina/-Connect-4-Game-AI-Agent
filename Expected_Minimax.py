import environment
import Heuristic
import copy

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
            max_child = generate_child(state, environment.RED, col)

    return max_child, max_eval

def MinNode(state, depth):
    if depth == 0 or state.isTerminal():
        return None, Heuristic.heuristic(state.mat, 1, -1)
    min_child = None
    min_eval  = float('inf')
    valid_cols = get_valid_columns(state)
    for col in valid_cols:
        eval, _ = ChanceNode(state, col, depth, environment.YELLOW)
        if eval < min_eval:
            min_eval  = eval
            min_child = generate_child(state, environment.YELLOW, col)

    return min_child, min_eval

def ChanceNode(state, chosenCol, depth, piece):
    probabilities = []
    top = state.mat[0]  
    # 0.6 probability for chosen column if not full
    if top[chosenCol] == 0:
        probabilities.append((chosenCol, 0.6))
    # Left - right availability
    leftAvailable  = (chosenCol - 1 >= 0 and top[chosenCol - 1] == 0)
    rightAvailable = (chosenCol + 1 < state.cols and top[chosenCol + 1] == 0)
    if leftAvailable and rightAvailable:
        probabilities.append((chosenCol - 1, 0.2))
        probabilities.append((chosenCol + 1, 0.2))
    elif leftAvailable and not rightAvailable:
        probabilities.append((chosenCol - 1, 0.4))
    elif rightAvailable and not leftAvailable:
        probabilities.append((chosenCol + 1, 0.4))
    # all blocked
    elif not leftAvailable and not rightAvailable and top[chosenCol] != 0:
        return Heuristic.heuristic(state.mat, 1, -1), None

    expected_value = 0

    for col, prob in probabilities:

        child = generate_child(state, piece, col)

        if child is None:
            # Column is full
            val = Heuristic.heuristic(state.mat, 1, -1)

        else:
            next_player = environment.RED if piece == environment.YELLOW else environment.YELLOW

            if next_player == environment.RED:
                _, val = MaxNode(child, depth - 1)
            else:
                _, val = MinNode(child, depth - 1)

        expected_value += prob * val

    return expected_value, None

def generate_child(state, piece, col):
    child = Connect4_clone(state)
    success = child.addPiece(piece, col)

    if not success:
        return None
    return child


def get_valid_columns(state):
    return [c for c in range(state.cols) if state.mat[0][c] == 0]


def Connect4_clone(state):
    new_state = environment.Connect4()
    new_state.mat = copy.deepcopy(state.mat)
    return new_state
