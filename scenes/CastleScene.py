import pygame
import random
from scenes.SceneBase import SceneBase
from helpers.player import Player
from helpers.item import Syringe, Bottle, Flask, ChocBar, Candy
from helpers.room import Room, TreatRoom

class CastleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # pass screen for dimensions
        self.screen = None

        # variables for scene
        self.bounding_box = 50

        # create bounding box
        self.walls = None

        self.rooms = None
        self.current_room = TreatRoom(self.player)
        self.current_room.screen = self.screen


        

    
    def ProcessInput(self, events, pressed_keys):
        self.player.ProcessInput(events, pressed_keys)
       
                
    
    def Update(self):
        self.all_sprites.update()
        self.current_room.update()
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