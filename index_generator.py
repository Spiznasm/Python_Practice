UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def index_generator(start_tiles,direction,height,width):
    """
    Helper function to create the index that will be used with the move method
    """
    if direction == UP or DOWN:
        end = height-1
    elif direction == LEFT or RIGHT:
        end = width-1
    #empty list to append the indices into
    index_grid = []
    #beginning with the starting coordinate of each line, generate
    #the rest of the coordinates in that line.
    for start_coordinate in start_tiles:
        coordinate_list = []
        coordinate_list.append(start_coordinate)
        next_coordinate = list(start_coordinate)
        while len(coordinate_list) <= end:
            next_coordinate[0] += OFFSETS[direction][0]
            next_coordinate[1] += OFFSETS[direction][1]
            coordinate_list.append(tuple(next_coordinate))
        index_grid.append(coordinate_list)
    return index_grid
        
            
