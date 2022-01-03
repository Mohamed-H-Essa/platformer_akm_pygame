import pygame
from meta_data import GameMetaData
# from main import draw_text
from draw_text import draw_text


class Player():
    def __init__(self, x, y, world):
        self.reset(x, y)
        self.world = GameMetaData.world

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.jumped == False and self.in_air == False:
                GameMetaData.jump_fx.play()
                self.vel_y = -15 * GameMetaData.scale_factor
                self.jumped = True
            if (key[pygame.K_SPACE] or key[pygame.K_UP]) == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5 * GameMetaData.scale_factor
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5 * GameMetaData.scale_factor
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10 * GameMetaData.scale_factor:  # * GameMetaData.scale_factor:
                self.vel_y = 10 * GameMetaData.scale_factor  # * GameMetaData.scale_factor
            dy += self.vel_y  # * GameMetaData.scale_factor

            # check for collision
            self.in_air = True
            # for tile in self.world.tile_list:
            for tile in GameMetaData.world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, GameMetaData.blob_group, False):
                game_over = -1
                GameMetaData.game_over_fx.play()

            # check for collision with lava
            if pygame.sprite.spritecollide(self, GameMetaData.lava_group, False):
                game_over = -1
                GameMetaData.game_over_fx.play()

            # check for collision with exit
            if pygame.sprite.spritecollide(self, GameMetaData.exit_group, False):
                game_over = 1

            # check for collision with platforms
            for platform in GameMetaData.platform_group:
                # collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', GameMetaData.font, GameMetaData.blue,
                      (GameMetaData.screen_width // 2) - 200*GameMetaData.scale_factor, GameMetaData.screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player onto screen
        GameMetaData.screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png').convert_alpha()
            img_right = pygame.transform.scale(
                img_right, (40 * GameMetaData.scale_factor, 80 * GameMetaData.scale_factor))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x * GameMetaData.scale_factor
        self.rect.y = y * GameMetaData.scale_factor
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
