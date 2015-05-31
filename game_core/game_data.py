__author__ = 'Tomasz Rzepka'

from actor import Tank, Wall, BulletSprite, HotBulletSprite, BonusSprite
from menu.configs import SCREEN_WIDTH, SCREEN_HEIGHT, config
from pygame.math import Vector2

import math
import pygame
import random

class GameData:
    def __init__(self):
        self.spawns = [(585, 70), (585, 600), (100, 335), (1050, 335),
                       (100, 100), (1050, 550), (100, 550), (1050, 100)]
        self.players = [Player(i) for i in xrange(4)]
        self._walls = [Wall(0+i*50, 0) for i in xrange(int(math.ceil(SCREEN_WIDTH/50.)))]
        self._walls += [Wall(0, 50+i*50) for i in xrange(int(math.ceil(SCREEN_HEIGHT/50.) - 1))]
        self._walls += [Wall(50+i*50, SCREEN_HEIGHT-50) for i in xrange(int(math.ceil(SCREEN_WIDTH/50.) - 1))]
        self._walls += [Wall(SCREEN_WIDTH-50, 50+i*50) for i in xrange(int(math.ceil(SCREEN_HEIGHT/50.) - 2))]
        self._walls += [Wall(200, 50), Wall(200, 200), Wall(200, 250), Wall(150, 250),
                        Wall(100, 250), Wall(50, 250)]
        self._walls += [Wall(450, 50), Wall(450, 100), Wall(450, 150), Wall(500, 200),
                        Wall(700, 50), Wall(700, 100), Wall(700, 150), Wall(650, 200)]
        self._walls += [Wall(950, 50), Wall(950, 200), Wall(950, 250), Wall(1000, 250),
                        Wall(1050, 250), Wall(1100, 250)]

        self._walls += [Wall(200, 700-50), Wall(200, 700-200), Wall(200, 700-250), Wall(150, 700-250),
                        Wall(100, 700-250), Wall(50, 700-250)]
        self._walls += [Wall(450, 700-50), Wall(450, 700-100), Wall(450, 700-150), Wall(500, 700-200),
                        Wall(700, 700-50), Wall(700, 700-100), Wall(700, 700-150), Wall(650, 700-200)]
        self._walls += [Wall(950, 700-50), Wall(950, 700-200), Wall(950, 700-250), Wall(1000, 700-250),
                        Wall(1050, 700-250), Wall(1100, 700-250)]
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.bullets = []
        self.bonuses = []
        self.bonus_spawn_time = 0
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
            npc = AITank(4)
            npc.turn_on()
            self.players.append(npc)

    def initiate(self):
        offset = 0
        for i, player in enumerate(self.players):
            if player.is_on:
                (player.tank.rect.x, player.tank.rect.y) = self.spawns[i-offset]
                self.sprites.add(player.tank)
                self.tanks.add(player.tank)
                if i == 0:
                    player.rotate(180)
                elif i == 2 or i == 4 or i == 6:
                    player.rotate(270)
                elif i == 3 or i == 5 or i == 7:
                    player.rotate(90)
            else:
                offset += 1

    def try_spawn_bonus(self):
        if config.allow_bonuses:
            if self.bonus_spawn_time == 0:
                bonuses = ('health', 'damage', 'speed', 'attack_speed')
                self.bonuses.append(Bonus(bonuses[random.randint(0, 3)]))
                self.sprites.add(self.bonuses[0].bonus)
                self.bonus_spawn_time = 500 + random.randint(0, 500)
            elif not self.bonuses:
                self.bonus_spawn_time -= 1

