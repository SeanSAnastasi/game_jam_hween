import pygame
import random
from helpers.enemy import Alfredo, Bob, MuscleBoi, Plant, PomPom
from helpers.player import Player
from helpers.item import Syringe, Bottle, Flask, ChocBar, Candy
from helpers.room import BossRoom, Room, TreatRoom, TrickRoom
from helpers.ui import UI, Text

boss_list = [Plant, PomPom, MuscleBoi]
random.shuffle(boss_list)

class SceneBase:

    def __init__(self, background_img, background_music, next_scene, player, rooms):
        self.next = self
        self.all_sprites = pygame.sprite.Group()
        self.player = player
        # self.all_sprites.add(self.player)
        # print([self.player.movement_speed,self.player.damage,self.player.shot_speed,self.player.shot_delay,self.player.max_health,self.player.current_health])
        # pass screen for dimensions
        self.screen = None
        self.ui = UI(self.player)
        # variables for sce  
        self.bounding_box = 65

        # create bounding box
        self.walls = None

        self.rooms = None
        self.current_room = Room(self.player)
        self.current_room.screen = self.screen

        self.background_img = pygame.image.load(background_img)
        self.background_img = pygame.transform.scale(self.background_img, (1200,800))
        self.background_img.get_rect().center = (600, 400)

        self.next_scene = next_scene

        if background_music:
            pygame.mixer.init()
            pygame.mixer.music.load(background_music)
            pygame.mixer.music.play(-1)
            pass
    
    def ProcessInput(self, events, pressed_keys):
        self.player.ProcessInput(events, pressed_keys)
        
       
    def checkCollisions(self):
        hit = self.current_room.checkCollision()
        if hit:
            if hit == "next":
                self.SwitchToScene(self.next_scene(self.player))
            else:    
                self.current_room = hit
                
    
    def Update(self):
        
        self.checkCollisions()
        # Do this only after the screen has been passed
        if self.walls == None:
            self.walls = self.screen.get_rect()
            self.walls.w -= self.bounding_box*2
            self.walls.h -= self.bounding_box*2
            self.walls.center = self.screen.get_rect().center
            self.player.movable_area = self.walls

        if self.current_room.screen == None:
            self.current_room.screen = self.screen
        
        if self.player.current_health <= 0:
            self.SwitchToScene(End())
        
        self.current_room.update()
        self.all_sprites.update()
        self.ui.update()
    
    def Render(self, screen):
        
        screen.blit(self.background_img, (0,0))
        
        self.current_room.draw(screen)
        self.all_sprites.draw(screen)
        self.ui.draw(screen)

    def generateFloor(self, degredation):
        room_stack = [self.current_room] 
        room_types = [TreatRoom, TrickRoom]
        last_room = self.current_room
        room_chance = 1

        while len(room_stack) > 0:
            false_chance = 1-room_chance
            has_south = random.choices(population=[True, False], weights=[room_chance, false_chance], k=1)
            has_north = random.choices(population=[True, False], weights=[room_chance, 1-room_chance], k=1)
            has_east = random.choices(population=[True, False], weights=[room_chance, 1-room_chance], k=1)
            has_west = random.choices(population=[True, False], weights=[room_chance, 1-room_chance], k=1)

            print([has_north, has_south, has_east, has_west])
            
            if has_north[0] and last_room.north == None:
               
                room = random.choice(room_types)(self.player)
                last_room.setNorth(room)
                room_stack.append(room)
            if has_south[0] and last_room.south == None:      
                room = random.choice(room_types)(self.player)
                last_room.setSouth(room)
                room_stack.append(room)
            if has_east[0] and last_room.east == None:        
                room = random.choice(room_types)(self.player)
                last_room.setEast(room)
                room_stack.append(room)
            if has_west[0] and last_room.west == None:
                room = random.choice(room_types)(self.player)
                last_room.setWest(room)
                room_stack.append(room)

            room_stack.pop(0)
            room_chance -= degredation
            if room_chance <0:
                room_chance = 0
            if room_stack:
                last_room = room_stack[0]
           

        boss_directions = ["north", "south", "east", "west"]
        if last_room.north != None:
            boss_directions.remove("north")
        if last_room.south != None:
            boss_directions.remove("south")
        if last_room.east != None:
            boss_directions.remove("east")
        if last_room.west != None:
            boss_directions.remove("west")

        choice = random.choice(boss_directions)

        if choice == "north":
            last_room.setNorth(BossRoom(self.player, boss_list.pop()))
        elif choice == "south":
            last_room.setSouth(BossRoom(self.player, boss_list.pop()))
        elif choice == "east":
            last_room.setEast(BossRoom(self.player, boss_list.pop()))
        elif choice == "west":
            last_room.setWest(BossRoom(self.player, boss_list.pop()))

            
            
        
        # is_obstacle = random.choices(population=[True, False], weights=[0.3,0.7], k=10)
        

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)


class CastleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self, "assets/images/1st_floor.png", "assets/music/castle_song.wav", CaveScene, Player(), 1)
        self.generateFloor(0.1)
        

class CaveScene(SceneBase):
    def __init__(self, player):
        SceneBase.__init__(self, "assets/images/2nd_floor.png", "assets/music/cave_song.wav", DungeonScene, player, 10)
        self.generateFloor(0.05)

class DungeonScene(SceneBase):
    def __init__(self, player):
        SceneBase.__init__(self, "assets/images/3rd_floor.png", "assets/music/dungeon_song.wav", End, player, 20)
        self.generateFloor(0.005)

class End(SceneBase):
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(Text("Game Over", 50, (0,0,0), 1000, 1000, 600, 300))
        self.all_sprites.add(Text("Press space to start over", 50, (0,0,0), 1000, 1000, 600, 400))
        self.background_img = pygame.image.load("assets/images/1st_floor.png")
        self.background_img = pygame.transform.scale(self.background_img, (1200,800))
        self.background_img.get_rect().center = (600, 400)
        self.next = self
        pygame.mixer.init()
        pygame.mixer.music.load('assets/music/SynthTest.wav')
        pygame.mixer.music.play(-1)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.SwitchToScene(CastleScene())
        return

    def Update(self):
        self.all_sprites.update()
        return

    def Render(self, screen):
    
        screen.blit(self.background_img, (0,0))
        
        
        self.all_sprites.draw(screen)

class Start(SceneBase):
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(Text("Trick, Treat or Slay", 60, (0,0,0), 1000, 1000, 600, 300))
        self.all_sprites.add(Text("Press space to start game", 50, (0,0,0), 1000, 1000, 600, 400))
        self.background_img = pygame.image.load("assets/images/1st_floor.png")
        self.background_img = pygame.transform.scale(self.background_img, (1200,800))
        self.background_img.get_rect().center = (600, 400)
        self.next = self
        pygame.mixer.init()
        pygame.mixer.music.load('assets/music/SynthTest.wav')
        pygame.mixer.music.play(-1)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.SwitchToScene(CastleScene())
        return

    def Update(self):
        self.all_sprites.update()
        return

    def Render(self, screen):
    
        screen.blit(self.background_img, (0,0))
        
        
        self.all_sprites.draw(screen)
        