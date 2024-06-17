from graphics import *

select_click = None
board = Board()  # Set board


def show_hover():  # Draws pointing effect
    x, y = pygame.mouse.get_pos()  # Gets position
    pos = cords_to_pos(Pos(y, x))

    if in_bounds(pos):  # If in boarders
        if board.selected_piece_pos:  # If there are effects
            if pos in board.valid_moves or pos in board.threatening_pieces or pos == board.selected_piece_pos:  # If on effect
                load_image(POINTING_ON_EFFECT, pos)  # Load correct image
            else:
                load_image(POINTING, pos)
        else:
            load_image(POINTING, pos)

    elif pos == UNDO_BUTTON_POS or pos == REDO_BUTTON_POS:  # If on button
        load_image(POINTING, pos)  # Load image

    elif board.coronation and (pos == QUEEN_POS or pos == KNIGHT_POS or pos == ROOK_POS or pos == BISHOP_POS):  # If in coronation and on buttons
        load_image(POINTING, pos)  # Load image


def pos_to_cords(col, row):  # Helps convert cells to cords better
    x = col * CELL_SIZE_COL + HEADER_COL
    y = row * CELL_SIZE_ROW + HEADER_ROW
    return x, y


def cords_to_pos(pos):  # Helps convert cords to cells better
    col = (pos.col - HEADER_COL) // CELL_SIZE_COL
    row = (pos.row - HEADER_ROW) // CELL_SIZE_ROW
    return Pos(row, col)


def load_piece(piece, pos):  # Loads pieces on screen
    col, row = pos.col, pos.row
    image = pygame.image.load(f"Images/{piece.color.value}/{piece.color.value}_{piece.piece_type.value}.png")
    SCREEN.blit(image, pos_to_cords(col, row))


def load_image(img, pos):  # Loads images on screen
    col, row = pos.col, pos.row
    SCREEN.blit(img, pos_to_cords(col, row))


def update_screen_in_game():  # Loads everything in game
    SCREEN.blit(BOARD, (0, 0))  # Draws the background

    for move in board.valid_moves:  # For valid move
        if board.at(move):  # If square has player
            if board.at(move).color == board.turn:  # If ally
                load_image(POSSIBLE_MOVES, move)  # Load normal effect
            else:  # If enemy
                load_image(EATING_EFFECT, move)  # Load eating effect
        else:  # If empty
            load_image(POSSIBLE_MOVES, move)  # Load normal effect

    for piece in board.threatening_pieces:  # For threatening piece
        if board.at(piece):  # If square has player
            load_image(THREATENING_EFFECT, piece)  # Load eating effect

    if board.selected_piece_pos:  # If selected piece is not empty
        load_image(SELECTING_EFFECT, board.selected_piece_pos)

    show_hover()  # Load hover

    # Load last move
    if board.last_move_from and board.last_move_to:
        load_image(LAST_MOVE_EFFECT, board.last_move_to)
        load_image(LAST_MOVE_EFFECT, board.last_move_from)

    # Load Check effect
    for row in range(len(board.pieces)):  # Run on every piece
        for col in range(len(board.pieces[0])):
            pos = Pos(row, col)  # Get pos
            piece = board.at(pos)  # Get piece
            if piece:  # If not None
                if piece.piece_type == PieceType.King:  # If king
                    if piece.color == Color.White:  # If white
                        if board.is_check(Color.White):  # If in check
                            load_image(CHECK_EFFECT, pos)  # Load
                    if piece.color == Color.Black:  # If black
                        if board.is_check(Color.Black):  # If in check
                            load_image(CHECK_EFFECT, pos)  # Load

    if board.coronation:  # If in coronation
        # Load images
        piece = board.at(board.coronation_piece_pos)
        if piece:
            load_piece(Queen(piece.color), QUEEN_POS)
            load_image(CORONATION_EFFECT, QUEEN_POS)
            load_piece(Knight(piece.color), KNIGHT_POS)
            load_image(CORONATION_EFFECT, KNIGHT_POS)
            load_piece(Rook(piece.color), ROOK_POS)
            load_image(CORONATION_EFFECT, ROOK_POS)
            load_piece(Bishop(piece.color), BISHOP_POS)
            load_image(CORONATION_EFFECT, BISHOP_POS)

    load_image(UNDO, UNDO_BUTTON_POS)  # Load undo image
    load_image(REDO, REDO_BUTTON_POS)  # Load redo image
    load_image(pygame.image.load(f"Images/In_Game/{board.turn.value}_Turn.png"), TURN_POS)  # Load turn image

    for row in range(len(board.pieces)):  # Checks a Specific piece
        for col in range(len(board.pieces[0])):  # Checks a Specific piece

            piece = board.at(Pos(row, col))  # Saves piece as variable

            if piece:  # If piece is not empty
                load_piece(piece, Pos(row, col))  # Load piece

    pygame.display.update()  # Update display


