import pygame
import sys
from functools import wraps
import os

from src import ChessException, JSON
from src.Board import Board
from src.Piece import King
from src.JSON import *

# constance for working with pixels
base_path = os.path.dirname(os.path.dirname(__file__))
WIDTH, HEIGHT = 600, 600
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
COLORS = [(240, 217, 181), (181, 136, 99)]


def log_move(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

def load_images(board_obj):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board_obj.board[r][c]
            if piece:
                full_path = os.path.join(base_path, piece.icon)
                img = pygame.image.load(full_path).convert_alpha()
                piece.image_surface = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))



def draw_game_state(screen, board_obj, valid_moves, dot_img):
        dot_size = dot_img.get_width()
        offset = (SQ_SIZE - dot_size) // 2
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                # Drawing cells
                color = COLORS[(r + c) % 2]
                rect = pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(screen, color, rect)

                # Drawing dots that shows possible moves
                if [r, c] in valid_moves:
                    screen.blit(dot_img, (c * SQ_SIZE + offset, r * SQ_SIZE + offset))

                # Drawing piece
                piece = board_obj.board[r][c]
                if piece:
                    screen.blit(piece.image_surface, rect)


def draw_winner_window(screen, text):
    window_width, window_height = 400, 150
    screen_width, screen_height = screen.get_size()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2


    overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (40, 40, 40, 230), (0, 0, window_width, window_height), border_radius=15)
    pygame.draw.rect(overlay, (212, 175, 55), (0, 0, window_width, window_height), width=3, border_radius=15)

    font = pygame.font.SysFont("Arial", 36, bold=True)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (window_width // 2, window_height // 2)

    overlay.blit(text_surface, text_rect)

    screen.blit(overlay, (x, y))

def save_move_to_log(message):
    log_path = os.path.join(base_path, "game_log.txt")
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")

    move_sound = pygame.mixer.Sound(os.path.join(base_path, "data/Sound/move.mp3"))
    capture_sound = pygame.mixer.Sound(os.path.join(base_path, "data/Sound/capture.mp3"))
    game_end_sound = pygame.mixer.Sound(os.path.join(base_path, "data/Sound/game_end.mp3"))
    castle_sound = pygame.mixer.Sound(os.path.join(base_path, "data/Sound/castle.mp3"))
    check_sound = pygame.mixer.Sound(os.path.join(base_path, "data/Sound/check.mp3"))

    move_sound.set_volume(1)
    capture_sound.set_volume(1)
    game_end_sound.set_volume(1)
    castle_sound.set_volume(1)
    check_sound.set_volume(1)

    # Creating obj Board
    board = Board()
    load_images(board)
    dot_img = pygame.image.load(os.path.join(base_path, "data/Pieces_img/dott.png")).convert_alpha()
    dot_img = pygame.transform.scale(dot_img, (SQ_SIZE * 0.35, SQ_SIZE * 0.35))

    clock = pygame.time.Clock()
    w_king_pos = [0, 3]
    b_king_pos = [7, 3]
    selected_sq = ()
    player_clicks = []
    valid_moves = []
    white_to_move = True
    game_over = False
    winner_text = ""

    if os.path.exists(os.path.join(base_path, "game_log.txt")):
        os.remove(os.path.join(base_path, "game_log.txt"))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    try:
                        SaveManager.save_game_to_json(board, white_to_move, "savegame.json")
                        save_move_to_log("--- Game was saved ---")
                    except ChessException as e:
                        print(e)

                elif event.key == pygame.K_l:
                    try:
                        white_to_move = SaveManager.load_game_from_json(board, "savegame.json")

                        load_images(board)
                        save_move_to_log("--- Game was loaded ---")

                        for piece, r, c in board.all_pieces():
                            if isinstance(piece, King):
                                if piece.color == "w":
                                    w_king_pos = [r, c]
                                else:
                                    b_king_pos = [r, c]

                        selected_sq = ()
                        player_clicks = []
                        valid_moves = []
                    except ChessException as e:
                        print(e)


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // SQ_SIZE
                    row = mouse_pos[1] // SQ_SIZE

                    if selected_sq == (row, col):
                        selected_sq = ()
                        player_clicks = []
                        valid_moves = []
                    else:
                        if len(player_clicks) == 0:
                            piece = board.board[row][col]
                            if piece is not None:
                                if (white_to_move and piece.color == "w") or (not white_to_move and piece.color == "b"):
                                    selected_sq = (row, col)
                                    player_clicks.append(selected_sq)
                        else:
                            selected_sq = (row, col)
                            player_clicks.append(selected_sq)

                    if len(player_clicks) == 2:
                        start_sq = player_clicks[0]
                        end_sq = player_clicks[1]

                        if [end_sq[0], end_sq[1]] in valid_moves:
                            moving_piece = board[start_sq[0]][start_sq[1]]
                            is_capture = board[end_sq[0]][end_sq[1]] is not None

                            log_msg = f"{moving_piece.color.upper()}: {start_sq} -> {end_sq}"
                            save_move_to_log(log_msg)

                            board.move_piece(start_sq, end_sq)
                            if is_capture:
                                capture_sound.play()
                            elif isinstance(board[end_sq[0]][end_sq[1]], King) and ((end_sq[1] - start_sq[1] == 2) or end_sq[1] - start_sq[1] == -2):
                                castle_sound.play()
                            else:
                                move_sound.play()
                            board[end_sq[0]][end_sq[1]].position = [end_sq[0], end_sq[1]]

                            for p, r, c in board.all_pieces():
                                if isinstance(p, King):
                                    if p.color == "w":
                                        w_king_pos = [r, c]
                                    else:
                                        b_king_pos = [r, c]

                            if white_to_move:
                                if board.is_checkmate(b_king_pos):
                                    game_over = True
                                    winner_text = "White Wins!"
                                    check_sound.play()
                                    game_end_sound.play()

                            else:
                                if board.is_checkmate(w_king_pos):
                                    game_over = True
                                    winner_text = "Black Wins!"
                                    check_sound.play()
                                    game_end_sound.play()

                            if white_to_move:
                                if board.is_stalemate(b_king_pos):
                                    game_over = True
                                    winner_text = "Stalemate"
                                    game_end_sound.play()
                            else:
                                if board.is_stalemate(w_king_pos):
                                    game_over = True
                                    winner_text = "Stalemate"
                                    game_end_sound.play()


                            white_to_move = not white_to_move
                            selected_sq = ()
                            player_clicks = []
                            valid_moves = []

                        else:
                            piece = board.board[row][col]
                            if piece is not None and (
                                    (white_to_move and piece.color == "w") or (
                                    not white_to_move and piece.color == "b")):
                                selected_sq = (row, col)
                                player_clicks = [selected_sq]
                            else:
                                selected_sq = ()
                                player_clicks = []
                            valid_moves = []




                    if len(player_clicks) == 1:
                         r, c = player_clicks[0]
                         if white_to_move:
                             valid_moves = board.get_valid_moves(r, c, w_king_pos)
                         else:
                             valid_moves = board.get_valid_moves(r, c, b_king_pos)

        draw_game_state(screen, board, valid_moves, dot_img)
        if game_over:
            draw_winner_window(screen, winner_text)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()