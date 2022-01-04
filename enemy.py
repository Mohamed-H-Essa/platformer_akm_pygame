import pygame
from pygame import transform

from meta_data import GameMetaData
from coordinated import Coordinated

# Kareem Taha


class Enemy(Coordinated, pygame.sprite.Sprite):
    def __init__(self, x, y):
        Coordinated.__init__(self, x, y)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png').convert_alpha()

        # self.image.set_alpha(128)
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() * GameMetaData.scale_factor, self.image.get_width() * GameMetaData.scale_factor))
        self.rect = self.image.get_rect()
        self.rect.x = self.x  # * GameMetaData.scale_factor
        self.rect.y = self.y  # * GameMetaData.scale_factor
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
