import pygame
from pygame import mixer


class GameMetaData:

    # Ahmed Ali group idea
    blob_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    lava_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()

    # these are static variables that can be accessed anywhere in the code through this class
    clock = pygame.time.Clock()
    fps = 60

    # Siko scale_factor idea
    # adding scale factor for different sceren reselutions
    scale_factor = 0.7
    # defining screen variables ( width and height )
    screen_width = 1000 * scale_factor
    screen_height = 1000 * scale_factor
    # define game variables
    tile_size = 50 * scale_factor
    game_over = 0
    main_menu = True
    level = 1
    max_levels = 5
    score = 0
    blue = (0, 0, 255)

    # TO-DO fix this method
    # edit: done
    @classmethod
    def metaGameStarter(cls):
        # TO-DO make this screen global
        # edit: done
        pygame.display.set_caption('Platformer')
        cls.screen = pygame.display.set_mode(
            (GameMetaData.screen_width, GameMetaData.screen_height))
        # necissaries that are called in the beginning of the game
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        pygame.init()
        pygame.mixer.music.load('img/music.wav')
        pygame.mixer.music.play(-1, 0.0, 5000)
        cls.coin_fx = pygame.mixer.Sound('img/coin.wav')
        cls.coin_fx.set_volume(0.5)
        cls.jump_fx = pygame.mixer.Sound('img/jump.wav')
        cls.jump_fx.set_volume(0.5)
        cls.game_over_fx = pygame.mixer.Sound('img/game_over.wav')
        cls.game_over_fx.set_volume(0.5)

    # define font
    @classmethod
    def defineFont(cls):
        cls.font = pygame.font.SysFont(
            'Bauhaus 93', int(70 * cls.scale_factor))
        cls.font_score = pygame.font.SysFont(
            'Bauhaus 93', int(30 * cls.scale_factor))
