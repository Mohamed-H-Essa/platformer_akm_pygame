import pygame
# from pygame import mixer
import pickle
from os import path
from draw_text import draw_text
from player import Player
from world import World
from coin import Coin
from meta_data import GameMetaData
from meta_data import GameMetaData
from player import Player
from button import Button
from pygame.locals import *


GameMetaData.metaGameStarter()
GameMetaData.defineFont()


white = (255, 255, 255)


# Sherif collected these assets so as to add cinsistency across sprites
sun_img = pygame.image.load('img/sun.png').convert_alpha()
sun_img = pygame.transform.scale(
    sun_img, (sun_img.get_width() * GameMetaData.scale_factor, sun_img.get_height() * GameMetaData.scale_factor))
bg_img = pygame.image.load('img/sky.png').convert_alpha()
bg_img = pygame.transform.scale(
    bg_img, (bg_img.get_width() * GameMetaData.scale_factor, bg_img.get_height() * GameMetaData.scale_factor))
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
restart_img = pygame.transform.scale(
    restart_img, (restart_img.get_width() * GameMetaData.scale_factor, restart_img.get_height() * GameMetaData.scale_factor))
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
start_img = pygame.transform.scale(
    start_img, (start_img.get_width() * GameMetaData.scale_factor, start_img.get_height() * GameMetaData.scale_factor))
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
exit_img = pygame.transform.scale(
    exit_img, (exit_img.get_width() * GameMetaData.scale_factor, exit_img.get_height() * GameMetaData.scale_factor))

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
        GameMetaData.world_data = pickle.load(pickle_in)
    GameMetaData.world = World(GameMetaData.world_data)
    # create dummy coin for showing the score
    score_coin = Coin(GameMetaData.tile_size // 2 * GameMetaData.scale_factor,
                      GameMetaData.tile_size // 2 * GameMetaData.scale_factor)
    GameMetaData.coin_group.add(score_coin)
    return GameMetaData.world


def main():
    # load in level data and create world
    if path.exists(f'./levels_data/level{GameMetaData.level}_data'):
        pickle_in = open(f'./levels_data/level{GameMetaData.level}_data', 'rb')
        GameMetaData.world_data = pickle.load(pickle_in)
    GameMetaData.world = World(GameMetaData.world_data)
    player = Player(
        100 * GameMetaData.scale_factor,
        GameMetaData.screen_height - 10 * GameMetaData.scale_factor,
        GameMetaData.world)

    # create dummy coin for showing the score
    score_coin = Coin(GameMetaData.tile_size // 2 * GameMetaData.scale_factor,
                      GameMetaData.tile_size // 2 * GameMetaData.scale_factor)
    GameMetaData.coin_group.add(score_coin)

    # creating buttons
    restart_button = Button(GameMetaData.screen_width // 2 - 50 * GameMetaData.scale_factor,
                            GameMetaData.screen_height // 2 + 100 * GameMetaData.scale_factor, restart_img)
    start_button = Button(GameMetaData.screen_width // 2 - 350 * GameMetaData.scale_factor,
                          GameMetaData.screen_height // 2, start_img)
    exit_button = Button(GameMetaData.screen_width // 2 + 150 * GameMetaData.scale_factor,
                         GameMetaData.screen_height // 2, exit_img)

    run = True

    while run:

        GameMetaData.clock.tick(GameMetaData.fps)

        GameMetaData.screen.blit(bg_img, (0, 0))
        GameMetaData.screen.blit(
            sun_img, (100*GameMetaData.scale_factor, 100*GameMetaData.scale_factor))

        if GameMetaData.main_menu == True:
            # does 2 things at the same time "excellent idea"
            if exit_button.draw():
                run = False
            # does 2 things at the same time "excellent idea"
            if start_button.draw():
                GameMetaData.main_menu = False
        else:
            GameMetaData.world.draw()

            if GameMetaData.game_over == 0:
                GameMetaData.blob_group.update()
                GameMetaData.platform_group.update()
                # update score
                # check if a coin has been collected, the "true" is for removing the collected ones
                if pygame.sprite.spritecollide(player, GameMetaData.coin_group, True):

                    GameMetaData.score += 1
                    GameMetaData.coin_fx.play()
                draw_text('X ' + str(GameMetaData.score) + '    FPS: ' + str(GameMetaData.clock.get_fps())[0:5], GameMetaData.font_score,
                          white, GameMetaData.tile_size - 10 * GameMetaData.scale_factor, 10 * GameMetaData.scale_factor)
                off_white = (30, 30, 30)
                level_text = GameMetaData.font.render(
                    'LEVEL: ' + str(GameMetaData.level), 1, off_white)
                GameMetaData.screen.blit(level_text, (GameMetaData.screen_width /
                                         2 - level_text.get_width() / 2, 50 * GameMetaData.scale_factor))

            # drawing everything onto the screan using the built in draw() method
            # see documentation for more details about how "draw" works in pygame
            """
                the draw method is a part of the pygame framework,
                it simply plots every sprite within the group onto the screen 
            """
            GameMetaData.blob_group.draw(GameMetaData.screen)
            GameMetaData.platform_group.draw(GameMetaData.screen)
            GameMetaData.lava_group.draw(GameMetaData.screen)
            GameMetaData.coin_group.draw(GameMetaData.screen)
            GameMetaData.exit_group.draw(GameMetaData.screen)
            # the player handles collision & movement etc
            """
            player movement are actually done here
            """
            GameMetaData.game_over = player.update(GameMetaData.game_over)

            # if player has died
            if GameMetaData.game_over == -1:  # -1 is the agreed upon value for losing
                # does 2 things at the same time "excellent idea"
                if restart_button.draw():  # providing a restart button so as to give another chance
                    GameMetaData.world_data = []
                    # the world object is used to turn raw world_data list into an actual-actionable object
                    GameMetaData.world = reset_level(
                        GameMetaData.level, player)
                    GameMetaData.game_over = 0
                    GameMetaData.score = 0

            # if player has completed the level
            if GameMetaData.game_over == 1:
                # reset game and go to next level
                GameMetaData.level += 1
                if GameMetaData.level <= GameMetaData.max_levels:
                    # reset level
                    GameMetaData.world_data = []  # emptying the world_data array
                    GameMetaData.world = reset_level(
                        GameMetaData.level, player)  # reset_level method will actually fill the world_data
                    GameMetaData.game_over = 0
                else:
                    draw_text('YOU WON, yaaaaaaaay!', GameMetaData.font, GameMetaData.blue,
                              (GameMetaData.screen_width // 2) - 140 * GameMetaData.scale_factor, GameMetaData.screen_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


main()
