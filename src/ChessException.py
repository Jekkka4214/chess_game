class ChessException(Exception):

    def __init__(self, message):
        super().__init__(f"Chess Game Error: {message}")
