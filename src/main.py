import pygame
import sys
from src.Board import Board
import os



# constance for working with pixels
base_path = os.path.dirname(os.path.dirname(__file__))
WIDTH, HEIGHT = 600, 600
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
COLORS = [(240, 217, 181), (181, 136, 99)]


def load_images(board_obj):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board_obj.board[r][c]
            if piece:
                # Склеиваем путь правильно
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

                # Drawing dotts that shows possible moves
                if [r, c] in valid_moves:
                    screen.blit(dot_img, (c * SQ_SIZE + offset, r * SQ_SIZE + offset))

                # Drawing piece
                piece = board_obj.board[r][c]
                if piece:
                    screen.blit(piece.image_surface, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")

    # Creating obj Board
    board = Board()
    load_images(board)
    dot_img = pygame.image.load(os.path.join(base_path, "data/Pieces_img/dott.png")).convert_alpha()
    dot_img = pygame.transform.scale(dot_img, (SQ_SIZE * 0.35, SQ_SIZE * 0.35))

    clock = pygame.time.Clock()
    selected_sq = ()
    player_clicks = []
    valid_moves = []
    white_to_move = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                        board.move_piece(start_sq, end_sq)
                        white_to_move = not white_to_move
                        selected_sq = ()
                        player_clicks = []
                        valid_moves = []

                    else:
                        piece = board.board[row][col]
                        if piece is not None and (
                                (white_to_move and piece.color == "w") or (not white_to_move and piece.color == "b")):
                            selected_sq = (row, col)
                            player_clicks = [selected_sq]
                        else:
                            selected_sq = ()
                            player_clicks = []
                        valid_moves = []

                if len(player_clicks) == 1:
                    r, c = player_clicks[0]
                    valid_moves = board.get_valid_moves(r, c)

        # drawing by 1 iteration
        draw_game_state(screen, board, valid_moves, dot_img)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()