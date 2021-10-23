import pygame
import random
from scenes.SceneBase import SceneBase
from helpers.player import Player
from helpers.item import Syringe, Bottle, Flask, ChocBar, Candy
from helpers.room import Room, TreatRoom, TrickRoom

class CaveScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # pass screen for dimensions
        self.screen = None

        # variables for sce  
        self.bounding_box = 100

        # create bounding box
        self.walls = None

        self.rooms = None
        self.current_room = Room(self.player)
        self.current_room.screen = self.screen

        # Placeholder before map generation
        self.room1 = TrickRoom(self.player)
        self.room2 = TreatRoom(self.player)
        self.room3 = TrickRoom(self.player)
        self.room4 = TrickRoom(self.player)
        self.room5 = TreatRoom(self.player)

        self.room1.setSouth(self.room2)
        self.room2.setEast(self.room3)
        self.room4.setNorth(self.room5)
        self.current_room.setEast(self.room1)
        self.current_room.setSouth(self.room4)

        

    
    def ProcessInput(self, events, pressed_keys):
        self.player.ProcessInput(events, pressed_keys)

        
       
    def checkCollisions(self):
        hit = self.current_room.checkCollision()
        if hit:
            self.current_room = hit
                
    
    def Update(self):
        self.all_sprites.update()
        self.current_room.update()
        self.checkCollisions()
        # Do this only after the screen has been passed
        if self.walls == None:
            self.walls = self.screen.get_rect()
            self.walls.w -= self.bounding_box*2
            self.walls.h -= self.bounding_box*2
            self.walls.center = self.screen.get_rect().center
            self.player.movable_area = self.walls

        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 0, 0))
        self.all_sprites.draw(screen)
        self.current_room.draw(screen)

    def generateFloor():
        pass