'''
In this design, the puzzle is stored in common list for best convenience.
Number tiles are represented by integer and blank space by " ".
Especially when we check if the puzzle is solvable,
we replace the " " by 0 to better compute the inverse sum.

Note that when looking for the blank position,
we use (row, column) to represent its coordinate,
as this helps us interpret it intuitively.

Also, the conclusion used to check sovability is noteworthy:
The randomly generated puzzle is solvable if and only if,
the size is odd and the total inverse sum is even,
or the size is even and the total inverse sum is odd,
provided that total inverse sum = inverse sum + x, y coordinates of blank space


Below is the decomposition of the program:

a. generate puzzles:
generate_a_puzzle() -> use random module to create puzzles in list form
check_if_solvable() -> check if the puzzle is solvable

b. input letters to represent direction:
prompt_designated letters() -> prompt input from users
validate_input_letters() -> check if the input is approriate

c. play puzzles:
display_the_puzzle() -> display the puzzle every time it is updated
locate_blank() -> find the empty space and return its location
find_proper_moves() -> find valid moves every time the puzzle is updated
play_the_puzzle() -> prompt input and update the puzzle 

d. main()
'''

from random import shuffle

def generate_a_puzzle(size:int) -> list:
    '''
    Parameter:
        size (int): An integer suggested to be >= 3
    
    Return:
        Returns the generated puzzle and its final appear in list form.
    '''
    while True:
        original_position = list(range(1, size**2))
        original_position.append(" ")
        shuffle(original_position)
        sequential_position = list(range(1, size**2))
        sequential_position.append(" ")
        if check_if_solvable(original_position, size):
            display_the_puzzle(original_position, size)
            return original_position, sequential_position

def check_if_solvable(position_list:list, size:int) -> bool:
    '''
    Parameters:
        position_list (list): The generated puzzle in list form
        size (int): An integer suggested to be >= 3
    
    Return:
        Returns the check result by comparing size and total inverse sum
    '''
    cordinate_sum = sum(locate_blank(position_list, size))
    check_list = [0 if i == " " else i for i in position_list]
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
        size (int): An integer suggested to be >= 3
    
    Return:
        Returns the cordinate of the empty space in list form
    '''
    cordinate = position_list.index(" ")
    x_cordinate = (cordinate % size) + 1
    y_cordinate = (cordinate // size) + 1
    return [x_cordinate, y_cordinate]

def display_the_puzzle(position_list:list, size:int) -> None:
    '''
    Parameters:
        position_list (list): The puzzle in process in list form
        size (int): An integer suggested to be >= 3
    '''
    print()
    for i in range(size**2):
        tile = str(position_list[i])
        print(tile.rjust(len(str(size**2-1))+1),end="")
        if (i+1) % size == 0:
            print()
    print()

def prompt_designated_letters() ->dict:
    '''
    Return:
        Returns the designated letters in dictionary form
    '''   
    while True:
        try:
            letters = input("Enter the four letters used for \
left, right, up and down move>").replace(" ", "")
            validate_input_letters(letters)
            direction = ["left", "right", "up", "down"]
            trans = list(letters.lower())
            designated_letters = {s:g for s,g in zip(direction, trans)}
            return designated_letters
        
        except ValueError as err_msg:
            print(err_msg)

def validate_input_letters(user_input:str) -> str:
    '''
    Parameters:
        user_input (str): The designated letters in string form
    
    Return:
        Returns the check result by raising value error
    '''    
    if not user_input.isalpha():
        raise ValueError("Your input should be all letters!")
    if len(user_input) != 4:
        raise ValueError("Your input should contain four letters!")
    if len(set(user_input.lower())) != len(user_input):
        raise ValueError("Your input should not contain repeated letters!")

def play_the_puzzle(designated_letters:dict, size:int) -> None:
    '''
    Parameters:
        designated_letters (dict): The designated letters in dictionary form
        size (int): An integer suggested to be >= 3
    '''
    cnt = 0
    
    trans, sequential_position = generate_a_puzzle(size)
    while trans != sequential_position:
        proper_moves = find_proper_moves(trans, designated_letters, size)
        index = trans.index(" ")
        # Validate the user input
        while True:
            move = (input("Enter your move(" + ", ".join(proper_moves)
                          + ")>").replace(" ","")).lower()
            if move not in [x[-1] for x in proper_moves]:
                print(f"Your choice should be made among {proper_moves}")
            else:
                break
        # Play the puzzle according to the user input
        if move == designated_letters["left"]:
            trans[index], trans[index+1] = trans[index+1], trans[index]
        if move == designated_letters["right"]:
            trans[index], trans[index-1] = trans[index-1], trans[index]
        if move == designated_letters["up"]:
            trans[index], trans[index+size] = trans[index+size], trans[index]
        if move == designated_letters["down"]:
            trans[index], trans[index-size] = trans[index-size], trans[index]
        display_the_puzzle(trans, size)   
        cnt += 1
    print(f"Congratulations! You solved the puzzle in {cnt} moves!")
    choice = input("Enter w to play again \
or any other keys to end the game>").replace(" ","")
    if choice == "w":
        play_the_puzzle(designated_letters, size)
    else:
        print("See u next time!")


def find_proper_moves(position_list:list, 
                           designated_letters:dict, 
                           size:int) -> list:
    '''
    Parameters:
        position_list (list): The puzzle in process in list form
        designated_letters (dict): The designated letters in dictionary form
        size (int): An integer suggested to be >= 3
    
    Return:
        Returns the proper moves in list form
    '''
    proper_moves = []
    x, y = locate_blank(position_list, size) 
    if x != size:
        proper_moves.append("left-" + designated_letters["left"])                                                                                            
    if x != 1:
        proper_moves.append("right-" + designated_letters["right"])
    if y != size:
        proper_moves.append("up-" + designated_letters["up"])
    if y != 1:
        proper_moves.append("down-" + designated_letters["down"])
    return proper_moves


def main():
    
    print("Welcome to Willow's puzzle game, \
try to repeatedly slide one adjacent tile, \
until all numbers are ordered sequentially \
from left to right, top to bottom.\n")
    size = 3
    designated_letters = prompt_designated_letters()
    play_the_puzzle(designated_letters, size)
    
main()
