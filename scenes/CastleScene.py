import pygame
from scenes.SceneBase import SceneBase
from helpers.player import Player

class CastleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # variables for scene
        self.bounding_box = 50
        self.display_width = 0
        self.display_height = 0

        # create bounding box
        self.walls = []
        

    
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
        pass
    
    def Render(self, screen):
        self.display_width, self.display_height = screen.get_size()

        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 0, 0))
        self.all_sprites.draw(screen)