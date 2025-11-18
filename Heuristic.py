ROWS = 6
COLUMNS = 7
WINDOWS = []

def init_windows():
    global WINDOWS
    
    # Calculating all windows (direction, positions)
    for r in range(ROWS):
        for c in range(COLUMNS-3):  #for 7 columns we have 4 distinct horizontal windows of size 4 
            WINDOWS.append(('H', [(r,c), (r,c+1), (r,c+2), (r,c+3)]))
    
    #vertical windows
    for c in range(COLUMNS):
        for r in range (ROWS-3):
            WINDOWS.append(('V', [(r,c), (r+1,c), (r+2,c), (r+3,c)]))
    
    #diagonals positive /////
    for r in range (ROWS-3):
        for c in range(COLUMNS-3):
            WINDOWS.append(('P', [(r,c), (r+1,c+1), (r+2,c+2), (r+3,c+3)]))
    
    #diagonals negative \\\\\
    for r in range(3,ROWS):
        for c in range(COLUMNS-3):
            WINDOWS.append(('N', [(r,c), (r-1,c+1), (r-2,c+2), (r-3,c+3)]))

init_windows()

def heuristic(board, player, opponent):
    score = 0
    player_threats = 0
    opponent_threats = 0
    
    # Compute the player pieces in the center column and add 3 points to each
    center = COLUMNS // 2
    for r in range(ROWS):
        if board[r][center] == player:
            score += 3
   
    for direction, positions in WINDOWS:
        # Extract the 4 cell values using the precomputed positions
        c0 = board[positions[0][0]][positions[0][1]]
        c1 = board[positions[1][0]][positions[1][1]] 
        c2 = board[positions[2][0]][positions[2][1]]
        c3 = board[positions[3][0]][positions[3][1]]
        
        # Manual counting as it is faster than .count()
        p_count = (c0 == player) + (c1 == player) + (c2 == player) + (c3 == player)
        o_count = (c0 == opponent) + (c1 == opponent) + (c2 == opponent) + (c3 == opponent)
        empty = 4 - p_count - o_count
        
        # Evaluating the window score based on the pieces count
        if p_count == 4:
            score += 10000
        elif o_count == 4:
            score -= 10000
        elif p_count == 3 and empty == 1:
            if is_playable(board, positions, direction):
                score += 150
                player_threats += 1
            else:
                score += 100
                player_threats += 1
        elif p_count == 2 and empty == 2:
            score += 10
        elif o_count == 3 and empty == 1:
            if is_playable(board, positions, direction):
                score -= 200
                opponent_threats += 1
            else:
                score -= 100
                opponent_threats += 1
        elif o_count == 2 and empty == 2:
            score -= 10
    
    # Evaluating Multiple threats (if there exist more than 2 threats, we must add a large penalty +/-)
    if opponent_threats >= 2:
        score -= 1000
    if player_threats >= 2:
        score += 800
    
    return score

def is_playable(board, positions, direction):
    # Vertical threats are always playable as the empty cell is at the top
    if direction == 'V':
        return True
    
    # Finding empty cell position
    for r, c in positions:
        if board[r][c] == 0:
            empty_r, empty_c = r, c
            break
    
    # Checking if the position is playable or not (in bottom row or has piece below)
    return empty_r == 0 or board[empty_r - 1][empty_c] != 0