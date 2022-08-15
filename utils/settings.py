import pygame
pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

FPS = 60
WIDTH, HEIGHT = 600, 700

ROWS = COLS = 50

TOOLBAR_HEIGHT = HEIGHT - WIDTH

PIXEL_SIZE = WIDTH // ROWS

BG_COLOR = WHITE

DRAW_GRID_LINES = True
MAKE_BG_TRANSPARENT_ON_SAVE = True

BUTTON_START_X = 5
GAP_BUTTON = 60
BUTTON_SIZE = 50

UNDO_LIST_SIZE = 100


def get_font(size):
    return pygame.font.SysFont("comicsans", size)


if __name__ == "__main__":
    # from .. import main
    print("Run the main module")
