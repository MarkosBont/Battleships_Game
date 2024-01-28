"""
MY License for battleships_coursework

Copyright (c) [2023] [Anonymous]

Permission is hereby granted, free of charge, to any person obtaining a copy
of the battleships_coursework software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from components import *
import logging

logging.basicConfig(filename='game_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Formats the logging file


def attack(coordinates: Tuple[int, int], board: List, battleships: Dict[str, int]) -> bool:
    """
    The function attack takes 3 arguments: the coordinates of the attack, the game board,
    and the dictionary battleships. The function checks whether there is a battleship at the
    coordinates of the board and returns False if there is no battleship, or True if the
    attack was successful.

    :param coordinates: A tuple which represents the coordinates that will be attacked on the board e.g., (1,2)
    :param board: The battleships board which will be attacked
    :param battleships: The dictionary battleships which is synchronised with the battleships board. This is needed as
    when a cell gets attacked and hits, the value of that battleship is decreased by 1.
    :return: Will either return True or False, True if the attack on the board was successful, meaning a ship was hit,
    and False if the hit was unsuccessful, meaning a ship was not hit.
    """

    board_cell = board[coordinates[1]][coordinates[0]]  # Assigns the value of the coordinates to a variable board_cell
    if board_cell is None:
        print("\nMiss!")
        return False
    else:  # In any other case, there is a battleship in the cell
        battleships[board_cell] -= 1  # Reduces the size of the battleship in the dictionary by 1
        board[coordinates[1]][coordinates[0]] = None  # Changes the coordinates of the board to None as that cell is now empty
        print("\nHit!")
        if battleships[board_cell] == 0:  # If the specific ship names' value is 0, a message that the ship is sunk is produced
            print('\nSunk the', board_cell, '!')
            logging.info('The %s %s', board_cell, 'has been sunk')
        return True


def cli_coordinates_input() -> Tuple[int, int]:
    """
    This is a parameterless function which asks the user for the row and column
    they want to attack. These coordinates are then stored in tuple form. The function makes sure that the input of the user is valid,
    it uses try, except in order to not produce an error if a ValueError arises.
    The tuple is finally returned.

    :return: The tuple of coordinates that the user input is returned. e.g., if the user input 3 then 4, the tuple (3,4) is returned.
    """
    global tuple_coordinates
    check = True
    while check:
        try:
            row_coordinate = int(input("\nPlease enter the y-coordinate that you want to attack, enter a number from 0 to the length of the board -1: \n"))  # Asks the user to input the x-coordinate
            column_coordinate = int(input("\nPlease enter the x-coordinate that you want to attack, enter a number from 0 to the length of the board -1: \n"))  # Asks the user to input the y-coordinate
            tuple_coordinates = (column_coordinate, row_coordinate)  # Stores these coordinates in tuple form
            check = False
        except ValueError:  # This will arise if the user inputs a wrong value. In this case, the user will have to enter them again.
            print("Invalid Input for either the x or y value, please enter them again")
            logging.warning('The player entered incorrect coordinates')

    return tuple_coordinates


def simple_game_loop():
    """
    This function is a parameterless function and is a procedure. It acts as the engine of the game as it starts the game with a welcome message,
    initialises the initial board without any ships, and initialises the ships according to
    the user's selection of which placement algorithm. Both of these happen using the default settings
    to create the game components. The user is then asked for the coordinates that they want to attack.
    The attack is then processed, a hit or miss message is produced. This process is repeated until all
    battleships have been sunk and a Game Over message is produced.
    """
    print('***************************************             '  # Welcome Message
          '\n       WELCOME TO BATTLESHIPS        '
          '\n***************************************'
          '\n                                       ')

    battleships_dictionary = create_battleships()  # Creates a dictionary with the battleships
    print('These are your battleships: ')
    for k, v in battleships_dictionary.items():
        print('Name:', k, ',', 'Size:', v)  # Prints the names and sizes of the user's battleships

    print(' ')
    check = True
    while check:
        placement = input(' Pick a placement algorithm by entering 1, 2, or 3:'
                          '\n   1) Simple (All Battleships Placed on the Left Rows)'
                          '\n   2) Randomly Placed Ships'
                          '\n   3) Custom placement according to your JSON file for the placement of the battleships, and your text file for the ship sizes')

        if placement == '1':
            placement = 'simple'
            logging.info('The player chose the simple placement')
            check = False
        elif placement == '2':
            placement = 'random'
            logging.info('The player chose the random placement')
            check = False
        elif placement == '3':
            placement = 'custom'
            logging.info('The player chose the custom placement')
            check = False
        else:
            print('\nOnly enter 1, 2, or 3\n')
    battle_board = place_battleships(initialise_board(), create_battleships(), placement)  # Initialises the battleships board
    if (placement == 'custom') and (battle_board is None):
        print("Your JSON file is incorrectly formatted, the ships may be overlapping, or each element in the JSON file is written incorrectly, or misplaced")
        logging.critical(" The player's JSON file is incorrectly formatted, the ships may be overlapping, or each element in the JSON file is written incorrectly, or misplaced")
    else:
        print(' ')
        print('This is the board that you will be playing on: \n')
        for i in battle_board:
            print(i)  # Produces a visual of the board that the user going to play on, including all the ships
        print(' ')

        flag = True
        while flag:
            if all(value == 0 for value in battleships_dictionary.values()):  # If all the values in the dictionary are 0, the game is over as all ships have been sunk
                flag = False  # This makes the game end as the while loop is broken
            else:
                flag1 = True
                while flag1:
                    coordinates = cli_coordinates_input()  # Assigns the tuple of coordinates to the variable coordinates
                    if len(battle_board) > coordinates[0] >= 0 and len(battle_board) > coordinates[1] >= 0:
                        flag1 = False
                    else:
                        print("Please enter valid coordinates, they have to be less than the length of the board and greater than 0\n")
                        logging.warning("The player entered a coordinate larger than the board length")
                logging.info('The player chose coordinates %s', coordinates)
                attack_result = attack(coordinates, battle_board, battleships_dictionary)  # Executes the attack on the board and stores the True or False value in the variable 'attack_result'
                if attack_result:
                    logging.info('The players attack was a hit')
                else:
                    logging.info('The players attack was a miss')

        print('\n ***********************************'  # Once the while loop is broken, a Game Over Message is produced
              '\n YOU SUNK ALL THE BATTLESHIPS! YOU WON'
              '\n But That Means That The Game Is Now Sadly Over:('
              '\n ***********************************')
        logging.info('The player has won the single player game')


if __name__ == '__main__':  # If this is run as the main program, the below function will be executed
    logging.info('The player has started a single player game')
    simple_game_loop()
    logging.info('The single player game has ended')
