import pygame
import random

from pygame.event import get
from helpers.obstacle import Bonepile, Chest, Gravestone, Rock, Web

from helpers.player import Player, Shot
from helpers.item import Syringe, Bottle, Flask, ChocBar, Candy
from helpers.door import Door, NorthDoor, SouthDoor, TrapDoor, WestDoor, EastDoor
from helpers.enemy import Alfredo, MuscleBoi, Plant, PomPom, Spider, Draugr, Ghost, Golem, Bob
from helpers.ui import FullHeart

class Room():
    def __init__(self, player):
        
        self.player_sprite_group = pygame.sprite.Group()
        self.enemy_sprite_group = pygame.sprite.Group()
        self.obstacle_sprite_group = pygame.sprite.Group()
        self.door_sprite_group = pygame.sprite.Group()
        self.shot_sprite_group = pygame.sprite.Group()
        self.sprite_groups = [self.obstacle_sprite_group, self.door_sprite_group, self.shot_sprite_group,self.player_sprite_group, self.enemy_sprite_group]
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

        self.enemy_sprite_group.add(MuscleBoi(self.player))

    def update(self):
        
        

        
        # add new shots to the sprite group
        for shot in self.player.get_new_shots():
            self.shot_sprite_group.add(shot)
            self.player.clear_new_shots()

        # Update screen for enemy where applicable
        # print(self.screen)
        for enemy in self.enemy_sprite_group:
            if type(enemy) == type(Golem(self.player)) and self.screen:
                enemy.screen = self.screen
                pygame.draw.circle(self.screen, (255, 20, 0), (600, 400), 20, 2)
                # if enemy.circle_timer >= enemy.circle_time:
                #     pygame.draw.circle(self.screen, (255, 20, 0), (enemy.rect.x, enemy.rect.y), enemy.circle_radius, 2)

        for all_sprites in self.sprite_groups:
            all_sprites.update()

    def checkCollision(self):
        
        gets_hit = pygame.sprite.spritecollide(self.player, self.door_sprite_group, False, pygame.sprite.collide_mask)
        if gets_hit and not(self.enemy_sprite_group):
            self.player.target_counter = 0
            self.shot_sprite_group.empty()
            for hit in gets_hit:
                if type(hit) == type(NorthDoor()):
                    self.player.move_player(None,580)
                    return self.north
                elif type(hit) == type(SouthDoor()):
                    self.player.move_player(None,120)
                    return self.south
                elif type(hit) == type(EastDoor()):
                    self.player.move_player(80,None)
                    return self.east
                elif type(hit) == type(WestDoor()):
                    self.player.move_player(1000,None)
                    return self.west
                elif type(hit) == type(TrapDoor()):
                    self.player.move_player(600,400)
                    return "next"
            
        
        for enemy in self.enemy_sprite_group:

            gets_hit = pygame.sprite.spritecollide(enemy, self.shot_sprite_group, True, pygame.sprite.collide_mask)

            if gets_hit:
                enemy.takeDamage(gets_hit[0].damage)

            gets_hit = pygame.sprite.spritecollide(enemy, self.player_sprite_group, False, pygame.sprite.collide_mask)

            if gets_hit:
                gets_hit[0].collided = True
                if gets_hit[0].target_counter == self.player.iframes:            
                    gets_hit[0].current_health -= 1
                    gets_hit[0].targetable = False
                    gets_hit[0].target_counter = 0
                    
                    direction = self.determineSide(self.player.rect, gets_hit[0].rect)
                    if direction == "top":
                        self.player.prevent_up = True
                    elif direction == "bottom":
                        self.player.prevent_down = True
                    elif direction == "left":
                        self.player.prevent_left = True
                    elif direction == "right":
                        self.player.prevent_right = True
                
                    # print(self.player.current_health)
            else:
                self.player.collided = False
                self.player.prevent_up = False
                self.player.prevent_down = False
                self.player.prevent_left = False
                self.player.prevent_right = False
                self.player.movement_speed = self.player.normal_speed
        
        for obstacle in self.obstacle_sprite_group:
            gets_hit = pygame.sprite.spritecollide(obstacle, self.shot_sprite_group, False, pygame.sprite.collide_mask)

            if gets_hit:
                if type(gets_hit[0]) != type(Web(0,0)):
                    gets_hit[0].kill()

        gets_hit = pygame.sprite.spritecollide(self.player, self.obstacle_sprite_group, False, pygame.sprite.collide_mask)

        if gets_hit:
            
            if type(gets_hit[0]) != type(Web(0,0)):
                direction = self.determineSide(self.player.rect, gets_hit[0].rect)
                if direction == "top":
                    self.player.prevent_up = True
                elif direction == "bottom":
                    self.player.prevent_down = True
                elif direction == "left":
                    self.player.prevent_left = True
                elif direction == "right":
                    self.player.prevent_right = True

                if type(gets_hit[0]) == type(Chest(0,0)):
                    if not(gets_hit[0].open):
                        gets_hit[0].openChest()
                        # print(gets_hit[0].getPosition()[0])
                        self.obstacle_sprite_group.add(FullHeart(gets_hit[0].getPosition()[0] + 50, gets_hit[0].getPosition()[1] - 50))
                if type(gets_hit[0]) == type(FullHeart(0,0)):
                    if self.player.current_health < self.player.max_health:
                        gets_hit[0].kill()
                        self.player.current_health += 1
                        return
            elif type(gets_hit[0]) == type(Web(0,0)):
                self.player.prevent_up = False
                self.player.prevent_down = False
                self.player.prevent_left = False
                self.player.prevent_right = False
                self.player.movement_speed = self.player.slow_speed
        else:
            self.player.prevent_up = False
            self.player.prevent_down = False
            self.player.prevent_left = False
            self.player.prevent_right = False
            self.player.movement_speed = self.player.normal_speed

    def draw(self, screen):
        
        for all_sprites in self.sprite_groups:
            all_sprites.draw(screen)

        # for enemy in self.enemy_sprite_group:
        #     if type(enemy) == type(Golem(self.player)) and self.screen:
        #         if enemy.circle_timer >= enemy.circle_time:
        #             pygame.draw.circle(self.screen, (255, 20, 0), (enemy.circle_pos_x, enemy.circle_pos_y), enemy.circle_radius, 2)
        
        
        
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
    
    def determineSide(self,rect1, rect2):
        if rect1.midtop[1] > rect2.midtop[1]:
            return "top"
        elif rect1.midleft[0] > rect2.midleft[0]:
            return "left"
        elif rect1.midright[0] < rect2.midright[0]:
            return "right"
        else:
            return "bottom"

