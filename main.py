"""
This is the main logic of 2048 game.
How do I document functions:

[-] Parametrs:
    [-] Optional
    :optional([default value]) param [name] [type]: -> [what the parametr does]
    
    [-] Required
    :param [name] [type]: -> [what the parametr does]

    (If the type is from enum I use 'enum [name of enum]' instead of '[type]')
    
[-] Return values:
    :return [type]: -> [when it returns what]

[-] Error raising:
    :raise [name of exception]: -> [when the exception is raised] 
"""

from enum   import Enum
from copy   import copy
from math   import log
from random import randint

class Directions(Enum):
    """Directions used for moving numbers on the board"""
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

class Board:
    """This is a grid with numbers"""
    def __init__(self, width: int = 10, height: int = 10, fill: bool = True):
        """
Initalization
:optional(10)   param width  int:  -> set width of the board
:optional(10)   param height int:  -> set height of the board
:optional(True) param fill   bool: -> fill the board on initalization?
        """
        self.size = (width, height)
        self._array = {}
        if fill: self.random_fill(percent=25)
    # [ ------------------------------------------------------------- ] #
    @property
    def width(self):
        """
Property for width
:return int: -> width
        """
        return self.size[0]
    @property
    def height(self):
        """
Property for height
:return int: -> height
        """
        return self.size[1]

    CHARSET = [" ", ".", "*", ":", "&", "%", "$", "@", "#"] # Character set for _number_to_char
    @classmethod
    def _number_to_char(cls, number):
        """
Converts number from the board to character in specific intensity
:param number int: -> Number you want to convert
:return str: -> The character
        """
        if number <= 0: return cls.CHARSET[0]
        
        index = int(log(number, 2))+1
        # - Why the F are you using logarithm there?
        # - Shut up, it works
        
        try: return cls.CHARSET[index]
        except IndexError: return cls.CHARSET[-1]
        
    # [ ------------------------------------------------------------- ] #
    def random_fill(self, number=1, percent=10):
        """
Fills board in random pattern
:optional(1)  param number  int: -> Number you want to spread
:optional(10) param percent int: -> Chance in 100 that field will be filled
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                if randint(0,100) <= percent:
                    if self.get_number(x,y) == 0:
                        self.place_number(number,x,y)
    
    def in_bounds(self, x, y):
        """
Checks if coordinates are in bounds
:param x int: -> x you want to check
:param y int: -> y you want to check
:return bool: -> True if coordinates are in bounds, otherwise False
        """
        if x < 0 or x+1 > self.width:   return False
        if y < 0 or y+1 > self.height:  return False
        return True
    
    def place_number(self, number, x, y):
        """
Places number in specified coords
:param number int: -> Number you want to place
:param x      int: -> x you want to place it in
:param y      int: -> y you want to place it in
:return bool: -> Success of the action; if there is already a number or coordinates are not in bounds it returns False
        """
        if not self.in_bounds(x, y):    return False
        if not number:                  return False
        self._array[x,y] = number # <- This can be kinda confuzing for new programmers, _array is actually a dictionary, not list. Its inserting number in key '(x,y)'
        return True
    
    def get_number(self, x, y):
        """
Checks what number is in specified coordinates
:param x int: -> x you want to check
:param y int: -> y you want to check
:return int: -> Number thats on this coordinates, if there is not it returns 0
        """
        try: return self._array[x,y]
        except KeyError: return 0
        
    def delete_number(self, x, y):
        """
Delete a number from coords
:param x      int: -> x you want to delete
:param y      int: -> y you want to delete
:return bool: -> Success of the action; if there is't a number here, it returns False
        """
        try:
            del self._array[x,y]
            return True
        except KeyError: return False
        
    def multiply_number(self, x, y):
        """
Multiplies number from coords
:param x      int: -> x you want to multiply
:param y      int: -> y you want to multiply
:return bool: -> Success of the action
        """
        number = self.get_number(x,y)*2
        return self.place_number(number,x,y)
    
    def _move_number(self, x, y, direction):
        """
Moves number from coordinates in specified direction
:param x      int: -> x you want to move
:param y      int: -> y you want to move
:param direction enum Directions: -> direction you want to move the number in
        """
        number = self.get_number(x, y)
        if not number: return # If target number is 0, we're done.
        
        target_position = [x,y]
        target_number = 0
        while True:
            temp_position = copy(target_position)                     #
            if   direction == Directions.UP:    temp_position[1] -= 1 # Moves 'cursor' in the 
            elif direction == Directions.DOWN:  temp_position[1] += 1 # direction specified
            elif direction == Directions.RIGHT: temp_position[0] += 1 # by an argument
            elif direction == Directions.LEFT:  temp_position[0] -= 1 #
            if not self.in_bounds(*temp_position): break # Breaks from the loop if moved cursor is not in bounds
            
            temp_number = self.get_number(*temp_position)
            if not temp_number: # If positions there's cursor on is not occupied, it goes back to start of the loop
                target_position = temp_position
                target_number = 0
                continue
            
            if temp_number != number: break # If number thats cursor on is not equal to number we're moving, it breaks out from the loop
            
            target_position = temp_position
            self.multiply_number(*target_position) # Finnaly, if number meets the same one, they merge
            self.delete_number(x, y)
            
            return # We're done here

        self.delete_number(x, y)
        self.place_number(number, *target_position)

    def __move_numbers(self, direction):
        """
Private subtask method of move.
:param direction enum Directions: -> Direction you want to move numbers in
        """
        number_coords = tuple(self._array.keys())
        for coord in number_coords:
            self._move_number(*coord, direction)
            
    def move(self, direction, fill=True):
        """
Moving all numbers
:param direction enum Directions: -> Direction you want to move numbers in
:optional(True) param fill bool:  -> Execute random_fill() after moving?
:raise AssertionError: -> If you think that html is a programming language and mess up with the code below
        """
        last_state    = "html"
        current_state = "programming language"
        # The two variables above have to be diffrent, otherwise we'll never enter the loop
        assert last_state != current_state
        
        while last_state != current_state: # While results of two moves in the row are different, it keeps trying till they're the same, so there is nothing else to move.
            last_state = tuple(self._array.keys())
            self.__move_numbers(direction)
            current_state = tuple(self._array.keys())
            
        if fill: self.random_fill() # If fill is not False it fills the board

    def visualize(self, border=False, fixsize=True):
        """
Visualizes the board.
:optional(False) param border  bool: -> Show border of the board?
:optional(True)  param fixsize bool: -> Fixes size of the characters; in commandline two characters in the row makes a square
:return str: -> The string of visualized board
        """
        lines = []
        if border:
            headerlen = self.width
            if fixsize: headerlen *= 2
            lines.append("+" + "-"*headerlen + "+") # Adds first line - the header
        
        for y in range(0, self.height):
            string = ""
            if border: string += "|" # Adds | as first character of the line
                
            for x in range(0, self.width):
                char = self._number_to_char(self.get_number(x,y))
                if fixsize: char *= 2
                string += char

            if border: string += "|" # Adds | as last character of the line
            lines.append(string) # Append finished line to lines
    
        if border:
            lines.append("+" + "-"*headerlen + "+") # Adds last line - the footer
        return "\n".join(lines)

