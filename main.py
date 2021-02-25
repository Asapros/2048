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
    def __init__(self, width=10, height=10, fill=True):
        self.size = (width, height)
        self._array = {}
        if fill: self.random_fill(percent=25)
    # [ ------------------------------------------------------------- ] #
    @property
    def width(self): return self.size[0]
    @property
    def height(self): return self.size[1]

    CHARSET = [" ", ".", "*", ":", "&", "%", "$", "@", "#"]
    @classmethod
    def _number_to_char(cls, number):
        if number <= 0: return cls.CHARSET[0]
        
        index = int(log(number, 2))+1
        # - Why the F are you using logarithm there?
        # - Shut up, it works
        
        try: return cls.CHARSET[index]
        except IndexError: return cls.CHARSET[-1]
        
    # [ ------------------------------------------------------------- ] #
    def random_fill(self, number=1, percent=10):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if randint(0,100) <= percent:
                    if self.get_number(x,y) == 0:
                        self.place_number(number,x,y)
    
    def in_bounds(self, x, y):
        if x < 0 or x+1 > self.width:   return False
        if y < 0 or y+1 > self.height:  return False
        return True
    
    def place_number(self, number, x, y):
        if not self.in_bounds(x, y):    return False # Returns False if coordinates are not in bounds
        if not number:                  return False # Returns False if number is 0
        self._array[x,y] = number
        return True
    
    def get_number(self, x, y):
        try: return self._array[x,y]
        except KeyError: return 0
        
    def delete_number(self, x, y):
        try:
            del self._array[x,y]
            return True
        except KeyError: return False
        
    def multiply_number(self, x, y):
        number = self.get_number(x,y)*2
        return self.place_number(number,x,y)
    
    def _move_number(self, x, y, direction):
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
        number_coords = tuple(self._array.keys())
        for coord in number_coords:
            self._move_number(*coord, direction)
            
    def move(self, direction, fill=True):
        last_state = 0
        current_state = 1
        
        while last_state != current_state:
            last_state = tuple(self._array.keys())
            self.__move_numbers(direction)
            current_state = tuple(self._array.keys())
            
        if fill: self.random_fill()

    def visualize(self, border=False, fixsize=True):
        lines = []
        if border:
            headerlen = self.width
            if fixsize:
                headerlen *= 2
            lines.append("+" + "-"*headerlen + "+")
        
        for y in range(0, self.height):
            string = ""
            if border: string += "|"
                
            for x in range(0, self.width):
                char = self._number_to_char(self.get_number(x,y))
                if fixsize: char *= 2
                string += char

            if border: string += "|"
            lines.append(string)
    
        if border:
            lines.append("+" + "-"*headerlen + "+")
        return "\n".join(lines)

