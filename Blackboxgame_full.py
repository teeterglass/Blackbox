# Author: John Teeter
# Date: 7/28/2020
# Description:  Black box game.  This will represent the black box game where
#  "atom" locations will be sent to the inside 9x9 of a 10x10 game board
# where the player will pass "rays" in from the outside ring of the game board
# and depending on the ray's intersection with atoms, will determine their exit
# locations.  Players will start off with 25 points.  1 point deducted for every
# entrance and exit.  5 points deducted for a wrong atom guess.  Game is over
# when player guesses locations of all atoms or points go negative.

import pygame
from functools import wraps


class BlackBoxGame:
    """Main game class to create Board object using Board class, create a
     player object using Player class, and create a list of Atom locations"""

    class ScoreChecker:
        @classmethod
        def check_score(cls, func):
            """checks to see if player has any points left"""
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                # check if score is positive
                if self.get_score() > 0:
                    res = func(self, *args, **kwargs)
                    return res
            return wrapper

    def __init__(self, screen, bb_settings):
        """initialize the parameters for the game"""
        self._board = None
        # generate a player
        self._player = Player(screen, bb_settings)
        self.image = pygame.image.load('board.bmp')
        self.rect = self.image.get_rect()
        self.screen = screen

    def print_board(self):
        """Prints the existing board for trouble shooting"""
        for row in self._board.get_whole_board():
            print(row)

    def update_board_atoms(self, list_atoms, screen):
        """update atoms after user picks how many they want"""
        self._board = Board(list_atoms, screen)
        self._player.update_num_atoms(len(list_atoms))

    def calculate_entry_exit(self, pos_y, pos_x):
        """calculate screen positions on grid given x, y"""
        return (pos_y * 70 + 35), (pos_x * 70 + 35)

    @ScoreChecker.check_score
    def shoot_ray(self, entry_x, entry_y, screen):
        """
        checks if coordinates are valid, modifies score correctly and returns
        exit tuple if applicable
        :param entry_x: row coordinate
        :param entry_y: column coordinate
        :return: False if incorrect location.  None if hit.  Exit Tuple else
        """
        # check to make sure entry_x and entry_y are valid
        if (entry_x in [0, 9] or entry_y in [0, 9]) and \
                self._board.get_board_item(entry_x, entry_y) != "o":

            exit_tup = self._board.find_exit(entry_x, entry_y)
            # returned 0 if hit
            if exit_tup == 0:
                # decrement entry only if not visited
                marker = self.get_hit_marker(screen)
                circle_tuple = self.calculate_entry_exit(entry_y, entry_x)
                marker.update_center(circle_tuple)
                self._player.add_entry_exit((entry_x, entry_y), marker,
                                            (entry_x, entry_y))
                return "Hit"
            elif exit_tup == 1:
                # decrement entry only if not visited
                marker = self.get_reflect_marker(screen)
                circle_tuple = self.calculate_entry_exit(entry_y, entry_x)
                marker.update_center(circle_tuple)
                self._player.add_entry_exit((entry_x, entry_y), marker,
                                            (entry_x, entry_y))
                return "reflect"
            else:
                # decrement both entry and exit if not already visited
                marker = self.get_color_marker()
                exit_x, exit_y = exit_tup
                circle_entry = self.calculate_entry_exit(entry_y, entry_x)
                circle_exit = self.calculate_entry_exit(exit_y, exit_x)
                marker.update_center(circle_entry, circle_exit)
                self._player.add_entry_exit((entry_x, entry_y),
                                            marker, exit_tup)
                return exit_tup
        else:
            # returns false if the shoot_ray point is invalid
            return "Bad shot"

    @ScoreChecker.check_score
    def guess_atom(self, atom_x, atom_y, screen):
        """
        Checks if atom where guessed by player and decrements if not.  Removes
        atom from list stored
        :param atom_x: row coordinate
        :param atom_y: column coordinate
        :screen: screen details
        :return: True if atom is there, False otherwise
        """

        if self._board.get_board_item(atom_x, atom_y) == 'x':
            # if there, add to player's list and remove from board list
            marker = self.get_atom_hit(screen)
            circle_tuple = self.calculate_entry_exit(atom_y, atom_x)
            marker.update_center(circle_tuple)
            self._player.add_atom_guess((atom_x, atom_y), marker)
            self._player.remove_atom()
            print("hit")
            return True
        else:
            # use the true/false in add_atom_guess return logic to decrement
            marker = self.get_atom_miss(screen)
            circle_tuple = self.calculate_entry_exit(atom_y, atom_x)
            marker.update_center(circle_tuple)
            if self._player.add_atom_guess((atom_x, atom_y), marker):
                self._player.dec_player_score(5)
                print("miss - 5")
                return False
            else:
                print("miss 0")
                return False

    def get_color_marker(self):
        """get color marker from board"""
        return self._board.get_color_marker_b()

    def get_hit_marker(self, screen):
        """get hit marker from board"""
        return self._board.get_hit_marker_b(screen)

    def get_reflect_marker(self, screen):
        """get reflect white marker from board class"""
        return self._board.get_reflect_marker_b(screen)

    def get_atom_hit(self, screen):
        """get atom hit marker from board class"""
        return self._board.get_atom_hit_b(screen)

    def get_atom_miss(self, screen):
        """get atom miss marker from board class"""
        return self._board.get_atom_miss_b(screen)

    def get_score(self):
        """returns player's score"""
        return self._player.get_points()

    def atoms_left(self):
        """return number of atoms left to find"""
        return self._board.get_atoms()

    def get_entry_exit(self):
        """return player's entry/exit list"""
        return self._player.get_moves()

    def get_atom_guess(self):
        """return player's atom guess list"""
        return self._player.get_atom_guess()

    def get_board_image(self):
        """return board image"""
        return self._board.get_board_image()

    def blitme(self):
        """Draw the board at its current location."""
        score_image, score_rect, atom_image, atom_rect = \
            self._player.get_score_image_rect()

        self.screen.blit(score_image, score_rect)
        self.screen.blit(atom_image, atom_rect)
        self.screen.blit(self.image, self.rect)


