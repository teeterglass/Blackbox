# Author: John Teeter
# Date: 7/28/2020
# Description:  Black box game.  This will represent the black box game where
#  "atom" locations will be sent to the inside 9x9 of a 10x10 game board
# where the player will pass "rays" in from the outside ring of the game board
# and depending on the ray's intersection with atoms, will determine their exit
# locations.  Players will start off with 25 points.  1 point deducted for every
# entrance and exit.  5 points deducted for a wrong atom guess.  Game is over
# when player guesses locations of all atoms or points go negative.

import sys
import pygame
from functools import wraps
from Game_pieces import Board, Player
from settings import Settings, GameStats
from random import randint
from Graphics_classes import Button, Marker, Scoreboard


class BlackBoxGame:
    """Main game class to create Board object using Board class, create a
     player object using Player class, and create a list of Atom locations"""

    class ScoreChecker:
        """Class to add decorators to methods that impact player's score"""
        @classmethod
        def check_score(cls, func):
            """checks to see if player has any points left"""
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                # check if score is positive
                if self._stats.get_points() > 0 and \
                        self._stats.get_num_atoms_left() > 0:
                    result = func(self, *args, **kwargs)
                    return result
                else:
                    return self._stats.set_status("replay")

            return wrapper

    def __init__(self):
        """initialize the parameters for the game"""
        self._board = None
        self._bb_settings = Settings()
        self._screen = pygame.display.set_mode((self._bb_settings.screen_width,
                                                self._bb_settings.screen_height))
        self._player = Player()
        self._stats = GameStats(self._bb_settings)
        self._scoreboard = Scoreboard(self._bb_settings, self._screen)
        self._image = pygame.image.load('board.bmp')
        self._rect = self._image.get_rect()
        self._play_mode_button_list = self.make_play_mode_buttons()
        self._replay_button_list = self.make_replay_buttons()

    def setup_new_game(self):
        """setup all parameters for a fresh game"""
        self._player = Player()
        self._stats = GameStats(self._bb_settings)
        self._scoreboard = Scoreboard(self._bb_settings, self._screen)

    def update_board_atoms(self, list_atoms):
        """update atoms after user picks how many they want"""
        self._board = Board(list_atoms, self._screen)
        self._stats.update_num_atoms(len(list_atoms))

    def calculate_entry_exit(self, pos_y, pos_x):
        """calculate screen positions on grid given x, y"""
        return (pos_y * 70 + 35), (pos_x * 70 + 35)

    @ScoreChecker.check_score
    def shoot_ray(self, entry_x, entry_y):
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
                marker = self.get_hit_marker()
                circle_tuple = self.calculate_entry_exit(entry_y, entry_x)
                marker.update_center(circle_tuple)
                points = self._player.add_entry_exit((entry_x, entry_y), marker,
                                                     (entry_x, entry_y))
                self._stats.dec_player_score(points)
                return "Hit"
            elif exit_tup == 1:
                # decrement entry only if not visited
                marker = self.get_reflect_marker()
                circle_tuple = self.calculate_entry_exit(entry_y, entry_x)
                marker.update_center(circle_tuple)
                points = self._player.add_entry_exit((entry_x, entry_y), marker,
                                            (entry_x, entry_y))

                self._stats.dec_player_score(points)

                return "reflect"
            else:
                # decrement both entry and exit if not already visited
                marker = self.get_color_marker()
                exit_x, exit_y = exit_tup
                circle_entry = self.calculate_entry_exit(entry_y, entry_x)
                circle_exit = self.calculate_entry_exit(exit_y, exit_x)
                marker.update_center(circle_entry, circle_exit)
                points = self._player.add_entry_exit((entry_x, entry_y),
                                                     marker, exit_tup)

                self._stats.dec_player_score(points)
                return exit_tup
        else:
            # returns false if the shoot_ray point is invalid
            return "Bad shot"

    @ScoreChecker.check_score
    def guess_atom(self, atom_x, atom_y):
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
            marker = self.get_atom_hit()
            circle_tuple = self.calculate_entry_exit(atom_y, atom_x)
            marker.update_center(circle_tuple)
            self._player.add_atom_guess((atom_x, atom_y), marker)
            self._stats.remove_atom()
            return True
        else:
            # use the true/false in add_atom_guess return logic to decrement
            marker = self.get_atom_miss()
            circle_tuple = self.calculate_entry_exit(atom_y, atom_x)
            marker.update_center(circle_tuple)
            if self._player.add_atom_guess((atom_x, atom_y), marker):
                self._stats.dec_player_score(5)
                return False
            else:
                return False

    def get_color_marker(self):
        """get color marker from board list"""
        return self._board.get_color_marker_b()

    def get_hit_marker(self):
        """get hit marker from board"""
        return Marker((0, 0, 0), self._screen)

    def get_reflect_marker(self):
        """get reflect white marker from board class"""
        return Marker((255, 255, 255), self._screen)

    def get_atom_hit(self):
        """get atom hit marker from board class"""
        return Marker((0, 128, 0), self._screen)

    def get_atom_miss(self):
        """get atom miss marker from board class"""
        return Marker((255, 0, 0), self._screen)

    def get_score(self):
        """returns player's score"""
        return self._stats.get_points()

    def atoms_left(self):
        """return number of atoms left to find"""
        return self._board.get_atoms()

    def get_entry_exit(self):
        """return player's entry/exit list"""
        return self._player.get_moves()

    def get_atom_guess(self):
        """return player's atom guess list"""
        return self._player.get_atom_guesses()

    def get_board_image(self):
        """return board image"""
        return self._board.get_board_image()

    def blitme(self):
        """Draw the board at its current location."""
        score_image, score_rect, atom_image, atom_rect = \
            self._scoreboard.get_score_image_rect(self._stats.get_points(),
                                             self._stats.get_num_atoms_left())

        self._screen.blit(score_image, score_rect)
        self._screen.blit(atom_image, atom_rect)
        self._screen.blit(self._image, self._rect)

    def check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self._stats.get_status() == "Start_game":
                    self.check_game_mode_button(mouse_x, mouse_y)
                elif self._stats.get_status() == "replay":
                    self.check_replay_button(mouse_x, mouse_y)
                else:
                    self.check_click(mouse_x, mouse_y)

    def check_game_mode_button(self, mouse_x, mouse_y):
        """Start a new game when the player clicks play"""
        for button in self._play_mode_button_list:
            if button.get_button_rect().collidepoint(mouse_x, mouse_y):
                button_clicked = button
                break
            else:
                button_clicked = None

        if button_clicked is not None and \
                self._stats.get_status() == "Start_game":
            self.start_game(button_clicked.get_num_atom())

    def check_replay_button(self, mouse_x, mouse_y):
        """check if they select yes or no"""
        for button in self._replay_button_list:
            if button.get_button_rect().collidepoint(mouse_x, mouse_y):
                button_clicked = button
                break
            else:
                button_clicked = None

        if button_clicked is not None and button_clicked.get_num_atom() == 1:
            self.setup_new_game()
        elif button_clicked is not None and button_clicked.get_num_atom() == 2:
            sys.exit()

    def manual_input(self):
        """create manual 4 atom list"""
        atom_list = []
        while len(atom_list) < 4:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    column = mouse_x // 70
                    row = mouse_y // 70
                    if 0 < column < 9 and 0 < row < 9:
                        if (row, column) not in atom_list:
                            atom_list.append((row, column))
        return atom_list

    def start_game(self, num_atom):
        """Start a new game"""

        # Reset the game statistics
        self._stats.set_status("playing")
        self.update_screen()
        if type(num_atom) == str:
            atom_list = self.manual_input()
            self.update_board_atoms(atom_list)
        else:
            atom_list = []
            while len(atom_list) < num_atom:
                atom_tup = randint(1, 8), randint(1, 8)
                if atom_tup not in atom_list:
                    atom_list.append(atom_tup)
            self.update_board_atoms(atom_list)

    def check_click(self, mouse_x, mouse_y):
        """Identify what the tuple is the player clicked on
        """
        # Change the x/y screen coordinates to grid coordinates
        column = mouse_x // 70
        row = mouse_y // 70

        if row in [0, 9] or column in [0, 9]:
            self.shoot_ray(row, column)
        elif 0 < row < 9 and 0 < column < 9:
            self.guess_atom(row, column)

    def update_screen(self):
        """update images on the screen and flip to the new screen"""

        # Redraw the screen during each pass through the loop.
        self._screen.fill(self._bb_settings.bg_color)

        # Redraw all markers around edge of board

        # Draw the play button if the game is inactive
        if self._stats.get_status() == "Start_game":
            for button in self._play_mode_button_list:
                button.draw_button()
        elif self._stats.get_status() == "replay":
            for button in self._replay_button_list:
                button.draw_button()
        else:
            self.blitme()
            shoot_markers = self.get_entry_exit()
            atom_markers = self.get_atom_guess()
            for marker in shoot_markers.values():
                marker[1].draw_marker()
            for atom in atom_markers.values():
                atom.draw_marker()
        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def make_replay_buttons(self):
        """make a replay buttons"""
        play_button_list = []
        play_button_1a = Button(self._screen, "Would you like to play again?",
                                350, 162, 0, True)
        play_button_list.append(play_button_1a)
        play_button_2a = Button(self._screen, "Yes", 200, 350, 1)
        play_button_list.append(play_button_2a)
        play_button_3a = Button(self._screen, "No", 500, 350, 2)
        play_button_list.append(play_button_3a)

        return play_button_list

    def make_play_mode_buttons(self):
        """
        Makes play button object list
        :return: list of 6 play buttons
        """
        play_button_list = []
        play_button_1a = Button(self._screen,"1 Atom Random", 200, 162, 1)
        play_button_list.append(play_button_1a)
        play_button_2a = Button(self._screen, "2 Atoms Random", 500, 162, 2)
        play_button_list.append(play_button_2a)
        play_button_3a = Button(self._screen, "3 Atoms Random", 200, 350, 3)
        play_button_list.append(play_button_3a)
        play_button_4a = Button(self._screen, "4 Atoms Random", 500, 350, 4)
        play_button_list.append(play_button_4a)
        play_button_5a = Button(self._screen, "5 Atoms Random", 200, 537, 5)
        play_button_list.append(play_button_5a)
        play_button_6a = Button(self._screen, "Manual 4 Atoms", 500, 537,
                                "4m")
        play_button_list.append(play_button_6a)

        return play_button_list


def main():
    """Full game play code"""

    pygame.init()
    pygame.display.init()

    # Set the pygame clock
    clock = pygame.time.Clock()

    pygame.display.set_caption("Blackbox game")
    current_game = BlackBoxGame()
    clock = pygame.time.Clock()

    while True:
        current_game.check_events()
        clock.tick(60)
        current_game.update_screen()

    pygame.quit()

if __name__ == '__main__':
    main()