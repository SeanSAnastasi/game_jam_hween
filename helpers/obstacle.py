import pygame
import random

# x,y position tiles 1-18

class Obstacle(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, image, x, y, multiplier):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        if not(image):
           
            self.image = pygame.Surface((50, 50))
            self.image.fill((200,20,40))
        else:
           
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (self.image.get_width() *multiplier, self.image.get_height()*multiplier))
            self.image.set_colorkey((0,0,0))
        

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (x, y)

        self.mask = pygame.mask.from_surface(self.image)



class Bonepile(Obstacle):
    def __init__(self, x, y):
        self.sprite_list = ["bonepile_1.png", "bonepile_2.png", "bonepile_3.png", "bonepile_4.png"]
        sprite = random.choice(self.sprite_list)
        file = "assets/images/"+sprite
        x_pos = 100+(x*64)
        y_pos = 90+(y*64)
        super().__init__(file, x_pos, y_pos, 3)

class Rock(Obstacle):
    def __init__(self, x, y):
        self.sprite_list = ["rock_1.png", "rock_2.png", "rock_3.png", "rock_4.png"]
        sprite = random.choice(self.sprite_list)
        file = "assets/images/"+sprite
        x_pos = 100+(x*64)
        y_pos = 90+(y*64)
        super().__init__(file, x_pos, y_pos, 4)

class Web(Obstacle):
    def __init__(self, x, y):
        self.sprite_list = ["web_1.png", "web_2.png", "web_3.png"]
        sprite = random.choice(self.sprite_list)
        file = "assets/images/"+sprite
        x_pos = 100+(x*64)
        y_pos = 90+(y*64)
        super().__init__(file, x_pos, y_pos, 2)

class Chest(Obstacle):
    def __init__(self, x, y):
        x_pos = 100+(x*64)
        y_pos = 90+(y*64)
        super().__init__("assets/images/chest_closed.png",  x_pos, y_pos, 4)

class Gravestone(Obstacle):
    def __init__(self, x, y):
        x_pos = 100+(x*64)
        y_pos = 90+(y*64)
        super().__init__("assets/images/gravestone.png",  x_pos, y_pos, 4)

