from graphics import *
from game_graphics import show_board

# Buttons
pvp = Button(TWO_PLAYERS, TWO_PLAYERS_HOVER, 450, 300, 1)
pvc = Button(SINGLE_PLAYER, SINGLE_PLAYER_HOVER, 450, 450, 1)
main_quit_game = Button(QUIT_MAIN, QUIT_MAIN_HOVER, 450, 650, 1)
end_quit_game = Button(QUIT, QUIT_HOVER, 266, 500, 0.45)
main_menu = Button(MAIN_MENU_BUTTON, MAIN_MENU_BUTTON_HOVER, 508, 500, 0.45)
super_easy = Button(SUPER_EASY, SUPER_EASY_HOVER, 250, 150, 1)
easy = Button(EASY, EASY_HOVER, 250, 300, 1)
medium = Button(MEDIUM, MEDIUM_HOVER, 250, 450, 1)
hard = Button(HARD, HARD_HOVER, 250, 600, 1)
pvc_choose_main_menu = Button(MAIN_MENU_BUTTON, MAIN_MENU_BUTTON_HOVER, 250, 735, 0.49)
pvc_choose_quit_game = Button(QUIT, QUIT_HOVER, 505, 735, 0.49)


def update_screen_menu():
    SCREEN.blit(MAIN_MENU, (0, 0))  # Load Screen
    pvp.draw()
    pvc.draw()
    main_quit_game.draw()
    pygame.display.update()


def update_screen_pvc_choose():
    SCREEN.blit(PVC_BACK, (0, 0))
    super_easy.draw()
    easy.draw()
    medium.draw()
    hard.draw()
    pvc_choose_main_menu.draw()
    pvc_choose_quit_game.draw()
    pygame.display.update()


def end_screen(color):  # Load end screen
    show_board()  # Load background board
    if color == Color.White:  # If white won
        SCREEN.blit(WHITE_WON, (0, 0))  # Load white won
    elif color == Color.Black:  # If black won
        SCREEN.blit(BLACK_WON, (0, 0))  # Load black won

    # Load buttons
    end_quit_game.draw()
    main_menu.draw()

    pygame.display.update()
