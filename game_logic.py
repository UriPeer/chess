from enum import Enum
from collections import deque
import math
from pprint import pprint


class Pos:  # Makes it easier to access pos
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __repr__(self):
        return f"{self.row} {self.col}"


class PieceType(Enum):  # Helps avoid typos
    Pawn = "Pawn"
    Rook = "Rook"
    Knight = "Knight"
    Bishop = "Bishop"
    Queen = "Queen"
    King = "King"


class Color(Enum):  # Helps orginize
    White = "White"
    Black = "Black"


class Direction(Enum):
    Right = "Right"
    Left = "Left"


class Piece:  # Makes a general piece class

    def __init__(self, piece_type, color):  # Gets type and color of piece and sets first move to True
        self.piece_type = piece_type
        self.color = color
        self.is_first_move = True

    def __repr__(self):
        piece_type = None
        color = None
        if self.color == Color.White:
            color = "W"
        elif self.color == Color.Black:
            color = "B"
        if self.piece_type == PieceType.King:
            piece_type = "K"
        elif self.piece_type == PieceType.Queen:
            piece_type = "Q"
        elif self.piece_type == PieceType.Rook:
            piece_type = "R"
        elif self.piece_type == PieceType.Bishop:
            piece_type = "B"
        elif self.piece_type == PieceType.Knight:
            piece_type = "N"
        elif self.piece_type == PieceType.Pawn:
            piece_type = "P"
        return f"{color} {piece_type}"

    def copy(self):
        pass

    def add_steps(self, col_direction, row_direction, board, piece_pos, do_once=False):  # Add steps to the moves list
        moves = []

        row = piece_pos.row
        col = piece_pos.col

        while True:  # Loop that adds the valid moves
            col += col_direction  # Changes the position of the next check based on the direction
            row += row_direction

            if not (0 <= col <= 7 and 0 <= row <= 7):  # Checks that we're inside the board
                break  # If not stop the process

            pos = Pos(row, col)
            if not board.at(pos):  # If the location is none
                moves.append(pos)  # Add move to list
            else:
                if self.color != board.at(pos).color:  # If the location has an enemy piece
                    moves.append(pos)  # Add Move to list
                break  # And stop the process

            if do_once:  # If the piece can move only 1 step at a time
                break  # Stop the process

        return moves  # Returns the moves

    def check_after_move(self, moves, board, pos):  # Returns the valid moves that don't cause a check
        # Copy the current state
        tmp_board = board.deepcopy()
        moves_to_remove = []
        for move in moves:  # For move
            tmp_board.move(pos, move)  # Move on temp board
            if tmp_board.is_check(self.color):  # If after move king in check
                moves_to_remove.append(move)  # Add unnecessary move to list
            tmp_board.undo()  # Undo move on temp board

        for move in moves_to_remove:  # Go over unnecessary moves
            moves.remove(move)  # Remove them

        return moves

    def valid_moves(self, pos, board):
        raise NotImplementedError()

    def possible_eating_moves(self, pos, board):  # Returns possible eating moves
        return self.valid_moves(pos, board)

    def eating_moves(self, pos, board):  # Returns all moves that can eat
        eating_moves = self.valid_moves(pos, board)  # Get valid moves
        removes = []
        for square in eating_moves:  # For move
            if not board.at(square):  # If empty
                removes.append(square)  # Add to removes
        for remove in removes:  # For move to remove
            eating_moves.remove(remove)  # Remove
        return eating_moves  # Return


