import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/door1Top.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() *3, self.image.get_height()*3))
        self.rect = self.image.get_rect()

class NorthDoor(Door):
    def __init__(self):
        super(NorthDoor, self).__init__()  
        self.image.set_colorkey((0,0,0))
        self.rect.center = (600,55)

class SouthDoor(Door):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey((0,0,0))
        self.rect.center = (600,745)
    
class WestDoor(Door):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image.set_colorkey((0,0,0))
        self.rect.center = (55,400)

class EastDoor(Door):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image.set_colorkey((0,0,0))
        self.rect.center = (1145,400)