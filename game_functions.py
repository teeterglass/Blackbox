import sys
import pygame
from random import randint

from button import Button
from Blackboxgame_full import BlackBoxGame


def check_events(bb_settings, screen, stats, play_button_list, game):
    """Respond to keypresses and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not stats.game_active:
                check_play_button(bb_settings, screen, stats, play_button_list,
                                  mouse_x, mouse_y, game)
            else:
                check_click(bb_settings, screen, stats, mouse_x, mouse_y,
                                  game)

def check_play_button(bb_settings, screen, stats, play_button_list,
                      mouse_x, mouse_y, game):
    """Start a new game when the player clicks play"""
    for button in play_button_list:
        if button.rect.collidepoint(mouse_x, mouse_y):
            button_clicked = button
            break
        else:
            button_clicked = None

    if button_clicked is not None and not stats.game_active:
        start_game(bb_settings, screen, stats, play_button_list,
                   button_clicked.num_atom, game)


def manual_input():
    """create manual 4 atom list"""
    atom_list = []
    while len(atom_list) < 4:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                column = mouse_x // 70
                row = mouse_y // 70
                if column > 1 and column < 9 and row > 1 and row < 9:
                    if (row, column) not in atom_list:
                        atom_list.append((row, column))

    return atom_list

def start_game(bb_settings, screen, stats, play_button_list, num_atom, game):
    """Start a new game"""

    # Reset the game statistics
    stats.game_active = True
    update_screen(bb_settings, screen, stats, play_button_list, game)
    if type(num_atom) == str:
        atom_list = manual_input()
        game.update_board_atoms(atom_list, screen)
    else:
        atom_list = []
        while len(atom_list) < num_atom:
            atom_tup = randint(1, 8), randint(1, 8)
            if atom_tup not in atom_list:
                atom_list.append(atom_tup)

        game.update_board_atoms(atom_list, screen)


def check_click(bb_settings, screen, stats, mouse_x, mouse_y, game):
    """Identify what the tuple is the player clicked on
    """
    # Change the x/y screen coordinates to grid coordinates
    column = mouse_x // 70
    row = mouse_y // 70
    if (row in [0, 9] or column in [0, 9]):
        game.shoot_ray(row, column, screen)
    else:
        game.guess_atom(row, column, screen)


def update_screen(bb_settings, screen, stats, play_button_list, game):
    """update images on the screen and flip to the new screen"""

    # Redraw the screen during each pass through the loop.
    screen.fill(bb_settings.bg_color)

    # Redraw all markers around edge of board

    # Draw the play button if the game is inactive
    if not stats.game_active:
        for button in play_button_list:
            button.draw_button()
    else:
        if game is None:
            pass
        else:
            game.blitme()
            shoot_markers = game.get_entry_exit()
            atom_markers = game.get_atom_guess()
            for marker in shoot_markers.values():
                marker[1].draw_marker()
            for atom in atom_markers.values():
                atom.draw_marker()
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def make_play_buttons(bb_settings, screen):
    """
    Makes play button object list
    :return: list of 6 play buttons
    """
    play_button_list = []
    play_button_1a = Button(bb_settings, screen, "1 Atom Random", 200, 162, 1)
    play_button_list.append(play_button_1a)
    play_button_2a = Button(bb_settings, screen, "2 Atoms Random", 500, 162, 2)
    play_button_list.append(play_button_2a)
    play_button_3a = Button(bb_settings, screen, "3 Atoms Random", 200, 350, 3)
    play_button_list.append(play_button_3a)
    play_button_4a = Button(bb_settings, screen, "4 Atoms Random", 500, 350, 4)
    play_button_list.append(play_button_4a)
    play_button_5a = Button(bb_settings, screen, "5 Atoms Random", 200, 537, 5)
    play_button_list.append(play_button_5a)
    play_button_6a = Button(bb_settings, screen, "Manual 4 Atoms", 500, 537,
                            "4m")
    play_button_list.append(play_button_6a)

    return play_button_list
