from .settings import *


class Button:
    def __init__(self, x=0, y=0, height=64, width=64, color=WHITE, text=None, text_color=None, selected_color=None):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.text = text
        self.text_color = text_color
        self.selected = False
        self.selected_color = selected_color or (156, 156, 156)

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))
        if not self.color == BLACK:
            pygame.draw.rect(win, BLACK, (self.x, self.y,
                             self.width, self.height), 2)
        else:
            pygame.draw.rect(win, WHITE, (self.x, self.y,
                             self.width, self.height), 2)
        if self.text:
            button_font = get_font(15)
            text_surface = button_font.render(self.text, 1, self.text_color)
            win.blit(text_surface, (self.x + self.width/2 - text_surface.get_width() /
                     2, self.y + self.height/2 - text_surface.get_height()/2))
        if self.selected or self.clicked(pygame.mouse.get_pos()):
            pygame.draw.rect(win, self.selected_color,
                             (self.x, self.y, self.width, self.height), 2)

    def clicked(self, pos):
        x, y = pos
        if not ((x >= self.x and x <= (self.x + self.width)) and (y >= self.y and y <= (self.y + self.height))):
            return False
        return True
