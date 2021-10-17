import pygame
from scenes.SceneBase import SceneBase
from helpers.player import Player

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
        

    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.move_up = True
                elif event.key == pygame.K_a:
                    self.player.move_left = True
                elif event.key == pygame.K_s:
                    self.player.move_down = True
                elif event.key == pygame.K_d:
                    self.player.move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.move_up = False
                if event.key == pygame.K_a:
                    self.player.move_left = False
                if event.key == pygame.K_s:
                    self.player.move_down = False
                if event.key == pygame.K_d:
                    self.player.move_right = False
                # Move to the next scene when the user pressed Enter
                # self.SwitchToScene(GameScene()) - This is an example of the code used
                pass
    
    def Update(self):
        self.all_sprites.update()
        
        # Do this only after the screen has been passed
        if self.walls == None:
            self.walls = self.screen.get_rect()
            self.walls.w -= self.bounding_box*2
            self.walls.h -= self.bounding_box*2
            print(self.walls)
            self.walls.center = self.screen.get_rect().center
            self.player.movable_area = self.walls

        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 0, 0))
        self.all_sprites.draw(screen)