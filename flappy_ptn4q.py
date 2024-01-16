import pygame
from pygame.locals import *

FPS = 32
scr_width = 288
scr_height = 512
game_image = {}
display_screen_window = pygame.display.set_mode((scr_width, scr_height))
play_ground = scr_height * 0.8
player = 'data/ptn4q.png'
bcg = 'data/bcg_city.png'


def gameplay():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
        # if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == pygame.MOUSEBUTTONDOWN:
        # dhgdhgdfgdgfdgf
        else:
            p_x = int(scr_width / 5)
            p_y = int((scr_height - game_image['player'].get_height()) / 2)
            display_screen_window.blit(game_image['background'], (0, 0))
            display_screen_window.blit(game_image['player'], (p_x, p_y))
            pygame.display.update()
            time_clock.tick(FPS)



if __name__ == "__main__":
    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy PTQ')

    game_image['background'] = pygame.image.load(bcg).convert()
    game_image['player'] = pygame.image.load(player).convert_alpha()


    while True:
        gameplay()

