import pygame

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.image.load("assets/images/player.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() *4, self.image.get_height()*4))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (600, 400)

        self.mask = pygame.mask.from_surface(self.image)

        # Base Stats
        self.movement_speed = 7
        self.damage = 2
        self.shot_speed = 10
        self.shot_delay = 2
        self.max_health = 5
        self.current_health = self.max_health  

        # Movement variables
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        self.shoot_left = False
        self.shoot_right = False
        self.shoot_down = False
        self.shoot_up = False
        self.shot_frames = int(30/self.shot_delay)
        self.shot_counter = self.shot_frames
        self.collided = False
        self.targetable = True
        self.iframes = 45
        self.target_counter = self.iframes
        self.slow_speed = self.movement_speed/2
        self.normal_speed = self.movement_speed

        self.image_flipped = False

        # Bounding box from scene for movement
        self.movable_area = None

        self.new_shots = []

        # used for collision with obstacles
        self.prevent_up = False
        self.prevent_down = False
        self.prevent_left = False
        self.prevent_right = False

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
                    self.shoot_right = True
                elif event.key == pygame.K_LEFT:
                    self.shoot_left = True
                elif event.key == pygame.K_DOWN:
                    self.shoot_down = True
                elif event.key == pygame.K_UP:
                    self.shoot_up = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.move_up = False
                if event.key == pygame.K_a:
                    self.move_left = False
                if event.key == pygame.K_s:
                    self.move_down = False
                if event.key == pygame.K_d:
                    self.move_right = False
                elif event.key == pygame.K_RIGHT:
                    self.shoot_right = False
                elif event.key == pygame.K_LEFT:
                    self.shoot_left = False
                elif event.key == pygame.K_DOWN:
                    self.shoot_down = False
                elif event.key == pygame.K_UP:
                    self.shoot_up = False

    def update(self):
        # self.shot_delay += 0.1
        self.shot_frames = int(30/self.shot_delay)

        
        if self.move_up and not(self.prevent_up):
            self.rect.y -= self.movement_speed
        elif self.move_down and not(self.prevent_down):
            self.rect.y += self.movement_speed
        elif self.move_left and not(self.prevent_left):
            if not(self.image_flipped):
                
                self.image = pygame.transform.flip(self.image, True, False)
                self.image_flipped = True
            self.rect.x -= self.movement_speed
        elif self.move_right and not(self.prevent_right):
            if self.image_flipped:
                
                self.image = pygame.transform.flip(self.image, True, False)
                self.image_flipped = False
            self.rect.x += self.movement_speed
        # else:
        #     if self.move_up:
        #         self.rect.y += self.movement_speed*3
        #     elif self.move_down:
        #         self.rect.y -= self.movement_speed*3
        #     elif self.move_left:
        #         self.rect.x += self.movement_speed*3
        #     elif self.move_right:
        #         self.rect.x -= self.movement_speed*3
        
        # For iframes
        if self.target_counter < self.iframes:
            self.target_counter += 1    
        else:
            self.targetable = True
        # For shots
        if self.shoot_down or self.shoot_left or self.shoot_right or self.shoot_up:
            if self.shot_counter >= self.shot_frames:
                self.shot_counter = 0
                if self.shoot_down:
                    self.shoot("south")
                elif self.shoot_up:
                    self.shoot("north")
                elif self.shoot_left:
                    self.shoot("west")
                elif self.shoot_right:
                    self.shoot("east")
        if self.shot_counter < self.shot_frames:
            self.shot_counter += 1

        if self.movable_area != None:
            self.rect.clamp_ip(self.movable_area)
        
        

    def shoot(self, direction=None):
        shot = Shot(direction, self.damage, self.shot_speed, self)
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
        self.normal_speed = self.movement_speed
        self.slow_speed = self.movement_speed/2
        self.damage += stats["damage"]
        self.shot_speed += stats["shot_speed"]
        self.shot_delay += stats["shot_delay"]
        self.max_health += stats["max_health"]
        self.current_health += stats["current_health"]

        if self.movement_speed < 2:
            self.movement_speed = 2
            self.normal_speed = self.movement_speed
            self.slow_speed = self.movement_speed/2
        if self.damage < 1:
            self.damage = 1
        if self.shot_speed < 4:
            self.shot_speed = 4
        if self.shot_delay < 1:
            self.shot_delay = 1
        if self.max_health < 1:
            self.max_health = 1
        if self.current_health < 1:
            self.current_health = 1

        print([self.movement_speed,self.damage,self.shot_speed,self.shot_delay,self.max_health,self.current_health])

class Shot(pygame.sprite.Sprite):

    def __init__(self, direction, damage=0, shot_speed=0, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.shot_speed = shot_speed

        self.image = pygame.image.load("assets/images/spitball.png")
        
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        
        self.mask = pygame.mask.from_surface(self.image)

        # This is done for generic with type
        if player != None:
            self.rect.center = player.rect.center
            self.direction = direction

            if self.direction == "north":
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction == "south":
                self.image = pygame.transform.rotate(self.image, -90)
            elif self.direction == "west":
                self.image = pygame.transform.rotate(self.image, 180)
                if not(player.image_flipped):
                    player.image = pygame.transform.flip(player.image, True, False)
                    player.image_flipped = True
            elif self.direction == "east":
                if player.image_flipped:
                    player.image = pygame.transform.flip(player.image, True, False)
                    player.image_flipped = False

    def update(self):
        if self.direction == "north":
            self.rect.y -= self.shot_speed
        elif self.direction == "south":
            self.rect.y += self.shot_speed
        elif self.direction == "west":
            self.rect.x -= self.shot_speed
        elif self.direction == "east":
            self.rect.x += self.shot_speed

        if self.rect.x < 50 or self.rect.x > 1150 or self.rect.y < 50 or self.rect.y > 750:
            self.kill()