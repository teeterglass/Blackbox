from pygame import font


class Settings():
    """A class to store all settings for Blackboard game"""

    def __init__(self):
        """Initialize the games's static settings."""
        # Screen Settings
        self.screen_width = 900
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        self.line_color = (0, 0, 0)
        self.square_width = 70
        self.square_height = 70
        self.margin = 10
        self.font = font.SysFont(None, 24)
        self.text_color = (30, 30, 30)


class GameStats():
    """Track statistics for Blackbox game"""

    def __init__(self, bb_settings):
        """Initialize statistics."""
        self._bb_settings = bb_settings
        self._game_active = "Start_game"
        self._points = 25
        self._atom_left = 0

    def set_status(self, new_value):
        """set status to a new value"""
        self._game_active = new_value

    def get_status(self):
        """return status of game"""
        return self._game_active

    def update_num_atoms(self, num_atoms):
        """recieve initial number of atoms"""
        self._atom_left = num_atoms

    def get_num_atoms_left(self):
        """return number of atoms left to be guessed"""
        return self._atom_left

    def remove_atom(self):
        """removes atom from list if guessed right"""
        self._atom_left -= 1

    def get_points(self):
        """returns the current point total for a player"""
        return self._points

    def dec_player_score(self, count):
        """decrements player's score by given count"""
        self._points -= count

