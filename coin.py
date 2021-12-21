import pygame
from meta_data import GameMetaData


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(
            img, (GameMetaData.tile_size // 2, GameMetaData.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
