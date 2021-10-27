import pygame
import math
import random


class Enemy(pygame.sprite.Sprite):
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
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *multiplier), int(self.image.get_height()*multiplier)))
            self.image.set_colorkey((0,0,0))
        

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (x, y)

        self.mask = pygame.mask.from_surface(self.image)

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
    
    def draw(screen):
        super().draw(screen)

class Draugr(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/draugr.png", random.randint(200, 1000), random.randint(200, 600), 3)
        self.player = player
        self.speed = 5

    def update(self):
         # Find direction vector (dx, dy) between enemy and player.
        dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        try:
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        except:
            print("under you")

class Ghost(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/ghost.png", random.randint(200, 1000), random.randint(200, 600), 3)
        self.player = player
        self.speed = 6
        self.back_speed = 4
        self.stop_time = random.randint(20,30)
        self.start_time =  random.randint(30,40)
        self.stop_timer = 0
        self.start_timer = 0


    def update(self):
        if self.stop_timer >= self.stop_time:
            # Find direction vector (dx, dy) between enemy and player.
            dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            try:
                dx, dy = dx / dist, dy / dist  # Normalize.
                # Move along this normalized vector towards the player at current speed.
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
                
            except:
                print("under you")
            self.start_timer += 1
            if self.start_timer >= self.start_time:
                self.stop_timer = 0 
        else:
            dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            try:
                dx, dy = dx / dist, dy / dist  # Normalize.
                # Move along this normalized vector towards the player at current speed.
                self.rect.x -= dx * self.back_speed
                self.rect.y += dy * self.back_speed
            except:
                print("under you")
            self.start_timer += 1
            self.start_timer = 0
            self.stop_timer += 1
            

class Golem(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/golem.png", random.randint(200, 1000), random.randint(200, 600), 2)
        self.player = player
        self.speed = 3
        self.circle_time = 60
        self.circle_timer = 0
        self.circle_radius = 20
        self.max_circle_radius = 200
        self.screen = None
        self.circle_pos_x = -1
        self.circle_pos_y = -1


    def update(self):
        # pygame.draw.circle(self.screen, (255, 20, 0), (600, 400), 20, 2)
         # Find direction vector (dx, dy) between enemy and player.
        dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        try:
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        except:
            print("under you")
        if self.screen:
            
            if self.circle_timer >= self.circle_time:
                self.speed = 0
                # if self.circle_pos_x == -1:
                #     self.circle_pos_x = self.rect.center[0]
                # if self.circle_pos_y == -1:
                #     self.circle_pos_y = self.rect.center[1]
                self.circle_radius += 5
                if self.circle_radius >= self.max_circle_radius:
                    self.circle_timer = 0
            else:
                # print("nocircle")
                self.circle_timer += 1
                self.circle_radius = 20
                # self.circle_pos_x = -1
                # self.circle_pos_y = -1
                self.speed = 3
 


class Spider(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/spider.png", random.randint(200, 1000), random.randint(200, 600), 1)

        self.player = player
        self.speed = 20
        self.stop_time = 40
        self.start_time = random.randint(6, 12)
        self.stop_timer = 0
        self.start_timer = 0


    def update(self):
        if self.stop_timer >= self.stop_time:
            # Find direction vector (dx, dy) between enemy and player.
            dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            try:
                dx, dy = dx / dist, dy / dist  # Normalize.
                # Move along this normalized vector towards the player at current speed.
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            except:
                print("under you")
            self.start_timer += 1

            if self.start_timer >= self.start_time:
                self.stop_timer = 0 
        else:
            self.start_timer = 0
            self.stop_timer += 1

class MuscleBoi(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/muscle_boi.png", 600, 400, 1)
        self.max_health = 35
        self.current_health = self.max_health

class Alfredo(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/alfredo.png", 600, 400, 1)
        self.max_health = 20
        self.current_health = self.max_health

class Bob(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/bob.png", 600, 400, 2)
        self.max_health = 25
        self.current_health = self.max_health

class Plant(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/plant.png", 600, 400, 1)
        self.max_health = 30
        self.current_health = self.max_health