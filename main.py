import pygame as pg

from constants import consts as c
from game_loop import game_loop
from game_over import game_over


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen(screen)
    
    while True:
        outcome, score = game_loop(screen)

        if outcome == "game_over":
            choice = game_over(screen, score)

            if choice == "restart":
                continue
            else:
                break
        else:
            break