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
from flask import render_template, jsonify
from flask import Flask, request
from mp_game_engine import *
import logging

app = Flask(__name__)
logging.basicConfig(filename='game_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Formats the logging file
player_ships = players['Human'][1]  # assigns the player's ships dictionary to the variable 'player_ships'


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    """
    This method handles the GET and POST requests for the placement interface of the program. In case of a GET request, the
    template is returned which allows the user to place their ships. In the case of a POST request, the player's placement design
    is received in the form of a JSON object and written, as a dictionary, to the placement.json file.
    :return: Success Message
    """
    global data
    if request.method == 'GET':
        logging.info('The placement template has been rendered')
        return render_template('placement.html', ships=player_ships, board_size=10)
    elif request.method == 'POST':
        data = request.get_json()  # The JSON object is received and assigned to the variable 'data' in the form of a dictionary
        file = open('placement.json', 'r')
        contents = json.load(file)  # The existing content of the file is loaded onto the variable 'contents'
        contents.update(data)  # The contents are updated with the dictionary received from the POST request
        file = open('placement.json', 'w')
        json.dump(contents, file)  # This writes the new dictionary to the file, in order for the player's board to be aligned to their choices during the placement.
        logging.info("The JSON Object has been received and written to the placement.json file")
        return jsonify({'message': 'Received'}), 200


ai_opponent_board = players['AI_Opponent'][0]   # Initialises the AI's board, including the battleships which have been placed randomly.
player_dictionary = players['Human'][1]  # Initialises the Player's dictionary and assigns it to the variable 'player_dictionary'
ai_opponent_dictionary = players['AI_Opponent'][1]  # Initialises the AI's dictionary and assigns it to the variable 'ai_opponent_dictionary'


@app.route('/', methods=['GET'])
def root():
    """
    The route of the method root is '/', it only accepts GET requests. The player's board is returned,
    according to their placement choices on the placement screen.
    """
    if request.method == 'GET':
        logging.info("The player's board has been sent successfully")
        return render_template('main.html', player_board=place_battleships(initialise_board(), create_battleships(), 'custom'))


player_board = players['Human'][0]   # Initialises the player's board, including the battleships which have been placed according to the custom JSON file.


@app.route('/attack', methods=['GET'])
def process_attack():
    """
    This method processes the player's and AI's attack on each board respectively. It updates each board with a Hit or Miss
    message through a red cell indicating a hit, and a dark-blue cell indicating a miss. It also verifies if either the player
    or the AI have won, producing a Game Over message in either scenario.
    """
    if request.method == 'GET':
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        player_coordinates = (x, y)  # A tuple containing x and y, representing the x and y coordinates is initialised.
        ai_coordinates = generate_attack()  # This generates a new, random tuple, each element within the board size.
        player_attack = attack_multiplayer(player_coordinates, ai_opponent_board, ai_opponent_dictionary, 'Player')  # The player's attack is carried out on the AI's board and a boolean True or False is assigned to the variable player_attack, depending on the success of the hit.
        attack_multiplayer(ai_coordinates, player_board, player_dictionary, 'AI_Opponent')
        if all(value == 0 for value in player_dictionary.values()):  # If all the values in the players dictionary are 0 ,this means that all the ships have length 0, indicating that all the ships have been sunk.
            logging.info('The AI Opponent has won')
            return jsonify({'hit': True, 'AI_Turn': ai_coordinates, 'finished': 'YOU LOSE! Game Over:( AI_Opponent wins'})
        if player_attack:  # If the player's attack was a hit
            if all(value == 0 for value in ai_opponent_dictionary.values()):  # If all the values in the AI's dictionary are 0 ,this means that all the ships have length 0, indicating that all the AI's ships have been sunk.
                logging.info('The Player has won')
                return jsonify({'hit': True, 'AI_Turn': ai_coordinates, 'finished': 'Congratulations! You Beat the AI!'})  # A Game Over message is generated as the player has won.
            else:  # In the case that all the values are not 0.
                if all(value == 0 for value in player_dictionary.values()):  # If all the values in the players dictionary are 0 ,this means that all the ships have length 0, indicating that all the ships have been sunk.
                    logging.info('The AI Opponent has won')
                    return jsonify({'hit': True, 'AI_Turn': ai_coordinates, 'finished': 'YOU LOSE! Game Over:( AI_Opponent wins'})  # If all the player's ships are sunk, the player has lost and a Game Over message is returned.
                else:  # If all the values in the dictionary are not 0
                    return jsonify({'hit': True, 'AI_Turn': ai_coordinates})
        else:  # If the player's attack is a miss
            if all(value == 0 for value in player_dictionary.values()):  # If all the values in the players dictionary are 0 ,this means that all the ships have length 0, indicating that all the ships have been sunk. This is verified again.
                logging.info('The AI Opponent has won')
                return jsonify({'hit': True, 'AI_Turn': ai_coordinates, 'finished': 'YOU LOSE! Game Over:( AI_Opponent wins'})  # If all the player's ships are sunk, the player has lost and a Game Over message is returned.
            else:  # If the values in the dictionary are not 0
                return jsonify({'hit': False, 'AI_Turn': ai_coordinates})


if __name__ == '__main__':  # If this is run as the main program, the below function will be executed
    print('Navigate to http://127.0.0.1:5000/placement to place your ships and then play!')
    print('Navigate to http://127.0.0.1:5000/ if you are happy with the board defined in placement.json file.')
    app.run()  # runs the Flask application
    logging.info('The GUI version of the multiplayer game has ended')
