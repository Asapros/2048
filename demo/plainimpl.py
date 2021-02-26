# You don't have to install any modules to play this version
import sys; sys.path.insert(0,'..') # Haha import hacking goes brrrrrrr
from main import Board, Directions


# <-[VALUES THAT CAN BE CHANGED BY USER]-> #

CONTROLS = {
    "w":Directions.UP,
    "s":Directions.DOWN,
    "a":Directions.LEFT,
    "d":Directions.RIGHT,
    "q":0
            }

SHOW_BORDER   = True
FIX_CELL_SIZE = True

BOARD_WIDTH  = 10; #BOARD_WIDTH  = 58
BOARD_HEIGHT = 10; #BOARD_HEIGHT = 27

# <--------------------------------------> #

def play():
    while True:
        boardstate = board.visualize(border=SHOW_BORDER, fixsize=FIX_CELL_SIZE)
        print(boardstate)
        key = input("->")
        
        try:
            direction = CONTROLS[key]
        except KeyError: continue
        
        if   direction == 0: return
        elif direction == 1:
            board.random_fill()
            continue
        
        
        board.move(direction)
        
if __name__ == "__main__":
    board = Board(width=BOARD_WIDTH, height=BOARD_HEIGHT) # Initalizes the board, see more info in main.py
    play()
