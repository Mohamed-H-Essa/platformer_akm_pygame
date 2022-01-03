import pygame
from meta_data import GameMetaData


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png').convert_alpha()
        self.image = pygame.transform.scale(
            img, (GameMetaData.tile_size, GameMetaData.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x#* GameMetaData.scale_factor
        self.rect.y = y #* GameMetaData.scale_factor
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x #* GameMetaData.scale_factor
        self.move_y = move_y #* GameMetaData.scale_factor

    def update(self):
        self.rect.x += self.move_direction * self.move_x  #* GameMetaData.scale_factor
        self.rect.y += self.move_direction * self.move_y # * GameMetaData.scale_factor
        print(f'direction{self.move_direction}')
        self.move_counter += 1
        if abs(self.move_counter) > 50: #* GameMetaData.scale_factor:
            # if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