def show_board():  # Loads all the static graphics for the game
    SCREEN.blit(BOARD, (0, 0))  # Draws the background
    load_image(UNDO, UNDO_BUTTON_POS)  # Load undo image
    load_image(REDO, REDO_BUTTON_POS)  # Load redo image
    load_image(pygame.image.load(f"Images/In_Game/{board.turn.value}_Turn.png"), TURN_POS)  # Load turn image

    for row in range(len(board.pieces)):  # Checks a Specific piece
        for col in range(len(board.pieces[0])):  # Checks a Specific piece

            piece = board.at(Pos(row, col))  # Saves piece as variable

            if piece:  # If piece is not empty
                load_piece(piece, Pos(row, col))  # Load piece

    # Load Check effect
    for row in range(len(board.pieces)):  # Run on every piece
        for col in range(len(board.pieces[0])):
            pos = Pos(row, col)  # Get pos
            piece = board.at(pos)  # Get piece
            if piece:  # If not None
                if piece.piece_type == PieceType.King:  # If king
                    if piece.color == Color.White:  # If white
                        if board.is_check(Color.White):  # If in check
                            load_image(CHECK_EFFECT, pos)  # Load
                    if piece.color == Color.Black:  # If black
                        if board.is_check(Color.Black):  # If in check
                            load_image(CHECK_EFFECT, pos)  # Load


def remove_effects():  # Removes effects
    board.selected_piece_pos = None
    board.valid_moves = []
    board.threatening_pieces = []
    return "None"  # Set last click to None


def set_effects(pos, click):  # Sets effects location
    if click == "left":  # If right click
        board.selected_piece_pos = pos
        board.valid_moves = board.get_moves(pos)
        board.threatening_pieces = []
        return "left"

    if click == "right":  # If right click
        board.selected_piece_pos = pos
        board.valid_moves = []
        board.threatening_pieces = board.get_threatening_pieces(pos)
        return "right"


