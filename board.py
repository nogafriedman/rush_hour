class Board:
    """
    Class board.
    defines various method responsible for dealing with the board:
    initiates and prints it, handles objects moving on the board,
    checks if objects stay within board boundaries.
    """

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.__board = self.initiate_board()
        self.__car_list = []  # a list of cars currently on board

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board_str = '* * * * * * * * * \n'
        for row_ind in range(len(self.__board)):
            board_str += '* '
            for col_ind in range(len(self.__board[row_ind])):
                board_str += self.__board[row_ind][col_ind] + ' '
            if row_ind == 3 and col_ind == 7:
                board_str += '\n'
            else:
                board_str += '* \n'
        board_str += '* * * * * * * * *'
        return board_str

    def initiate_board(self):  # added function
        """
        creates the board in the beginning of the game
        :return: visual representation of the board
        """
        empty_board = [['_', '_', '_', '_', '_', '_', '_'],
                       ['_', '_', '_', '_', '_', '_', '_'],
                       ['_', '_', '_', '_', '_', '_', '_'],
                       ['_', '_', '_', '_', '_', '_', '_', 'E'],
                       ['_', '_', '_', '_', '_', '_', '_'],
                       ['_', '_', '_', '_', '_', '_', '_'],
                       ['_', '_', '_', '_', '_', '_', '_']]
        return empty_board

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        board_coordinates = \
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
             (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
             (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
             (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
             (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
             (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
             (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
        return board_coordinates

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        possible_moves = []
        for car in self.__car_list:
            car_name = car.get_name()
            valid_moves_dict = car.possible_moves()
            for key in valid_moves_dict:
                target_cell = car.movement_requirements(key)[0]
                if self.cell_content(target_cell) is None \
                        and self.check_borders(target_cell):
                    possible_moves.append((car_name, key, valid_moves_dict[key]))
        return possible_moves

    def check_borders(self, target_coordinate):  # added function
        """
        checks if the target cell the car is moving into is inside the
        board's borders
        :return: True if cell is within board borders, False if not
        """
        if target_coordinate in self.cell_list():
            return True
        else:
            return False

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return 3, 7

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        for car in self.__car_list:
            if coordinate in car.car_coordinates():
                return car.get_name()
        return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"

        # check if car name is already taken:
        for existing_car in self.__car_list:
            if existing_car.get_name() == car.get_name():
                return False

        coordinates = car.car_coordinates()  # a list of tuples
        for coordinate in coordinates:
            # checks if car coordinates are within board borders and if
            # they're not occupied by other cars (proceeds only if valid):
            if self.cell_content(coordinate) is None and self.check_borders(
                    coordinate):
                # add car to board and mark the cell with the car name:
                self.__board[coordinate[0]][coordinate[1]] = car.get_name()

            else:
                return False  # if couldn't add car to board
        # if car was added successfully to board, add it to the list of cars:
        self.__car_list.append(car)
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        car = self.__get_car_id(name)
        if car is False:
            return False
        else:
            required_cell = car.movement_requirements(movekey)[0]
            if self.cell_content(required_cell) is None and self.check_borders(
                    required_cell):
                # cell is free and within boundaries- move the car:
                old_coordinates = car.car_coordinates().copy()
                if car.move(movekey):  # if car moved successfully:
                    new_coordinates = car.car_coordinates()
                    # remove old coordinates from board:
                    for coordinate in old_coordinates:
                        self.__board[coordinate[0]][coordinate[1]] = '_'
                    # add the car to it's new coordinates on board:
                    for coordinate in new_coordinates:
                        self.__board[coordinate[0]][coordinate[1]] = car.get_name()
                    return True
            else:
                return False

    def __get_car_id(self, name):  # added function
        """
        finds the car id based on it's name
        :param name: string - car name (for example 'Y')
        :return: the car's id, or False if no such car exists
        """
        for car in self.__car_list:
            if car.get_name() == name:
                return car
        else:
            return False
