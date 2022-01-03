import pygame
from meta_data import GameMetaData


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    GameMetaData.screen.blit(
        img, (x * GameMetaData.scale_factor, y * GameMetaData.scale_factor))
