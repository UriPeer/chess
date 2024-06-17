import pygame
from game_logic import *

pygame.init()

SCREEN = pygame.display.set_mode([1000, 1000])  # Set up the drawing window
pygame.display.set_caption("Chess Project")  # Set the name of the window
FPS = 60  # Sets the FPS of the game


# IN GAME GRAPHICS CONSTANTS
# Images
BOARD = pygame.image.load("Images/In_Game/Chess_Board.png")
EATING_EFFECT = pygame.image.load("Images/In_Game/Eating_Effect.png")
POINTING_ON_EFFECT = pygame.image.load("Images/In_Game/Pointing_On_Effect.png")
POINTING = pygame.image.load("Images/In_Game/Pointing_Effect.png")
POSSIBLE_MOVES = pygame.image.load("Images/In_Game/Possible_Move_Effect.png")
SELECTING_EFFECT = pygame.image.load("Images/In_Game/Selecting_Effect.png")
THREATENING_EFFECT = pygame.image.load("Images/In_Game/Threatening_Effect.png")
CHECK_EFFECT = pygame.image.load("Images/In_Game/Check_Effect.png")
LAST_MOVE_EFFECT = pygame.image.load("Images/In_Game/Last_Move_Effect.png")
CORONATION_EFFECT = pygame.image.load("Images/In_Game/Coronation_Effect.png")
UNDO = pygame.image.load("Images/In_Game/Undo.png")
REDO = pygame.image.load("Images/In_Game/Redo.png")

# Boarders
MIN_X = 100
MAX_X = 900
MIN_Y = 100
MAX_Y = 900

# Headers and sizes
HEADER_COL = 100
HEADER_ROW = 100
CELL_SIZE_COL = 100
CELL_SIZE_ROW = 100

# Buttons
UNDO_BUTTON_POS = Pos(-1, -1)
REDO_BUTTON_POS = Pos(-1, 0)
TURN_POS = Pos(-1, 8)
QUEEN_POS = Pos(2, 8)
KNIGHT_POS = Pos(3, 8)
ROOK_POS = Pos(4, 8)
BISHOP_POS = Pos(5, 8)


# MENU GRAPHICS CONSTANTS
# Images
SINGLE_PLAYER = pygame.image.load("Images/Main_Menu/Single_Player.png")
SINGLE_PLAYER_HOVER = pygame.image.load("Images/Main_Menu/Single_Player_Hover.png")
TWO_PLAYERS = pygame.image.load("Images/Main_Menu/Two_Players.png")
TWO_PLAYERS_HOVER = pygame.image.load("Images/Main_Menu/Two_Players_Hover.png")
QUIT = pygame.image.load("Images/Main_Menu/Quit_Game.png")
QUIT_HOVER = pygame.image.load("Images/Main_Menu/Quit_Game_Hover.png")
QUIT_MAIN = pygame.image.load("Images/Main_Menu/Quit_Game_Main.png")
QUIT_MAIN_HOVER = pygame.image.load("Images/Main_Menu/Quit_Game_Main_Hover.png")
MAIN_MENU_BUTTON = pygame.image.load("Images/Main_Menu/Main_Menu_Button.png")
MAIN_MENU_BUTTON_HOVER = pygame.image.load("Images/Main_Menu/Main_Menu_Button_Hover.png")
MAIN_MENU = pygame.image.load("Images/Main_Menu/Main_Menu.png")
WHITE_WON = pygame.image.load("Images/Main_Menu/White_Won.png")
BLACK_WON = pygame.image.load("Images/Main_Menu/Black_Won.png")
SUPER_EASY = pygame.image.load("Images/Main_Menu/Super_Easy.png")
SUPER_EASY_HOVER = pygame.image.load("Images/Main_Menu/Super_Easy_Hover.png")
EASY = pygame.image.load("Images/Main_Menu/Easy.png")
EASY_HOVER = pygame.image.load("Images/Main_Menu/Easy_Hover.png")
MEDIUM = pygame.image.load("Images/Main_Menu/Medium.png")
MEDIUM_HOVER = pygame.image.load("Images/Main_Menu/Medium_Hover.png")
HARD = pygame.image.load("Images/Main_Menu/Hard.png")
HARD_HOVER = pygame.image.load("Images/Main_Menu/Hard_Hover.png")
PVC_BACK = pygame.image.load("Images/Main_Menu/PVC.png")


class Button:
    def __init__(self, image, hover_image, x, y, scale):  # Gets button
        width = image.get_width()  # Get image sizes
        height = image.get_height()
        hover_width = hover_image.get_width()  # Get hover image sizes
        hover_height = hover_image.get_height()
        self.image = pygame.transform.scale(image, (width * scale, height * scale))  # Set image by scale
        self.hover_image = pygame.transform.scale(hover_image, (hover_width * scale, hover_height * scale))  # Set hover image by scale
        self.rect = self.image.get_rect()  # Get bounding box
        self.rect.topleft = (x, y)  # Set pos
        self.pressed = False

    def draw(self):  # Draws button and returns true if clicked
        pos = pygame.mouse.get_pos()  # Get mouse pos

        if self.rect.collidepoint(pos):  # If mouse hovers over the button
            SCREEN.blit(self.hover_image, (self.rect.x, self.rect.y))  # Draw hover picture
        else:  # If not hovered
            SCREEN.blit(self.image, (self.rect.x, self.rect.y))  # Load normal image

    def click(self):
        pos = pygame.mouse.get_pos()  # Get mouse pos

        if self.rect.collidepoint(pos):  # If mouse hovers over the button
            if pygame.mouse.get_pressed()[0] == 1:  # If pressed
                self.pressed = True  # Set pressed to true
            elif pygame.mouse.get_pressed()[0] == 0 and self.pressed:  # If not pressed and last time was pressed
                self.pressed = False  # Set pressed to false
                return True
        else:  # If not colliding
            self.pressed = False  # Set pressed to false(To avoid bugs)


class Screens(Enum):
    main = "main"
    pvp = "pvp"
    pvc = "pvc"
    pvc_choose = "pvc_ch"
    end_screen = "end"
