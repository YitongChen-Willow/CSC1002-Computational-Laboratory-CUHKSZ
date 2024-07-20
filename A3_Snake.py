"""
Here is the data model:

g_snake_tail -> stored in tuple list to represent location
g_monster -> stored in list[turtle.Turtle]
g_food -> stored in list[turtle.Turtle]

Note here that specific global variables are set
in bool type to check the game condition.
"""

import turtle
import random
from functools import partial

g_screen = None
g_intro = None
g_status = None

g_snake = None
g_snake_tail = []
g_snake_sz = 5
g_monster = []
g_food = []
   
g_key_pressed = None
g_last_pressed = None
g_contact = 0
g_timer = 0

g_is_completed = False
g_paused = False
g_blocked = False

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"

FONT_INTRO = ("Arial",16,"normal")
FONT_STATUS = ("Arial",18,"normal")
TIMER_SNAKES = [300,500]
TIMER_SNAKE = 300

SZ_SQUARE = 20      

DIM_PLAY_AREA = 500
DIM_STAT_AREA = 60
DIM_MARGIN = 30

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
       "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_UP:90, KEY_DOWN:270, KEY_LEFT:180, KEY_RIGHT:0}

def create_turtle(x:int, y:int, color:str = "red", border:str = "black") \
    -> turtle.Turtle:
    """    
    Args:
        x (int): The x-coordinate of the turtle's initial position.
        y (int): The y-coordinate of the turtle's initial position.
        color (str, optional): Color of the turtle's body. Defaults red.
        border (str, optional): Color of the turtle's border. Defaults black.
    
    Returns:
        turtle.Turtle: The newly created turtle object.
    """

    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x, y)
    return t

def initialize_food() -> None:
    """
    Initializes food items at random locations.
    Here we move the turtle twice to match it with the number.
    """

    for j in range(5):
        
        x_cor = random.choice([random.randrange(-240,-60,20),\
                               random.randrange(80,240,20)])
        y_cor = random.choice([random.randrange(-270,-70,20),\
                               random.randrange(10,210,20)])

        food = create_turtle(x_cor, y_cor, "", "black")
        food.hideturtle()
        food.goto(x_cor-3, y_cor-10)
        food.write(str(j+1), font=("Arial",12)) 
        food.goto(x_cor, y_cor)
        g_food.append(food)
    
def initialize_monster() -> list[turtle.Turtle]:
    """
    Returns:
        list[turtle.Turtle]: List of 4 turtle objects representing the monster.
    """

    for _ in range(4):
        
        x_cor = random.choice([random.randrange(-230,-90,20),\
                               random.randrange(110,230,20)])
        y_cor = random.choice([random.randrange(-260,-80,20),\
                               random.randrange(20,200,20)])

        monster = create_turtle(x_cor, y_cor, COLOR_MONSTER, "")
        g_monster.append(monster)

    return g_monster

