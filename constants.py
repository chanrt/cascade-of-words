from os import path
import pygame as pg


class Constants:
    def __init__(self):
        pg.init()
        self.fps = 60
        self.dt = 1.0 / self.fps
        self.folder_path = path.dirname(__file__)

        self.spawn_time = 1500
        self.spawn_prob = 0.4
        self.word_speed = 20

        self.min_length = 4
        self.max_length = 10

        self.bg_color = pg.Color("black")
        self.titlebar_color = pg.Color("blue")

        self.word_font = pg.font.Font(path.join(self.folder_path, "data", "merriweather.ttf"), 20)
        self.style_font = pg.font.Font(path.join(self.folder_path, "data", "motion_picture.ttf"), 40)

    def set_screen(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

    def set_dt(self, dt):
        self.dt = dt


consts = Constants()