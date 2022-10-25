from os import path
from random import randint
from time import time
import pygame as pg

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

    score_text = Text(c.screen_width - 50, 20, "Score: 0", screen)
    score_text.set_font(c.style_font)
    score = 0

    spawn_word = pg.USEREVENT + 1
    pg.time.set_timer(spawn_word, c.spawn_time)

    while True:
        start = time()
        clock.tick(c.fps)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == spawn_word:
                random_word = english_words[randint(0, len(english_words) - 1)]
                word_x = randint(100, c.screen_width - 100)
                new_word = Text(word_x, 0, random_word, screen)
                new_word.set_font(c.word_font)
                words.append(new_word)
                word_texts.append(random_word)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                if pg.K_a <= event.key <= pg.K_z:
                    user_input += chr(event.key).lower()

                    for i in range(c.min_length, c.max_length + 1):
                        substring = user_input[len(user_input) - i:]

                        if substring in word_texts:
                            word_texts.remove(substring)
                            word = get_word(words, substring)
                            words.remove(word)
                            score += len(substring)
                            score_text.set_text(f"Score: {score}")
                            

        for word in words:
            word.move_down(c.word_speed * c.dt)

        screen.fill(c.bg_color)

        for word in words:
            word.render()

        pg.draw.rect(screen, c.titlebar_color, (0, 0, c.screen_width, 50))
        title.render()
        score_text.render()

        pg.display.flip()
        
        end = time()
        c.set_dt(end - start)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen(screen)
    game_loop(screen)