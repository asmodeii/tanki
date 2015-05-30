__author__ = 'Tomasz Rzepka'

from actor import Tank, Wall
import pygame

class GameData:
    def __init__(self):
        self.spawns = [(600, 100), (600, 700), (100, 400), (1100, 400),
                       (100, 100), (1100, 700), (100, 700), (1100, 100)]
        self.players = [Player(i) for i in xrange(4)]
        self.walls = [Wall(i*2+100, 500) for i in xrange(10)]
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.npc_number = 0
        for wall in self.walls:
            self.sprites.add(wall)
            self.walls.add(wall)

    def clear(self):
        self.players = self.players[:4]
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.npc_number = 0
        for wall in self.walls:
            self.sprites.add(wall)
            self.walls.add(wall)

    def add_npcs(self, number):
        for i in xrange(number):
            npc = Player(4)
            npc.turn_on()
            self.players.append(npc)

    def initiate(self):
        offset = 0
        for i, player in enumerate(self.players):
            if player.is_on:
                (player.tank.rect.x, player.tank.rect.y) = self.spawns[i-offset]
                self.sprites.add(player.tank)
                self.tanks.add(player.tank)
            else:
                offset += 1


class Player:
    def __init__(self, tank_id):
        self.is_on = False
        self.tank = Tank(tank_id)
        self.enemy_tanks = []

    def set_enemy_tanks(self, enemy_tanks):
        self.enemy_tanks = enemy_tanks

    def turn_on(self):
        self.is_on = True
        self.tank.is_on = True

    def turn_off(self):
        self.tank.change_image(0)
        self.is_on = False
        self.tank.is_on = False
