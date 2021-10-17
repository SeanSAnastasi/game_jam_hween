import pygame
from pygame.mixer import fadeout

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.Surface((50, 50))
        self.image.fill((0,0,0))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (220, 220)

        # Movement variables
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False

        # Base Stats
        self.movement_speed = 5
        self.damage = 1
        self.shot_speed = 4
        self.shot_delay = 2
        self.max_health = 5
        self.current_health = self.max_health

        # Bounding box from scene for movement
        self.movable_area = None

    def update(self):
        # any code here will happen every time the game loop updates
        # self.rect.x -= 5
        # if self.rect.left < 0:
        #     self.rect.left = 0

        if self.move_up:
            self.rect.y -= self.movement_speed
        elif self.move_down:
            self.rect.y += self.movement_speed
        elif self.move_left:
            self.rect.x -= self.movement_speed
        elif self.move_right:
            self.rect.x += self.movement_speed

        if self.movable_area != None:
            self.rect.clamp_ip(self.movable_area)

