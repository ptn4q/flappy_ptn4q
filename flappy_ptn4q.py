import pygame
import sys
import random
from pygame.locals import *
import time

FPS = 32
scr_width = 288
scr_height = 512
game_image = {}
game_audio_sound = {}
display_screen_window = pygame.display.set_mode((scr_width, scr_height))


def menu():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        else:
            display_screen_window.blit(pygame.image.load('data/menu.png').convert(), (0, 0))
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and 79 <= event.pos[0] <= 210:
                if 214 <= event.pos[1] <= 247:
                    return ['data/bcg_default.png', 1, -4]
                elif 286 <= event.pos[1] <= 319:
                    return ['data/bcg_cave.png', 2, -4]
                elif 358 <= event.pos[1] <= 391:
                    return ['data/bcg_city.png', 3, -6]


def gameplay(level_parameters):
    game_image['background'] = pygame.image.load(level_parameters[0]).convert()
    game_image['base'] = pygame.image.load(f'data/base{level_parameters[1]}.png').convert()
    game_image['pipe'] = (
        pygame.transform.rotate(pygame.image.load(f'data/pipe{level_parameters[1]}.png').convert_alpha(), 180),
        pygame.image.load(f'data/pipe{level_parameters[1]}.png').convert_alpha())
    game_image['player'] = pygame.image.load(f'data/ptn4q{level_parameters[1]}.png').convert_alpha()
    # в зависимости от выбора уровня загружаются разные изображения
    score = 0
    p_x = int(scr_width / 5)
    p_y = int(scr_width / 2)

    pip1 = random_pipes()
    pip2 = random_pipes()

    top_pips = [
        {'x': scr_width + 200, 'y': pip1[0]['y']},
        {'x': scr_width + 200 + (scr_width / 2), 'y': pip2[0]['y']},
    ]

    lower_pips = [
        {'x': scr_width + 200, 'y': pip1[1]['y']},
        {'x': scr_width + 200 + (scr_width / 2), 'y': pip2[1]['y']},
    ]

    pip_v = level_parameters[2]  # скорость передвижения труб(по x)
    p_v = -8  # скорость передвижения птички(по y)
    p_flap_v = -8
    p_flap = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) \
                    or event.type == pygame.MOUSEBUTTONDOWN:
                if p_y > 0:
                    p_v = p_flap_v
                    p_flap = True
                    game_audio_sound['wing'].play()

        cr_tst = colliding(p_x, p_y, top_pips,
                           lower_pips)
        if cr_tst:
            return
            # while True:
            #     display_screen_window.blit(pygame.image.load('data/death_message.png').convert(), (0, 0))
            #     for event in pygame.event.get():
            #         if event.type == pygame.MOUSEBUTTONDOWN and 250 <= event.pos[1] <= 450:
            #             if 0 <= event.pos[0] <= 114:
            #                 gameplay(level_parameters)
            #             elif 115 <= event.pos[0] <= 228:
            #                 return

        p_mid_pos = p_x + game_image['player'].get_width() / 2
        for pipe in top_pips:
            pip_mid_pos = pipe['x'] + game_image['pipe'][0].get_width() / 2
            if pip_mid_pos <= p_mid_pos < pip_mid_pos - pip_v:
                score += 1
                game_audio_sound['point'].play()

        if p_v < 10 and not p_flap:
            p_v += 1

        if p_flap:
            p_flap = False
        p_y = p_y + min(p_v, scr_height * 0.8 - p_y - game_image['player'].get_height())

        for pip_upper, pip_lower in zip(top_pips, lower_pips):
            pip_upper['x'] += pip_v
            pip_lower['x'] += pip_v

        if 0 < top_pips[0]['x'] < 5:
            new_pip = random_pipes()
            top_pips.append(new_pip[0])
            lower_pips.append(new_pip[1])

        if top_pips[0]['x'] < -game_image['pipe'][0].get_width():
            top_pips.pop(0)
            lower_pips.pop(0)

        display_screen_window.blit(game_image['background'].convert(), (0, 0))

        for pip_upper, pip_lower in zip(top_pips, lower_pips):
            display_screen_window.blit(game_image['pipe'][0], (pip_upper['x'], pip_upper['y']))
            display_screen_window.blit(game_image['pipe'][1], (pip_lower['x'], pip_lower['y']))

        display_screen_window.blit(game_image['base'], (0, scr_height * 0.8))
        display_screen_window.blit(game_image['player'], (p_x, p_y))

        list_score_numbs = [int(x) for x in list(str(score))]
        k = 0
        for numb in list_score_numbs:
            k += game_image['numbers'][numb].get_width()
        score_x = (scr_width - k) / 2

        for numb in list_score_numbs:
            display_screen_window.blit(game_image['numbers'][numb], (score_x, scr_height * 0.12))
            score_x += game_image['numbers'][numb].get_width()

        pygame.display.update()
        time_clock.tick(FPS)


def colliding(p_x, p_y, up_pipes, low_pipes):
    if p_y > scr_height * 0.8 - 25 or p_y < 0:
        game_audio_sound['hit'].play()
        return True

    for pipe in up_pipes:
        if (p_y < game_image['pipe'][0].get_height() + pipe['y']) and abs(p_x - pipe['x']) < \
                game_image['pipe'][0].get_width() - 20:
            game_audio_sound['hit'].play()
            return True

    for pipe in low_pipes:
        if (p_y + game_image['player'].get_height() > pipe['y']) and abs(p_x - pipe['x']) < \
                game_image['pipe'][0].get_width() - 20:
            game_audio_sound['hit'].play()
            return True

    return False


def random_pipes():
    pip_h = game_image['pipe'][0].get_height()
    off_s = scr_height / 3
    yes2 = off_s + random.randrange(0, int(scr_height - game_image['base'].get_height() - 1.2 * off_s))
    pipeX = scr_width + 10
    y1 = pip_h - yes2 + off_s
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': yes2}
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy ptn4q')
    game_image['death_wind'] = pygame.image.load('data/death_message.png').convert_alpha()
    game_image['numbers'] = (
        pygame.image.load('data/0.png').convert_alpha(),
        pygame.image.load('data/1.png').convert_alpha(),
        pygame.image.load('data/2.png').convert_alpha(),
        pygame.image.load('data/3.png').convert_alpha(),
        pygame.image.load('data/4.png').convert_alpha(),
        pygame.image.load('data/5.png').convert_alpha(),
        pygame.image.load('data/6.png').convert_alpha(),
        pygame.image.load('data/7.png').convert_alpha(),
        pygame.image.load('data/8.png').convert_alpha(),
        pygame.image.load('data/9.png').convert_alpha(),
    )
    game_audio_sound['hit'] = pygame.mixer.Sound('data/hit.wav')
    game_audio_sound['point'] = pygame.mixer.Sound('data/point.wav')
    game_audio_sound['wing'] = pygame.mixer.Sound('data/wing.wav')

    while True:
        if parameters := menu():
            gameplay(parameters)
