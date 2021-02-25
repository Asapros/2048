# pip install windows-curses
from main import Board, Directions
import curses


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

def play(screen):
    while True:
        screen.clear()
        boardstate = board.visualize(border=SHOW_BORDER, fixsize=FIX_CELL_SIZE)
        
        try: screen.addstr(boardstate)
        except:
            print("Your screen is too small!")
            return
        
        screen.refresh()
        key = screen.getkey()
        
        try:
            direction = CONTROLS[key]
        except KeyError: continue
        
        if   direction == 0: return
        elif direction == 1:
            board.random_fill()
            continue
        
        
        board.move(direction)
        
if __name__ == "__main__":
    try: curses.initscr()
    except AttributeError: input("You can't open it from IDE!")
    curses.noecho()
    curses.cbreak()
    
    board = Board(width=BOARD_WIDTH, height=BOARD_HEIGHT)
    curses.wrapper(play)
    
    curses.endwin()
