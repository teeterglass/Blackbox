import pygame


class Button:
    """Class to describe a button"""

    def __init__(self, bb_settings, screen, msg, x_center, y_center, num_atom):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 100
        self.button_color = (0, 0, 140)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 28)
        self.num_atom = num_atom

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x_center, y_center)

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """msg is not a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw a blank button and then draw message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Marker:
    """Class to model a pair of markers for the entry, exit locations/atoms"""
    def __init__(self, color, screen):
        """initialization of marker variables"""
        self._screen = screen
        self._screen_circle = self._screen.get_rect()
        self._circle_center = (0, 0), (0, 0)
        self._circle_color = color
        # Build the button's rect object and center it
        self._circle_rad = 30

    def draw_marker(self):
        """Draw a blank marker(s) for entry/exit/atom"""
        pygame.draw.circle(self._screen, self._circle_color,
                           self._circle_center[0], self._circle_rad)
        if self._circle_center[1] != (0, 0):
            pygame.draw.circle(self._screen, self._circle_color,
                               self._circle_center[1], self._circle_rad)

    def update_center(self, center_entry, center_exit=(0, 0)):
        """updates center once marker has been assigned"""
        self._circle_center = center_entry, center_exit


class Scoreboard:
    """class to describe the score board operations"""

    def __init__(self, bb_settings, screen):
        self._bb_settings = bb_settings
        self._screen = screen
        self._screen_rect = self._screen.get_rect()
        self.prep_score_board()

    def prep_score_board(self):
        """Turn the score into a rendered image."""

        current_score = "Lets get started!"
        num_atoms = "Atoms to be found!"
        self._score_image = self._bb_settings.font.render(current_score, True,
                                             self._bb_settings.text_color,
                                             self._bb_settings.bg_color)

        self._atom_image = self._bb_settings.font.render(num_atoms, True,
                                             self._bb_settings.text_color,
                                             self._bb_settings.bg_color)
        # Display the score at the top right of the screen.
        self._score_rect = self._score_image.get_rect()
        self._score_rect.right = self._screen_rect.right - 20
        self._score_rect.top = 20

        self._atom_rect = self._atom_image.get_rect()
        self._atom_rect.right = self._screen_rect.right - 20
        self._atom_rect.top = 80

    def get_score_image_rect(self, points, atom_left):
        """returns score image and rect"""
        current_score = str(points) + " Points"
        if points <= 0:
            num_atoms = "You lost!"
        elif atom_left > 0:
            num_atoms = str(atom_left) + " Atoms left"
        else:
            num_atoms = "You Won!"

        self._score_image = self._bb_settings.font.render(current_score, True,
                                             self._bb_settings.text_color,
                                             self._bb_settings.bg_color)

        self._atom_image = self._bb_settings.font.render(num_atoms, True,
                                             self._bb_settings.text_color,
                                             self._bb_settings.bg_color)

        return self._score_image, self._score_rect, \
               self._atom_image, self._atom_rect


