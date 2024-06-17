from game_graphics import *
from menu_graphics import *
import random


def main():  # Main function
    global board
    running = True
    screen = Screens.main
    clock = pygame.time.Clock()
    winning_color = None
    bot_difficulty = 0
    while running:  # Starts game loop

        clock.tick(FPS)  # Sets FPS

        for event in pygame.event.get():  # Gets events
            if event.type == pygame.QUIT:  # If event is quit
                running = False  # Stop the loop

            if event.type == pygame.MOUSEBUTTONUP:  # If event is mouse up (click)
                if screen == Screens.pvp or screen == screen.pvc:  # If in 1v1
                    on_mouse_click_pvp(event.button)  # Call on mouse for pvp

            if event.type == pygame.KEYUP:  # If a key is pressed
                if event.key == pygame.K_z:  # If key is Z
                    if screen == Screens.pvp:  # If in 1v1
                        board.undo()
                if event.key == pygame.K_r:  # If key is R
                    if screen == Screens.pvp:  # If in 1v1
                        board.redo()
                if event.key == pygame.K_SPACE:  # If key is R
                    # if screen == Screens.pvp:  # If in 1v1
                    move = minimax(board, 2, board.turn, True)[1]
                    board.move(move[0], move[1])

        if screen == Screens.main:  # If in main menu
            update_screen_menu()
            if pvp.click():  # If clicked on pvp
                # Go to game
                screen = Screens.pvp
                winning_color = None

            elif pvc.click():  # If clicked on pvc
                screen = Screens.pvc_choose
                winning_color = None

            elif main_quit_game.click():  # If clicked on quit
                running = False  # Stop game

        elif screen == Screens.pvp:  # If in 1v1
            if board.is_checkmate(Color.White):  # If white lost
                # End game
                screen = Screens.end_screen
                winning_color = Color.Black
            elif board.is_checkmate(Color.Black):  # If black lost
                # End game
                screen = Screens.end_screen
                winning_color = Color.White

            board.set_coronation()  # Check coronation and do coronation
            update_screen_in_game()  # Update board

        elif screen == Screens.pvc:
            if board.is_checkmate(Color.White):  # If white lost
                # End game
                screen = Screens.end_screen
                winning_color = Color.Black
            elif board.is_checkmate(Color.Black):  # If black lost
                # End game
                screen = Screens.end_screen
                winning_color = Color.White
            elif board.turn == Color.Black:
                update_screen_in_game()  # Update board
                if bot_difficulty:
                    move = minimax(board, bot_difficulty, board.turn, True)[1]
                    board.move(move[0], move[1])
                else:
                    move = random.choice(board.get_possible_moves())
                    board.move(move[0], move[1])
            update_screen_in_game()  # Update board

        elif screen == Screens.pvc_choose:
            update_screen_pvc_choose()
            if super_easy.click():
                screen = Screens.pvc
                bot_difficulty = 0
            elif easy.click():
                screen = Screens.pvc
                bot_difficulty = 1
            elif medium.click():
                screen = Screens.pvc
                bot_difficulty = 2
            elif hard.click():
                screen = Screens.pvc
                bot_difficulty = 3
            elif pvc_choose_main_menu.click():
                screen = Screens.main
            elif pvc_choose_quit_game.click():
                running = False

        elif screen == Screens.end_screen:
            end_screen(winning_color)  # Show ending screen

            if main_menu.click():  # If clicked on main menu button
                # Go to menu
                screen = Screens.main
                winning_color = None

                board.reset()  # Reset board

            if end_quit_game.click():  # If clicked on quit button
                running = False  # Quit


main()
