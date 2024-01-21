import pygame
import sys
from pygame.locals import *

FPS = 32
scr_width = 288
scr_height = 512
game_image = {}
display_screen_window = pygame.display.set_mode((scr_width, scr_height))
play_ground = scr_height * 0.8
player = 'data/ptn4q.png'


def menu():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        else:
            display_screen_window.blit(pygame.image.load('data/menu.png').convert(), (0, 0))
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] >= 79 and event.pos[0] <= 210:
                    if event.pos[1] >= 214 and event.pos[1] <= 247:
                        return 'data/bcg_default.png'
                    elif event.pos[1] >= 286 and event.pos[1] <= 319:
                        return 'data/bcg_cave.png'
                    elif event.pos[1] >= 358 and event.pos[1] <= 391:
                        return 'data/bcg_city.png'


def level(bcg):
    p_x = int(scr_width / 5)
    p_y = int((scr_height - game_image['player'].get_height()) / 2)
    game_image['background'] = pygame.image.load(bcg).convert()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)\
            or event.type == pygame.MOUSEBUTTONDOWN:
                return None
            else:
                display_screen_window.blit(game_image['background'], (0, 0))
                display_screen_window.blit(game_image['player'], (p_x, p_y))
                pygame.display.update()
                time_clock.tick(FPS)

# def gameplay():





if __name__ == "__main__":
    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy PTQ')
    game_image['player'] = pygame.image.load(player).convert_alpha()

    while True:
        if  a := menu():
            level(a)

