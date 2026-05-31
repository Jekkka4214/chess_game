import json
import re

from src.ChessException import ChessException
from src.Piece import *

class Board:

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.move_history = []
        for i in range (0,8):                                                                               #Creating new board with pieces
            self.board[1][i] = Pawn("w", [1,i], "data/Pieces_img/w_Pawn.png")
            self.board[6][i] = Pawn("b", [6, i], "data/Pieces_img/b_Pawn.png")
            match i:
                case 0 | 7:
                    self.board[0][i] = Rook("w",[0,i],"data/Pieces_img/w_Rook.png", False)
                    self.board[7][i] = Rook("b",[7,i],"data/Pieces_img/b_Rook.png",False)

                case 1 | 6:
                    self.board[0][i] = Knight("w",[0,i],"data/Pieces_img/w_Knight.png")
                    self.board[7][i] = Knight("b", [7, i], "data/Pieces_img/b_Knight.png")

                case 2 | 5:
                    self.board[0][i] = Bishop("w", [0, i], "data/Pieces_img/w_Bishop.png")
                    self.board[7][i] = Bishop("b", [7, i], "data/Pieces_img/b_Bishop.png")

                case 3:
                    self.board[0][i] = King("w", [0, i], "data/Pieces_img/w_King.png",False)
                    self.board[7][i] = King("b", [7, i], "data/Pieces_img/b_King.png",False)
                case 4:
                    self.board[0][i] = Queen("w", [0, i], "data/Pieces_img/w_Queen.png")
                    self.board[7][i] = Queen("b", [7, i], "data/Pieces_img/b_Queen.png")


    def __getitem__(self, item):
        return self.board[item]

    def all_pieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece is not None:
                    yield piece, r, c

    def get_squares_of_color(self, color):
        check_color = lambda p: p.color == color

        return {(r, c) for p, r, c in self.all_pieces() if check_color(p)}

    def get_rook_moves(self, piece, row, col):
        moves = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for dr,dc in directions:
            for i in range(1, 8):
                nr, nc = row + dr * i, col + dc * i
                if 0 <= nr <= 7 and 0 <= nc <= 7:
                    cell_piece = self.board[nr][nc]                             #Rook moves
                    if cell_piece is None:
                        moves.append([nr, nc])
                    elif cell_piece.color != piece.color:
                        moves.append([nr, nc])
                        break
                    else:
                        break
                else:
                    break

        return moves




    def get_bishop_moves(self, piece, row, col):
        moves = []
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = row + dr * i, col + dc * i
                if 0 <= nr <= 7 and 0 <= nc <= 7:
                    cell_piece = self.board[nr][nc]                          #Bishop moves
                    if cell_piece is None:
                        moves.append([nr, nc])
                    elif cell_piece.color != piece.color:
                        moves.append([nr, nc])
                        break
                    else:
                        break
                else:
                    break
        return moves





    def get_knight_moves(self, piece, row, col):
        moves = []
        offsets = [(2, 1), (1, 2), (1, -2),
                   (-2, 1), (-1, 2), (2, -1),
                   (-1, -2), (-2, -1)]

        for r,c in offsets:
            nr,nc = row + r, col + c                                                                            #Knight moves
            if 0 <= nr <= 7 and 0 <= nc <= 7:
                cell_piece = self.board[nr][nc]

                if cell_piece is None or cell_piece.color != piece.color:
                   moves.append([nr,nc])

        return moves


    def get_w_pawn_moves(self, piece, row, col):
        moves = []
        if self.board[row + 1][col] is None:
            if row != 1:
                moves.append([row + 1, col])
            else:
                moves.append([row + 1, col])
                if self.board[row + 2][col] is None:                                                            # White Pawn moves
                    moves.append([3, col])
        return moves + self.get_w_pawn_take_moves(piece, row, col)

    def get_w_pawn_take_moves(self, piece, row, col):
        moves = []
        if col != 7:
            target_right = self.board[row + 1][col + 1]
            if target_right is not None and target_right.color != piece.color:
                moves.append([row + 1, col + 1])

        if col != 0:
            target_left = self.board[row + 1][col - 1]
            if target_left is not None and target_left.color != piece.color:
                moves.append([row + 1, col - 1])
        return moves


    def get_b_pawn_moves(self,piece, row, col):
        moves = []
        if self.board[row - 1][col] is None:
            if row != 6:
                moves.append([row - 1, col])
            else:
                moves.append([row - 1, col])
                if self.board[row - 2][col] is None:                                                               # Black Pawn moves
                    moves.append([4, col])
        return moves + self.get_b_pawn_take_moves(piece, row, col)


    def get_b_pawn_take_moves(self,piece, row, col):
        moves = []
        if col != 7:
            target_right = self.board[row - 1][col + 1]
            if target_right is not None and target_right.color != piece.color:
                moves.append([row - 1, col + 1])

        if col != 0:
            target_left = self.board[row - 1][col - 1]
            if target_left is not None and target_left.color != piece.color:
                moves.append([row - 1, col - 1])
        return moves



    def is_king_not_checked(self, piece, row, col):
        enemy_color = "b" if piece.color == "w" else "w"

        cardinal_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in cardinal_directions:
            for i in range(1, 8):
                nr, nc = row + dr * i, col + dc * i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    target = self.board[nr][nc]
                    if target is not None:
                        if target.color == enemy_color and isinstance(target, (Rook, Queen)):
                            return False
                        break
                else:
                    break

        diagonal_directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in diagonal_directions:
            for i in range(1, 8):
                nr, nc = row + dr * i, col + dc * i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    target = self.board[nr][nc]
                    if target is not None:
                        if target.color == enemy_color and isinstance(target, (Bishop, Queen)):
                            return False
                        break
                else:
                    break

        knight_offsets = [(2, 1), (1, 2), (1, -2), (-2, 1), (-1, 2), (2, -1), (-1, -2), (-2, -1)]
        for dr, dc in knight_offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board[nr][nc]
                if target is not None and target.color == enemy_color and isinstance(target, Knight):
                    return False


        pawn_dir = 1 if piece.color == "w" else -1
        for dc in [-1, 1]:
            nr, nc = row + pawn_dir, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board[nr][nc]
                if target is not None and target.color == enemy_color and isinstance(target, Pawn):
                    return False

        king_offsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in king_offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board[nr][nc]
                if target is not None and target.color == enemy_color and isinstance(target, King):
                    return False

        return True


    def get_king_moves(self,piece, row, col):
        moves = []

        if not piece.has_moved and self.is_king_not_checked(piece, row, col):

            right_rook = self.board[row][7]
            if isinstance(right_rook, Rook) and not right_rook.has_moved:
                can_castle_long = True
                for i in range(4, 7):
                    if self.board[row][i] is not None:
                        can_castle_long = False
                        break
                    if not self.is_king_not_checked(piece, row, i):
                        can_castle_long = False
                        break
                if can_castle_long:
                    moves.append([row, col + 2])

            left_rook = self.board[row][0]
            if isinstance(left_rook, Rook) and not left_rook.has_moved:
                can_castle_short = True
                for i in range(1, 3):
                    if self.board[row][i] is not None or not self.is_king_not_checked(piece, row, i):
                        can_castle_short = False
                        break
                    if not self.is_king_not_checked(piece, row, i):
                        can_castle_short = False
                        break
                if can_castle_short:
                    moves.append([row, col - 2])


        offsets = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]                                        #King moves
        for r, c in offsets:
            nr,nc = row + r, col + c
            if 0 <= nr <= 7 and 0 <= nc <= 7:
                cell_piece = self.board[nr][nc]
                #checking if King won't be checked on that cell
                if (cell_piece is None or cell_piece.color != piece.color) and self.is_king_not_checked(piece, nr, nc):
                    moves.append([nr,nc])

        return moves



    def get_queen_moves(self, piece, row, col):
        return self.get_bishop_moves(piece,row,col) + self.get_rook_moves(piece,row,col)                        #Queen moves consists of moves of Bishop and Rook

    def get_valid_moves(self, row, col, king_pos):
        piece = self.board[row][col]
        if piece is None:
            return []

        if isinstance(piece, Pawn):
            moves = self.get_w_pawn_moves(piece, row, col) if piece.color == "w" else self.get_b_pawn_moves(piece, row,
                                                                                                            col)
        elif isinstance(piece, Knight):
            moves = self.get_knight_moves(piece, row, col)
        elif isinstance(piece, Bishop):
            moves = self.get_bishop_moves(piece, row, col)
        elif isinstance(piece, Rook):
            moves = self.get_rook_moves(piece, row, col)
        elif isinstance(piece, Queen):
            moves = self.get_queen_moves(piece, row, col)
        elif isinstance(piece, King):
            moves = self.get_king_moves(piece, row, col)
        else:
            return []

        valid_moves = []

        for move in moves:
            target_row, target_col = move[0], move[1]

            saved_target_piece = self.board[target_row][target_col]

            self.board[target_row][target_col] = piece
            self.board[row][col] = None

            current_king_pos = [target_row, target_col] if isinstance(piece, King) else king_pos

            king_piece = self.board[current_king_pos[0]][current_king_pos[1]]

            if king_piece and self.is_king_not_checked(king_piece, current_king_pos[0], current_king_pos[1]):
                valid_moves.append(move)

            self.board[row][col] = piece
            self.board[target_row][target_col] = saved_target_piece

        return valid_moves

    def is_checkmate(self, king_pos):
        king_piece = self.board[king_pos[0]][king_pos[1]]
        if king_piece is None:
            return False

        if not self.is_king_not_checked(king_piece, king_pos[0], king_pos[1]):
            if len(self.get_valid_moves(king_pos[0], king_pos[1], king_pos)) == 0:

                for r in range(8):
                    for c in range(8):
                        piece = self.board[r][c]
                        if piece is not None and piece.color == king_piece.color:
                            possible_moves = self.get_valid_moves(r, c, king_pos)
                            if len(possible_moves) > 0:
                                return False

                return True

        return False

    def is_stalemate(self, king_pos):
        king_piece = self.board[king_pos[0]][king_pos[1]]
        if king_piece is None:
            return False
        if self.is_king_not_checked(king_piece, king_pos[0], king_pos[1]):
            if len(self.get_valid_moves(king_pos[0], king_pos[1], king_pos)) == 0:

                for r in range(8):
                    for c in range(8):
                        piece = self.board[r][c]
                        if piece is not None and piece.color == king_piece.color:
                            possible_moves = self.get_valid_moves(r, c, king_pos)
                            if len(possible_moves) > 0:
                                return False

                return True

        return False




    def move_piece(self, start_sq, end_sq):
        piece = self.board[start_sq[0]][start_sq[1]]

        if isinstance(piece, (Rook, King)):
            piece.has_moved = True

        if isinstance(piece, King):
            if end_sq[1] - start_sq[1] == 2 and self.is_king_not_checked(piece, start_sq[0], start_sq[1]):
                self.board[end_sq[0]][4] = self.board[end_sq[0]][7]
                self.board[end_sq[0]][7] = None

            elif start_sq[1] - end_sq[1] == 2 and self.is_king_not_checked(piece, start_sq[0], start_sq[1]):
                self.board[end_sq[0]][2] = self.board[end_sq[0]][0]
                self.board[end_sq[0]][0] = None

        self.board[end_sq[0]][end_sq[1]] = piece                                        #Moves
        self.board[start_sq[0]][start_sq[1]] = None
        piece.position = [end_sq[0], end_sq[1]]



















