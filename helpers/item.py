import pygame
import random


class Syringe(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.image.load("assets/images/syringe.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1.5), int(self.image.get_height()*1.5)))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (600, 400)

    def get_change(self):
        movement_speed = 0
        damage = random.randint(-2,2)
        shot_speed = 0
        shot_delay = 0
        max_health = 0
        current_health = 0
        change = {
            "type"              : "stats",
            "movement_speed"    : movement_speed,
            "damage"            : damage,
            "shot_speed"        : shot_speed,
            "shot_delay"        : shot_delay,
            "max_health"        : max_health,
            "current_health"    : current_health
        }
        return change

 
    def update(self):
        pass

class Bottle(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.image.load("assets/images/bottle.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *2), int(self.image.get_height()*2)))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (600, 400)

    def get_change(self):
        movement_speed = 0
        damage = 0
        shot_speed = random.randint(-2,2)
        shot_delay = random.randint(-2,2)
        max_health = 0
        current_health = 0
        change = {
            "type"              : "refresh",
            "movement_speed"    : movement_speed,
            "damage"            : damage,
            "shot_speed"        : shot_speed,
            "shot_delay"        : shot_delay,
            "max_health"        : max_health,
            "current_health"    : current_health
        }
        return change

    def update(self):
        pass

class Flask(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.image.load("assets/images/flask.png")
        
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *2), int(self.image.get_height()*2)))
        self.image.set_colorkey((0,0,0))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (600, 400)

    def get_change(self):
        movement_speed = random.randint(-2,2)
        damage = 0
        shot_speed = 0
        shot_delay = 0
        max_health = random.randint(-2,2)
        current_health = random.randint(-2,2)
        change = {
            "type"              : "stats",
            "movement_speed"    : movement_speed,
            "damage"            : damage,
            "shot_speed"        : shot_speed,
            "shot_delay"        : shot_delay,
            "max_health"        : max_health,
            "current_health"    : current_health
        }
        return change

    def update(self):
        pass

class ChocBar(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.image.load("assets/images/chocbar.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *2), int(self.image.get_height()*2)))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (600, 400)

    def get_change(self):
        movement_speed = random.randint(-2,2)
        damage = 0
        shot_speed = random.randint(-2,2)
        shot_delay = 0
        max_health = 0
        current_health = 0
        change = {
            "type"              : "stats",
            "movement_speed"    : movement_speed,
            "damage"            : damage,
            "shot_speed"        : shot_speed,
            "shot_delay"        : shot_delay,
            "max_health"        : max_health,
            "current_health"    : current_health
        }
        return change

    def update(self):
        pass

class Candy(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.image.load("assets/images/candy.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *2), int(self.image.get_height()*2)))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (600, 400)

    def get_change(self):
        movement_speed = 1
        damage = 1
        shot_speed = 1
        shot_delay = 1
        max_health = 1
        current_health = 1
        change = {
            "type"              : "effect",
            "movement_speed"    : movement_speed,
            "damage"            : damage,
            "shot_speed"        : shot_speed,
            "shot_delay"        : shot_delay,
            "max_health"        : max_health,
            "current_health"    : current_health
        }
        return change

    def update(self):
        pass

