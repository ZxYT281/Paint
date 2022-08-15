from utils.button import Button
from utils import *
from PIL import Image
import sys

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint ● Python ● Divyanshu")

sys.setrecursionlimit(10000)


def init_grid(rows, cols, color):
    grid = []
    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid


def write_image(filename):
    image = Image.new("RGBA", (ROWS, COLS))
    # data = f"P3 {ROWS} {COLS}\n 255\n"
    for i, row in enumerate(grid):
        for j, (r, g, b) in enumerate(row):
            # data += f" {r} {g} {b} "
            image.putpixel((j, i), (r, g, b))
            if ((r, g, b) == BG_COLOR) and MAKE_BG_TRANSPARENT_ON_SAVE:
                image.putpixel((j, i), (r, g, b, 0))

    #     data += "\n"
    image.save(filename.replace(".ppm", ".png"), "PNG")
    # with open(filename, "w") as f:
    #     f.write(data)


def load_image(filename):
    image = Image.open(filename)
    if image.width > COLS or image.height > ROWS:
        return

    for i in range(ROWS + 1):
        pass


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i *
                             PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.aaline(win, BLACK, (0, i * PIXEL_SIZE),
                               (WIDTH, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.aaline(win, BLACK, (i * PIXEL_SIZE, 0),
                               (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)
    pygame.draw.line(win, BLACK, (0, HEIGHT - TOOLBAR_HEIGHT),
                     (WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    for button in buttons:
        button.draw(win)

    pygame.display.update()


def get_row_col_from_pos(pos):

    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise KeyError

    return row, col


def get_color_at(y, x):
    try:
        return grid[y][x]
    except IndexError:
        return (0, 0, 0)


def color_near(y, x, color):
    try:

        # Right
        if grid[y][x + 1] != drawing_color and grid[y][x + 1] == color:
            grid[y][x+1] = drawing_color
            color_near(y, x + 1, color)

        if grid[y][x - 1] != drawing_color and grid[y][x - 1] == color:
            grid[y][x-1] = drawing_color
            color_near(y, x - 1, color)

        if grid[y + 1][x] != drawing_color and grid[y + 1][x] == color:
            grid[y + 1][x] = drawing_color
            color_near(y + 1, x, color)

        if grid[y - 1][x] != drawing_color and grid[y - 1][x] == color:
            grid[y - 1][x] = drawing_color
            color_near(y - 1, x, color)
        # grid[y][x] = (128, 128, 128)
    except IndexError:
        return

    return


def undo(undo_list):
    try:
        grid[undo_list[len(undo_list)-1][0]][undo_list[len(undo_list)-1]
                                             [1]] = undo_list[len(undo_list)-1][2]
        undo_list.pop(len(undo_list)-1)
    except:
        pass


run = True
clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLUE

buttons_y = HEIGHT - TOOLBAR_HEIGHT/2 - 12.5

buttons = [
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, BLACK),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, WHITE),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, RED),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, GREEN),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, BLUE),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, YELLOW),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, WHITE, "ERASE", BLACK),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, WHITE, "COLOR", RED),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, WHITE, "CLEAR", RED),
    Button(0, buttons_y, BUTTON_SIZE, BUTTON_SIZE, WHITE, "FILL", BLACK),
]
undo_list = []

prev_btn_pos = BUTTON_START_X
for btn in buttons:
    btn.x = prev_btn_pos
    prev_btn_pos += GAP_BUTTON

while run:
    clock.tick(FPS)
    pygame.time.get_ticks()
    draw(WIN, grid, buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                undo(undo_list)
            if event.key == pygame.K_s:
                filenamersf = pygame.time.get_ticks()  # input("Name: ")
                write_image(f"pictures/{filenamersf}.ppm")
            if event.key == pygame.K_l:
                DRAW_GRID_LINES = not DRAW_GRID_LINES
            if event.key == pygame.K_j:
                MAKE_BG_TRANSPARENT_ON_SAVE = not MAKE_BG_TRANSPARENT_ON_SAVE

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            try:
                row, col = get_row_col_from_pos(pos)
                if buttons[9].selected:
                    color_near(row, col, get_color_at(row, col))

                if not grid[row][col] == drawing_color:
                    temp_col = grid[row][col]
                    grid[row][col] = drawing_color
                if len(undo_list) < UNDO_LIST_SIZE:
                    undo_list.append([row, col, temp_col])
                else:
                    undo_list.pop(0)
            except KeyError:
                for button in buttons:
                    button.selected = False
                    if not button.clicked(pos):
                        continue
                    if button.text == "CLEAR":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        undo_list = []
                        continue
                    if button.text == "COLOR":
                        BG_COLOR = drawing_color

                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        continue
                    if button.text == "ERASE":
                        drawing_color = BG_COLOR
                        button.selected = True
                        continue

                    if button.text == "FILL":
                        button.selected = True
                        button.selected_color = drawing_color
                        continue

                    button.selected = True
                    drawing_color = button.color
