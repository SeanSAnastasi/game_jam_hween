import pygame
from scenes.scenes import CastleScene, Start

def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Trick, Treat or Slay')
    image = pygame.image.load("assets/images/player.png")
    pygame.display.set_icon(image)
    active_scene = starting_scene()

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
                
        active_scene.screen = screen
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(fps)

# Change parameters here for different screen sizes, FPS and starting scenes
run_game(1200, 800, 30, Start)