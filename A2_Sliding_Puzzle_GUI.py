'''
Here is the data model:

Puzzle -> stored in common list  a.Number tiles: integer b.blank space: " "
Tiles -> stored in list[turtle.Turtle]
Num_tiles -> stored in list[turtle.Turtle]
Actually, num_tiles is a duplicated set of tiles by hiding original shape.

Note that the display sequence of the puzzle is from bottom to top.
This means that the elements in the puzzle list are not in regular sequence.
Therefore, part of the codes are specifically designed to modulate the order,
which might be a little bit tricky here.

Also, the conclusion used to check sovability is noteworthy:
The randomly generated puzzle is solvable if and only if,
the size is odd and the total inverse sum is even,
or the size is even and the total inverse sum is odd,
provided that total inverse sum = inverse sum + x, y coordinates of blank space.

Below is the decomposition of the program:

a. generate puzzles:
generate_a_puzzle() -> use random module to create puzzles in list form
check_if_solvable() -> check if the puzzle is solvable

b. display puzzles:
create_a_tile() -> use turtle graphics to create a single tile
display_tiles() -> put tiles into appropriate positions and color them
clone_tiles() -> generate a duplicated set of tiles and change original setting
write_numbers() -> mark tiles with according numbers
The last one is detached as a single function because of its reusability.

c. play puzzles:
set_mouse_click() -> handle the mouse click and do exchange if needed
is_adjacent() -> check if the selected tile is adjacent to the blank tile
locate_blank() -> find the empty space and return its location

'''

from random import shuffle
import turtle

def generate_a_puzzle(size:int) -> list:
    '''
    Parameter:
        size (int): An integer suggested to be 3,4 or 5
    
    Return:
        Returns the generated puzzle and its final appear in list form.
    '''
    while True:

        original_position = list(range(1, size**2))
        original_position.append(" ")
        shuffle(original_position)

        key_position = []
        for i in range(1, size+1):
            append_list = list(range(size*(size-i)+1, size*(size-i)+size+1))
            key_position += append_list
        key_position = [" " if i == size*size else i for i in key_position]

        if check_if_solvable(original_position, size):
            return original_position, key_position

def check_if_solvable(position_list:list, size:int) -> bool:
    '''
    Parameters:
        position_list (list): The generated puzzle in list form
        size (int): An integer suggested to be 3,4 or 5
    
    Return:
        Returns the check result by comparing size and total inverse sum
    '''
    x, y = locate_blank(position_list, size)
    cordinate_sum = (x-1) + (size-y)

    check_list = []
    for i in range(1, size+1):
        for j in range(size*(size-i), size*(size-i)+size):
            check_list.append(position_list[j])
    check_list = [0 if i == " " else i for i in check_list]

    inverse_sum = 0
    for i in range(size**2):
        for j in range(i):
            if check_list[j] > check_list[i]:
                inverse_sum += 1

    inverse_sum += cordinate_sum
    if (size % 2) != (inverse_sum % 2):
        return True
    return False