class TrickRoom(Room):
    def __init__(self, player):
        super(TrickRoom, self).__init__(player)
        enemy_list = [Draugr, Golem, Ghost, Spider]
        number_of_enemies = [4, 3, 5, 10]
        enemy = random.choice(enemy_list)
        for i in range(random.randint(1, number_of_enemies[enemy_list.index(enemy)])):          
                self.enemy_sprite_group.add(enemy(player))
            
        # Add random obstacles max 10
        is_obstacle = random.choices(population=[True, False], weights=[0.3,0.7], k=10)
        for i in is_obstacle:
            if i:
                self.obstacle_list = [Rock, Web, Bonepile, Chest, Gravestone]
                self.obstacle_list_weights = [0.3,0.2,0.3,0.1,0.3]
                obstacle = random.choices(population=self.obstacle_list, weights=self.obstacle_list_weights, k=1)
                self.obstacle_sprite_group.add(obstacle[0](random.randint(1,15), random.randint(1,9)))

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
        # Add random obstacles max 10
        is_obstacle = random.choices(population=[True, False], weights=[0.3,0.7], k=10)
        for i in is_obstacle:
            if i:
                self.obstacle_list = [Rock, Web, Bonepile, Chest, Gravestone]
                obstacle = random.choice(self.obstacle_list)
                self.obstacle_sprite_group.add(obstacle(random.randint(1,15), random.randint(1,9)))

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
    def __init__(self, player, enemy):
        super().__init__(player)
        # enemy_list = [Alfredo, Bob, MuscleBoi] if enemies == None else enemies
        # enemy = random.choice(enemy_list)
        self.boss = enemy(player)
        self.enemy_sprite_group.add(self.boss)
        # Add random obstacles max 10
        is_obstacle = random.choices(population=[True, False], weights=[0.3,0.7], k=10)
        for i in is_obstacle:
            if i:
                self.obstacle_list = [Rock, Web, Bonepile, Chest, Gravestone]
                obstacle = random.choice(self.obstacle_list)
                self.obstacle_sprite_group.add(obstacle(random.randint(1,15), random.randint(1,9)))
        
        self.boss_dead = False

        
    def update(self):
        super().update()
        if self.boss.current_health <= 0 and not(self.boss_dead):
            self.killBoss()
            self.boss_dead = True

    def killBoss(self):
        self.door_sprite_group.add(TrapDoor())