class Player:
    def __init__(self, tank_id):
        self.damage_bonus = False
        self.speed_bonus = 0
        self.attack_speed_bonus = 0
        self.angle = 0
        self.vector = (0.0, -1.0)
        self.position_debt = (0.0, 0.0)
        self.health = 3
        self.speed = 1
        self.action_drive = self.none_action
        self.action_rotate = self.none_action
        self.is_on = False
        self.cool_down = 0
        self.max_cool_down = 50
        self.tank = Tank(tank_id, self)

    def turn_on(self):
        self.is_on = True
        self.tank.is_on = True

    def turn_off(self):
        self.tank.change_image(0)
        self.is_on = False
        self.tank.is_on = False

    def rotate(self, angle):
        """rotate an image while keeping its center and size"""
        old_angle = self.angle
        old_vector = self.vector
        old_image = self.tank.image
        old_rect = self.tank.rect
        if self.speed_bonus:
            speed = self.speed + 2
        else:
            speed = self.speed
        self.angle += angle*speed
        self.rotate_vector()
        rot_image = pygame.transform.rotate(self.tank.base_image, self.angle)
        old_center = self.tank.rect.center
        rot_rect = rot_image.get_bounding_rect()
        self.tank.image = rot_image
        self.tank.rect = rot_rect
        self.tank.rect.center = old_center
        obstacles_hit = pygame.sprite.spritecollide(self.tank, game_data.tanks, False)
        obstacles_hit += pygame.sprite.spritecollide(self.tank, game_data.walls, False)
        if len(obstacles_hit) > 1:
            self.tank.image = old_image
            self.tank.rect = old_rect
            self.vector = old_vector
            self.angle = old_angle
            return False
        return True

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
        if self.speed_bonus:
            speed = self.speed + 2
        else:
            speed = self.speed
        (fractional_x, integral_x) = math.modf(vec_x*speed+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y*speed+debt_y)
        old_x = self.tank.rect.x
        old_y = self.tank.rect.y
        self.tank.rect.x -= integral_x
        self.tank.rect.y += integral_y
        obstacles_hit = pygame.sprite.spritecollide(self.tank, game_data.tanks, False)
        obstacles_hit += pygame.sprite.spritecollide(self.tank, game_data.walls, False)
        self.position_debt = (fractional_x, fractional_y)
        if len(obstacles_hit) > 1:
            self.tank.rect.x = old_x
            self.tank.rect.y = old_y
            return False
        return True

    def backward(self):
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        if self.speed_bonus:
            speed = self.speed + 1
        else:
            speed = self.speed
        (fractional_x, integral_x) = math.modf(vec_x*speed+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y*speed+debt_y)
        old_x = self.tank.rect.x
        old_y = self.tank.rect.y
        self.tank.rect.x += integral_x
        self.tank.rect.y -= integral_y
        obstacles_hit = pygame.sprite.spritecollide(self.tank, game_data.tanks, False)
        obstacles_hit += pygame.sprite.spritecollide(self.tank, game_data.walls, False)
        self.position_debt = (fractional_x, fractional_y)
        if len(obstacles_hit) > 1:
            self.tank.rect.x = old_x
            self.tank.rect.y = old_y
            return False
        return True

    def set_action_drive(self, action):
        self.action_drive = action

    def set_action_rotate(self, action):
        self.action_rotate = action

    def act(self):
        if self.is_on:
            self.action_rotate()
            self.action_drive()
            if self.cool_down > 0:
                self.cool_down -= 1
            if self.speed_bonus > 0:
                self.speed_bonus -= 1

    def none_action(self):
        pass

    def fire(self):
        if self.is_on and not self.cool_down:
            if self.attack_speed_bonus > 0:
                self.attack_speed_bonus -= 1
            else:
                self.cool_down = self.max_cool_down
            if self.damage_bonus:
                bullet = Bullet(self.vector, self.tank.rect.center, damage=5)
                self.damage_bonus = False
            else:
                bullet = Bullet(self.vector, self.tank.rect.center)
            game_data.bullets.append(bullet)
            while pygame.sprite.collide_rect(self.tank, bullet.bullet):
                if bullet.initial_forward():
                    self.damage(bullet.damage)
                    bullet.destroy()
                    return
            game_data.sprites.add(bullet.bullet)

    def damage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            game_data.sprites.remove(self.tank)
            game_data.tanks.remove(self.tank)
            self.turn_off()


