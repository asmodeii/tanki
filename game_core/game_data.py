__author__ = 'Tomasz Rzepka'

from actor import Tank, Wall
from menu.configs import SCREEN_WIDTH, SCREEN_HEIGHT
import math
import pygame

class GameData:
    def __init__(self):
        self.spawns = [(600, 100), (600, 650), (100, 400), (1000, 400),
                       (100, 100), (1000, 650), (100, 650), (1000, 100)]
        self.players = [Player(i) for i in xrange(4)]
        self._walls = [Wall(0+i*50, 0) for i in xrange(int(math.ceil(SCREEN_WIDTH/50.)))]
        self._walls += [Wall(0, 50+i*50) for i in xrange(int(math.ceil(SCREEN_HEIGHT/50.) - 1))]
        self._walls += [Wall(50+i*50, SCREEN_HEIGHT-50) for i in xrange(int(math.ceil(SCREEN_WIDTH/50.) - 1))]
        self._walls += [Wall(SCREEN_WIDTH-50, 50+i*50) for i in xrange(int(math.ceil(SCREEN_HEIGHT/50.) - 2))]
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.npc_number = 0
        for wall in self._walls:
            self.sprites.add(wall)
            self.walls.add(wall)

    def clear(self):
        self.players = self.players[:4]
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.npc_number = 0
        for wall in self._walls:
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
        for player in self.players:
            player.set_sprites(self.sprites)


class Player:
    def __init__(self, tank_id):
        self.angle = 0
        self.vector = (0.0, -1.0)
        self.position_debt = (0.0, 0.0)
        self.action_drive = self.none_action
        self.action_rotate = self.none_action
        self.is_on = False
        self.tank = Tank(tank_id)
        self.obstacles = pygame.sprite.Group()

    def set_sprites(self, sprites):
        self.obstacles = sprites.copy()
        self.obstacles.remove(self.tank)

    def turn_on(self):
        self.is_on = True
        self.tank.is_on = True

    def turn_off(self):
        self.tank.change_image(0)
        self.is_on = False
        self.tank.is_on = False

    def rotate(self, angle):
        """rotate an image while keeping its center and size"""
        self.angle += angle
        self.rotate_vector()
        orig_rect = self.tank.image.get_rect()
        rot_image = pygame.transform.rotate(self.tank.base_image, self.angle)
        rot_rect = self.tank.rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.tank.image = rot_image

    def rotate_vector(self):
        """Rotate a vector `v` by the given angle, relative to the anchor point."""
        x, y = (0.0, -1.0)
        rad = math.radians(self.angle)
        cos_theta = math.cos(rad)
        sin_theta = math.sin(rad)

        nx = x*cos_theta - y*sin_theta
        ny = x*sin_theta + y*cos_theta
        self.vector = (nx, ny)

    def forward(self):
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        (fractional_x, integral_x) = math.modf(vec_x+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y+debt_y)
        old_x = self.tank.rect.x
        old_y = self.tank.rect.y
        self.tank.rect.x -= integral_x
        self.tank.rect.y += integral_y
        obstacles_hit = pygame.sprite.spritecollide(self.tank, self.obstacles, False)
        if obstacles_hit:
            self.tank.rect.x = old_x
            self.tank.rect.y = old_y
        self.position_debt = (fractional_x, fractional_y)

    def backward(self):
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        (fractional_x, integral_x) = math.modf(vec_x+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y+debt_y)
        old_x = self.tank.rect.x
        old_y = self.tank.rect.y
        self.tank.rect.x += integral_x
        self.tank.rect.y -= integral_y
        obstacles_hit = pygame.sprite.spritecollide(self.tank, self.obstacles, False)
        if obstacles_hit:
            self.tank.rect.x = old_x
            self.tank.rect.y = old_y
        self.position_debt = (fractional_x, fractional_y)

    def set_action_drive(self, action):
        self.action_drive = action

    def set_action_rotate(self, action):
        self.action_rotate = action

    def act(self):
        if self.is_on:
            self.action_rotate()
            self.action_drive()

    def none_action(self):
        pass
