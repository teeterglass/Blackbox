
import pygame
import sys
from random import randint
from functools import wraps
from time import sleep
from settings import Settings, GameStats
import game_functions as gf
from Blackboxgame_full import BlackBoxGame


def main():
    """Full game play code"""

    pygame.init()
    pygame.display.init()

    # Set up blackboard game settings
    bb_settings = Settings()

    # Set the pygame clock
    clock = pygame.time.Clock()

    # create a screen object
    screen = pygame.display.set_mode(
        (bb_settings.screen_width, bb_settings.screen_height))

    pygame.display.set_caption("Blackbox game")

    # initialize game stats
    stats = GameStats(bb_settings)

    # Make the Play Buttons.
    play_button_list = gf.make_play_buttons(bb_settings, screen)

    game = BlackBoxGame(screen, bb_settings)
    clock = pygame.time.Clock()


    while True:
        gf.check_events(bb_settings, screen, stats, play_button_list, game)
        clock.tick(60)
        gf.update_screen(bb_settings, screen, stats, play_button_list, game)

    pygame.quit()

if __name__ == '__main__':
    main()