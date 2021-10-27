import pygame

class UI():
    # sprite for the Player
    def __init__(self, player):
        self.player = player

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(Arms())
        self.all_sprites.add(Text(str(self.player.damage),25,(255,255,255), 100, 100, 80, 150))
        self.all_sprites.add(Boots())
        self.all_sprites.add(Text(str(self.player.movement_speed),25,(255,255,255), 100, 100, 80, 200))
        self.all_sprites.add(Hourglass())
        self.all_sprites.add(Text(str(self.player.shot_delay),25,(255,255,255), 100, 100, 80, 250))
        self.all_sprites.add(Spitball())
        self.all_sprites.add(Text(str(self.player.shot_speed),25,(255,255,255), 100, 100, 80, 300))
        self.max_hp = self.player.max_health     
        self.curr_hp = self.player.current_health
        self.dmg = self.player.damage
        self.speed = self.player.movement_speed
        self.delay = self.player.shot_delay
        self.shot_speed = self.player.shot_speed

        for i in range(self.max_hp):
            if i < self.curr_hp:
                self.all_sprites.add(FullHeart(((30*i)+150),50))
            else:
                self.all_sprites.add(EmptyHeart((30*i)+150,50))
        
        
        
        
       

    def update(self):
        if self.player.current_health != self.curr_hp or self.player.max_health != self.max_hp or self.dmg != self.player.damage or self.speed != self.player.movement_speed or self.delay != self.player.shot_delay or self.shot_speed != self.player.shot_speed:
            self.updateGroup()
        
    def draw(self, screen):
        self.all_sprites.draw(screen)
        pass
    def updateGroup(self):
        self.all_sprites.empty()
        self.all_sprites.add(Arms())
        self.all_sprites.add(Text(str(self.player.damage),25,(255,255,255), 100, 100, 80, 150))
        self.all_sprites.add(Boots())
        self.all_sprites.add(Text(str(self.player.movement_speed),25,(255,255,255), 100, 100, 80, 200))
        self.all_sprites.add(Hourglass())
        self.all_sprites.add(Text(str(self.player.shot_delay),25,(255,255,255), 100, 100, 80, 250))
        self.all_sprites.add(Spitball())
        self.all_sprites.add(Text(str(self.player.shot_speed),25,(255,255,255), 100, 100, 80, 300))
        self.max_hp = self.player.max_health     
        self.curr_hp = self.player.current_health
        self.dmg = self.player.damage
        self.speed = self.player.movement_speed
        self.delay = self.player.shot_delay
        self.shot_speed = self.player.shot_speed

        for i in range(self.max_hp):
            if i < self.curr_hp:
                self.all_sprites.add(FullHeart(((30*i)+150),50))
            else:
                self.all_sprites.add(EmptyHeart((30*i)+150,50))

class FullHeart(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("assets/images/heart - full.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.02), int(self.image.get_height()*0.02)))
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)

class EmptyHeart(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("assets/images/heart.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.02), int(self.image.get_height()*0.02)))
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)

class Arms(pygame.sprite.Sprite):
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("assets/images/arms.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.03), int(self.image.get_height()*0.03)))

        self.rect = self.image.get_rect()
        self.rect.center = (40, 150)

class Boots(pygame.sprite.Sprite):
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("assets/images/boots - winged.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.03), int(self.image.get_height()*0.03)))

        self.rect = self.image.get_rect()
        self.rect.center = (40, 200)

class Hourglass(pygame.sprite.Sprite):
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("assets/images/hourglass.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.03), int(self.image.get_height()*0.03)))

        self.rect = self.image.get_rect()
        self.rect.center = (40, 250)

class Spitball(pygame.sprite.Sprite):
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("assets/images/spitball ui.png")

        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() *0.03), int(self.image.get_height()*0.03)))

        self.rect = self.image.get_rect()
        self.rect.center = (40, 300)

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height, posx, posy):
        # Call the parent class (Sprite) constructor  
        pygame.sprite.Sprite.__init__(self)
    
        self.font = pygame.font.SysFont("Arial", size)
        self.font.bold = True
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)