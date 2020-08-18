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
        self.bb_settings = bb_settings
        self.game_active = False

