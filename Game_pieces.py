import pygame
from Graphics_classes import Marker


class Board:
    """class to initialize the board space and track entry and exit paths"""

    def __init__(self, list_atoms, screen):
        """initialization of board"""
        self._board = [['' for num in range(10)] for num in range(10)]
        self.place_atoms_corners(list_atoms)
        self._image = pygame.image.load('board.bmp')
        self._marker_list = []
        self.create_markers(screen)
        self._atom_list = list_atoms

    def get_atom_left(self):
        """return number of atoms"""
        return len(self._atom_list)

    def place_atoms_corners(self, list_atoms):
        """places atoms on the board as 'x' and 'o' in corners"""
        # for every atom, place an 'x' on the board
        for atom in list_atoms:
            row, column = atom
            self._board[row][column] = "x"
        # place a 'o' in each corner
            self._board[0][0] = "o"
            self._board[9][9] = "o"
            self._board[9][0] = "o"
            self._board[0][9] = "o"

    def create_markers(self, screen):
        """generate a list of markers to be attached to in-out locations"""
        color_list = [(0, 255, 0), (255, 255, 255), (0, 200, 0),
                      (0, 0, 128), (0, 0, 255), (200, 0, 0), (255, 100, 100),
                      (255, 0, 230), (255, 100, 10), (115, 0, 0), (0, 255, 255)]

        for color in color_list:
            self._marker_list.append(Marker(color, screen))

    def get_color_marker_b(self):
        """return first colored marker off list"""
        return self._marker_list.pop()

    def get_board_item(self, row_pos, column_pos):
        """returns character on board at location given"""
        return self._board[row_pos][column_pos]

    def find_exit(self, entry_x, entry_y):
        """
        Finds the edge iteration of exit solution and then calls function to
        complete final path finding inside game board
        :param entry_x: entry point of row
        :param entry_y: entry point of column
        :return: returns None if hit, otherwise returns exit coordinate in tuple
        """
        # direction is step direction.  d for down, u for up, r right
        # l for left.  first 2 are for row, column direction when added.  second
        # 2 numbers describe the boxes "small"(subtract) or "large"(add) to
        # either side of the "middle"

        if entry_x == 0:
            direction = [1, 0, 0, 1, "d"]
        elif entry_x == 9:
            direction = [-1, 0, 0, 1, "u"]
        elif entry_y == 0:
            direction = [0, 1, 1, 0, "r"]
        elif entry_y == 9:
            direction = [0, -1, 1, 0, "l"]

        next_middle, next_large, next_small = \
            self.pull_locations(entry_x, entry_y, direction)

        # hit or reflection coming right off the edge
        if next_middle == 'x':
            return 0
        elif next_large == 'x' or next_small == 'x':
            return 1

        # otherwise enter the game board and ultimately return tuple
        else:
            entry_x = entry_x + direction[0]
            entry_y = entry_y + direction[1]
            return self.follow_path(entry_x, entry_y, direction)

    def follow_path(self, entry_x, entry_y, direction):
        """
        2nd part of find_exit() to loop through game board "path"
        :param entry_x: entry of game board x
        :param entry_y: entry of game board y
        :param direction: direction of travel
        :return: None if a "hit" is found, otherwise return exit coord in tuple
        """

        while entry_x not in [0, 9] and entry_y not in [0,9]:

            next_middle, next_large, next_small = \
                self.pull_locations(entry_x, entry_y, direction)

            # found a "hit" return None
            if next_middle == 'x':
                return 0
            else:
                direction = self.calculate_direction(next_large, next_small,
                                                     direction)
            # advance to the next square
            entry_x = entry_x + direction[0]
            entry_y = entry_y + direction[1]

        return entry_x, entry_y

    def pull_locations(self, entry_x, entry_y, direction):
        """
        Helper function to simplify follow path.  Pulls board locations for
        next_middle, next_large, next_small
        :param entry_x: location on board in row
        :param entry_y: location on board in column
        :param direction: direciton travelling
        :return: next_middle, next_large, next_small
        """

        # pull next "middle" of 3 in play pieces from board and return
        next_middle = self._board[entry_x + direction[0]][
            entry_y + direction[1]]
        # pull next "towards bottom/right" of 3 in play pieces from board
        next_large = self._board[entry_x + direction[0] + direction[2]] \
            [entry_y + direction[1] + direction[3]]
        # pull next "towards upper/left of 3 in play pieces from board
        next_small = self._board[entry_x + direction[0] - direction[2]] \
            [entry_y + direction[1] - direction[3]]

        return next_middle, next_large, next_small

    def calculate_direction(self, next_large, next_small, direction):
        """
        calculate direction based on next_large, next_small and return direction
        :param next_large: location on board next large
        :param next_small: location on board next small
        :param direction: current direction
        :return: new direction
        """
        # (go down for left/right or go right for up/down previous)
        if next_small == 'x':
            # if both are 'x' then have to do a 180
            if next_large == 'x':
                if direction[4] == 'u':
                    direction = [1, 0, 0, 1, "d"]
                elif direction[4] == 'd':
                    direction = [-1, 0, 0, 1, "u"]
                elif direction[4] == 'r':
                    direction = [0, -1, 1, 0, "l"]
                elif direction[4] == 'l':
                    direction = [0, 1, 1, 0, "r"]
            # otherwise just take the appropriate 90 degree turn
            elif direction[4] == 'u' or direction[4] == 'd':
                direction = [0, 1, 1, 0, "r"]
            elif direction[4] == 'l' or direction[4] == 'r':
                direction = [1, 0, 0, 1, "d"]

        # (go up for left/right or go left for up/down previous)
        elif next_large == 'x':
            if direction[4] == 'u' or direction[4] == 'd':
                direction = [0, -1, 1, 0, "l"]
            elif direction[4] == 'l' or direction[4] == 'r':
                direction = [-1, 0, 0, 1, "u"]

        return direction