class AITank(Player, object):
    def __init__(self, tank_id):
        super(AITank, self).__init__(tank_id)
        self.states = ['running', 'rotating', 'targeting', 'idle']
        self.state = 'idle'
        self.prev_angle = self.angle
        self.prev_center = self.tank.rect.center
        self.max_state_change_frame = 50
        self.state_change_frame = 0
        self.target = self.tank
        self.desired_angle = self.angle

    def laser_target(self, tank, vector):
        bullet = Bullet(vector, self.tank.rect.center, damage=0)
        while not pygame.sprite.collide_rect(tank, bullet.bullet):
            if bullet.initial_forward():
                return False
        return True

    def act(self):
        if self.is_on:

            if self.state_change_frame == 0:
                self.state_change_frame = self.max_state_change_frame
                if self.state == 'patrolling' or self.state == 'idle':
                    for player in game_data.players[:4]:
                        if player.is_on:
                            self.target = player.tank.rect
                            vec = Vector2(- self.target.centerx + self.tank.rect.centerx,
                                          self.target.centery - self.tank.rect.centery)
                            if vec.length() < 350:
                                normalized_vec = vec.normalize()
                                if self.laser_target(player.tank, (normalized_vec.x, normalized_vec.y)):
                                    cur_vec = Vector2(self.vector)
                                    self.desired_angle = vec.angle_to(cur_vec)
                                    if self.desired_angle > 180:
                                        self.desired_angle -= 360
                                    print self.desired_angle
                                    self.state = 'targeting'
                                    print "target aquired"
                                else:
                                    self.state = 'patrolling'
                                    print "patrolling"
                elif self.state == 'targeting':
                    self.state = 'patrolling'
            else:
                self.state_change_frame -= 1

class Bullet:
    def __init__(self, vector, center, damage=1, speed=3, duration=150):
        self.vector = vector
        self.damage = damage
        self.speed = speed
        self.duration = duration
        self.position_debt = (0.0, 0.0)
        if damage > 1:
            self.bullet = HotBulletSprite(center)
        else:
            self.bullet = BulletSprite(center)

    def destroy(self):
        if self in game_data.bullets:
            game_data.bullets.remove(self)
        if self.bullet in game_data.sprites:
            game_data.sprites.remove(self.bullet)

    def initial_forward(self):
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        (fractional_x, integral_x) = math.modf(vec_x*3+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y*3+debt_y)
        self.bullet.rect.x -= integral_x
        self.bullet.rect.y += integral_y
        walls_hit = pygame.sprite.spritecollide(self.bullet, game_data.walls, False)
        if walls_hit:
            return True
        self.position_debt = (fractional_x, fractional_y)
        return False

    def forward(self):
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        (fractional_x, integral_x) = math.modf(vec_x*3+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y*3+debt_y)
        old_x = self.bullet.rect.x
        old_y = self.bullet.rect.y
        self.bullet.rect.x -= integral_x
        self.bullet.rect.y += integral_y
        tanks_hit = pygame.sprite.spritecollide(self.bullet, game_data.tanks, False)
        for tank in tanks_hit:
            tank.parent.damage(self.damage)
            self.destroy()
        walls_hit = pygame.sprite.spritecollide(self.bullet, game_data.walls, False)
        if walls_hit:
            diff_x = walls_hit[0].rect.centerx - self.bullet.rect.centerx
            diff_y = walls_hit[0].rect.centery - self.bullet.rect.centery
            if abs(diff_x) > abs(diff_y):
                self.vector = (lambda x: (-x[0], x[1]))(self.vector)
            else:
                self.vector = (lambda x: (x[0], -x[1]))(self.vector)

            self.bullet.rect.x = old_x
            self.bullet.rect.y = old_y
        self.position_debt = (fractional_x, fractional_y)

    def act(self):
        self.duration -= 1
        if self.duration < 0:
            self.destroy()
        if self.damage == 1:
            self.bullet.animate()
        self.forward()

    def none_action(self):
        pass

class Bonus:
    def __init__(self, bonus_type, duration=500):
        self.duration = duration
        self.position_debt = (0.0, 0.0)
        self.bonus_type = bonus_type
        self.bonus = BonusSprite(bonus_type, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    def destroy(self):
        if self in game_data.bonuses:
            game_data.bonuses.remove(self)
        if self.bonus in game_data.sprites:
            game_data.sprites.remove(self.bonus)

    def act(self):
        self.duration -= 1
        if self.duration < 0:
            self.destroy()
        tanks_hit = pygame.sprite.spritecollide(self.bonus, game_data.tanks, False)
        for tank in tanks_hit:
            if self.bonus_type == 'health':
                tank.parent.damage(-5)
            elif self.bonus_type == 'damage':
                tank.parent.damage_bonus = True
            elif self.bonus_type == 'speed':
                tank.parent.speed_bonus = 1000
            elif self.bonus_type == 'attack_speed':
                tank.parent.attack_speed_bonus = 10
            self.destroy()

    def none_action(self):
        pass
game_data = GameData()
