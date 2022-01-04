import pygame
from meta_data import GameMetaData
from coordinated import Coordinated


# Kareem taha
class Exit(Coordinated, pygame.sprite.Sprite):
    def __init__(self, x, y):
        Coordinated.__init__(self, x, y)
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png').convert_alpha()
        self.image = pygame.transform.scale(
            img, (GameMetaData.tile_size, int(GameMetaData.tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
