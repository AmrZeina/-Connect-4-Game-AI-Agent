import numpy as np
ROWS=6
COLUMNS=7

def heuristic(board, player_piece, opponent_piece):
    score=0

    WEIGHT_THREE=100    #the score for a 3 in a row
    WEIGHT_TWO=10   #the score for a 2 in a row

    center_column=[i for i in list(board[:,board.shape[1]//2])] #to extract the center column
    center_count=center_column.count(player_piece)
    score+=center_count*3

    for window in get_all_windows(board):
        score+=evaluate_window(window,player_piece, opponent_piece, WEIGHT_THREE, WEIGHT_TWO)
    
    return score

def get_all_windows(board):
    windows=[]
    #horizontal windows
    for r in range (ROWS):
        for c in range(COLUMNS-3):  #for 7 columns we have 4 distinct horizontal windows of size 4 
            window=[board[r,c], board[r,c+1], board[r,c+2], board[r,c+3]]
            windows.append(window)
    
    #vertical windows
    for c in range(COLUMNS):
        for r in range (ROWS-3):
            window=[board[r,c], board[r+1,c], board[r+2,c], board[r+3,c]]
            windows.append(window)

    #diagonals \\\\\
    for r in range(3,ROWS):
        for c in range(COLUMNS-3):
            window=[board[r,c], board[r-1,c+1], board[r-2,c+2], board[r-3,c+3]]
            windows.append(window)

    #diagonals /////
    for r in range (ROWS-3):
        for c in range(COLUMNS-3):
            window=[board[r,c], board[r+1,c+1], board[r+2,c+2], board[r+3,c+3]]
            windows.append(window)

    return windows
        

def evaluate_window(window,player_piece, opponent_piece, WEIGHT_THREE, WEIGHT_TWO):
    score=0
    player_count=window.count(player_piece)
    opponent_count=window.count(opponent_piece)
    empty_count=window.count(0)

    if player_count==4:
        score+=1000000000
    elif opponent_count==4:
        score-=1000000000

    elif player_count==3 and empty_count==1:
        score+=WEIGHT_THREE
    elif player_count==2 and empty_count==2:
        score+=WEIGHT_TWO
    
    if opponent_count == 3 and empty_count == 1:
        score -= WEIGHT_THREE*1.5
    elif opponent_count == 2 and empty_count == 2:
        score -= WEIGHT_TWO

    return score





board = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 2, 0, 0, 0],
    [0, 1, 2, 2, 0, 0, 0],
    [1, 2, 2, 1, 0, 0, 0]
])

# Evaluate for player 1
score_player1 = heuristic(board, 1, 2)
print(f"Score for player 1: {score_player1}")

# Evaluate for player 2  
score_player2 = heuristic(board, 2, 1)
print(f"Score for player 2: {score_player2}")

        




