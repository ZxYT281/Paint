from .settings import FADE_TIME, get_font


class FadeText:
    def __init__(self, x, y, text, text_color) -> None:
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        self.lifetime = FADE_TIME
        self.txt = get_font(30).render(
            self.text, False, self.text_color, (255, 255, 255))

    def update(self, win):
        if self.lifetime > 0:
            self.txt.set_alpha(min(255, self.lifetime * 100))
            win.blit(self.txt, (self.x, self.y))
            self.lifetime -= 0.1
