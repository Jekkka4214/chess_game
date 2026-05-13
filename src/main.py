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


def draw_game_state(screen, board_obj):
    #Drawing board
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # 1.draw cell
            color = COLORS[(r + c) % 2]
            rect = pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)

            # 2. draw piece
            piece = board_obj.board[r][c]
            if piece:
                screen.blit(piece.image_surface, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")

    # Creating obj Board
    chess_game_board = Board()
    load_images(chess_game_board)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()
            #     row = mouse_pos[0] // SQ_SIZE
            #     col =  mouse_pos[1] // SQ_SIZE
            #     if not (chess_game_board[row,col] == None):
            #         chess_game_board.get_valid_moves(row,col)

        # drawing by 1 iteration
        draw_game_state(screen, chess_game_board)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()