class King(Piece):  # King piece class
    def __init__(self, color):  # Set up type and color
        super().__init__(PieceType.King, color)

    def copy(self):
        new_piece = King(self.color)
        new_piece.is_first_move = self.is_first_move
        return new_piece

    def can_castle(self, board, pos, direction):
        if not self.is_first_move:  # Check if kings first move
            return False

        # Handle rook
        rook_pos = Pos(pos.row, pos.col + 3) if direction == Direction.Right else Pos(pos.row, pos.col - 4)  # Get rook pos
        if not in_bounds(rook_pos):  # Check if in bounds
            return False
        rook = board.at(rook_pos)  # Get rook
        if not rook or not rook.is_first_move or rook.piece_type != PieceType.Rook:  # Check if rook is eligible to castle
            return False

        # checks if there is nothing between rook and king
        in_between = [5, 6] if direction == Direction.Right else [3, 2, 1]
        for col in in_between:
            piece = board.at(Pos(pos.row, col))
            if piece:
                return False

        # checks if the king and kings path are under threat
        cols = [4, 5, 6] if direction == Direction.Right else [4, 3, 2]
        for col in cols:
            if board.under_threat(Pos(pos.row, col), self.color):
                return False

        return True

    def valid_moves(self, pos, board, check_check=True):  # Returns valid moves
        moves = []  # List of all valid moves

        # Directions
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                moves += self.add_steps(i, j, board, pos, do_once=True)  # Add valid moves based on direction

        if self.can_castle(board, pos, Direction.Right):  # If king can castle to the right
            moves.append(Pos(pos.row, pos.col + 2))
        if self.can_castle(board, pos, Direction.Left):  # If king can castle to the left
            moves.append(Pos(pos.row, pos.col - 2))

        if check_check:
            moves = self.check_after_move(moves, board, pos)

        return moves


class Knight(Piece):
    def __init__(self, color):  # Set up type and color
        super().__init__(PieceType.Knight, color)

    def copy(self):
        new_piece = Knight(self.color)
        new_piece.is_first_move = self.is_first_move
        return new_piece

    def valid_moves(self, pos, board, check_check=True):  # Returns valid moves
        moves = []  # List of all valid moves

        # Way of moving
        for i in [2, -2]:
            for j in [-1, 1]:
                vertical_pos = Pos(pos.row + i, pos.col + j)  # Vertical way of moving
                horizontal_pos = Pos(pos.row + j, pos.col + i)  # Horizontal way of moving

                for possible_pos in [vertical_pos, horizontal_pos]:  # For every possible move
                    if in_bounds(possible_pos):  # If in board
                        if not board.at(possible_pos):  # If empty
                            moves.append(possible_pos)  # Add move to list
                        else:
                            if self.color != board.at(possible_pos).color:  # If the location has an enemy piece
                                moves.append(possible_pos)  # Add Move to list

        if check_check:
            moves = self.check_after_move(moves, board, pos)

        return moves


class Bishop(Piece):
    def __init__(self, color):  # Set up type and color
        super().__init__(PieceType.Bishop, color)

    def copy(self):
        new_piece = Bishop(self.color)
        new_piece.is_first_move = self.is_first_move
        return new_piece

    def valid_moves(self, pos, board, check_check=True):  # Returns valid moves
        moves = []  # List of all valid moves

        # Directions
        for i in [-1, 1]:
            for j in [-1, 1]:
                moves += self.add_steps(i, j, board, pos)  # Add valid moves based on direction

        if check_check:
            moves = self.check_after_move(moves, board, pos)

        return moves


class Rook(Piece):
    def __init__(self, color):  # Set up type and color
        super().__init__(PieceType.Rook, color)

    def copy(self):
        new_piece = Rook(self.color)
        new_piece.is_first_move = self.is_first_move
        return new_piece

    def valid_moves(self, pos, board, check_check=True):  # Returns valid moves
        moves = []  # List of all valid moves

        # Directions
        for i in [-1, 1]:
            moves += self.add_steps(0, i, board, pos)  # Add valid moves based on direction
            moves += self.add_steps(i, 0, board, pos)

        if check_check:
            moves = self.check_after_move(moves, board, pos)

        return moves


class Queen(Piece):
    def __init__(self, color):  # Set up type and color
        super().__init__(PieceType.Queen, color)

    def copy(self):
        new_piece = Queen(self.color)
        new_piece.is_first_move = self.is_first_move
        return new_piece

    def valid_moves(self, pos, board, check_check=True):  # Returns valid moves
        moves = []  # List of all valid moves

        # Directions
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                moves = moves + self.add_steps(i, j, board, pos)  # Add valid moves based on direction

        if check_check:
            moves = self.check_after_move(moves, board, pos)

        return moves