def configure_play_area() -> tuple[turtle.Turtle, turtle.Turtle]:
    """
    Returns:
        tuple[turtle.Turtle, turtle.Turtle]: Motion border and status border.
    """

    # motion border
    m = create_turtle(0,0,"","black")
    sz = DIM_PLAY_AREA//SZ_SQUARE
    m.shapesize(sz, sz, 3)
    m.goto(0,-DIM_STAT_AREA//2)

    # status border
    s = create_turtle(0,0,"","black")
    sz_w, sz_h = DIM_STAT_AREA//SZ_SQUARE, DIM_PLAY_AREA//SZ_SQUARE
    s.shapesize(sz_w, sz_h, 3)
    s.goto(0,DIM_PLAY_AREA//2)  

    # turtle to write introduction
    intro = create_turtle(-120,60)
    intro.hideturtle()
    intro.write("Click anywhere to start!", font=FONT_INTRO)

    # turtle to write status
    status = create_turtle(0,0,"","black")
    status.hideturtle()
    status.goto(-220,s.ycor()-15)

    return intro, status

def configure_screen() -> turtle.Screen:
    """
    Returns:
        turtle.Screen: The configured Turtle screen.
    """

    s = turtle.Screen()
    s.tracer(0)    # disable auto screen refresh
    s.title("Snake by Willow")
    w = DIM_PLAY_AREA + DIM_MARGIN*2
    h = DIM_PLAY_AREA + DIM_MARGIN*2 + DIM_STAT_AREA
    s.setup(w, h)
    s.mode("standard")
    return s

def update_status():
    """
    Updates the status display on the screen.
    """

    motion = "Paused" if g_paused == True else g_key_pressed
    g_status.clear()
    status = f'Contact:{g_contact}   Time:{g_timer}   Motion:{motion}'
    g_status.write(status, font=FONT_STATUS)

def on_key_pressed(key):
    """
    Handles the user's arrow key press event.
    Then calls the `update_status()` function to update the status.
    
    Args:
        key (str): One of 'Up', 'Down', 'Left', or 'Right'.
    """

    global g_key_pressed, g_last_pressed, g_paused

    if g_is_completed:
        return

    if key == "space":
        if g_key_pressed != "space":
            g_last_pressed = g_key_pressed
            g_key_pressed = key
            g_paused = True
        elif g_key_pressed == "space":
            g_key_pressed = g_last_pressed
            g_paused = False
        update_status()
        return
    
    g_key_pressed = key
    g_paused = False
    update_status()

def on_timer_count() -> None:
    """
    Updates the time. This function is called repeatedly.
    """

    global g_timer

    if g_is_completed:
        return

    g_timer += 1
    update_status()
    g_screen.ontimer(on_timer_count,1000)

def on_timer_snake() -> None:
    """
    Advances the snake's movement. This function is called repeatedly.
    
    If no key has been pressed or the snake is paused or blocked, 
    the function simply schedules itself to be called again.
    If the game has been completed, the function simply returns.
    Otherwise, it performs the following steps:
    
    1. Clones the snake's head as a new body segment.
    2. Advances the snake's position by setting the heading based 
        on the last key pressed (`g_key_pressed`) and 
        moving the snake forward by `SZ_SQUARE` units.
    3. If the snake's head is on top of the food, the food is consumed.
    4. If the snake has consumed all food items, the game is completed.
    5. If the number of stamped segments exceeds the current snake size, 
        removes the last segment by clearing the oldest stamp.
    6. Updates the Turtle screen to reflect the changes.
    7. Schedules the function to be called again.
    """

    global TIMER_SNAKE, g_blocked, g_is_completed

    if g_is_completed:
        return

    x,y = g_snake.pos()
    if over_boundary(x, y, "snake", g_key_pressed):

        g_blocked = True
        g_screen.ontimer(on_timer_snake, TIMER_SNAKE)
        return
    g_blocked = False

    if g_paused or g_blocked or (g_key_pressed is None):
        g_screen.ontimer(on_timer_snake, TIMER_SNAKE)
        return
    
    # Clone the head as body
    g_snake.color(*COLOR_BODY)
    g_snake.stamp()
    g_snake_tail.append(g_snake.pos())
    g_snake.color(COLOR_HEAD)

    # Advance snake
    g_snake.setheading( HEADING_BY_KEY[g_key_pressed] )
    g_snake.forward(SZ_SQUARE)
    
    # Consume food if needed
    consume_food()
    
    # Judge the game condition
    if (len(g_snake.stampItems) == 20) and g_snake_sz == 20:
        finish_game("winner")
        g_is_completed = True

    # Shifting or extending the tail
    # Remove the last square on Shifting
    if len(g_snake.stampItems) > g_snake_sz:
        g_snake.clearstamps(1)
        g_snake_tail.pop(0)
        TIMER_SNAKE = TIMER_SNAKES[0]
    else:
        TIMER_SNAKE = TIMER_SNAKES[1]

    g_screen.update()
    g_screen.ontimer(on_timer_snake, TIMER_SNAKE)


def on_timer_monster() -> None:
    """
    Advances the monster's movement. This function is called repeatedly.
    
    The function performs the following steps:
    
    1. If the monster collides with the head of snake, the game is over.
    2. Increases the g_contact if needed.
    3. Calculates the heading for the monster to move towards the snake.
    4. Sets the monster's heading to the calculated value.
    5. Moves the monster forward by `SZ_SQUARE` units.
    6. Updates the Turtle screen to reflect the changes.
    7. Schedules the function to be called again after a random delay 
        between `TIMER_SNAKE-100` and `TIMER_SNAKE+100` milliseconds.
    """

    global g_is_completed
    
    if g_is_completed:
        return
    
    for monster in g_monster:

        # Judge the condition
        if monster.distance(g_snake) < SZ_SQUARE:
            finish_game("loser")
            g_is_completed = True
            return
        
        # Increase contact if needed
        is_contact(monster)
        
        # Calculate the heading
        angle = monster.towards(g_snake)
        qtr = angle//45
        vib = random.choice([-1,1])
        heading = qtr * 45 if qtr % 2 == 0 else (qtr+vib) * 45

        monster.setheading(heading)
        x,y = monster.pos()
        if not over_boundary(x, y, "monster", heading):
            monster.forward(SZ_SQUARE)

    g_screen.update()
    delay = random.randint(TIMER_SNAKE-100, TIMER_SNAKE+100)
    g_screen.ontimer(on_timer_monster, delay)

def on_timer_food() -> None:
    """
    Shifts the food items. This function is called repeatedly.

    The function performs the following steps:
    
    1. If the game is completed, the function simply returns.
    2. Randomly choose the number of existing food items to shift.
    3. Select the food items needed to be shifted and add them to a list.
    4. Shift the selected food to a random place.
    5. Updates the Turtle screen to reflect the changes.
    6. Schedules the function to be called again after a random delay.
    """

    if g_is_completed:
        return
    
    cnt = 0
    shifter = 0
    shift_food = []

    if g_snake_sz == 20:
        return
    
    # Randomly choose the shifted food number
    for food in g_food:
        cnt += 1 if food != None else 0
    num_shift = random.randint(1,cnt)
    
    # Select the food items needed to be shifted
    while shifter < num_shift:
        for food in g_food:
            if food != None:
                g_food[g_food.index(food)].clear()
                shift_food.append(food)
                shifter += 1
    
    # Shift the food
    for shifter in shift_food:

        x,y = shifter.pos()
        while True:
            del_x = random.randint(-2,2) * SZ_SQUARE
            del_y = random.randint(-2,2) * SZ_SQUARE
            if x+del_x >=-230 and x+del_x <= 230 and\
                  y+del_y >= -260 and y+del_y <= 200:
                break
        shifter.goto(x+del_x-3, y+del_y-10)
        shifter.write(str(g_food.index(shifter)+1), font=("Arial",12))
        shifter.goto(x+del_x, y+del_y)

    g_screen.update()
    delay = random.randint(5000, 10000)
    g_screen.ontimer(on_timer_food, delay)
        
def consume_food() -> None:
    """
    Modifies:
        g_snake_sz (int): Increments the size of the snake's body if needed.
    """

    global g_snake_sz

    for food in g_food:
        if food and food.distance(g_snake) < (SZ_SQUARE/2):
            g_food[g_food.index(food)].clear()
            g_snake_sz += g_food.index(food)+1
            g_food[g_food.index(food)] = None

def over_boundary(x:float, y:float, case:str, direction) -> bool:
    """
    Args:
        x (float): The x coordinate of the object.
        y (float): The y coordinate of the object.
        case (str): The object type.
        direction: The direction of the object. Either string or integer.

    Returns:
        True if the object is out of the boundary, otherwise False.
    """

    if case == "snake":
        if (direction == "Up" and y > 200) or\
           (direction == "Down" and y < -260) or\
           (direction == "Left" and x < -230) or\
           (direction == "Right" and x > 230):
            return True
        return False

    if case == "monster":
        if (x < -220 and direction == 180) or \
           (x > 220 and direction == 0) or \
           (y < -250 and direction == 270) or \
           (y > 190 and direction == 90):
            return True
        return False
        
def is_contact(monster: turtle.Turtle) -> None:
    """
    Args:
        monster (turtle.Turtle): The monster to check.
    """

    global g_contact

    for i in range(len(g_snake_tail)):
        x_snake, y_snake = g_snake_tail[i]
        x_monster, y_monster = monster.pos()
        distance_sq = (x_snake-x_monster)**2 + (y_snake-y_monster)**2
        if distance_sq < SZ_SQUARE**2:
            g_contact += 1
            update_status()
            return
        
def finish_game(case:str) -> None:
    """
    Args:
        case (str): The reason of the game ending.
    """

    info = create_turtle(0,-30)
    info.hideturtle()
    info.color("red")
    
    if case == "winner":
        info.write("Winner !!", align = "center",\
                   font = ("Arial",28,"normal"))
    else:
        info.write("Game Over !!", align = "center",\
                   font = ("Arial",28,"normal"))
            
def start_game(x:float, y:float):
    """
    Args:
        x (float): The x coordinate of the mouse click.
        y (float): The y coordinate of the mouse click.
    """

    global g_timer

    g_screen.onscreenclick(None)
    g_intro.clear()
    initialize_food()

    on_timer_count()
    on_timer_snake()
    on_timer_monster()
    on_timer_food()

    for key in (KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, KEY_SPACE):
        g_screen.onkey(partial(on_key_pressed,key), key)

if __name__ == "__main__":

    g_screen = configure_screen()
    g_intro, g_status = configure_play_area()

    update_status()

    g_monster = initialize_monster()
    g_snake = create_turtle(0,-30, COLOR_HEAD, "")

    g_screen.onscreenclick(start_game) # set up a mouse-click call back

    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()
