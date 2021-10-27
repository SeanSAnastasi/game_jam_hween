import pygame
import math
import random
import os


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
        self.frame = 0
        self.frame_swap_at = 4
        self.frame_swap_counter = 0


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
                file_num = str(self.frame % 4)
                while len(file_num) < 4:
                    file_num = "0"+file_num
                file = "assets/animations/ghost-move/ghost-move"+file_num+".png"
                print(file)
                if os.path.exists(file) and self.speed >0:
                    
                    center = self.rect.center
                    self.image = pygame.image.load(file)
                    if center[0] > self.player.rect.x:
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *3), int(self.image.get_height()*3)))
                    self.image.set_colorkey((0,0,0))
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.mask = pygame.mask.from_surface(self.image)
                    self.frame_swap_counter += 1
                    if self.frame_swap_counter >= self.frame_swap_at:
                        self.frame += 1
                        self.frame_swap_counter = 0
                
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
        self.frame = 0
        self.frame_swap_at = 4
        self.frame_swap_counter = 0

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
            file_num = str(self.frame % 4)
            while len(file_num) < 4:
                file_num = "0"+file_num
            file = "assets/animations/golem-walk/golem-walk"+file_num+".png"
            print(file)
            if os.path.exists(file) and self.speed >0:
                
                center = self.rect.center
                self.image = pygame.image.load(file)
                if center[0] < self.player.rect.x:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *2), int(self.image.get_height()*2)))
                self.image.set_colorkey((255,255,255))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
                self.frame_swap_counter += 1
                if self.frame_swap_counter >= self.frame_swap_at:
                    self.frame += 1
                    self.frame_swap_counter = 0
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
        self.player = player
        self.circle_time = 60
        self.circle_timer = 0
        self.circle_radius = 20
        self.max_circle_radius = 200
        self.screen = None
        self.circle_pos_x = -1
        self.circle_pos_y = -1
        self.atk = None
        self.frame = 0
    def update(self):
        if self.atk == None:
            dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            try:
                dx, dy = dx / dist, dy / dist  # Normalize.
                # Move along this normalized vector towards the player at current speed.
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            except:
                print("under you")
            
                
            if self.circle_timer >= self.circle_time:
                self.speed = 0
                self.atk = random.randint(1,3)
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
        elif self.atk == 1:
            self.charge(str(self.frame))
            self.frame += 1
        elif self.atk == 2:
            self.attack(str(self.frame))
            self.frame += 1
        elif self.atk == 3:
            self.swirl(str(self.frame))
            self.frame += 1

    def charge(self, frame):
        file_num = frame
        while len(file_num) < 4:
            file_num = "0"+file_num
        file = "assets/animations/ghost - 1 arm charge/frame"+file_num+".png"
        if os.path.exists(file):
            print(file)
            center = self.rect.center
            self.image = pygame.image.load(file)
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        else:
            print(file)
            self.atk = None
            self.frame = 0
            self.circle_timer = 0
            # self.circle_pos_x = -1
            # self.circle_pos_y = -1
            self.speed = 3
            center = self.rect.center
            self.image = pygame.image.load("assets/images/muscle_boi.png")
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
    def attack(self, frame):
        file_num = frame
        while len(file_num) < 4:
            file_num = "0"+file_num
        file = "assets/animations/ghost - 2 arms attack/frame"+file_num+".png"
        if os.path.exists(file):
            print(file)
            center = self.rect.center
            self.image = pygame.image.load(file)
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        else:
            print(file)
            self.atk = None
            self.frame = 0
            self.circle_timer = 0
            # self.circle_pos_x = -1
            # self.circle_pos_y = -1
            self.speed = 3
            center = self.rect.center
            self.image = pygame.image.load("assets/images/muscle_boi.png")
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
    def swirl(self, frame):
        file_num = frame
        while len(file_num) < 4:
            file_num = "0"+file_num
        file = "assets/animations/ghost - swirl attack/frame"+file_num+".png"
        if os.path.exists(file):
            print(file)
            center = self.rect.center
            self.image = pygame.image.load(file)
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        else:
            print(file)
            self.atk = None
            self.frame = 0
            self.circle_timer = 0
            # self.circle_pos_x = -1
            # self.circle_pos_y = -1
            self.speed = 3
            center = self.rect.center
            self.image = pygame.image.load("assets/images/muscle_boi.png")
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)


