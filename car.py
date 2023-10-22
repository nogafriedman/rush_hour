#######################################
# FILE : car.py
# WRITER : Noga_Friedman , nogafri , 209010479
# Exercise: ex9
# DESCRIPTION: A class Car of Rush Hour program.
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# WEB PAGES I USED: -
#######################################

class Car:
    """
    Class car.
    has various methods responsible for dealing with a single car that
    doesn't know the rules of the board/game - can move according to it's own
    rules on the board.
    """
    VERTICAL = 0
    HORIZONTAL = 1
    POSSIBLE_MOVES = 'udrl'
    UP = 'u'
    DOWN = 'd'
    RIGHT = 'r'
    LEFT = 'l'

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name  # Capital letter -
        # Yellow/Blue/Orange/White/Green/Red
        self.__length = length  # number of cells taken by the car, int (2-4)
        self.__location = location  # (row, col) - (y,x)
        self.__orientation = orientation  # vertical - 0, horizontal - 1

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates = []
        if self.__orientation is Car.VERTICAL:  # 0
            for i in range(self.__length):
                coordinates.append((self.__location[0] + i, self.__location[1]))
        if self.__orientation is Car.HORIZONTAL:  # 1
            for i in range(self.__length):
                coordinates.append((self.__location[0], self.__location[1] + i))
        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        valid_moves = None
        if self.__orientation is Car.VERTICAL:
            valid_moves = {'u': "moves the car one cell upwards",
                           'd': "moves the car one cell downward"}
        if self.__orientation is Car.HORIZONTAL:
            valid_moves = {'r': "moves the car one cell to the right",
                           'l': "moves the car one cell to the left"}
        return valid_moves

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        required_empty_cell = []
        coordinates = self.car_coordinates()
        if self.__orientation is Car.VERTICAL:
            if movekey is Car.UP:
                required_empty_cell.append(
                    (coordinates[0][0] - 1, coordinates[0][1]))
            if movekey is Car.DOWN:
                required_empty_cell.append(
                    (coordinates[-1][0] + 1, coordinates[-1][1]))
        if self.__orientation is Car.HORIZONTAL:
            if movekey is Car.RIGHT:
                required_empty_cell.append(
                    (coordinates[-1][0], coordinates[-1][1] + 1))
            if movekey is Car.LEFT:
                required_empty_cell.append(
                    (coordinates[0][0], coordinates[0][1] - 1))
        return required_empty_cell

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in Car.POSSIBLE_MOVES:
            return False
        if movekey is Car.UP and self.__orientation is Car.VERTICAL:
            self.__location = (self.__location[0] - 1, self.__location[1])
            return True
        elif movekey is Car.DOWN and self.__orientation is Car.VERTICAL:
            self.__location = (self.__location[0] + 1, self.__location[1])
            return True
        elif movekey is Car.RIGHT and self.__orientation is Car.HORIZONTAL:
            self.__location = (self.__location[0], self.__location[1] + 1)
            return True
        elif movekey is Car.LEFT and self.__orientation is Car.HORIZONTAL:
            self.__location = (self.__location[0], self.__location[1] - 1)
            return True
        else:
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
