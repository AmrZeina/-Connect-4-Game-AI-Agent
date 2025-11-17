from Menu import run_menu 
from GUI import Connect4GUI

if __name__ == "__main__":
    algorithm, depth = run_menu()
    game = Connect4GUI(algorithm, depth)
    game.run()