class Pawn(Piece):
    def __init__(self, color):  # Set up type and color
        super().__init__(PieceType.Pawn, color)
        self.last_move_2 = False

    def copy(self):
        new_piece = Pawn(self.color)
        new_piece.is_first_move = self.is_first_move
        new_piece.last_move_2 = self.last_move_2
        return new_piece

    def valid_moves(self, pos, board, check_check=True):  # Returns valid moves
        moves = []  # List of all valid moves

        row_offset = -1 if self.color == Color.White else 1

        # Basic movement
        forward_1 = Pos(pos.row + row_offset, pos.col)
        forward_2 = Pos(pos.row + row_offset * 2, pos.col)

        if in_bounds(forward_1):
            if not board.at(forward_1):  # If forward is empty
                moves.append(forward_1)  # Add move to list

            if in_bounds(forward_2):
                if self.is_first_move and not board.at(forward_2) and not board.at(forward_1):  # If its the first move and 2 forward is empty
                    moves.append(forward_2)  # Add move to list

        for i in [-1, 1]:  # Eating directions
            diagonal = Pos(forward_1.row, forward_1.col + i)  # Basic eating pos
            if in_bounds(diagonal):
                if board.at(diagonal) and self.color != board.at(diagonal).color:  # If the diagonal cell has an enemy
                    moves.append(diagonal)  # Add move to list

        # in passing
        for col_offset in [1, -1]:  # check right and left pieces
            piece_pos = Pos(pos.row, pos.col + col_offset)

            if not in_bounds(piece_pos):  # if not out of board
                continue

            piece = board.at(piece_pos)

            if not piece:  # If there is a piece
                continue

            if piece.piece_type != PieceType.Pawn:  # if piece is pawn
                continue

            if piece.color == Color:  # if piece is other color
                continue

            if not piece.last_move_2:  # if pawn only moved 2 squares
                continue

            moves.append(Pos(pos.row + row_offset, pos.col + col_offset))

        if check_check:
            moves = self.check_after_move(moves, board, pos)

        return moves

    def possible_eating_moves(self, pos, board):  # Returns possible eating moves
        eating_moves = []
        direction = -1 if self.color == Color.White else 1
        if in_bounds(Pos(pos.row + 1 * direction, pos.col + 1)):
            eating_moves.append(Pos(pos.row + 1 * direction, pos.col + 1))
        if in_bounds(Pos(pos.row + 1 * direction, pos.col - 1)):
            eating_moves.append(Pos(pos.row + 1 * direction, pos.col - 1))
        return eating_moves


def in_bounds(pos):
    return 0 <= pos.row <= 7 and 0 <= pos.col <= 7  # checks if within bounds


def other_color(color):
    if color == Color.Black:
        return Color.White
    if color == Color.White:
        return Color.Black


def minimax(board, depth, starting_color, maximizing_player, alpha=-math.inf, beta=math.inf):
    if depth == 0 or board.is_checkmate(Color.White) or board.is_checkmate(Color.Black):
        return board.get_score(starting_color), board

    best_move = None
    value_op = -1 if maximizing_player else 1
    value = math.inf*value_op

    for move in board.get_possible_moves():
        board.move(move[0], move[1])
        ev = minimax(board, depth-1, starting_color, not maximizing_player, alpha, beta)[0]
        if (ev > value and maximizing_player) or (ev < value and not maximizing_player):
            value = ev
            best_move = move
        if (value >= beta and maximizing_player) or (value <= alpha and not maximizing_player):
            board.undo()
            break
        if maximizing_player:
            alpha = max(alpha, value)
        else:
            beta = min(beta, value)

        board.undo()
    return value, best_move


