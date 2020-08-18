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