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
from game_engine import cli_coordinates_input
import logging

logging.basicConfig(filename='game_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Formats the logging file


players = {'AI_Opponent': [place_battleships(initialise_board(), create_battleships(), 'random'), create_battleships()],  # Initialises the player and the AI opponent in a dictionary with their names as the keys and a list containing their board, and their dictionary of ships as the values.
           'Human': [place_battleships(initialise_board(), create_battleships(), 'custom'), create_battleships()]}

already_guessed = []  # Initialises the list in which previous guesses of the AI will be appended in through the generate_attack() function.
already_guessed_mp = []  # Initialises the list in which previous guesses of the AI will be appended in through the difficulty level functions.


def generate_attack(board_size: int = 10) -> Tuple[int, int]:
    """
    The generate_attack function has one argument with a default value of  10, indicating the size of the board.
    The function generates a random tuple with two elements (x,y). This tuple will be used to attack the users board
    when the user plays against an AI opponent. x corresponds to the column that will be attacked and y corresponds to the
    row that will be attacked. If the tuple created has  been generated previously, thus already guessed, the function
    will keep producing a tuple until one that has not been guessed is produced. This tuple is then returned.

    :param board_size: This parameter is the size of the board and a tuple is generated according to this parameter
    :return: attack_tuple: The attack tuple containing the random coordinates is returned
    """
    attack_tuple = (0, 0)
    guess_verifier = True
    while guess_verifier:
        y_coordinate = random.randint(0, board_size - 1)
        x_coordinate = random.randint(0, board_size - 1)
        attack_tuple: Tuple[int, int] = (x_coordinate, y_coordinate)

        if attack_tuple not in already_guessed:  # Verifies that the attack tuple has not already been guessed by checking if it exists in the list
            guess_verifier = False  # This exits the while loop
        else:
            continue  # If the tuple has already been generated, another random one is generated. This loop continues until a new tuple is generated.

    already_guessed.append(attack_tuple)  # If the tuple has not already been guessed, it is appended to the list
    return attack_tuple


def attack_multiplayer(coordinates: Tuple[int, int], board: List, battleships: Dict[str, str], type_of_opponent: str) -> bool:
    """
    The function checks whether there is a battleship at the coordinates of the board and returns
    False if there is no battleship, or True if the attack was successful. It is similar to the attack()
    function but has an extra argument in order to produce more insightful Hit or Miss messages in the command-line
    when a player, or the AI Opponent attacks the board.

    :param coordinates: A tuple which represents the coordinates that will be attacked on the board e.g., (1,2)
    :param board: The battleships board which will be attacked
    :param battleships: The dictionary battleships which is synchronised with the battleships board.
     This is needed as when a cell gets attacked and hits, the value of that battleship is decreased by 1.
    :param type_of_opponent: This will determine which message is produced in the command-line depending on a hit or miss.
    :return: True or False 2will be returned depending on whether the attack was a hit or miss. A more insightful message will
    be printed, but not returned.
    """

    if type_of_opponent == 'AI_Opponent':
        board_cell = board[coordinates[1]][coordinates[0]]  # Assigns the value of the coordinates to a variable board_cell
        if board_cell is None:
            print("\nMiss by the AI!")
            logging.info('The AI missed at %s', (coordinates[0], coordinates[1]))
            return False
        else:
            battleships[board_cell] -= 1  # Reduces the size of the battleship in the dictionary by 1
            board[coordinates[1]][coordinates[0]] = None  # Changes the coordinates of the board to None as that cell is now empty
            print("\nHit by the AI!")
            logging.info('The AI hit the ship at %s', (coordinates[1], coordinates[0]))
            if battleships[board_cell] == 0:  # If the specific ship names' value is 0, a message that the ship is sunk is produced
                print('\nThe AI has sunk your', board_cell, '!')
                logging.info("The AI has sunk the player's %s", board_cell)
            return True
    elif type_of_opponent == 'Player':
        board_cell = board[coordinates[1]][coordinates[0]]  # Assigns the value of the coordinates to a variable board_cell
        if board_cell is None:
            print("\nMiss by you!")
            logging.info('The Player missed at %s', (coordinates[1], coordinates[0]))
            return False
        else:
            battleships[board_cell] -= 1  # Reduces the size of the battleship in the dictionary by 1
            board[coordinates[1]][coordinates[0]] = None  # Changes the coordinates of the board to None as that cell is now empty
            print("\nHit by you!")
            logging.info('The Player hit the ship at %s', (coordinates[1], coordinates[0]))
            if battleships[board_cell] == 0:  # If the specific ship names' value is 0, a message that the ship is sunk is produced
                print('\nYou have sunk the', board_cell, '!')
                logging.info("The Player has sunk the AI's %s", board_cell)
            return True


def list_of_player_tuples(json_file: str = 'placement.json', battleships_dictionary: Dict = create_battleships()) -> List:
    """
    This function creates a list of tuples of the form (x,y) where each tuple is a position of a ship on the board. Therefore,
    all the positions of the board which include player ships will be returned in the form of a list.

    :param json_file: Takes the custom placement file as a parameter
    :param battleships_dictionary: Takes the player's battleships dictionary which includes the ship sizes
    :return: Will return a list containing all the positions of the player's ships
    """
    player_dictionary = json_read(json_file)  # Creates a dictionary with the ships and positions according to the placement file
    doomed_tuples = []
    for key, value in player_dictionary.items():
        battleship_name = key
        battleship_size = battleships_dictionary[battleship_name]
        for x in range(battleship_size):
            if value[2] == 'h':  # If the direction is horizontal
                generated_tuple = (int(value[0])+x, int(value[1]))  # Generates a tuple which is definitely a position of a ship, as we know value[0] and value[1] are positions of ships according to placement.json
                doomed_tuples.append(generated_tuple)  # Appends this tuple to the doomed_tuple list of tuples.
            elif value[2] == 'v':  # If the direction is vertical
                generated_tuple = (int(value[0]), int(value[1])+x)  # Generates a tuple which is definitely a position of a ship, as we know value[0] and value[1] are positions of ships according to placement.json
                doomed_tuples.append(generated_tuple)  # Appends this tuple to the doomed_tuple list of tuples.
    return doomed_tuples


def chance_33_tuple(list_of_tuples: List) -> Tuple[int, int]:
    """
    This function will have a 33.33% definite chance of hitting a player ship as it has a 1 in 3 chance of selecting a position which
    a ship lies in. If this 33.33% chance is chosen, then a random tuple from the doomed_tuples list is chosen. After it is chosen,
    this tuple is added to the already_guessed_mp list where in order for the next tuples to be chosen, they have to not be in the
    already_guessed_mp list. If the 33.33% chance is not chosen, a random tuple is generated using the generate_attack() function.
    The chance of initially hitting a ship through this function is 29/6 as there is a 1/3 chance if the chance is chosen.
    If not, there is initially a 15/100 chance that a tuple which contains a ship is chosen. Thus, 1/3 + 15/100 = 29/60 = 0.483
    :param list_of_tuples: This is the list of tuples which the chosen tuples will be selected from
    :return: Will return a tuple in order to attack the player's board.
    """
    verify = True
    selected_tuple = (0, 0)
    random_number = random.randint(0, 2)
    if random_number == 0:
        while verify:
            selected_tuple = random.choice(list_of_tuples)  # Randomly chooses a tuple from the list_of_tuples and assigns it to the variable 'selected_tuple'
            if selected_tuple not in already_guessed_mp:
                selected_tuple = selected_tuple  # If the selected tuple has not already been guessed
                break
            else:
                continue
    else:  # If the random number is 1 or 2
        selected_tuple = generate_attack()  # A random tuple will be generated
    already_guessed_mp.append(selected_tuple)  # The tuple generated is appended to the already_guessed_mp list
    return selected_tuple


def chance_50_tuple(list_of_tuples: List) -> Tuple[int, int]:
    """
    This function will have a 50% definite chance of hitting a player ship as it has a 1 in 2 chance of selecting a position which
    a ship lies in. If this 50% chance is chosen, then a random tuple from the doomed_tuples list is chosen. After it is chosen,
    this tuple is added to the already_guessed_mp list where in order for the next tuples to be chosen, they have to not be in the
    already_guessed_mp list. If the 50% chance is not chosen, a random tuple is generated using the generate_attack() function.
    The chance of initially hitting a ship through this function is 13/20 as there is a 1/2 chance if the chance is chosen.
    If not, there is initially a 15/100 chance that a tuple which contains a ship is chosen. Thus, 1/2 + 15/100 = 13/20 = 0.65.
    :param list_of_tuples: This is the list of tuples which the chosen tuples will be selected from
    :return: Will return a tuple in order to attack the player's board.
    """
    random_number = random.randint(0, 1)
    selected_tuple = (0, 0)
    if random_number == 0:
        verify = True
        while verify:
            selected_tuple = random.choice(list_of_tuples)  # Randomly chooses a tuple from the list_of_tuples and assigns it to the variable 'selected_tuple'
            if selected_tuple not in already_guessed_mp:
                selected_tuple = selected_tuple  # If the tuple has not already been guessed
                break
            else:
                continue
    elif random_number == 1:
        selected_tuple = generate_attack()  # A random tuple will be generated
    already_guessed_mp.append(selected_tuple)
    return selected_tuple  # The generated tuple is returned


def chance_66_tuple(list_of_tuples: List) -> Tuple[int, int]:
    """
    This function will have a 66.66% definite chance of hitting a player ship as it has a 2 in 3 chance of selecting a position which
    a ship lies in. If this 66.66% chance is chosen, then a random tuple from the doomed_tuples list is chosen. After it is chosen,
    this tuple is added to the already_guessed_mp list where in order for the next tuples to be chosen, they have to not be in the
    already_guessed_mp list. If the 66.66% chance is not chosen, a random tuple is generated using the generate_attack() function.
    The chance of initially hitting a ship through this function is 49/60 as there is a 2/3 chance if the chance is chosen.
    If not, there is initially a 15/100 chance that a tuple which contains a ship is chosen. Thus, 2/3 + 15/100 = 49/60 = 0.82.
    :param list_of_tuples: This is the list of tuples which the chosen tuples will be selected from
    :return: Will return a tuple in order to attack the player's board.
    """
    random_number = random.randint(0, 2)
    selected_tuple = (0, 0)
    if random_number == 0 or random_number == 1:  # If the random number is 0 or 1
        verify = True
        while verify:
            selected_tuple = random.choice(list_of_tuples)  # Chooses a tuple from the list_of_tuples and assigns it to the variable 'selected_tuple'
            if selected_tuple not in already_guessed_mp:  # If the selected tuple has not already been guessed
                selected_tuple = selected_tuple
                break
            else:
                continue
    elif random_number == 2:  # If the random number is 2
        selected_tuple = generate_attack()  # A random tuple will be generated
    already_guessed_mp.append(selected_tuple)
    return selected_tuple  # The generated tuple is returned


def definite_hit(list_of_tuples: List) -> Tuple[int, int]:
    """
    This function will have a 100%  chance of hitting a player ship as it has a 2 in 3 chance of selecting a position which
    a ship lies in. Thus, it generates a tuple which is definitely a position that a player's ship is in. In order for the player
    to beat this mode, they have to guess 15 straight positions of the AI's guesses.
    :param list_of_tuples: This is the list of tuples which the chosen tuples will be selected from
    :return: Will return a tuple in order to attack the player's board. This tuple will definitely produce a hit.
    """
    verify = True
    while verify:
        selected_tuple = random.choice(list_of_tuples)  # Chooses a tuple from the list_of_tuples and assigns it to the variable 'selected_tuple'
        if selected_tuple not in already_guessed_mp:  # If the selected tuple has not already been guessed
            already_guessed_mp.append(selected_tuple)
            return selected_tuple
        else:  # If the tuple has previously been guessed
            continue


def ai_opponent_game_loop():
    print('***************************************             '  # Welcome Message
          '\n       WELCOME TO BATTLESHIPS        '
          '\n***************************************'
          '\nYOU ARE PLAYING AGAINST AN AI OPPONENT'
          '\n***************************************'
          '\n '
          '\nYou both have the same number and sizes of battleships, these are: ')

    battleships_dictionary = create_battleships()  # Creates a dictionary with the battleships of both the AI opponent and the player.
    for k, v in battleships_dictionary.items():
        print('Name:', k, ',', 'Size:', v)  # Prints the names and sizes of the user's and AI's battleships.
    print('')

    print('This is YOUR board, according to the custom placement file: ')
    player_board = players['Human'][0]   # Initialises the player's board, including the battleships which have been placed according to the custom JSON file.
    ai_opponent_board = players['AI_Opponent'][0]   # Initialises the AI's board, including the battleships which have been placed randomly.
    try:
        for line in player_board:
            print(line)
    except TypeError:  # If a TypeError occurs, it will inform the user that there is an issue with their files.
        print('')
        print('There is an issue with the text file your battleships are in, or your JSON file, or the placement of your ships meaning that tey are overlapping, please check them and try again:'
              '\n This may be a difference between the two files in the spelling of your battleship names, or the battleship sizes.'
              '\n Also, your ships may be overlapping and therefore are not all placed on the board. ')
        logging.critical("There is an issue with the player's JSON, text files, or the ships are overlapping in the placement. The game has ended prematurely due to this reason.")
        sys.exit()  # This terminates the program as it cannot continue with incorrect files.

    print(' ')

    check1 = True
    while check1:
        difficulty_level = input('Choose a Difficulty Level:'  
                                 '\nEnter 1 for Easy Difficulty'
                                 '\nEnter 2 for Manageable Difficulty'
                                 '\nEnter 3 for Medium Difficulty'
                                 '\nEnter 4 for Hard Difficulty'
                                 '\nEnter 5 for Impossible Difficulty\n')
        if difficulty_level == '1':
            check1 = False
            logging.info('The player chose the easy difficulty')
        elif difficulty_level == '2':
            check1 = False
            logging.info('The player chose the manageable difficulty')
        elif difficulty_level == '3':
            check1 = False
            logging.info('The player chose the medium difficulty')
        elif difficulty_level == '4':
            check1 = False
            logging.info('The player chose the hard difficulty')
        elif difficulty_level == '5':
            check1 = False
            logging.info('The player chose the impossible difficulty')
        else:  # if an incorrect input is chosen, the user has to enter a correct input for the game to continue
            print('Wrong input, please try again\n')
    print("\nAttack the AI's board!")
    win = 0
    flag = True
    ai_dictionary = players['AI_Opponent'][1]
    player_dictionary = players['Human'][1]
    doomed_tuples = list_of_player_tuples()  # Creates a list of all the player's tuples which contain a ship
    while flag:
        if all(value == 0 for value in player_dictionary.values()):  # If all the values in the player dictionary are 0, the game is over as all ships have been sunk, the AI wins
            win = 0
            break  # This will escape the while loop
        elif all(value == 0 for value in ai_dictionary.values()):  # If all the values in the AI dictionary are 0, the game is over as all ships have been sunk, the Player wins
            win = 1
            break  # This will escape the while loop
        else:
            check = True
            try:
                while check:
                    coordinates = cli_coordinates_input()
                    if len(player_board) > coordinates[0] >= 0 and len(player_board) > coordinates[1] >= 0:  # verifies that each coordinates size is less than or equal to the length of the board, if not, this would produce a ValueError
                        attack_multiplayer(coordinates, ai_opponent_board, players['AI_Opponent'][1], 'Player')  # Executes the attack on the AI's board and assigns the True or False value to a variable
                        if all(value == 0 for value in ai_dictionary.values()):  # If all the values in the AI dictionary are 0, the game is over as all ships have been sunk, the Player wins
                            flag = False
                            win = 1
                            break  # This exits the while loop
                        print("\nNow it's the AI opponent's turn...")
                        if difficulty_level == '1':
                            ai_attack_result = attack_multiplayer(generate_attack(), player_board, players['Human'][1], 'AI_Opponent')  # Executes the attack on the Players board and assigns the result to a variable
                        elif difficulty_level == '2':
                            selected_tuple = chance_33_tuple(doomed_tuples)
                            ai_attack_result = attack_multiplayer(selected_tuple, player_board, players['Human'][1], 'AI_Opponent')  # Executes the attack on the Players board and assigns the result to a variable
                        elif difficulty_level == '3':
                            selected_tuple = chance_50_tuple(doomed_tuples)
                            ai_attack_result = attack_multiplayer(selected_tuple, player_board, players['Human'][1], 'AI_Opponent')  # Executes the attack on the Players board and assigns the result to a variable
                        elif difficulty_level == '4':
                            selected_tuple = chance_66_tuple(doomed_tuples)
                            ai_attack_result = attack_multiplayer(selected_tuple, player_board, players['Human'][1], 'AI_Opponent')  # Executes the attack on the Players board and assigns the result to a variable
                        elif difficulty_level == '5':
                            selected_tuple = definite_hit(doomed_tuples)
                            ai_attack_result = attack_multiplayer(selected_tuple, player_board, players['Human'][1], 'AI_Opponent')  # Executes the attack on the Players board and assigns the result to a variable
                        if ai_attack_result:
                            logging.info("The AI has hit the player's ship")
                        else:
                            logging.info("The AI has missed the player's ships")
                        if all(value == 0 for value in player_dictionary.values()):  #
                            flag = False
                            win = 0  # If all the values in the Players dictionary are 0, the game is over as all ships have been sunk, the AI wins
                            break  # This exits the while loop
                        print("\nThis is how your board looks after the AI's attack:")
                        for line in player_board:
                            print(line)
                        check = False
                    else:
                        print("Invalid Input, enter coordinates that are 0 or above, and less than the length of the board")  # If the user's coordinate input is invalid, they are asked to input the coordinate again
            except TypeError:
                print('There is an issue with the file your battleships are in, and your JSON file, please check them and try again')
                logging.critical("There is an issue with the player's JSON and txt files. The game has ended prematurely due to this reason.")
                win = 2  # In order for no Game Over message to br printed, win is set to 2 which prints nothing, instead only prints the error message above
                break

    if win == 1:
        print('\n ***********************************'  
              '\n            CONGRATULATIONS         '
              "\n   YOU SUNK ALL THE AI's BATTLESHIPS!"
              '\n              YOU WIN!!!             '
              '\n ***********************************')
        logging.info('The player has won')

    if win == 0:
        print('\n ***********************************'  
              '\n THE AI SUNK ALL YOUR BATTLESHIPS!!!'
              '\n           YOU LOSE:('
              '\n ***********************************')
        logging.info('The AI has won')

        if win == 2:  # Only the above error message is printed as this indicated an error in the text and JSON files
            print('')


if __name__ == '__main__':  # If this is run as the main program, the below function will be executed
    logging.info('The multiplayer game has started')
    ai_opponent_game_loop()
    logging.info('The multiplayer game has ended')
