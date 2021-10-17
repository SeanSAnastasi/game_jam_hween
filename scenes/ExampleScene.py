import pygame
from scenes.SceneBase import SceneBase

#--------------------------------------------------------------------------
# THIS IS NOT MEANT TO BE USED IN GAME BUT COPIED INTO THE GAME
#-------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.Surface((50, 50))
        self.image.fill((0,0,0))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (0, 0)

    def update(self):
        # any code here will happen every time the game loop updates
        self.rect.x -= 5
        if self.rect.left < 0:
            self.rect.left = 0

class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.all_sprites = pygame.sprite.Group()
        player = Player()
        self.all_sprites.add(player)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                # self.SwitchToScene(GameScene()) - This is an example of the code used
                pass
    
    def Update(self):
        self.all_sprites.update()
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 0, 0))
        self.all_sprites.draw(screen)