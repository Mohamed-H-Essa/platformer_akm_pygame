import pygame
from meta_data import GameMetaData


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() * GameMetaData.scale_factor, self.image.get_height() * GameMetaData.scale_factor))
        self.rect = self.image.get_rect()
        self.rect.x = x  # * GameMetaData.scale_factor
        self.rect.y = y  # * GameMetaData.scale_factor
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # print('hi')
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        GameMetaData.screen.blit(self.image, self.rect)

        return action