class Alfredo(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/alfredo.png", 600, 400, 1)
        self.max_health = 20
        self.current_health = self.max_health
        self.circle_time = 60
        self.circle_timer = 0
        self.circle_radius = 20
        self.max_circle_radius = 200
        self.screen = None
        self.circle_pos_x = -1
        self.circle_pos_y = -1

class Bob(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/bob.png", 600, 400, 2)
        self.max_health = 25
        self.current_health = self.max_health

class Plant(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/plant.png", 600, 400, 0.8)
        self.max_health = 30
        self.current_health = self.max_health
        self.player = player
        self.circle_time = 60
        self.circle_timer = 0
        self.circle_radius = 20
        self.max_circle_radius = 200
        self.screen = None
        self.circle_pos_x = -1
        self.circle_pos_y = -1
        self.atk = None
        self.frame = 0
        self.transformed = False
    def update(self):
        print(self.transformed)
        if self.atk == None:
            dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            try:
                dx, dy = dx / dist, dy / dist  # Normalize.
                # Move along this normalized vector towards the player at current speed.
                # self.rect.x += dx * self.speed
                # self.rect.y += dy * self.speed
            except:
                print("under you")
            
                
            if self.circle_timer >= self.circle_time:
                self.speed = 0
                self.atk = random.randint(1,5)
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
        elif self.atk == 1:
            self.boom(str(self.frame))
            self.frame += 1
        elif self.atk == 2:
            self.berry(str(self.frame))
            self.frame += 1
        elif self.atk == 3:
            self.transformation(str(self.frame))
            self.frame += 1
        elif self.atk == 4:
            self.flash(str(self.frame))
            self.frame += 1
        elif self.atk == 5:
            self.superboom(str(self.frame))
            self.frame += 1
        

    def boom(self, frame):
        if self.transformed:
            file_num = frame
            while len(file_num) < 4:
                file_num = "0"+file_num
            file = "assets/animations/plant - boomboom/frame"+file_num+".png"
            if os.path.exists(file):
                print(file)
                center = self.rect.center
                self.image = pygame.image.load(file)
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
            else:
                print(file)
                self.atk = None
                self.frame = 0
                self.circle_timer = 0
                # self.circle_pos_x = -1
                # self.circle_pos_y = -1
                self.speed = 3
                center = self.rect.center
                self.image = pygame.image.load("assets/images/plant_angry.png")
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
        else:
            self.atk = None
            self.frame = 0

    def berry(self, frame):
        if not(self.transformed):
            file_num = frame
            while len(file_num) < 4:
                file_num = "0"+file_num
            file = "assets/animations/plant - red berry attack/frame"+file_num+".png"
            if os.path.exists(file):
                print(file)
                center = self.rect.center
                self.image = pygame.image.load(file)
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
            else:
                print(file)
                self.atk = None
                self.frame = 0
                self.circle_timer = 0
                # self.circle_pos_x = -1
                # self.circle_pos_y = -1
                self.speed = 3
                center = self.rect.center
                self.image = pygame.image.load("assets/images/plant.png")
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
        else:
            self.atk = None
            self.frame = 0
            
    def transformation(self, frame):
        if not(self.transformed):
            
            file_num = frame
            while len(file_num) < 4:
                file_num = "0"+file_num
            file = "assets/animations/plant - transformation/frame"+file_num+".png"
            if os.path.exists(file):
                print(file)
                center = self.rect.center
                self.image = pygame.image.load(file)
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
            else:
                print(file)
                self.atk = None
                self.frame = 0
                self.circle_timer = 0
                # self.circle_pos_x = -1
                # self.circle_pos_y = -1
                self.speed = 3
                center = self.rect.center
                self.image = pygame.image.load("assets/images/plant_angry.png")
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
                self.transformed = True
        else:
            self.atk = None
            self.frame = 0

    def flash(self, frame):
        if self.transformed:
            self.transformed = True
            file_num = frame
            while len(file_num) < 4:
                file_num = "0"+file_num
            file = "assets/animations/plant - white flash/frame"+file_num+".png"
            if os.path.exists(file):
                print(file)
                center = self.rect.center
                self.image = pygame.image.load(file)
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
            else:
                print(file)
                self.atk = None
                self.frame = 0
                self.circle_timer = 0
                # self.circle_pos_x = -1
                # self.circle_pos_y = -1
                self.speed = 3
                center = self.rect.center
                self.image = pygame.image.load("assets/images/plant_angry.png")
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
        else:
            self.atk = None
            self.frame = 0
            
    def superboom(self, frame):
        if self.transformed:
            file_num = frame
            while len(file_num) < 4:
                file_num = "0"+file_num
            file = "assets/animations/plant- supermegaboomboom/frame"+file_num+".png"
            if os.path.exists(file):
                print(file)
                center = self.rect.center
                self.image = pygame.image.load(file)
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
            else:
                print(file)
                self.atk = None
                self.frame = 0
                self.circle_timer = 0
                # self.circle_pos_x = -1
                # self.circle_pos_y = -1
                self.speed = 3
                center = self.rect.center
                self.image = pygame.image.load("assets/images/plant_angry.png")
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.8), int(self.image.get_height()*0.8)))
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pygame.mask.from_surface(self.image)
        else:
            self.atk = None
            self.frame = 0
            

    

