import pygame
import random

from pygame.event import get

from helpers.player import Player, Shot
from helpers.item import Syringe, Bottle, Flask, ChocBar, Candy
from helpers.door import Door, NorthDoor, SouthDoor, TrapDoor, WestDoor, EastDoor

class Room():
    def __init__(self, player):
        
        self.player_sprite_group = pygame.sprite.Group()
        self.enemy_sprite_group = pygame.sprite.Group()
        self.obstacle_sprite_group = pygame.sprite.Group()
        self.door_sprite_group = pygame.sprite.Group()
        self.sprite_groups = [self.player_sprite_group,self.enemy_sprite_group, self.obstacle_sprite_group, self.door_sprite_group]
        self.player = player
        self.player_sprite_group.add(self.player)

        # pass screen for dimensions
        self.screen = None

        # self.background = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) 
        

        # Places for other rooms
        self.north = None
        self.south = None
        self.west = None
        self.east = None
      

    def update(self):
        
        for all_sprites in self.sprite_groups:
            all_sprites.update()

        
        # add new shots to the sprite group
        for shot in self.player.get_new_shots():
            self.player_sprite_group.add(shot)
            self.player.clear_new_shots()

    def checkCollision(self):
        gets_hit = pygame.sprite.spritecollide(self.player, self.door_sprite_group, False)
        if gets_hit:
            for hit in gets_hit:
                if type(hit) == type(NorthDoor()):
                    self.player.move_player(None,600)
                    return self.north
                elif type(hit) == type(SouthDoor()):
                    self.player.move_player(None,200)
                    return self.south
                elif type(hit) == type(EastDoor()):
                    self.player.move_player(200,None)
                    return self.east
                elif type(hit) == type(WestDoor()):
                    self.player.move_player(1000,None)
                    return self.west
                elif type(hit) == type(TrapDoor()):
                    self.player.move_player(600,400)
                    return "next"

    def draw(self, screen):
        
        for all_sprites in self.sprite_groups:
            all_sprites.draw(screen)
        
    def getDoorSpriteGroup(self):
        return self.door_sprite_group
    def setNorth(self, north):
        self.north = north
        self.door_sprite_group.add(NorthDoor())
        north.south = self
        north.door_sprite_group.add(SouthDoor())
    def setSouth(self, south):
        self.south = south
        self.door_sprite_group.add(SouthDoor())
        south.north = self
        south.door_sprite_group.add(NorthDoor())
    def setEast(self, east):
        self.east = east
        self.door_sprite_group.add(EastDoor())
        east.west = self
        east.door_sprite_group.add(WestDoor())
    def setWest(self, west):
        self.west = west
        self.door_sprite_group.add(WestDoor())
        west.east = self
        west.door_sprite_group.add(EastDoor())
    
class TrickRoom(Room):
    def __init__(self, player):
        super(TrickRoom, self).__init__(player)


    def update(self):
        super().update()

    def draw(self, screen):
        super().draw(screen)

class TreatRoom(Room):
    def __init__(self, player):
        super(TreatRoom, self).__init__(player)
        self.item_sprite_group = pygame.sprite.Group()
        self.sprite_groups.append(self.item_sprite_group)
        self.item_list = [Syringe, Bottle, Flask, ChocBar, Candy]
        item = random.choice(self.item_list)
        self.item_sprite_group.add(item())

    def update(self):
        super(TreatRoom, self).update()
        self.checkCollisions()
        pass

    def draw(self, screen):
        super(TreatRoom, self).draw(screen)
        pass

    def checkCollisions(self):
        gets_hit = pygame.sprite.spritecollide(self.player, self.item_sprite_group, True)

        for item in gets_hit:
            self.player.updateStats(item.get_change())

class BossRoom(Room):
    def __init__(self, player):
        super().__init__(player)
        self.killBoss()
        
    def killBoss(self):
        self.door_sprite_group.add(TrapDoor())