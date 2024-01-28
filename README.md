
# Introduction

The Battleships coursework project demonstrates a successful implementation of all required initial functionality as listed on ELE.
The program runs via the `game_engine` module for single-player mode, `mp_game_engine` module for multiplayer mode against an AI, and `main` module for
multiplayer mode against an AI with a graphical user interface.

Notably, I have expanded the project's scope by incorporating some additional
functionality within the `mp_game_engine` module-the introduction of five difficulty levels provides users with a diverse range
of challenges, from easy to impossible. I have done this by the AI having an increased probability (for increasing difficulty levels)
of selecting a tuple which represents a definite ship position. Additionally, I have added the `attack_multiplayer()` function which is
similar to the `attack()` function although accepts an additional argument `type_of_opponent` which either takes the value 'Player', or 
'AI_opponent'. This function outputs more meaningful messages to the command-line after each attack. 

Each module is thoroughly documented using type hinting, docstrings, and comments, ensuring clarity and ease of
understanding for anyone interested in reading the code. This approach ensures that any individual willing to collaborate
to this project is able to understand the purpose of each module and function. Moreover, defensive programming was used
in order to not make the program crash in case of an unexpected error such as an invalid ship placement, wrong file format etc.

Logging has also been used through all game types, where each individual log is added to the file `game_log.log`. This keeps
information such as when the game started, the tuple the player and the AI chose, which ship is hit and/or sunk, and when the
game ends.

#    Functions Of The Project
1) You can play single player mode, by attacking a known board until you sink all the ships.

2) You can play multiplayer mode through the command-line against an AI Opponent, by attacking their board, and it attacks yours.
This mode also includes **difficulty levels** which you can pick.
If either your or the AI's ships are all sunk, the Game is Over. You win if you sink all the AI's ships. 

3) You can play multiplayer mode through a graphical user interface against an AI Opponent, by attacking their board,
and it attacks yours. If either your or the AI's ships are all sunk, the Game is Over. You win if you sink all the AI's ships. 

#    Dependencies
In order for all the program to run smoothly, the below dependencies need to be considered:
###  Imports
There is only 1 external import which you will need to install. This is Flask. You can do this through your terminal or command prompt by
entering `pip install Flask`
### Configuration Files
In order for the program to run as intended, you must have two files in the main directory, 'battleships.txt' and 'placement.json'.
The files take the form of:
          
Battleships.txt:
          
    Aircraft Carrier: 5
    Battleship: 4
    Cruiser: 3
    ...

It is crucial for the battleship name and size to come in this order and to also be separated with a colon(:).
If not, the program will not work and a relevant error message will be produced. 
          
placement.json:

    {"Aircraft Carrier": ["0", "0", "h"],
     "Battleship": ["3", "1", "h"],
     ...}
             
It is crucial for this file to follow this format. In the position of the keys, you must enter the battleship name.
It is vital that this name also exists in the 'battleships.txt' file and has a respective size. In the position of
the values, there is a list. In the first element of this list, is the starting x-coordinate that the ship will be placed.
In the second element, goes the starting y-coordinate that the ship will be placed. In the third element, goes the string
'v' or 'h' strictly, indicating vertical or horizontal placement respectively. 

### Python Version
The python version that this project was developed on is Python 3.7. If your Python version is outdated, this may cause the program to
crash. If so, please install Python 3.7 and try again.

#   How To Execute The Project  

**Note:** This project was developed on PyCharm, therefore it is ideal to run on PyCharm or any other IDE if possible.

##    Instructions to run the single player game:

   **Note:** This game only ends when the player sinks all the ships on the board.
   **Note:** In order for the program to run as intended, your battleships.txt file must exist and be formatted correctly.

   When having downloaded all python files and templates from the zip file, navigate to the game_engine.py module and
   run it as the entry path to the program. In the command line, you will be presented with instructions on how to pick
   the type of placement for the ships. After selecting a placement algorithm, you will be prompted with a message to select
   the coordinates which you want to attack. After entering these, a hit or miss message will be produced according to whether
   the attack was successful or not. This loop continues until all the ships have been sunk, producing a Game Over message.

##    Instructions to run the multiplayer player game against an AI Opponent:
   **Note:** In order for the program to run as intended, your battleships.txt and placement.json files
         must exist and be formatted correctly.
   
   When having downloaded all python files and templates from the zip file, navigate to the placement.json file
   in order to place all your battleships as you wish. When having entered x-coord, y-coord, and 'h' or 'v' values for each 
   battleship, ensure that each battleship name also exists in the file 'battleships.txt' and is formatted correctly. 
   Then, navigate to the mp_game_engine.py module and run it as the entry path to the program.
   In the command line, you will be presented with instructions on how to pick the difficulty level you wish.
   The AI's board will have a random placement which will not be revealed. After picking a difficulty level, you will be prompted
   with a message to enter the coordinates which you want to attack. After entering these, a hit or miss message will be produced
   according to whether the attack was successful or not. The AI will then attack your board and a hit or miss message will be
   produced again. This loop continues until all the ships have been sunk, on either your board or the AI's board. When either 
   event occurs, a relevant Game Over message will be produced. 

##    Instructions to run the multiplayer player game against an AI Opponent through a graphical user interface:
   **Note:** In order for the program to run as intended, your battleships.txt and placement.json files
         must exist and be formatted correctly.
   
   When having downloaded all python files and templates from the zip file, navigate to the main.py file and run it as the entry
   path to the program. A message will be printed, including a link which you need to click in order to access the game. This link
   which is 'http://127.0.0.1:5000/placement', will navigate you to a page where you can manually place your battleships on a board. 
   After placing all your ships, click the send board button and the page will automatically redirect you to the next page which is
   can be accessed through 'http://127.0.0.1:5000/'. After being redirected, you can attack the AI's board by clicking on a cell on
   AI's board. After clicking a cell, if the cell turns light blue, this means that you have missed. If the cell turns red, that
   indicates a hit. After attacking the board, the AI will immediately attack you board, with the coordinate being referenced in the
   game log on the left of the page. Every attack can also be seen on the board labelled Player Board on the right of the page. Information
   on which ships have been sunk can be found through the command-line.
   Continue attacking the AI's board until you sink all the AI's ships, or the AI sinks all your ships. If either happens, a relevant
   game over message will be produced.

   **IMPORTANT:** In order to run the game again, you need to first run it again from main.py as the entry path to the program. Then,
                  you can navigate to 'http://127.0.0.1:5000/placement' and restart the game, or if you wish to have the same board as last game,
                  simply navigate to 'http://127.0.0.1:5000/' directly. 

#    Testing Battleships
The robustness of the implementation is validated through comprehensive testing. 
All initial tests from ELE pass successfully, affirming the correctness of the core functionality.
All tests found on ELE and additional tests can be found in the `tests` package.
Furthermore, I have written additional tests which are introduced in the `test_functionality` module.
These additional tests all pass, confirming the functionality of the added difficulty levels.
In order to run the tests on ELE, navigate to the `test_students.py` module and run it as the entry path to
the program. In order to run the additional tests which I have written, navigate to the `test_functionality`
module and run that as the entry path to the program.

#    License For The Project

My License for battleships_coursework

Copyright (c) [2023-Indefinite] [Anonymous]

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


   
    

