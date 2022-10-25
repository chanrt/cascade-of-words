import pygame as pg

class Text:
    def __init__(self, x, y, text, screen):
        self.x = x
        self.y = y
        self.screen = screen

        # display state
        self.display = True

        # text
        self.text = text
        self._text_color = pg.Color("white")
        self._font = pg.font.SysFont("arial", 20)
        self._font_size = 20

        self.init_display_text()

    def set_font(self, font):
        self._font = font
        self.init_display_text()

    def set_text(self, text):
        self.text = text
        self.init_display_text()

    def set_text_color(self, color):
        self._text_color = color
        self.init_display_text()

    def init_display_text(self):
        self.display_text = self._font.render(self.text, True, self._text_color)
        self.text_rect = self.display_text.get_rect(center=(self.x + self._font_size / 2, self.y + self._font_size / 2))

    def move_down(self, dy):
        self.y += dy
        self.init_display_text()

    def render(self):
        if self.display:
            self.screen.blit(self.display_text, self.text_rect)