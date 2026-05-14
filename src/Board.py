from src.Piece import *

class Board:

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
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
                if self.board[row + 2][col] is None:                     # White Pawn moves
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
                if self.board[row - 2][col] is None:                  # Black Pawn moves
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



    def is_king_not_checked(self,piece, row, col):

        enemy_color = "b" if piece.color == "w" else "w"
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for move in self.get_knight_moves(Knight(piece.color,[row,col],""), row, col):
            possible_target = self.board[move[0]][move[1]]
            if isinstance(possible_target, Knight) and possible_target.color == enemy_color:
                return False

        for move in self.get_bishop_moves(Bishop(piece.color,[row,col],""), row, col):          #Checking is King checked
            possible_target = self.board[move[0]][move[1]]
            if isinstance(possible_target, Bishop) and possible_target.color == enemy_color:
                return False

        for move in self.get_rook_moves(Rook(piece.color,[row,col],"",""), row, col):
            possible_target = self.board[move[0]][move[1]]
            if isinstance(possible_target, Rook) and possible_target.color == enemy_color:
                return False

        for move in self.get_queen_moves(Queen(piece.color,[row,col],""), row, col):
            possible_target = self.board[move[0]][move[1]]
            if isinstance(possible_target, Queen) and possible_target.color == enemy_color:
                return False


        for c, r in offsets:
            nr, nc = row + r, col + c
            if 0 <= nr <= 7 and 0 <= nc <= 7:
                possible_target = self.board[nr][nc]
                if isinstance(possible_target, King) and possible_target.color == enemy_color:
                    return False

        pawn_dir = 1 if piece.color == "w" else -1
        for dc in [-1, 1]:
            nr, nc = row + pawn_dir, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board[nr][nc]
                if isinstance(target, Pawn) and target.color == enemy_color:
                    return False

        return True


    def get_king_moves(self,piece, row, col):
        moves = []
        offsets = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]                               #King moves
        for r, c in offsets:
            nr,nc = row + r, col + c
            if 0 <= nr <= 7 and 0 <= nc <= 7:
                cell_piece = self.board[nr][nc]
                #checking if King won't be checked on that cell
                if (cell_piece is None or cell_piece.color != piece.color) and self.is_king_not_checked(piece, nr, nc):
                    moves.append([nr,nc])

        return moves



    def get_queen_moves(self, piece, row, col):
        return self.get_bishop_moves(piece,row,col) + self.get_rook_moves(piece,row,col)              #Queen moves consists of moves of Bishop and Rook



    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        moves = []

        match piece:
             case piece if isinstance(piece, Pawn) and piece.color == "w":
                 moves = self.get_w_pawn_moves(piece, row, col)

             case piece if isinstance(piece, Pawn) and piece.color == "b":
                 moves = self.get_b_pawn_moves(piece, row, col)

             case piece if isinstance(piece, Knight):
                 moves = self.get_knight_moves(piece, row, col)                     #Method that is called from main for getting valid moves

             case piece if isinstance(piece, Bishop):
                 moves = self.get_bishop_moves(piece, row, col)

             case piece if isinstance(piece, Rook):
                 moves = self.get_rook_moves(piece, row, col)

             case piece if isinstance(piece, Queen):
                moves = self.get_queen_moves(piece, row, col)

             case piece if isinstance(piece, King):
                 moves = self.get_king_moves(piece, row, col)

        return moves


    def move_piece(self, start_sq, end_sq):
        self.board[end_sq[0]][end_sq[1]] = self.board[start_sq[0]][start_sq[1]]
        self.board[start_sq[0]][start_sq[1]] = None



















