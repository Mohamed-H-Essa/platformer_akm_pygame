import pygame
from meta_data import GameMetaData
from coordinated import Coordinated


# Kareem Taha
class Lava(Coordinated, pygame.sprite.Sprite):
    def __init__(self, x, y):
        Coordinated.__init__(self, x, y)
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(
            img, (GameMetaData.tile_size, GameMetaData.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = self.x  # * GameMetaData.scale_factor
        self.rect.y = self.y  # * GameMetaData.scale_factor
