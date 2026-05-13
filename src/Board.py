from src.Piece import *

class Board:

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        for i in range (0,8):
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
                    self.board[0][i] = Queen("w", [0, i], "data/Pieces_img/w_Queen.png")
                    self.board[7][i] = Queen("b", [7, i], "data/Pieces_img/b_Queen.png")
                case 4:
                    self.board[0][i] = King("w", [0, i], "data/Pieces_img/w_King.png",False)
                    self.board[7][i] = King("b", [7, i], "data/Pieces_img/b_King.png",False)


    def get_rook_moves(self, piece, row, col):
        moves = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for dir in directions:
            for i in range(1, 8):
                nr, nc = row + dir * i, col + dir * i
                if 0 <= nr <= 7 and 0 <= nc <= 7:
                    cell_piece = self.board[nr][nc]
                    if cell_piece is None:
                        moves.append([nr, nc])
                    elif cell_piece.color != piece.color:
                        moves.append([nr, col])
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
                if 0 <= nr < 8 and 0 <= nc < 8:
                    cell_piece = self.board[nr][nc]
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

        for c,r in offsets:
            if 0 <= row + c <= 7 and 0 <= col + r <= 7:
                cell_piece = self.board[row + c][col + r]

                if cell_piece is None or cell_piece.color != piece.color:
                   moves.append(list((c,r)))

        return moves


    def get_w_pawn_moves(self, piece, row, col):
        moves = []
        if self.board[row + 1][col] is None:
            if row != 1:
                moves.append([row + 1, col])
            else:
                moves.append([row + 1, col])
                if self.board[row + 2][col] is None:  # w_Pawn moves
                    moves.append([3, col])

        if col is not 7:
            target_right = self.board[row + 1][col + 1]
            if target_right is not None and target_right.color != piece.color:
                moves.append([row + 1, col + 1])

        if col is not 0:
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
                if self.board[row - 2][col] is None:  # b_Pawn moves
                    moves.append([5, col])

        if col is not 7:
            target_right = self.board[row - 1][col + 1]
            if target_right is not None and target_right.color != piece.color:
                moves.append([row - 1, col + 1])

        if col is not 0:
            target_left = self.board[row - 1][col - 1]
            if target_left is not None and target_left.color != piece.color:
                moves.append([row - 1, col - 1])
        return moves


    def get_king_moves(self,piece, row, col):
        moves = []
        offsets = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        for c, r in offsets:
            nr,nc = col + c, row + r
            if 0 <= nr <= 7 and 0 <= nc <= 7:







    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        moves = []

        match piece:
             case piece if isinstance(piece, Pawn) and piece.color == "w":
                 moves = self.get_w_pawn_moves(piece,row,col)

             case piece if isinstance(piece, Pawn) and piece.color == "b":
                 moves = self.get_b_pawn_moves(piece, row, col)

             case piece if isinstance(piece, Knight):
                 moves = self.get_knight_moves(piece, row, col)

             case piece if isinstance(piece, Bishop):
                 moves = self.get_bishop_moves(piece,row,col)

             case piece if isinstance(piece, Rook):
                 moves = self.get_rook_moves(piece,row,col)

             case piece if isinstance(piece, Queen):
                moves = self.get_bishop_moves(piece,row,col) + self.get_rook_moves(piece,row,col)

















