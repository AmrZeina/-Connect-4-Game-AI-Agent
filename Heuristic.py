import numpy as np
ROWS=6
COLUMNS=7

def heuristic(board, player_piece, opponent_piece):
    score=0

    WEIGHT_THREE=100    #the score for a 3 in a row
    WEIGHT_TWO=10   #the score for a 2 in a row

    center_column=[i for i in list(board[:,COLUMNS//2])] #to extract the center column
    center_count=center_column.count(player_piece)
    score+=center_count*3

    player_threats=0
    opponent_threats=0

    for window_data in get_all_windows(board):
        cells=window_data['cells']
        start_pos=window_data['start_pos']
        direction=window_data['direction']

        window_score,window_player_threat,window_opponent_threat=evaluate_window(board, cells, start_pos, direction, player_piece, opponent_piece, WEIGHT_THREE, WEIGHT_TWO)
        score+=window_score
      
        #Evaluating Multiple threats(The next step will be a win definitely)
        if window_player_threat:
            player_threats += 1
        if window_opponent_threat:
            opponent_threats += 1
    #if there exist more than 2 threats, we must add a large penalty +/-
    if opponent_threats>=2:
        score-=WEIGHT_THREE*10
    if player_threats>=2:
        score+=WEIGHT_THREE*8

    
    return score


def get_all_windows(board):
    windows=[]  #list of dictionaries
    #horizontal windows
    for r in range (ROWS):
        for c in range(COLUMNS-3):  #for 7 columns we have 4 distinct horizontal windows of size 4 
            windows.append({
                'cells': [board[r,c], board[r,c+1], board[r,c+2], board[r,c+3]],
                'start_pos': (r,c),
                'direction': 'horizontal'
            })       

    #vertical windows
    for c in range(COLUMNS):
        for r in range (ROWS-3):
            windows.append({
                'cells': [board[r,c], board[r+1,c], board[r+2,c], board[r+3,c]],
                'start_pos': (r,c),
                'direction': 'vertical'
            })    

    #diagonals \\\\\
    for r in range(3,ROWS):
        for c in range(COLUMNS-3):
            windows.append({
                'cells': [board[r,c], board[r-1,c+1], board[r-2,c+2], board[r-3,c+3]],
                'start_pos': (r,c),
                'direction': 'diagonal_negative'
            })    

    #diagonals /////
    for r in range (ROWS-3):
        for c in range(COLUMNS-3):
            windows.append({
                'cells': [board[r,c], board[r+1,c+1], board[r+2,c+2], board[r+3,c+3]],
                'start_pos': (r,c),
                'direction': 'diagonal_positive'
            })    

    return windows
        

def evaluate_window(board, cells, start_pos, direction, player_piece, opponent_piece, WEIGHT_THREE, WEIGHT_TWO):
    score=0
    player_count=cells.count(player_piece)
    opponent_count=cells.count(opponent_piece)
    empty_count=cells.count(0)

    player_threat=False
    opponent_threat=False

    if player_count==4:
        score+=1000000000
    elif opponent_count==4:
        score-=1000000000

    if player_count==3 and empty_count==1:
        if playable_threat(board, cells, start_pos, direction):
            score += WEIGHT_THREE*1.5
            player_threat=True
        else:
            score += WEIGHT_THREE
            player_threat=True
    elif player_count==2 and empty_count==2:
        score+=WEIGHT_TWO
    
    if opponent_count == 3 and empty_count == 1:
        if playable_threat(board, cells, start_pos, direction):
            score -= WEIGHT_THREE*2
            opponent_threat=True
        else:
            score -= WEIGHT_THREE
            opponent_threat=True       
    elif opponent_count == 2 and empty_count == 2:
        score -= WEIGHT_TWO

    return score,player_threat,opponent_threat



def playable_threat(board, cells, start_pos, direction):
    #finding empty cell position within the window
    r,c=start_pos
    window_empty_position=None
    board_empty_position= (0,0)

    for i in range (len(cells)):
        if cells[i]==0:
            window_empty_position=i
            break

    #finding empty cell position within the board
    #horizontal
    if direction =='horizontal':
        board_empty_position=(r , c+window_empty_position)
    #vertical
    if direction == 'vertical':     #always playable as the empty cell is at the top
        return True
    # diaonal
    if direction =='diagonal_positive':
        board_empty_position= (r+window_empty_position , c+window_empty_position)
    elif direction == 'diagonal_negative':
        board_empty_position= (r-window_empty_position , c+window_empty_position)

    #chencking if the position is playable or not
    empty_r, empty_c = board_empty_position
    if empty_r == 0:
        return True
    elif board[empty_r - 1 , empty_c ] !=0:
        return True
    else: 
        return False
    


"""
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
"""