class Marker:
    """Class to model a pair of markers for the entry, exit locations/atoms"""
    def __init__(self, color, screen):
        """initialization of marker variables"""
        self.screen = screen
        self.screen_circle = screen.get_rect()
        self.circle_center = (0, 0), (0, 0)
        self.circle_color = color
        # Build the button's rect object and center it
        self.circle_rad = 30

    def draw_marker(self):
        """Draw a blank marker(s) for entry/exit/atom"""
        pygame.draw.circle(self.screen, self.circle_color, self.circle_center[0],
                           self.circle_rad)
        if self.circle_center[1] != (0,0):
            pygame.draw.circle(self.screen, self.circle_color,
                               self.circle_center[1], self.circle_rad)

    def update_center(self, center_entry, center_exit=(0, 0)):
        """updates center once marker has been assigned"""
        self.circle_center = center_entry, center_exit


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

    def get_hit_marker_b(self, screen):
        """returns black marker"""
        return Marker((0, 0, 0), screen)

    def get_reflect_marker_b(self, screen):
        """returns a white marker"""
        return Marker((255, 255, 255), screen)

    def get_atom_hit_b(self, screen):
        """returns a green marker"""
        return Marker((0, 128, 0), screen)

    def get_atom_miss_b(self, screen):
        """returns a red marker"""
        return Marker((255, 0, 0), screen)

    def get_board_item(self, row_pos, column_pos):
        """returns character on board at location given"""
        return self._board[row_pos][column_pos]

    def get_board_image(self):
        """returns board image"""
        return self._image

    def get_whole_board(self):
        """returns entire board for printing"""
        return self._board

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


class Player:
    """Class to track the player's points and store move/guess locations"""

    def __init__(self, screen, bb_settings):
        """moves will track the players previous moves and guesses"""
        self._moves = {}
        self._atom_guess = {}
        self._points = 25
        self._atom_left = 0
        self.bb_settings = bb_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self._score_image = None
        self._score_rect = None
        self._atom_image = None
        self._atom_rect = None
        self.prep_score_board()

    def update_num_atoms(self, num_atoms):
        """recieve initial number of atoms"""
        self._atom_left = num_atoms

    def remove_atom(self):
        """removes atom from list if guessed right"""
        self._atom_left -= 1

    def get_moves(self):
        """returns the list of entry and exit the player has visited"""
        return self._moves

    def get_points(self):
        """returns the current point total for a player"""
        return self._points

    def get_atom_guess(self):
        """returns the atom guesses the player has already taken"""
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

        self.dec_player_score(count)

    def dec_player_score(self, count):
        """decrements player's score by given count"""
        self._points -= count

    def prep_score_board(self):
        """Turn the score into a rendered image."""

        current_score = str(self._points) + " Points"
        num_atoms = str(self._atom_left) + " Atoms left"
        self._score_image = self.bb_settings.font.render(current_score, True,
                                             self.bb_settings.text_color,
                                             self.bb_settings.bg_color)

        self._atom_image = self.bb_settings.font.render(num_atoms, True,
                                             self.bb_settings.text_color,
                                             self.bb_settings.bg_color)
        # Display the score at the top right of the screen.
        self._score_rect = self._score_image.get_rect()
        self._score_rect.right = self.screen_rect.right - 20
        self._score_rect.top = 20

        self._atom_rect = self._atom_image.get_rect()
        self._atom_rect.right = self.screen_rect.right - 20
        self._atom_rect.top = 80

    def get_score_image_rect(self):
        """returns score image and rect"""
        current_score = str(self._points) + " Points"
        if self._points <= 0:
            num_atoms = "You lost!"
        elif self._atom_left > 0:
            num_atoms = str(self._atom_left) + " Atoms left"
        else:
            num_atoms = "You Won!"

        self._score_image = self.bb_settings.font.render(current_score, True,
                                             self.bb_settings.text_color,
                                             self.bb_settings.bg_color)

        self._atom_image = self.bb_settings.font.render(num_atoms, True,
                                             self.bb_settings.text_color,
                                             self.bb_settings.bg_color)

        return self._score_image, self._score_rect, \
               self._atom_image, self._atom_rect
