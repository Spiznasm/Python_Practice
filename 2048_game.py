"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    zeroes = 0
    reordered = []
    combined = []
    skip = False
    #iterate through the list counting zeroes and 
    #appending non-zeroes to a new list
    for num in line:
        if num == 0:
            zeroes +=1
        else:
            reordered.append(num)
    #add the zeroes on the end of the new list 
    for num in range(zeroes):
        reordered.append(0)

    zeroes = 0
    
    for num in range(len(reordered)):
        #Comparing a member of the list to the next member
        #could throw and IndexError if there is no next
        #member, the try/except will hand the error
        try:
            #skip will be True after numbers are merged
            #a continue here prevents merging the same
            #number twice
            if skip == True:
                skip = False
                continue
            else:
                if reordered[num] == 0:
                    zeroes +=1
                #when adjacent number match, one becomes
                #double and the other becomes 0, then we
                #skip the number that became 0 in the 
                #iteration
                elif reordered[num] == reordered[num+1]:
                    combined.append(reordered[num]*2)
                    zeroes +=1
                    skip = True
                else:
                    combined.append(reordered[num])

        except IndexError:
            combined.append(reordered[num])

    for num in range(zeroes):
        combined.append(0)

    return combined

def index_generator(start_tiles,direction,tile_count):
    """
    Helper function to create the index that will be used with the move method
    tile_count will be the grid height for UP and DOWN and width for RIGHT and LEFT
    """
    #empty list to append the indices into
    index_grid = []
    #beginning with the starting coordinate of each line, generate
    #the rest of the coordinates in that line.
    for start_coordinate in start_tiles:
        coordinate_list = []
        coordinate_list.append(start_coordinate)
        next_coordinate = list(start_coordinate)
        while len(coordinate_list) <= tile_count-1:
            next_coordinate[0] += OFFSETS[direction][0]
            next_coordinate[1] += OFFSETS[direction][1]
            coordinate_list.append(tuple(next_coordinate))
        index_grid.append(coordinate_list)
    return index_grid

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        initialize the height, width, empty list that will
        hold the tile values, and the index used for moving
        """
        self._height = grid_height
        self._width = grid_width
        self._grid = []
        self.reset()
        #blank lists to hold starting coordinates for each direction
        left_start = []
        right_start = []
        up_start = []
        down_start = []
        #fill the empty lists with the correct starting coordinates
        for row in range(self._height):
            left_start.append((row,0))
            right_start.append((row,self._width-1))
        for column in range(self._width):
            up_start.append((0,column))
            down_start.append((self._height-1,column))
        #use the index_generator function to populate a dictionary with 
        #the move indices for each direction
        self._index = {UP:index_generator(up_start,UP,self._height),
                      DOWN:index_generator(down_start,DOWN,self._height),
                      LEFT:index_generator(left_start,LEFT,self._width),
                      RIGHT:index_generator(right_start,RIGHT,self._width)}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = []
        #fill the board with all zeroes
        for high in range(self._height):
            self._grid.append([])
            for dummy_wide in range(self._width):
                self._grid[high].append(0)
                
        self.new_tile()
        self.new_tile()
            
       
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_string = ""
        for line in self._grid:
            grid_string += str(line) + '\n'
        return grid_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved_grid = []
        #create a grid that is the same size as the board 
        #and fill it with zeroes
        for high in range(self._height):
            moved_grid.append([])
            for dummy_wide in range(self._width):
                moved_grid[high].append(0)
        
        for line in self._index[direction]:
            merge_line = []
            
            for coordinate in line:
                merge_line.append(self.get_tile(coordinate[0],coordinate[1]))
            new_line = merge(merge_line)
            for coordinate in line:
                #use the coordinates in the index to locate the position in the 
                #grid to input the merged value which is pulled using the position 
                #of the coordinate in the index.
                moved_grid[coordinate[0]][coordinate[1]]=new_line[line.index(coordinate)]
        #check if any tiles moved by comparing the board before the move
        #to the newly formed board after the move.
        if moved_grid == self._grid:
            pass
        else:
            self._grid = moved_grid
            self.new_tile()  
        
        
            

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #list all the tiles in a single list
        all_tiles = []
        for high in range(self._height):
            for wide in range(self._width):
                all_tiles.append(self._grid[high][wide])
        new_row = random.randrange(0,self._height)
        new_column = random.randrange(0,self._width)
        #check the all_tiles list to make sure there is a
        #zero in at least 1 tile.
        if 0 not in all_tiles:
            pass
        #if the randomly chosen tile is not a zero, retry
        elif self._grid[new_row][new_column]!= 0:
            self.new_tile()
        else:
            self._grid[new_row][new_column]=random.choice([2,2,2,2,2,2,2,2,2,4])
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col]=value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
