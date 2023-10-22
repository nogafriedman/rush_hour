#######################################
# FILE : game.py
# WRITER : Noga_Friedman , nogafri , 209010479
# Exercise: ex9
# DESCRIPTION: A class Game of Rush Hour program.
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# WEB PAGES I USED: -
#######################################
import helper
import sys
from car import *
from board import *


class Game:
    """
    Class game.
    Handles the running of the game itself - asks for player input and
    checks for validity, calls for changes on the board according to the input,
    checks if the game has been won.
    """
    VALID_COLORS = ['R', 'G', 'W', 'O', 'B', 'Y']

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        # implement your code here (and then delete the next line - 'pass')
        self.board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        while True:
            # print the board:
            print(self.board)
            # print the optional moves the user can make:
            print("Possible moves:")
            possible_moves = self.board.possible_moves()
            for move in possible_moves:
                print(move)
            # ask for input:
            name_dir_input = input("Choose the car you'd like to move "
                                   "and in what direction: ")

            # if input isn't valid (not the correct format), print a message
            # informing the user then start the loop again asking for input:
            check = self.__check_input(name_dir_input)
            if check == -1:
                return 'quit'
            if check == 0:
                print("Invalid input. Input should be in the form of "
                      "car name,direction (for example Y,r).")
            # if input is valid:
            else:
                name = name_dir_input[0]
                movekey = name_dir_input[2]
                # check if the move can be made:
                if self.__check_move_legal(name, movekey, possible_moves):
                    # move is legal - move the car:
                    self.board.move_car(name, movekey)  # end of function
                    return
                else:
                    # if the move picked couldn't be made:
                    print("Illegal move. Move has to be one of the legal "
                          "moves appearing on the list.")

    def __check_input(self, user_input):  # added function
        """
        checks if the input given by the user is valid.
        input has to be a string of a capital letter (a car in the game)
        and a non capital letter (for direction) separated by a comma:
        for example "Y,d" = move the yellow car down.
        :return: 1 if valid, 0 if not, -1 to exit the game
        """
        if user_input == '!':
            return -1
        if len(user_input) != 3 or user_input[1] != ',':
            return 0
        if user_input[0] not in Game.VALID_COLORS:
            return 0
        if user_input[2] not in 'udlr':
            return 0
        return 1

    def __check_move_legal(self, name, movekey, possible_moves):  # added function
        """
        check if the move the user wants to make is legal.
        :param name: str - capital letter representing the car
        :param movekey: str - non capital letter representing the direction
        :param possible_moves: list of tuples of the form (name,movekey,description)
                 representing legal moves
        :return: True if move is legal, False if it isn't
        """
        for move in possible_moves:
            if name == move[0] and movekey == move[1]:
                return True
        return False

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while not self.check_win():  # while no cars arrived at (3, 7)
            if self.__single_turn() == 'quit':
                return  # if player decides to quit the game - finish running
        # if player has won - only when while loop breaks:
        print(self.board)
        print("You win!")
        return


    def check_win(self):  # added function
        """
        checks if the game is over (if user arrives at coordinate (3,7))
        :return: True if user won, False if not
        """
        if self.board.cell_content(self.board.target_location()) is not None:
            return True
        return False

    def start_game(self):  # added function
        """
        loads the json file with the game data and initiates a new game.
        json file will be in the format of:
        {
        "O":[2,[2,3],0],
        "R":[2,[0,0],1]
        }
        (a dictionary, where the key is a car name and the value is a list,
        containing the car's length, location and orientation)
        :return: None
        """
        game_dict = helper.load_json(sys.argv[1])

        # check if the car data loaded is valid, if valid add to game:
        for key in game_dict:
            value = game_dict[key]
            length = value[0]
            location = value[1]
            orientation = value[2]
            # check format validity:
            if len(value) != 3 or len(location) != 2 or not isinstance(length,
                                                                    int):
                continue
            # check validity for current key:
            if key not in Game.VALID_COLORS:  # invalid car name
                continue
            if length <= 1 or length >= 5:  # invalid car length
                continue
            if orientation != 0 and orientation != 1:  # invalid orientation
                continue
            car = Car(key, length, location, orientation)
            if not self.board.add_car(car):
                continue  # invalid location/cells occupied/name taken


if __name__ == "__main__":
    board = Board()  # create board object - initiate.board
    game = Game(board)  # create game object and load the created board into it
    game.start_game()  # loads json, adds valid cars to board
    game.play()  # a loop of single_turn until user won