def on_mouse_click_pvp(button):  # on click
    global select_click
    if button == 1:  # If left click
        pos = Pos(pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[0])
        square_pos = cords_to_pos(pos)  # Get square pos
        if not in_bounds(square_pos):
            if square_pos == UNDO_BUTTON_POS:  # If on undo button
                board.undo()
            elif square_pos == REDO_BUTTON_POS:  # If on redo button
                board.redo()

            if not board.coronation:  # If in coronation
                return
            elif square_pos == QUEEN_POS:  # If clicked on queen pos
                board.undo_states.append(board.deepcopy())  # Add to undo
                piece = board.at(board.coronation_piece_pos)
                board.change_piece(board.coronation_piece_pos, Queen(piece.color))  # Turn into queen
                board.coronation = False
                board.coronation_piece_pos = None

            elif square_pos == KNIGHT_POS:  # If clicked on knight pos
                board.undo_states.append(board.deepcopy())  # Add to undo
                piece = board.at(board.coronation_piece_pos)
                board.change_piece(board.coronation_piece_pos, Knight(piece.color))  # Turn into knight
                board.coronation = False
                board.coronation_piece_pos = None

            elif square_pos == ROOK_POS:  # If clicked on rook pos
                board.undo_states.append(board.deepcopy())  # Add to undo
                piece = board.at(board.coronation_piece_pos)
                board.change_piece(board.coronation_piece_pos, Rook(piece.color))  # Turn into rook
                board.coronation = False
                board.coronation_piece_pos = None

            elif square_pos == BISHOP_POS:  # If clicked on bishop pos
                board.undo_states.append(board.deepcopy())  # Add to undo
                piece = board.at(board.coronation_piece_pos)
                board.change_piece(board.coronation_piece_pos, Bishop(piece.color))  # Turn into bishop
                board.coronation = False
                board.coronation_piece_pos = None
            return

        if board.coronation:  # If in coronation don't make a move
            return

        square = board.at(square_pos)  # Get square
        if board.selected_piece_pos:
            if square_pos in board.valid_moves:  # If on valid moves
                board.move(board.selected_piece_pos, square_pos)  # Move
                if board.is_check(Color.White):
                    pass
                select_click = remove_effects()
                return

        if square:  # If clicked on a piece
            if square.color == board.turn:  # If on a piece of the current turn
                if board.selected_piece_pos:
                    if square_pos == board.selected_piece_pos:  # If clicked on the selected square
                        if select_click == "right":  # If last click was right
                            select_click = set_effects(square_pos, "left")
                            return
                        else:  # If last click is left or None
                            select_click = remove_effects()
                            return
                select_click = set_effects(square_pos, "left")
                return
            else:  # If on an enemy piece
                select_click = remove_effects()
                return
        else:  # If clicked on an empty slot
            select_click = remove_effects()
            return

    elif button == 3:  # If right click
        pos = Pos(pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[0])
        square_pos = cords_to_pos(pos)  # Get square pos
        if not in_bounds(square_pos):
            if square_pos == UNDO_BUTTON_POS:  # If on undo button
                board.undo()
            if square_pos == REDO_BUTTON_POS:  # If on redo button
                board.redo()

            if not board.coronation:  # If in coronation
                return
            elif square_pos == QUEEN_POS:  # If clicked on queen pos
                board.undo_states.append(board.deepcopy())  # Add to undo
                piece = board.at(board.coronation_piece_pos)
                board.change_piece(board.coronation_piece_pos, Queen(piece.color))  # Turn into queen
                board.coronation = False
                board.coronation_piece_pos = None

            elif square_pos == KNIGHT_POS:  # If clicked on knight pos
                board.undo_states.append(board.deepcopy())  # Add to undo
                piece = board.at(board.coronation_piece_pos)
                board.change_piece(board.coronation_piece_pos, Knight(piece.color))  # Turn into knight
                board.coronation = False
                board.coronation_piece_pos = None

            elif square_pos == ROOK_POS:  # If clicked on rook pos
                board.undo_states.append(board.deepcopy())  # Add to undo
                piece = board.at(board.coronation_piece_pos)
                board.change_piece(board.coronation_piece_pos, Rook(piece.color))  # Turn into rook
                board.coronation = False
                board.coronation_piece_pos = None

            elif square_pos == BISHOP_POS:  # If clicked on bishop pos
                board.undo_states.append(board.deepcopy())  # Add to undo
                piece = board.at(board.coronation_piece_pos)
                board.change_piece(board.coronation_piece_pos, Bishop(piece.color))  # Turn into bishop
                board.coronation = False
                board.coronation_piece_pos = None
            return

        if board.coronation:  # If in coronation don't select
            return

        if board.selected_piece_pos:  # If a piece is selected
            if board.selected_piece_pos == square_pos:  # If on selected piece
                if select_click == "left":  # If last click was left
                    select_click = set_effects(square_pos, "right")
                    return
                else:  # If last click is right or None
                    select_click = remove_effects()
                    return
            else:  # If not on selected piece
                select_click = set_effects(square_pos, "right")
        else:  # If there is no selected piece
            select_click = set_effects(square_pos, "right")