class Player:
    """Class to track the player's points and store move/guess locations"""

    def __init__(self, screen, bb_settings):
        """moves will track the players previous moves and guesses"""
        self._moves = {}
        self._atom_guess = {}
        self.bb_settings = bb_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self._score_image = None
        self._score_rect = None
        self._atom_image = None
        self._atom_rect = None

    def get_moves(self):
        """returns the list of entry and exit the player has visited"""
        return self._moves

    def get_atom_guesses(self):
        """returns atom guesses"""
        return self._atom_guess

    def add_atom_guess(self, guess, marker):
        """
        checks if a guess is in player's history and returns true and adds
        the guess and decrements how many are left.  Otherwise returns false
        :param guess: current guess tuple being taken
        :return: True if not in previous guesses, false otherwise
        """
        if guess in self._atom_guess:
            return False
        else:
            self._atom_guess[guess] = marker
            return True

    def add_entry_exit(self, entry, marker_obj, exit_tup=None):
        """
        accepts an entry and optional exit tuple and checks if either are in
        previous history.  If both are, no decrement.  if one or the other are
        then decrement player score by 1.  If neither, dec 2
        :param entry: entry tuple
        :param marker_obj: marker to be placed in dictionary
        :param exit_tup: exit tuple
        :return: none
        """
        count = 0
        # check if the entry tuple has already been added to dictionary
        if entry not in self._moves.keys():
            # if it hasn't, check if exit tuple is not default
            if exit_tup not in [0, 1]:
                # add them both and add the "reverse" trip
                self._moves[entry] = [exit_tup, marker_obj]
                self._moves[exit_tup] = [entry, marker_obj]
                # 1 for a reflection, 2 for other paths
                if exit_tup == entry:
                    count += 1
                else:
                    count += 2
            else:
                # just add the entry.  This represents a Hit or edge reflection
                self._moves[entry] = None
                count += 1

        return count




