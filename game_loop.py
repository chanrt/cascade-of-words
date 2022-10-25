from os import environ, path
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from random import randint
from time import time
import pygame as pg

from button import Button
from constants import consts as c
from text import Text


def get_word(words, text):
    for word in words:
        if word.text == text:
            return word
    return -1


def game_loop(screen):
    clock = pg.time.Clock()

    words = []
    word_texts = []
    user_input = ""

    english_words = open(path.join(c.folder_path, "data", "english_words.txt")).read().split("\n")
    english_words = list(filter(lambda x: len(x) >= c.min_length and len(x) <= c.max_length, english_words))
    
    title = Text(c.screen_width // 2, 20, "Cascade of Words", screen)
    title.set_font(c.style_font)

    score_text = Text(c.screen_width - 100, 20, "Score: 0", screen)
    score_text.set_font(c.word_font)
    score = 0

    about_text = Text(c.screen_width // 2, c.screen_height - 35, "Developed by ChanRT | Fork me at GitHub", screen)
    about_text.set_font(c.word_font)

    restart_button = Button(100, c.screen_height - 25, 100, 40, screen, "Restart")
    quit_button = Button(c.screen_width - 100, c.screen_height - 25, 100, 40, screen, "Quit")

    pg.mixer.music.load(path.join(c.folder_path, "data", "bg_music.mp3"))
    pg.mixer.music.play(-1)

    word_finish = pg.mixer.Sound(path.join(c.folder_path, "data", "word_finish.wav"))
    game_over = pg.mixer.Sound(path.join(c.folder_path, "data", "game_over.wav"))

    spawn_word = pg.USEREVENT + 1
    pg.time.set_timer(spawn_word, c.spawn_time)

    spawn_faster = pg.USEREVENT + 2
    pg.time.set_timer(spawn_faster, 20000)

    while True:
        start = time()
        clock.tick(c.fps)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.mixer.music.stop()
                return "exit", score

            if event.type == spawn_word:
                random_word = english_words[randint(0, len(english_words) - 1)]
                word_x = randint(100, c.screen_width - 100)
                new_word = Text(word_x, 20, random_word, screen)
                new_word.set_font(c.word_font)
                words.append(new_word)
                word_texts.append(random_word)

            if event.type == spawn_faster:
                c.spawn_time -= 50
                if c.spawn_time < 1000:
                    c.spawn_time = 1000

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mixer.music.stop()
                    return "exit", score
                if pg.K_a <= event.key <= pg.K_z:
                    user_input += chr(event.key).lower()

                    for i in range(c.min_length, c.max_length + 1):
                        substring = user_input[len(user_input) - i:]

                        if substring in word_texts:
                            word_finish.play()
                            word_texts.remove(substring)
                            word = get_word(words, substring)
                            words.remove(word)
                            score += len(substring)
                            score_text.set_text(f"Score: {score}")

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
                    words = []
                    word_texts = []
                    score = 0
                    score_text.set_text(f"Score: {score}")

                if quit_button.left_clicked:
                    pg.mixer.music.stop()
                    return "exit", score

            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                click = event.button
                restart_button.check_released(mouse_pos, click)
                quit_button.check_released(mouse_pos, click)

        for word in words:
            word.move_down(c.word_speed * c.dt)

            if word.y > c.screen_height - 50:
                pg.mixer.music.stop()
                game_over.play()
                return "game_over", score

        screen.fill(c.bg_color)

        for word in words:
            word.render()

        pg.draw.rect(screen, c.titlebar_color, (0, 0, c.screen_width, 50))
        title.render()
        score_text.render()

        pg.draw.rect(screen, c.titlebar_color, (0, c.screen_height - 50, c.screen_width, 50))
        restart_button.render()
        quit_button.render()
        about_text.render()

        pg.display.flip()
        
        end = time()
        c.set_dt(end - start)


if __name__ == '__main__':    
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen(screen)
    game_loop(screen)