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
import random
import json
import sys
from typing import *


def initialise_board(size: int = 10) -> List[List[Optional[None]]]:
    """
    This function initialises the board for the battleships. It has one argument with a
    default value of 10, creating a 10x10 board. This board is made up of a list of lists.

    :param
        size: This is the size of the board

    :returns:
        board: the board with empty cells, represented by None
    """
    board = [[None]*size for x in range(size)]  # Creates a board composed of lists of lists, according to the argument 'size'.
    return board


def create_battleships(filename: Optional[str] = "battleships.txt") -> Dict[str, int]:
    """
    The create_battleships function has one optional argument with default value 'battleships.txt'.
    The function creates the dictionary 'battleships'  with each battleship name and size stored as
    the key value pair respectfully. It is important to note that in the battleships.txt file, the
    format of the battleships must be :
        name: size
    and then the next battleships below (the ':' is vital as this is the strip point which assigns the
    name and size to each battleship according to the file).

    :param filename: This is the file which the dictionary will be created from, it has to take the format of name:size

    :returns: battleships: The dictionary called battleships will be returned, it contains the ship names as keys, and the ship values as sizes.
    """
    file = open(filename, 'r')  # Opens the file and assigns it to the variable 'file'
    file_lines = file.readlines()  # reads each line of the file separately
    battleships = {}

    for line in file_lines:
        if line.strip():  # this checks whether the line is empty, it will only read if the line is not empty
            try:
                battleship_name, battleship_size = line.strip().split(':')  # assigns values to the variables from the file
            except ValueError:
                print("There is an error with your battleships in the file,"
                      "\nplease check that all the sizes are correct for each ship, "  # Error message produced
                      "\nand that each battleship name and size is separated by :")
                sys.exit()  # Exits the program completely, since the game cannot continue with an incorrect file
            try:
                battleships[battleship_name.title()] = int(battleship_size)  # adds the variables created to the dictionary as a key value pair
            except ValueError:
                print("There is an error with your battleships in the file,"
                      "\nplease check that all the sizes are correct for each ship, "  # Error message produced
                      "\nand that each battleship name and size is separated by :")
                sys.exit()  # Exits the program completely, since the game cannot continue with an incorrect file
    return battleships  # returns the dictionary which contains the battleships as the keys, and their sizes as the values.


def json_read(filename: Optional[str] = 'placement.json') -> Dict:
    """
    This function takes a JSON file as an argument, and returns the file in the form of a dictionary which can be accessed.

    :param filename: This is the JSON file that will be read

    :return: custom_placement_dictionary: This is the dictionary that will be returned
    """
    file = open(filename, 'r')  # Opens the file and assigns it to the variable 'file'
    custom_placement_dictionary = json.load(file)  # Loads  'file' to the dictionary.

    return custom_placement_dictionary