def locate_blank(position_list: list, size: int) -> list:
    '''
    Parameters:
        position_list (list): The puzzle in process in list form
        size (int): An integer suggested to be 3,4 or 5
    
    Return:
        Returns the cordinate of the empty space in list form
    '''
    cordinate = position_list.index(" ")
    x_cordinate = (cordinate % size) + 1
    y_cordinate = (cordinate // size) + 1
    return [x_cordinate, y_cordinate]

def display_tiles(x:int, size:int) -> list[turtle.Turtle]:
    '''
    Parameters:
        x (int): An integer represents the start point of diplay
        size (int): An integer suggested to be 3,4 or 5

    Return:
        Returns the list contaning all the turtle tiles
    '''
    t = create_a_tile()
    sz = 90
    tiles = []

    for cy in range(x, x+sz*size, sz):
        for cx in range(x, x+sz*size, sz):
            t.goto(cx,cy)
            tiles.append(t)
            t = t.clone()
    t.hideturtle()

    for i in range(len(tiles)):
        if trans[i] != " ":
            tiles[i].color("lightgreen")
        else:
            tiles[i].color("white")

    return tiles
        
def create_a_tile(sz:int=4, border:int=5) -> turtle.Turtle:
    '''
    Parameters:
        sz (int): An integer represents the size of the tile
        border (int): An integer represents the border of the tile

    Return:
        Returns the created turtle tile
    '''
    t = turtle.Turtle("square")
    t.up()
    t.shapesize(sz, sz, border)
    return t

def clone_tiles(tiles:list[turtle.Turtle]) -> list[turtle.Turtle]:
    '''
    Parameters:
        tiles (list[turtle.Turtle]): A list contaning all the turtle tiles

    Return:
        Returns the list contaning all the turtle num_tiles
    '''
    numbers = []
    
    for t in tiles:
        n = t.clone()
        n.hideturtle()
        n.goto(t.xcor(), t.ycor()-12)
        n.color("blue")
        n.pensize(15)
        numbers.append(n)

    return numbers

def write_numbers(trans:list, clone_tiles:list[turtle.Turtle]) -> None:
    '''
    Parameters:
        trans (list): The puzzle in process in list form
        clone_tiles (list[turtle.Turtle]): A list contaning all cloned tiles
    '''
    for i in range(len(clone_tiles)):
        clone_tiles[i].write(trans[i], font=("Arial",20), align="center")

def set_mouse_click(x:float, y:float) -> None:
    '''
    Parameters:
        x,y (float): Represent the coordinate of the click position
    '''
    row = (y+190)//90 + 1
    col = (x+190)//90 + 1
    xcor, ycor = locate_blank(trans, size)

    # prohibit the mouseclick event to avoid trouble
    turtle.onscreenclick(None)

    if is_adjacent(row, col, xcor, ycor):

        num_blank = int(ycor*size - (size-xcor) - 1)
        num_tile = int(row*size - (size-col) - 1)

        # do the exchange of tiles
        trans[num_blank],trans[num_tile] = trans[num_tile], trans[num_blank]
        number_tiles[num_tile].clear()
        blank_position = tiles[num_blank].position()
        tile_position  = tiles[num_tile].position()
        tiles[num_tile].goto(blank_position)
        tiles[num_blank].speed(0)
        tiles[num_blank].goto(tile_position)
        tiles[num_tile], tiles[num_blank] = tiles[num_blank], tiles[num_tile]
        write_numbers(trans, number_tiles)

        # check whether the puzzle has been solved
        if trans == key:
            for i in range(0, size*size):
                if trans[i] != " ":
                    tiles[i].color("red")
            write_numbers(trans, number_tiles)

    # turn on the mouseclick event
    turtle.onscreenclick(set_mouse_click)
        
def is_adjacent(row:int, column:int, xcor:int, ycor:int) -> bool:
    '''
    Parameters:
        row,column (int): The position of the mouse click
        xcor,ycor(int): The position of the blank tile

    Return:
        Returns the check result of whether is adjacent or not
    '''
    adjacent_tiles = []

    if xcor > 1:
        adjacent_tiles.append((xcor-1,ycor))
    if xcor < size:
        adjacent_tiles.append((xcor+1,ycor))
    if ycor > 1:
        adjacent_tiles.append((xcor,ycor-1))
    if ycor < size:
        adjacent_tiles.append((xcor,ycor+1))

    if (column, row) in adjacent_tiles:
        return True
    return False
    
if __name__ == "__main__":

    size = int(turtle.numinput("Willow's Puzzle", "Enter \
the size of the game 3,4 or 5:", minval = 3, maxval = 5))
    trans, key = generate_a_puzzle(size)
    turtle.setup(600,600)

    tiles = display_tiles(-150, size)
    number_tiles = clone_tiles(tiles)
    write_numbers(trans, number_tiles)

    turtle.onscreenclick(set_mouse_click)

    turtle.Screen().mainloop()
