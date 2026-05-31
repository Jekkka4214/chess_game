import json
import re
from src.ChessException import ChessException
from src.Piece import Pawn, Knight, Bishop, Rook, Queen, King

class SaveManager:
    @staticmethod
    def save_game_to_json(board_obj, white_to_move, filename="savegame.json"):
        if not re.match(r"^[a-zA-Z0-9_\-]+\.json$", filename):
            raise ChessException("Invalid file name")

        pieces_data = []
        for piece, r, c in board_obj.all_pieces():
            pieces_data.append({
                "type": piece.__class__.__name__,
                "color": piece.color,
                "position": [r, c],
                "icon": piece.icon,
                "has_moved": getattr(piece, "has_moved", False)
            })

        game_state = {
            "white_to_move": white_to_move,
            "pieces": pieces_data
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(game_state, f, indent=4)

    @staticmethod
    def load_game_from_json(board_obj, filename="savegame.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                game_state = json.load(f)

            board_obj.board = [[None for _ in range(8)] for _ in range(8)]
            classes_map = {cls.__name__: cls for cls in [Pawn, Knight, Bishop, Rook, Queen, King]}

            for p_data in game_state["pieces"]:
                cls = classes_map[p_data["type"]]
                r, c = p_data["position"]
                if cls in (Rook, King):
                    board_obj.board[r][c] = cls(p_data["color"], [r, c], p_data["icon"], p_data["has_moved"])
                else:
                    board_obj.board[r][c] = cls(p_data["color"], [r, c], p_data["icon"])

            return game_state["white_to_move"]

        except FileNotFoundError:
            print(f"Warning: File {filename} not found.")
            return True
        except Exception as e:
            raise ChessException(f"Cannot load safe: {e}")