def place_battleships(board=initialise_board(), ships=create_battleships(), algorithm='simple'):
    """
    This function is used to place the battleships onto the game board. It takes 3 arguments,
    the game board, the battleship's dictionary, and the algorithm which has a default value
    set to simple.

    The simple algorithm automatically places each battleship on the left columns
    of each row. Each battleship is placed on a separate row and takes up as many columns
    as its size in the dictionary.

    The random algorithm places each battleship randomly on the board, ensuring that no two
    battleships overlap each other. Each battleship is placed either horizontally or vertically,
    this is also randomly decided using the import random. The first coordinate that the battleship
    will be placed is determined randomly, whilst the consequent parts of the battleship are placed
    depending on whether the placement.json is vertical or horizontal. In order to ensure that the board
    includes all parts of every battleship, a test is carried out and the board is returned only if
    this check succeeds.

    The custom algorithm places each battleship according to the placement.json file in the directory.
    The json file needs to have a specific format:
    {
        'battleship_name : [ship_size, direction ('horizontal' or 'vertical'), starting row, starting column]
        ...
    }
    If not formatted in this way, the algorithm will not work.
    In order to ensure that the board includes all parts of every battleship, a test is carried out and the
    board is returned only if this check succeeds, meaning that all battleships have been placed correctly.

    :param board: This argument has a default value of initialise_board() which is an empty board filled with None in each cell.
     It is used as the board which the ships will be placed on
    :param ships: Has a default value of create_battleships(), see the function for its description
    :param algorithm: This will determine how the battleships are placed, it can have 3 values, 'simple', the default value,
    'random', and 'custom'

    :return: The function will either return None and this will be handled, producing a sufficient error message. Oppositely,
    if all goes smoothly (e.g., the files match up) the board containing the battleships will be returned according to the placement
    algorithm that the user has chosen.
    """

    number_of_battleships = len(ships)
    list_of_battleships = list(ships.items())  # Creates a list of tuples that each hold the key value pair of the ship name and size
    if algorithm == 'simple':
        if number_of_battleships <= len(board):  # Verifies that the number of battleships does not exceed the board size.
            for p in range(number_of_battleships):
                battleship_name, battleship_size = list_of_battleships[p]  # Assigns a name and size to each battleship, according to the list of tuples.
                if battleship_size <= len(board):
                    for column in range(battleship_size):
                        board[p][column] = battleship_name  # Assigns the battleship_name to each cell in the table, according to its size.
                else:
                    print("The battleships' size is too big,"
                          " please have all battleship sizes be equal or smaller than ", len(board))
                    return None
        else:
            print('There are too many battleships in the file, please reduce this to ', len(board), ' or lower')
            return None  # Produces an error message that the number of battleships exceeds the number of rows

        return board  # Returns the board, now including the battleships placed at the left of each row.
    elif algorithm == 'random':
        total_check = True
        while total_check:  # This acts as a while loop of the whole placement.json algorithm, in order to check if all the battleships are finally placed
            if number_of_battleships <= len(board):  # Verifies that the number of battleships does not exceed the board size.
                for p in range(number_of_battleships):
                    battleship_name, battleship_size = list_of_battleships[p]  # Assigns a name and size to each battleship, according to the list of tuples.
                    if battleship_size <= len(board):
                        flag = True
                        while flag:  # This while loop will ensure that if a battleship is placed, there is no part of any other battleship in its position
                            row_random = random.randint(0, len(board) - 1)
                            column_random = random.randint(0, len(board) - 1)
                            placement_direction = random.randint(1, 2)  # Randomly chooses 1 or 2, 1 indicating that the battleship will be placed horizontally, 2 vertically

                            if placement_direction == 1:  # If the battleship is placed horizontally
                                if all(board[row_random][none_test] is None for none_test in range(battleship_size)):  # Verifies that all the elements that the battleship is going to be placed in are None, meaning they are empty
                                    for q in range(battleship_size):
                                        board[row_random][q] = battleship_name  # Assigns the battleship's name to every cell
                                    flag = False
                                else:
                                    continue  # If a battleship overlaps with the one trying to be placed, continue will move onto the next iteration of the while loop, producing a different coordinate

                            elif placement_direction == 2:  # If the battleship is placed vertically
                                if all(board[none_test][column_random] is None for none_test in range(battleship_size)):  # Verifies that all the elements that the battleship is going to be placed in are None, meaning they are empty
                                    for q in range(battleship_size):
                                        board[q][column_random] = battleship_name  # Assigns the battleship's name to every cell
                                    flag = False
                                else:
                                    continue

                    else:
                        print("The battleships' size is too big,"
                              " please have all battleship sizes be equal or smaller than ", len(board))
                        return None

                    board_total_ship_sizes = 0
                    expected_total_ship_sizes = 0

                    for value in ships.values():
                        expected_total_ship_sizes += value  # Sums up all the sizes of the battleships on the file
                    for row in board:
                        for cell in row:
                            if cell is not None:
                                board_total_ship_sizes += 1  # Sums up all the elements on the board that aren't None, meaning a battleship is there

                    if expected_total_ship_sizes == board_total_ship_sizes:  # If the expected total battleships are equal to the actual battleships on the board, then we know that they have all been placed correctly
                        total_check = False
                    else:  # If the expected total battleships are not equal to the actual battleships on the board, then the outer while loop restarts, until it produces a correct board
                        total_check = True
            else:
                print('There are too many battleships in the file, please reduce this to ', len(board), ' or lower')
                return None

        return board  # returns the board, containing the randomly placed battleships
    elif algorithm == 'custom':
        total_battleship_size = 0
        for battleship_name, value in json_read().items():  # assigns each key and the value(s) to variables
            if battleship_name not in ships.keys():
                print("Your battleships.txt file does not match up with the JSON file")
                return None
            battleship_size = ships[battleship_name]
            total_battleship_size += battleship_size
            direction = value[2]
            starting_row = int(value[1])
            starting_column = int(value[0])
            if starting_column > len(board) - battleship_size or starting_row > len(board) - battleship_size:  # checks if there is an invalid coordinate
                print('A ship in your placement file has an incorrect x or y coordinate, change this and try again.')
                sys.exit()
            if direction == "h":  # horizontal placement of the battleship
                for q in range(battleship_size):
                    board[starting_row][starting_column+q] = battleship_name  # Every cell on the board according to the starting placement, the horizontal direction and the battleship size will now contain the battleship name
            elif direction == "v":  # vertical placement of the battleship
                for q in range(battleship_size):
                    board[starting_row+q][starting_column] = battleship_name  # Every cell on the board according to the starting placement, the vertical direction and the battleship size will now contain the battleship name
            else:
                return None  # Will output an error message if the JSON file does not have 'horizontal' or 'vertical' in the second index of the value list (in the game_engine module)

        board_total_ship_sizes = 0
        for row in board:
            for cell in row:
                if cell is not None:
                    board_total_ship_sizes += 1  # Sums up all the elements on the board that aren't None, meaning a battleship is there

        if total_battleship_size == board_total_ship_sizes:  # If the expected total battleships are equal to the actual battleships on the board, then we know that they have all been placed correctly
            return board
        else:  # If the expected total battleships are not equal to the actual battleships on the board, then an error message will be produced in the game_engine module.
            return None