class Board:
    def __init__(self):  # Sets board representation
        self.pieces = [[Rook(Color.Black), Knight(Color.Black), Bishop(Color.Black), Queen(Color.Black), King(Color.Black), Bishop(Color.Black), Knight(Color.Black), Rook(Color.Black)],
                       [Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black)],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White)],
                       [Rook(Color.White), Knight(Color.White), Bishop(Color.White), Queen(Color.White), King(Color.White), Bishop(Color.White), Knight(Color.White), Rook(Color.White)]
                       ]
        self.undo_states = deque()  # Sets the board state list for undo command
        self.redo_states = deque()  # Sets the board state list for redo command
        self.turn = Color.White  # Turn
        self.valid_moves = []  # All the valid moves that are visible on screen
        self.selected_piece_pos = None
        self.threatening_pieces = []
        self.last_move_from = None
        self.last_move_to = None
        self.coronation = False
        self.coronation_piece_pos = None

    def __repr__(self):
        return f"{self.pieces}"

    def at(self, pos):  # Returns piece
        return self.pieces[pos.row][pos.col]

    def get_moves(self, pos, check_check=True):  # Returns all valid moves for piece in the board
        return self.at(pos).valid_moves(pos, self, check_check)

    def change_turn(self):  # Changes the turn
        if self.turn == Color.White:
            self.turn = Color.Black

        elif self.turn == Color.Black:
            self.turn = Color.White

    def move(self, from_pos, to_pos):  # Moves a piece from one cell to another
        piece = self.at(from_pos)  # Get piece

        # Add board state to undo list
        self.undo_states.append(self.deepcopy())

        #  if in passing is happening
        if piece.piece_type == PieceType.Pawn:  # if piece moved is pawn
            row_offset = 1 if piece.color == Color.White else -1
            if from_pos.col != to_pos.col:  # if pawn moves diagonally
                eat_piece_pos = Pos(to_pos.row + row_offset, to_pos.col)
                eat_piece = self.at(eat_piece_pos)  # Get piece to eat
                if eat_piece:  # If not None
                    if eat_piece.piece_type == PieceType.Pawn:  # If pawn
                        if eat_piece.last_move_2:  # If last move moves 2
                            self.pieces[eat_piece_pos.row][eat_piece_pos.col] = None  # Eat

        # If castling
        if piece.piece_type == PieceType.King:  # If piece is king
            if piece.is_first_move:  # If piece is first move
                if to_pos.col == from_pos.col + 2:  # If right castling

                    # Get rook
                    rook_pos = Pos(from_pos.row, from_pos.col + 3)
                    rook = self.at(rook_pos)

                    # Move rook
                    self.pieces[rook_pos.row][rook_pos.col] = None
                    self.pieces[rook_pos.row][rook_pos.col - 2] = rook
                    rook.is_first_move = False

                if to_pos.col == from_pos.col - 2:  # If left castling

                    # Get rook
                    rook_pos = Pos(from_pos.row, from_pos.col - 4)
                    rook = self.at(rook_pos)

                    # Move rook
                    self.pieces[rook_pos.row][rook_pos.col] = None
                    self.pieces[rook_pos.row][rook_pos.col + 3] = rook
                    rook.is_first_move = False

        # Move Piece
        self.pieces[from_pos.row][from_pos.col] = None
        self.pieces[to_pos.row][to_pos.col] = piece

        # Set last move 2 to false on all pieces
        for row in range(len(self.pieces)):
            for col in range(len(self.pieces[0])):
                on_piece = self.at(Pos(row, col))
                if on_piece:
                    if on_piece.piece_type == PieceType.Pawn:
                        on_piece.last_move_2 = False

        # if the pawn moved two squares
        if piece.piece_type == PieceType.Pawn:
            for diff in [2, -2]:
                if from_pos.row + diff == to_pos.row:
                    piece.last_move_2 = True

        piece.is_first_move = False

        self.last_move_from = from_pos
        self.last_move_to = to_pos
        self.change_turn()  # Change turn
        self.redo_states = deque()

    def under_threat(self, pos, color):  # check if position given is under threat

        for row in range(len(self.pieces)):  # Run on every square
            for col in range(len(self.pieces[0])):
                threat_pos = Pos(row, col)
                threat_piece = self.at(threat_pos)
                if not threat_piece:  # If square is None
                    continue

                if threat_piece.piece_type == PieceType.King and threat_piece.is_first_move:  # If king and is kings first move
                    continue

                if color == threat_piece.color:
                    continue

                moves = self.get_moves(threat_pos, False)  # Get piece moves
                if pos in moves:  # If threatened
                    return True

        return False  # If not threatened false

    def get_threatening_pieces(self, pos):  # Returns all pieces threatening a square
        threatening_pieces_pos = []
        for row in range(len(self.pieces)):  # Run on every piece
            for col in range(len(self.pieces[0])):
                piece_pos = Pos(row, col)  # Get pos
                piece = self.at(piece_pos)  # Get piece

                if piece:  # If not None
                    eating_moves = piece.possible_eating_moves(piece_pos, self)
                    if pos in eating_moves:  # If threatening
                        threatening_pieces_pos.append(piece_pos)  # Add piece
        return threatening_pieces_pos

    def is_check(self, color):
        for row in range(len(self.pieces)):  # Run on every square
            for col in range(len(self.pieces[0])):
                pos = Pos(row, col)
                piece = self.at(pos)
                if not piece:  # If square is None
                    continue

                if piece.color != color:  # If not the right color
                    continue

                if piece.piece_type != PieceType.King:  # if piece is not king
                    continue

                if self.under_threat(pos, piece.color):  # if the king is threatened
                    return True

        return False

    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
        for row in range(len(self.pieces)):  # Run on every square
            for col in range(len(self.pieces[0])):
                # Get piece
                pos = Pos(row, col)
                piece = self.at(pos)

                if not piece:  # If piece is None
                    continue

                if piece.color != color:  # If piece is the right color
                    continue

                if self.get_moves(pos):  # If has valid moves
                    return False

        return True

    def can_coronate(self, pos):  # Returns true if a pawn is at the right pos to coronate
        piece = self.at(pos)  # Get piece
        if piece:  # If piece is tool
            if piece.piece_type == PieceType.Pawn:  # If pawn
                correct_row = 7 if piece.color == Color.Black else 0  # Get correct pos
                if pos.row == correct_row:  # If in correct pos
                    return True
        return False

    def set_coronation(self):
        for row in range(len(self.pieces)):  # Go on every piece
            for col in range(len(self.pieces[0])):
                pos = Pos(row, col)  # Get pos
                if self.can_coronate(pos):  # If can coronate
                    self.coronation = True
                    self.coronation_piece_pos = pos

    def get_possible_moves(self):  # Get all child boards for the board
        moves = []  # Set list

        for row in range(len(self.pieces)):  # Run on every square
            for col in range(len(self.pieces[0])):
                # Get piece
                pos = Pos(row, col)
                piece = self.at(pos)

                if not piece:  # If piece is None
                    continue

                if piece.color != self.turn:  # If piece is the right color
                    continue

                for move in piece.valid_moves(pos, self):  # Get piece moves
                    moves.append((pos, move))

        return moves

    def change_piece(self, pos, new_piece):  # Changes a piece on the board
        self.pieces[pos.row][pos.col] = new_piece

    def change_board(self, new_board):
        # Change pieces
        for row in range(len(self.pieces)):
            for col in range(len(self.pieces[0])):
                pos = Pos(row, col)
                piece = new_board.at(pos)
                self.change_piece(pos, piece)
        # Change everything else
        self.undo_states = new_board.undo_states
        self.redo_states = new_board.redo_states
        self.turn =  new_board.turn
        self.valid_moves = new_board.valid_moves
        self.selected_piece_pos = new_board.selected_piece_pos
        self.threatening_pieces = new_board.threatening_pieces
        self.last_move_from = new_board.last_move_from
        self.last_move_to = new_board.last_move_to
        self.coronation = new_board.coronation
        self.coronation_piece_pos = new_board.coronation_piece_pos

    def get_score(self, color):
        points = 0
        for row in range(len(self.pieces)):
            for piece in range(len(self.pieces[0])):
                pos = Pos(row, piece)
                piece = self.at(pos)
                if piece:
                    if piece.color == color:
                        if piece.piece_type == PieceType.Pawn:
                            points += 80
                        elif piece.piece_type == PieceType.Rook:
                            points += 500
                        elif piece.piece_type == PieceType.Knight:
                            points += 300
                        elif piece.piece_type == PieceType.Bishop:
                            points += 310
                        elif piece.piece_type == PieceType.Queen:
                            points += 900
                        points += len(piece.valid_moves(pos, self)) * 3
                        points += len(piece.eating_moves(pos, self)) * 20

                    else:
                        if piece.piece_type == PieceType.Pawn:
                            points -= 80
                        elif piece.piece_type == PieceType.Rook:
                            points -= 500
                        elif piece.piece_type == PieceType.Knight:
                            points -= 300
                        elif piece.piece_type == PieceType.Bishop:
                            points -= 310
                        elif piece.piece_type == PieceType.Queen:
                            points -= 900
                        points -= len(piece.valid_moves(pos, self)) * 3
                        points -= len(piece.eating_moves(pos, self)) * 20
        if self.is_checkmate(color):
            points = math.inf
        if self.is_checkmate(other_color(color)):
            points = -math.inf

        return points

    def deepcopy(self):  # Returns a copy of the board
        tmp_board = Board()

        for r in range(len(self.pieces)):  # Run on every square
            for c in range(len(self.pieces[0])):
                pos = Pos(r, c)  # Save pos
                piece = self.at(pos)  # Save piece
                # Copy piece
                if piece:
                    tmp_board.change_piece(pos, piece.copy())
                else:
                    tmp_board.change_piece(pos, None)

        # Save other variables
        tmp_board.last_move_from = self.last_move_from
        tmp_board.last_move_to = self.last_move_to
        tmp_board.coronation = self.coronation
        tmp_board.coronation_piece_pos = self.coronation_piece_pos
        tmp_board.turn = self.turn
        return tmp_board

    def undo(self):
        if self.undo_states:  # If you can undo
            new_board = self.undo_states.pop()  # Get new board
            self.redo_states.append(self.deepcopy())  # Add to redo
            self.pieces = new_board.pieces  # Undo

            # Reset effects
            self.selected_piece_pos = None
            self.threatening_pieces = []
            self.valid_moves = []

            # Load last move effect
            self.last_move_from = new_board.last_move_from
            self.last_move_to = new_board.last_move_to
            self.turn = new_board.turn
            self.coronation_piece_pos = new_board.coronation_piece_pos
            self.coronation = new_board.coronation

    def redo(self):
        if self.redo_states:  # If you can undo
            new_board = self.redo_states.pop()  # Get new board
            self.undo_states.append(self.deepcopy())  # Add to undo
            self.pieces = new_board.pieces  # Redo

            # Reset effects
            self.selected_piece_pos = None
            self.threatening_pieces = []
            self.valid_moves = []

            # Load effects
            self.last_move_from = new_board.last_move_from
            self.last_move_to = new_board.last_move_to
            self.turn = new_board.turn
            self.coronation_piece_pos = new_board.coronation_piece_pos
            self.coronation = new_board.coronation

    def reset(self):  # Resets board to normal
        self.pieces = [[Rook(Color.Black), Knight(Color.Black), Bishop(Color.Black), Queen(Color.Black), King(Color.Black), Bishop(Color.Black), Knight(Color.Black), Rook(Color.Black)],
                       [Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black), Pawn(Color.Black)],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White), Pawn(Color.White)],
                       [Rook(Color.White), Knight(Color.White), Bishop(Color.White), Queen(Color.White), King(Color.White), Bishop(Color.White), Knight(Color.White), Rook(Color.White)]
                       ]
        self.undo_states = deque()  # Sets the board state list for undo command
        self.redo_states = deque()  # Sets the board state list for redo command
        self.turn = Color.White  # Turn
        self.valid_moves = []  # All the valid moves that are visible on screen
        self.selected_piece_pos = None
        self.threatening_pieces = []
        self.last_move_from = None
        self.last_move_to = None
        self.coronation = False
        self.coronation_piece_pos = None
