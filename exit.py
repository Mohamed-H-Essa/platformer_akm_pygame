import pygame
from meta_data import GameMetaData


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png').convert_alpha()
        self.image = pygame.transform.scale(
            img, (GameMetaData.tile_size, int(GameMetaData.tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x  # * GameMetaData.scale_factor
        self.rect.y = y  # * GameMetaData.scale_factor
