import pygame
from meta_data import GameMetaData
from enemy import Enemy
# from platform import Platform
from lava import Lava
from platforma import Platform
from coin import Coin
from exit import Exit


class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(
                        dirt_img, (GameMetaData.tile_size, GameMetaData.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * GameMetaData.tile_size
                    img_rect.y = row_count * GameMetaData.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(
                        grass_img, (GameMetaData.tile_size, GameMetaData.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * GameMetaData.tile_size
                    img_rect.y = row_count * GameMetaData.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * GameMetaData.tile_size,
                                 row_count * GameMetaData.tile_size + 15)
                    GameMetaData.blob_group.add(blob)
                if tile == 4:
                    platform = platform.Platform(
                        col_count * GameMetaData.tile_size, row_count * GameMetaData.tile_size, 1, 0)
                    GameMetaData.platform_group.add(platform)
                if tile == 5:
                    platform = Platform(
                        col_count * GameMetaData.tile_size, row_count * GameMetaData.tile_size, 0, 1)
                    GameMetaData.platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * GameMetaData.tile_size, row_count *
                                GameMetaData.tile_size + (GameMetaData.tile_size // 2))
                    GameMetaData.lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * GameMetaData.tile_size + (GameMetaData.tile_size // 2),
                                row_count * GameMetaData.tile_size + (GameMetaData.tile_size // 2))
                    GameMetaData.coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * GameMetaData.tile_size, row_count *
                                GameMetaData.tile_size - (GameMetaData.tile_size // 2))
                    GameMetaData.exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            GameMetaData.screen.blit(tile[0], tile[1])
