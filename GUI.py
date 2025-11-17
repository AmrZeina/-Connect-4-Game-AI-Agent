import pygame
import sys
import time
import environment as env
import Heuristic
import Minimax                
import Minimax_alpha_beta     
import Expected_Minimax       


pygame.init()
ROWS = env.ROWS
COLS = env.COLS

SQUARE_SIZE = 90
RADIUS = int(SQUARE_SIZE / 2 - 6)
WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE
WINDOW_SIZE = (WIDTH, HEIGHT)

#Colors
BLUE = (30, 80, 200)
BLACK = (0, 0, 0)
RED_COLOR = (220, 40, 40)
YELLOW_COLOR = (240, 220, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 180, 0)
LIGHT_BLUE = (100, 150, 255)

FONT = pygame.font.SysFont("monospace", 20)
SMALL_FONT = pygame.font.SysFont("monospace", 16)
TREE_FONT = pygame.font.SysFont("monospace", 12)


class Connect4GUI:
    def __init__(self, algorithm, depth):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Connect-4 AI Agent")

        self.reset(algorithm, depth)

    def reset(self, algorithm, depth):
        self.game = env.Connect4()
        self.started = True

        self.depth = depth
        self.ai_algorithm = algorithm   #minimax / alpha-beta / expectimax

        #Human plays first with YELLOW, AI plays with RED
        self.human_piece = env.YELLOW
        self.ai_piece = env.RED

        self.last_ai_msg = ""
        self.running = True
        self.game_over = False
        self.winner = None
        self.human_score = 0
        self.ai_score = 0
        self.show_tree = False
        self.tree_nodes = []

    def draw_board(self):
        #Clear entire screen with white background
        self.screen.fill(WHITE)
        
        #Draw header section with white background
        header_rect = pygame.Rect(0, 0, WIDTH, SQUARE_SIZE)
        pygame.draw.rect(self.screen, WHITE, header_rect)
        
        #Draw header text with black color
        algorithm_text = FONT.render(f"Algorithm: {self.ai_algorithm}", True, BLACK)
        depth_text = FONT.render(f"Depth: {self.depth}", True, BLACK)
        
        self.screen.blit(algorithm_text, (10, 10))
        self.screen.blit(depth_text, (WIDTH - 120, 10))

        if self.game_over:
            if self.winner == "human":
                status = SMALL_FONT.render(f"Game Over - HUMAN WINS! {self.human_score}-{self.ai_score} Press SPACE to restart", True, BLACK)
            elif self.winner == "ai":
                status = SMALL_FONT.render(f"Game Over - AI WINS! {self.ai_score}-{self.human_score} Press SPACE to restart", True, BLACK)
            else:
                status = SMALL_FONT.render(f"Game Over - DRAW! {self.human_score}-{self.ai_score} Press SPACE to restart", True, BLACK)
        else:
            status = SMALL_FONT.render("Human (YELLOW) vs AI (RED) - Your turn (T=Toggle Tree)", True, BLACK)
        
        self.screen.blit(status, (10, 40))

        if self.last_ai_msg:
            info = SMALL_FONT.render(self.last_ai_msg, True, BLACK)
            self.screen.blit(info, (10, 60))

        #Board squares
        for c in range(COLS):
            for r in range(ROWS):
                #Draw blue square for board
                pygame.draw.rect(
                    self.screen, BLUE,
                    (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )
                #Draw white circle for empty slot
                pygame.draw.circle(
                    self.screen, WHITE,
                    (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                     int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)),
                    RADIUS
                )

        #Draw game pieces
        for c in range(COLS):
            for r in range(ROWS):
                val = self.game.mat[r][c]
                if val == env.RED:
                    color = RED_COLOR
                elif val == env.YELLOW:
                    color = YELLOW_COLOR
                else:
                    continue

                pygame.draw.circle(
                    self.screen, color,
                    (c * SQUARE_SIZE + SQUARE_SIZE // 2,
                     (r + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                    RADIUS
                )

        pygame.display.update()

    def draw_tree_panel(self):
        """Draw tree visualization panel"""
        if not self.show_tree or not self.tree_nodes:
            return

        # Create a surface for the tree panel
        tree_width = 400
        tree_height = 500
        tree_surface = pygame.Surface((tree_width, tree_height))
        tree_surface.fill(WHITE)
        
        pygame.draw.rect(tree_surface, BLACK, (0, 0, tree_width, tree_height), 2)
        
        title = TREE_FONT.render("MINIMAX TREE VISUALIZATION", True, BLACK)
        tree_surface.blit(title, (10, 10))
        
        y_offset = 40
        for i, node in enumerate(self.tree_nodes[:15]):  #Limit to 15 nodes for display
            if y_offset > tree_height - 30:
                break
                
            node_color = GREEN if node['selected'] else LIGHT_BLUE
            pygame.draw.rect(tree_surface, node_color, (10, y_offset, tree_width - 20, 30))
            pygame.draw.rect(tree_surface, BLACK, (10, y_offset, tree_width - 20, 30), 1)
            
            node_text = f"Col {node['col']}: H={node['heuristic']:.1f}"
            text_surface = TREE_FONT.render(node_text, True, BLACK)
            tree_surface.blit(text_surface, (15, y_offset + 8))
            
            y_offset += 35
        
        #Draw info about total nodes
        info_text = f"Showing {min(len(self.tree_nodes), 15)} of {len(self.tree_nodes)} nodes"
        info_surface = TREE_FONT.render(info_text, True, BLACK)
        tree_surface.blit(info_surface, (10, tree_height - 20))
        
        #Blit tree surface to main screen
        self.screen.blit(tree_surface, (WIDTH - tree_width - 10, SQUARE_SIZE + 10))

    def human_move(self, x):
        col = int(x // SQUARE_SIZE)
        if col < 0 or col >= COLS:
            return False
        return self.game.addPiece(self.human_piece, col)

    def count_connected_fours(self, piece):
        """Count all connected fours for the given piece"""
        board = self.game.mat
        count = 0
        
        #Check horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if (board[r][c] == piece and 
                    board[r][c+1] == piece and 
                    board[r][c+2] == piece and 
                    board[r][c+3] == piece):
                    count += 1
        
        #Check vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                if (board[r][c] == piece and 
                    board[r+1][c] == piece and 
                    board[r+2][c] == piece and 
                    board[r+3][c] == piece):
                    count += 1
        
        #Check diagonal positive (\)
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if (board[r][c] == piece and 
                    board[r+1][c+1] == piece and 
                    board[r+2][c+2] == piece and 
                    board[r+3][c+3] == piece):
                    count += 1
        
        #Check diagonal negative (/)
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if (board[r][c] == piece and 
                    board[r-1][c+1] == piece and 
                    board[r-2][c+2] == piece and 
                    board[r-3][c+3] == piece):
                    count += 1
        
        return count

    def determine_winner(self):
        """Count connected fours for both players and determine winner"""
        self.human_score = self.count_connected_fours(self.human_piece)
        self.ai_score = self.count_connected_fours(self.ai_piece)
        
        if self.human_score > self.ai_score:
            return "human"
        elif self.ai_score > self.human_score:
            return "ai"
        else:
            return "draw"

    def analyze_tree(self):
        """Analyze the minimax tree and prepare data for visualization"""
        self.tree_nodes = []
        
        children = self.game.getChildren(self.ai_piece)
        best_heuristic = -float('inf')
        best_col = None
        
        for child in children:
            #Detect which column changed
            col = None
            for c in range(COLS):
                if any(child.mat[:, c] != self.game.mat[:, c]):
                    col = c
                    break
            
            if col is not None:
                heuristic_val = Heuristic.heuristic(child.mat, self.ai_piece, self.human_piece)
                
                #Track the best move
                if heuristic_val > best_heuristic:
                    best_heuristic = heuristic_val
                    best_col = col
                
                self.tree_nodes.append({
                    'col': col,
                    'heuristic': heuristic_val,
                    'selected': False
                })
        
        # Mark the selected move
        if best_col is not None:
            for node in self.tree_nodes:
                if node['col'] == best_col:
                    node['selected'] = True
                    break

    #AI LOGIC
    def ai_move(self):
        start = time.time()

        chosen_child = None
        chosen_col = None

        # 1- MINIMAX WITHOUT ALPHA-BETA  (Minimax.py)
        if self.ai_algorithm == "minimax":
            try:
                chosen_child = Minimax.minimax(self.game, self.depth)
            except Exception as e:
                pass

        # 2- MINIMAX WITH ALPHA-BETA (Minimax_alpha_beta.py)
        elif self.ai_algorithm == "alpha-beta":
            try:
                chosen_child, _ = Minimax_alpha_beta.Maximize(
                    self.game, self.depth, -float("inf"), float("inf")
                )
            except Exception as e:
                pass

        # 3- EXPECTIMAX (Expected_Minimax.py)
        elif self.ai_algorithm == "expectimax":
            try:
                chosen_child = Expected_Minimax.Expectimax(self.game, self.depth)
            except Exception as e:
                pass

        # If no AI child computed, fallback to first available move
        if chosen_child is None:
            # Find first available column
            for col in range(COLS):
                if self.game.mat[0][col] == 0:
                    self.game.addPiece(self.ai_piece, col)
                    chosen_col = col
                    break
            if chosen_col is None:
                return

        else:
            # Detect which column changed
            for c in range(COLS):
                if any(self.game.mat[:, c] != chosen_child.mat[:, c]):
                    chosen_col = c
                    break

            if chosen_col is None:
                return

            # Apply move
            self.game.addPiece(self.ai_piece, chosen_col)

        elapsed = time.time() - start
        heur = Heuristic.heuristic(self.game.mat, self.ai_piece, self.human_piece)

        self.last_ai_msg = f"AI played column {chosen_col} | Heuristic: {heur:.1f} | Time: {elapsed:.3f}s"

        # Analyze tree for visualization
        self.analyze_tree()

    def check_game_end(self):
        #Check if board is full
        if self.game.isTerminal():
            #Board is full, now determine winner by counting connected fours
            self.winner = self.determine_winner()
            self.game_over = True
            return True
        
        return False

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            #Control frame rate
            clock.tick(60)
            
            #Always draw the board first
            self.draw_board()
            
            #Draw tree panel if enabled
            if self.show_tree:
                self.draw_tree_panel()
                pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                # ----------------- GAMEPLAY -----------------
                if self.started and not self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_t:  # T key toggles tree view
                            self.show_tree = not self.show_tree
                    
                    if event.type == pygame.MOUSEMOTION:
                        # Clear just the top part where the moving piece is
                        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, SQUARE_SIZE))
                        
                        # Redraw header text
                        algorithm_text = FONT.render(f"Algorithm: {self.ai_algorithm}", True, BLACK)
                        depth_text = FONT.render(f"Depth: {self.depth}", True, BLACK)
                        status_text = "Human (YELLOW) vs AI (RED) - Your turn (T=Toggle Tree)"
                        status = SMALL_FONT.render(status_text, True, BLACK)
                        
                        self.screen.blit(algorithm_text, (10, 10))
                        self.screen.blit(depth_text, (WIDTH - 120, 10))
                        self.screen.blit(status, (10, 40))
                        
                        if self.last_ai_msg:
                            info = SMALL_FONT.render(self.last_ai_msg, True, BLACK)
                            self.screen.blit(info, (10, 60))
                        
                        # Draw moving yellow piece
                        posx = event.pos[0]
                        pygame.draw.circle(self.screen, YELLOW_COLOR,
                                         (posx, SQUARE_SIZE // 2), RADIUS)
                        
                        pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        posx = event.pos[0]

                        # human move
                        if self.human_move(posx):
                            self.draw_board()
                            
                            # Check if board is full after human move
                            if self.check_game_end():
                                continue

                            # AI move
                            self.ai_move()
                            self.draw_board()
                            self.check_game_end()

                #Reset game if it's over and space is pressed
                elif self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset(self.ai_algorithm, self.depth)

        pygame.quit()
        sys.exit()