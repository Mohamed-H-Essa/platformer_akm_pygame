import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
from draw_text import draw_text
from player import Player
from world import World
from coin import Coin
from meta_data import GameMetaData
from meta_data import GameMetaData
from player import Player


GameMetaData.metaGameStarter()
GameMetaData.defineFont()


white = (255, 255, 255)


# load images
sun_img = pygame.image.load('img/sun.png')  # .convert()
bg_img = pygame.image.load('img/sky.png').convert()
restart_img = pygame.image.load('img/restart_btn.png').convert()
start_img = pygame.image.load('img/start_btn.png').convert()
exit_img = pygame.image.load('img/exit_btn.png').convert()

# function to reset level


def reset_level(level, player):
    player.reset(100, GameMetaData.screen_height - 130)
    GameMetaData.blob_group.empty()
    GameMetaData.platform_group.empty()
    GameMetaData.coin_group.empty()
    GameMetaData.lava_group.empty()
    GameMetaData.exit_group.empty()

    # load in level data and create world
    if path.exists(f'./levels_data/level{level}_data'):
        pickle_in = open(f'./levels_data/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    # create dummy coin for showing the score
    score_coin = Coin(GameMetaData.tile_size // 2, GameMetaData.tile_size // 2)
    GameMetaData.coin_group.add(score_coin)
    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print('hi')
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        GameMetaData.screen.blit(self.image, self.rect)

        return action


def main():
    # load in level data and create world
    if path.exists(f'./levels_data/level{GameMetaData.level}_data'):
        pickle_in = open(f'./levels_data/level{GameMetaData.level}_data', 'rb')
        GameMetaData.world_data = pickle.load(pickle_in)
        # print(len(world_data))
    world = World(GameMetaData.world_data)
    player = Player(100, GameMetaData.screen_height - 130, world)
    # player = Player(100, GameMetaData.screen_height - 130)

    # GameMetaData.blob_group = pygame.sprite.Group()
    # GameMetaData.platform_group = pygame.sprite.Group()
    # GameMetaData.lava_group = pygame.sprite.Group()
    # GameMetaData.coin_group = pygame.sprite.Group()
    # GameMetaData.exit_group = pygame.sprite.Group()

    # create dummy coin for showing the score
    score_coin = Coin(GameMetaData.tile_size // 2, GameMetaData.tile_size // 2)
    GameMetaData.coin_group.add(score_coin)

    # # load in level data and create world
    # if path.exists(f'level{GameMetaData.level}_data'):
    #     pickle_in = open(f'level{GameMetaData.level}_data', 'rb')
    #     world_data = pickle.load(pickle_in)
    #     # print(len(world_data))
    # world = World(world_data)

    # create buttons
    restart_button = Button(GameMetaData.screen_width // 2 - 50,
                            GameMetaData.screen_height // 2 + 100, restart_img)
    start_button = Button(GameMetaData.screen_width // 2 - 350,
                          GameMetaData.screen_height // 2, start_img)
    exit_button = Button(GameMetaData.screen_width // 2 + 150,
                         GameMetaData.screen_height // 2, exit_img)

    run = True

    while run:

        GameMetaData.clock.tick(GameMetaData.fps)

        GameMetaData.screen.blit(bg_img, (0, 0))
        GameMetaData.screen.blit(sun_img, (100, 100))

        if GameMetaData.main_menu == True:
            if exit_button.draw():
                run = False
            if start_button.draw():
                GameMetaData.main_menu = False
        else:
            world.draw()

            if GameMetaData.game_over == 0:
                GameMetaData.blob_group.update()
                GameMetaData.platform_group.update()
                # update score
                # check if a coin has been collected
                if pygame.sprite.spritecollide(player, GameMetaData.coin_group, True):
                    GameMetaData.score += 1
                    GameMetaData.coin_fx.play()
                draw_text('X ' + str(GameMetaData.score) + '''    FPS: ''' + str(GameMetaData.clock.get_fps())[0:5], GameMetaData.font_score,
                          white, GameMetaData.tile_size - 10, 10)

            GameMetaData.blob_group.draw(GameMetaData.screen)
            GameMetaData.platform_group.draw(GameMetaData.screen)
            GameMetaData.lava_group.draw(GameMetaData.screen)
            GameMetaData.coin_group.draw(GameMetaData.screen)
            GameMetaData.exit_group.draw(GameMetaData.screen)

            GameMetaData.game_over = player.update(GameMetaData.game_over)

            # if player has died
            if GameMetaData.game_over == -1:
                if restart_button.draw():
                    world_data = []
                    world = reset_level(GameMetaData.level, player)
                    GameMetaData.game_over = 0
                    GameMetaData.score = 0

            # if player has completed the level
            if GameMetaData.game_over == 1:
                # reset game and go to next level
                GameMetaData.level += 1
                if GameMetaData.level <= GameMetaData.max_levels:
                    # reset level
                    world_data = []
                    world = reset_level(GameMetaData.level, player)
                    GameMetaData.game_over = 0
                else:
                    draw_text('YOU WIN!', GameMetaData.font, GameMetaData.blue,
                              (GameMetaData.screen_width // 2) - 140, GameMetaData.screen_height // 2)
                    if restart_button.draw():
                        GameMetaData.level = 1
                        # reset level
                        world_data = []
                        world = reset_level(GameMetaData.level)
                        GameMetaData.game_over = 0
                        GameMetaData.score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
