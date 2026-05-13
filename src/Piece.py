class Piece:

    def __init__(self, color, position, icon):

        self.color = color
        self.position = position
        self.icon = icon


class Pawn(Piece):

    def __init__(self, color, position, icon):
        super().__init__(color,position,icon)



class Knight(Piece):

    def __init__(self, color, position, icon):
        super().__init__(color,position,icon)



class Bishop(Piece):

    def __init__(self, color, position, icon):
        super().__init__(color,position,icon)



class Rook(Piece):

    def __init__(self, color, position, icon, has_moved):
        super().__init__(color,position,icon)
        self.has_moved = has_moved



class Queen(Piece):

    def __init__(self, color, position, icon):
        super().__init__(color,position,icon)



class King(Piece):

    def __init__(self, color, position, icon, has_moved):
        super().__init__(color,position,icon)
        self.has_moved = has_moved