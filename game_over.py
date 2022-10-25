import pygame as pg

from button import Button
from constants import consts as c
from text import Text


def game_over(screen, score):
    title = Text(c.screen_width // 2, c.screen_height // 2 - 100, "Cascade of Words", screen)
    title.set_font(c.style_font)

    score_text = Text(c.screen_width // 2, c.screen_height // 2, f"Your score: {score}", screen)
    score_text.set_font(c.word_font)

    restart_button = Button(c.screen_width // 2 - 100, c.screen_height // 2 + 100, 100, 50, screen, "Restart")
    quit_button = Button(c.screen_width // 2 + 100, c.screen_height // 2 + 100, 100, 50, screen, "Quit")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "exit"

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return "exit"

            if event.type == pg.MOUSEMOTION:
                mouse_pos = pg.mouse.get_pos()
                restart_button.update(mouse_pos)
                quit_button.update(mouse_pos)

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                click = event.button
                restart_button.check_clicked(mouse_pos, click)
                quit_button.check_clicked(mouse_pos, click)

                if restart_button.left_clicked:
                    return "restart"

                if quit_button.left_clicked:
                    return "exit"
                
        screen.fill(c.bg_color)

        title.render()
        score_text.render()
        restart_button.render()
        quit_button.render()

        pg.display.flip()