import pygame

class Enemy(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, image, x, y, multiplier):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        if not(image):
            print("not")
            self.image = pygame.Surface((50, 50))
            self.image.fill((200,20,40))
        else:
            print("img")
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (self.image.get_width() *multiplier, self.image.get_height()*multiplier))
            self.image.set_colorkey((0,0,0))
        

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (x, y)


        self.max_health = 6
        self.current_health = self.max_health

        # Bounding box from scene for movement
        self.movable_area = None

        self.new_shots = []

    def update(self):
        pass

    def takeDamage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.kill()
        pass

class Draugr(Enemy):
    def __init__(self):
        super().__init__("assets/images/draugr.png", 600, 400, 2)

class Ghost(Enemy):
    def __init__(self):
        super().__init__("assets/images/ghost.png", 600, 400, 2)

class Golem(Enemy):
    def __init__(self):
        super().__init__("assets/images/golem.png", 600, 400, 2)

class Spider(Enemy):
    def __init__(self):
        super().__init__("assets/images/spider.png", 600, 400, 2)

class MuscleBoi(Enemy):
    def __init__(self):
        super().__init__("assets/images/muscle_boi.png", 600, 400, 1)
        self.max_health = 35
        self.current_health = self.max_health

class Alfredo(Enemy):
    def __init__(self):
        super().__init__("assets/images/alfredo.png", 600, 400, 1)
        self.max_health = 20
        self.current_health = self.max_health

class Bob(Enemy):
    def __init__(self):
        super().__init__("assets/images/bob.png", 600, 400, 2)
        self.max_health = 25
        self.current_health = self.max_health

class Plant(Enemy):
    def __init__(self):
        super().__init__("assets/images/plant.png", 600, 400, 1)
        self.max_health = 30
        self.current_health = self.max_health