class PomPom(Enemy):
    def __init__(self, player):
        super().__init__("assets/images/pompom.png", 600, 400, 1)
        self.max_health = 30
        self.current_health = self.max_health
        self.player = player
        self.circle_time = 60
        self.circle_timer = 0
        self.circle_radius = 20
        self.max_circle_radius = 200
        self.screen = None
        self.circle_pos_x = -1
        self.circle_pos_y = -1
        self.atk = None
        self.frame = 0
    def update(self):
        # pygame.draw.circle(self.screen, (255, 20, 0), (600, 400), 20, 2)
         # Find direction vector (dx, dy) between enemy and player.
        if self.atk == None:
            dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            try:
                dx, dy = dx / dist, dy / dist  # Normalize.
                # Move along this normalized vector towards the player at current speed.
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            except:
                print("under you")
            
                
            if self.circle_timer >= self.circle_time:
                self.speed = 0
                self.atk = random.randint(1,3)
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
        elif self.atk == 1:
            self.kick_swirl(str(self.frame))
            self.frame += 1
        elif self.atk == 2:
            self.laser_beam(str(self.frame))
            self.frame += 1
        elif self.atk == 3:
            self.pink_throw(str(self.frame))
            self.frame += 1
        

    def kick_swirl(self, frame):
        file_num = frame
        while len(file_num) < 4:
            file_num = "0"+file_num
        file = "assets/animations/pompom - kick swirl/frame"+file_num+".png"
        if os.path.exists(file):
            print(file)
            center = self.rect.center
            self.image = pygame.image.load(file)
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        else:
            print(file)
            self.atk = None
            self.frame = 0
            self.circle_timer = 0
            # self.circle_pos_x = -1
            # self.circle_pos_y = -1
            self.speed = 3
            center = self.rect.center
            self.image = pygame.image.load("assets/images/pompom.png")
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        
    def laser_beam(self, frame):
        file_num = frame
        while len(file_num) < 4:
            file_num = "0"+file_num
        file = "assets/animations/pompom - laser beam/frame"+file_num+".png"
        if os.path.exists(file):
            print(file)
            center = self.rect.center
            self.image = pygame.image.load(file)
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        else:
            print(file)
            self.atk = None
            self.frame = 0
            self.circle_timer = 0
            # self.circle_pos_x = -1
            # self.circle_pos_y = -1
            self.speed = 3
            center = self.rect.center
            self.image = pygame.image.load("assets/images/pompom.png")
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
    def pink_throw(self, frame):
        file_num = frame
        while len(file_num) < 4:
            file_num = "0"+file_num
        file = "assets/animations/pompom - pink throw/frame"+file_num+".png"
        if os.path.exists(file):
            # print(self.img)
            center = self.rect.center
            self.image = pygame.image.load(file)
            # print(center[0])
            # print()
            if center[0] < self.player.rect.x:
                self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
            # print(self.img)
        else:
            print(file)
            self.atk = None
            self.frame = 0
            self.circle_timer = 0
            # self.circle_pos_x = -1
            # self.circle_pos_y = -1
            self.speed = 3
            center = self.rect.center
            self.image = pygame.image.load("assets/images/pompom.png")
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *1), int(self.image.get_height()*1)))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
