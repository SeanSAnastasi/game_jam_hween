import pygame
import random
from scenes.SceneBase import SceneBase
from helpers.player import Player, Shot
from helpers.item import Syringe, Bottle, Flask, ChocBar, Candy

class Room(SceneBase):
    def __init__(self, player):
        SceneBase.__init__(self)
        self.player_sprite_group = pygame.sprite.Group()
        self.enemy_sprite_group = pygame.sprite.Group()
        self.obstacle_sprite_group = pygame.sprite.Group()
        self.sprite_groups = [self.player_sprite_group,self.enemy_sprite_group, self.obstacle_sprite_group]
        self.player = player
        self.player_sprite_group.add(self.player)

        # pass screen for dimensions
        self.screen = None

        # variables for scene
        self.bounding_box = 50

        # create bounding box
        self.walls = None

        self.background = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) 


    def update(self):
        for all_sprites in self.sprite_groups:
            all_sprites.update()
        # Do this only after the screen has been passed
        if self.walls == None and self.screen != None:
            self.walls = self.screen.get_rect()
            self.walls.w -= self.bounding_box*2
            self.walls.h -= self.bounding_box*2
            self.walls.center = self.screen.get_rect().center
            self.player.movable_area = self.walls

        # add new shots to the sprite group
        

        for shot in self.player.get_new_shots():
            self.player_sprite_group.add(shot)
            self.player.clear_new_shots()

        
        pass

    def draw(self, screen):
        screen.fill(self.background)
        for all_sprites in self.sprite_groups:
            all_sprites.draw(screen)
        pass
    
    def checkCollisions(self):
        pass
    
class TrickRoom():
    def __init__(self, player):

        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class TreatRoom(Room):
    def __init__(self, player):
        super(TreatRoom, self).__init__(player)
        self.item_sprite_group = pygame.sprite.Group()
        self.sprite_groups.append(self.item_sprite_group)
        self.item_list = [Syringe, Bottle, Flask, ChocBar, Candy]
        item = random.choice(self.item_list)
        self.item_sprite_group.add(item())

        # Places for other rooms
        self.north = None
        self.south = None
        self.west = None
        self.east = None

    def update(self):
        super().update()
        self.checkCollisions()
        pass

    def draw(self, screen):
        super().draw(screen)
        pass

    def checkCollisions(self):
        super().checkCollisions()
        gets_hit = pygame.sprite.spritecollide(self.player, self.item_sprite_group, True)

        for item in gets_hit:
            self.player.updateStats(item.get_change())

    