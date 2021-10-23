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
        self.rect.center = (600, 400)

        # Movement variables
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False

        # Base Stats
        self.movement_speed = 5
        self.damage = 1
        self.shot_speed = 10
        self.shot_delay = 2
        self.max_health = 5
        self.current_health = self.max_health

        # Bounding box from scene for movement
        self.movable_area = None

        self.new_shots = []

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_up = True
                elif event.key == pygame.K_a:
                    self.move_left = True
                elif event.key == pygame.K_s:
                    self.move_down = True
                elif event.key == pygame.K_d:
                    self.move_right = True
                elif event.key == pygame.K_RIGHT:
                    self.shoot()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.move_up = False
                if event.key == pygame.K_a:
                    self.move_left = False
                if event.key == pygame.K_s:
                    self.move_down = False
                if event.key == pygame.K_d:
                    self.move_right = False

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

    def shoot(self, direction=None):
        shot = Shot(self.damage, self.shot_speed, self)
        self.new_shots.append(shot)
    
    def get_new_shots(self):
        return self.new_shots
    
    def clear_new_shots(self):
        self.new_shots = []

    def move_player(self, x, y):
        move_x = x
        move_y = y
        if x == None:
            move_x = self.rect.x
        if y == None:
            move_y = self.rect.y

        self.rect.x = move_x
        self.rect.y = move_y

    def updateStats(self, stats):
        self.movement_speed += stats["movement_speed"]
        self.damage += stats["damage"]
        self.shot_speed += stats["shot_speed"]
        self.shot_delay += stats["shot_delay"]
        self.max_health += stats["max_health"]
        self.current_health += stats["current_health"]

        print([self.movement_speed,self.damage,self.shot_speed,self.shot_delay,self.max_health,self.current_health])

class Shot(pygame.sprite.Sprite):

    def __init__(self, damage=0, shot_speed=0, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.shot_speed = shot_speed

        self.image = pygame.Surface((15, 15))
        self.image.fill((255,255,255))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen

        # This is done for generic with type
        if player != None:
            self.rect.center = player.rect.center

    def update(self):
        self.rect.x += self.shot_speed