"""
Module for game logic
"""
__author__ = 'Tomasz Rzepka'

from game_core.actor import Tank, Wall, BulletSprite, HotBulletSprite, BonusSprite
from application.configs import SCREEN_WIDTH, SCREEN_HEIGHT, CONFIGURATION
from pygame.math import Vector2

import math
import pygame
import random


class GameElements(object):
    """
    Container for game elements
    """
    def __init__(self):
        """
        Initializes Game Elements
        """
        self.spawns = [(585, 70), (585, 600), (100, 335), (1050, 335),
                       (100, 100), (1050, 550), (100, 550), (1050, 100)]
        self.players = [Player(i) for i in xrange(4)]
        self.obstacles = [Wall(0+i*50, 0) for i in xrange(int(math.ceil(SCREEN_WIDTH/50.)))]
        self.obstacles += [Wall(0, 50+i*50) for i in xrange(int(math.ceil(SCREEN_HEIGHT/50.) - 1))]
        self.obstacles += [Wall(50+i*50, SCREEN_HEIGHT-50)
                           for i in xrange(int(math.ceil(SCREEN_WIDTH/50.) - 1))]
        self.obstacles += [Wall(SCREEN_WIDTH-50, 50+i*50)
                           for i in xrange(int(math.ceil(SCREEN_HEIGHT/50.) - 2))]
        self.obstacles += [Wall(200, 50), Wall(200, 200), Wall(200, 250), Wall(150, 250),
                           Wall(100, 250), Wall(50, 250), Wall(450, 50), Wall(450, 100),
                           Wall(450, 150), Wall(500, 200), Wall(700, 50), Wall(700, 100),
                           Wall(700, 150), Wall(650, 200), Wall(950, 50), Wall(950, 200),
                           Wall(950, 250), Wall(1000, 250), Wall(1050, 250), Wall(1100, 250),
                           Wall(200, 700-50), Wall(200, 700-200), Wall(200, 700-250),
                           Wall(150, 700-250), Wall(100, 700-250), Wall(50, 700-250),
                           Wall(450, 700-50), Wall(450, 700-100), Wall(450, 700-150),
                           Wall(500, 700-200), Wall(700, 700-50), Wall(700, 700-100),
                           Wall(700, 700-150), Wall(650, 700-200), Wall(950, 700-50),
                           Wall(950, 700-200), Wall(950, 700-250), Wall(1000, 700-250),
                           Wall(1050, 700-250), Wall(1100, 700-250)]
        self.bullets = []
        self.bonuses = []

    def get_obstacles(self):
        """
        PyLint love.
        """
        return self.obstacles

    def get_tanks(self):
        """
        PyLint love.
        """
        return self.players


class GameData(object):
    """
    Base class for game instance.
    """
    def __init__(self):
        """
        Initializes game with default values.
        """
        self.elements = GameElements()
        self.tanks = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.bonus_spawn_time = 0
        self.npc_number = 0
        for wall in self.elements.obstacles:
            self.sprites.add(wall)
            self.walls.add(wall)

    def clear(self):
        """
        Clears Game Data to initial values.
        """
        self.elements.players = [Player(i) for i in xrange(4)]
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.elements.bonuses = []
        self.elements.bullets = []
        self.bonus_spawn_time = 0
        self.npc_number = 0
        for wall in self.elements.obstacles:
            self.sprites.add(wall)
            self.walls.add(wall)

    def add_npcs(self, number):
        """
        Adds AI controlled tanks to game.
        :param number: number of non player characters to be added
        """
        while number > 0:
            npc = AITank(4)
            npc.turn_on()
            self.elements.players.append(npc)
            number -= 1

    def initiate(self):
        """
        Initiates game data before game starts(sets players positions and sets sprites).
        """
        offset = 0
        for i, player in enumerate(self.elements.players):
            if player.status['is_on']:
                current_position = i-offset
                (player.tank.rect.x, player.tank.rect.y) = self.elements.spawns[current_position]
                self.sprites.add(player.tank)
                self.tanks.add(player.tank)
                if current_position == 0:
                    player.rotate(180)
                elif current_position == 2 or current_position == 4 or current_position == 6:
                    player.rotate(270)
                elif current_position == 3 or current_position == 5 or current_position == 7:
                    player.rotate(90)
            else:
                offset += 1

    def try_spawn_bonus(self):
        """
        Checks if it is allowed to spawn bonus if yes it does so.
        """
        if CONFIGURATION.allow_bonuses:
            if self.bonus_spawn_time == 0:
                bonuses = ('health', 'damage', 'speed', 'attack_speed')
                self.elements.bonuses.append(Bonus(bonuses[random.randint(0, 3)]))
                self.sprites.add(self.elements.bonuses[0].bonus)
                self.bonus_spawn_time = 500 + random.randint(0, 500)
            elif not self.elements.bonuses:
                self.bonus_spawn_time -= 1


class Player(object):
    """
    Base Tank controls.
    """
    def __init__(self, tank_id):
        """
        :param tank_id: number of graphic for tank
        :return:
        """
        self.moving = {
            'angle': 0,
            'position_debt': (0.0, 0.0),
            'vector': (0.0, -1.0)}
        self.status = {
            'health': 5,
            'speed': 1,
            'is_on': False,
            'cool_down': 0,
            'max_cool_down': 50,
            'damage_bonus': False,
            'speed_bonus': 0,
            'attack_speed_bonus': 0,
        }
        self.action_drive = self.none_action
        self.action_rotate = self.none_action
        self.tank = Tank(tank_id, self)

    def turn_on(self):
        """
        Turns player on.
        """
        self.status['is_on'] = True
        self.tank.is_on = True

    def turn_off(self):
        """
        Turns player off.
        """
        self.tank.change_image(0)
        self.status['is_on'] = False
        self.tank.is_on = False

    def rotate(self, angle):
        """
        Rotate an image while keeping its center and size.
        :param angle: angle to rotate
        """
        old_angle = self.moving['angle']
        old_vector = self.moving['vector']
        old_image = self.tank.image
        old_rect = self.tank.rect
        if self.status['speed_bonus']:
            speed = self.status['speed'] + 2
        else:
            speed = self.status['speed']
        self.moving['angle'] += angle*speed
        self.rotate_vector()
        rot_image = pygame.transform.rotate(self.tank.base_image, self.moving['angle'])
        old_center = self.tank.rect.center
        rot_rect = rot_image.get_bounding_rect()
        self.tank.image = rot_image
        self.tank.rect = rot_rect
        self.tank.rect.center = old_center
        obstacles_hit = pygame.sprite.spritecollide(self.tank, GAME_DATA.tanks, False)
        obstacles_hit += pygame.sprite.spritecollide(self.tank, GAME_DATA.walls, False)
        if len(obstacles_hit) > 1:
            self.tank.image = old_image
            self.tank.rect = old_rect
            self.moving['vector'] = old_vector
            self.moving['angle'] = old_angle
            return False
        return True

    def rotate_vector(self):
        """
        Rotate a vector `v` by the given angle (set in base).
        """
        x_position, y_position = (0.0, -1.0)
        rad = math.radians(self.moving['angle'])
        cos_theta = math.cos(rad)
        sin_theta = math.sin(rad)

        nx_position = x_position*cos_theta - y_position*sin_theta
        ny_position = x_position*sin_theta + y_position*cos_theta
        self.moving['vector'] = (nx_position, ny_position)

    def forward(self):
        """
        Moves player forward if there is no obstacle ahead.
        :return: True if succeeded/ False if hit obstacle.
        """
        (vec_x, vec_y) = self.moving['vector']
        (debt_x, debt_y) = self.moving['position_debt']
        if self.status['speed_bonus']:
            speed = self.status['speed'] + 2
        else:
            speed = self.status['speed']
        (fractional_x, integral_x) = math.modf(vec_x*speed+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y*speed+debt_y)
        old_x = self.tank.rect.x
        old_y = self.tank.rect.y
        self.tank.rect.x -= integral_x
        self.tank.rect.y += integral_y
        obstacles_hit = pygame.sprite.spritecollide(self.tank, GAME_DATA.tanks, False)
        obstacles_hit += pygame.sprite.spritecollide(self.tank, GAME_DATA.walls, False)
        self.moving['position_debt'] = (fractional_x, fractional_y)
        if len(obstacles_hit) > 1:
            self.tank.rect.x = old_x
            self.tank.rect.y = old_y
            return False
        return True

    def backward(self):
        """
        Moves player forward if there is no obstacle ahead.
        :return: True if succeeded/ False if hit obstacle.
        """
        (vec_x, vec_y) = self.moving['vector']
        (debt_x, debt_y) = self.moving['position_debt']
        if self.status['speed_bonus']:
            speed = self.status['speed'] + 1
        else:
            speed = self.status['speed']
        (fractional_x, integral_x) = math.modf(vec_x*speed+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y*speed+debt_y)
        old_x = self.tank.rect.x
        old_y = self.tank.rect.y
        self.tank.rect.x += integral_x
        self.tank.rect.y -= integral_y
        obstacles_hit = pygame.sprite.spritecollide(self.tank, GAME_DATA.tanks, False)
        obstacles_hit += pygame.sprite.spritecollide(self.tank, GAME_DATA.walls, False)
        self.moving['position_debt'] = (fractional_x, fractional_y)
        if len(obstacles_hit) > 1:
            self.tank.rect.x = old_x
            self.tank.rect.y = old_y
            return False
        return True

    def set_action_drive(self, action):
        """
        :param action: sets action(forward/backward) to be executed on act()
        """
        self.action_drive = action

    def set_action_rotate(self, action):
        """
        :param action: sets action(turn) to be executed on act()
        """
        self.action_rotate = action

    def act(self):
        """
        Executes current actions and ticks time for cooldowns and timers
        """
        if self.status['is_on']:
            self.action_rotate()
            self.action_drive()
            if self.status['cool_down'] > 0:
                self.status['cool_down'] -= 1
            if self.status['speed_bonus'] > 0:
                self.status['speed_bonus'] -= 1

    @staticmethod
    def none_action():
        """
        Null action(for performance reasons) to be executed when no action is set.
        """
        pass

    def fire(self):
        """
        Fires bullet if tank is allowed to do so(not in cool down and is on)
        """
        if self.status['is_on'] and not self.status['cool_down']:
            if self.status['attack_speed_bonus'] > 0:
                self.status['attack_speed_bonus'] -= 1
            else:
                self.status['cool_down'] = self.status['max_cool_down']
            if self.status['damage_bonus']:
                bullet = Bullet(self.moving['vector'], self.tank.rect.center, damage=5)
                self.status['damage_bonus'] = False
            else:
                bullet = Bullet(self.moving['vector'], self.tank.rect.center)
            GAME_DATA.elements.bullets.append(bullet)
            while pygame.sprite.collide_rect(self.tank, bullet.bullet):
                if bullet.initial_forward():
                    self.damage(bullet.damage)
                    bullet.destroy()
                    return
            GAME_DATA.sprites.add(bullet.bullet)

    def damage(self, dmg):
        """
        Deals dmg and turns tank off if health is <= 0
        :param dmg: takes dmg number from health
        """
        self.status['health'] -= dmg
        if self.status['health'] <= 0:
            GAME_DATA.sprites.remove(self.tank)
            GAME_DATA.tanks.remove(self.tank)
            self.turn_off()


class AITank(Player, object):
    """
    Tank controlled by AI
    """
    def __init__(self, tank_id):
        """
        :param tank_id: tank graphic id
        """
        super(AITank, self).__init__(tank_id)
        self.state = 'patrolling'
        self.ai_moving = {
            'prev_angle': self.moving['angle'],
            'prev_center': self.tank.rect.center,
            'desired_angle': 0,
            'back': 0
        }
        self.max_state_change_frame = 10
        self.state_change_frame = 0
        self.target = self.tank


    def laser_target(self, tank, vector):
        """
        :param tank: tank to be targeted
        :param vector: vector for targeting
        :return: True if there are no obstacles, False otherwise
        """
        bullet = Bullet(vector, self.tank.rect.center, damage=0)
        while not pygame.sprite.collide_rect(tank, bullet.bullet):
            if bullet.initial_forward():
                return False
        return True

    def find_target(self, player):
        """
        Find target to attack.
        :return: True if found target, False otherwise
        """
        self.target = player.tank
        vec = Vector2(- self.target.rect.centerx + self.tank.rect.centerx,
                      self.target.rect.centery - self.tank.rect.centery)
        if vec.length() < 350:
            normalized_vec = vec.normalize()
            if self.laser_target(player.tank, (normalized_vec.x, normalized_vec.y)):
                cur_vec = Vector2(self.moving['vector'])
                self.ai_moving['desired_angle'] = cur_vec.angle_to(vec)
                if self.ai_moving['desired_angle'] > 180:
                    self.ai_moving['desired_angle'] -= 360
                elif self.ai_moving['desired_angle'] < -180:
                    self.ai_moving['desired_angle'] += 360
                self.state = 'targeting'
                return True
            else:
                self.state = 'patrolling'
                return False

    def targeting(self):
        """
        Targets enemy and fires.
        """
        if self.ai_moving['desired_angle'] >= 1:
            self.rotate(1)
            self.ai_moving['desired_angle'] -= 1
        elif self.ai_moving['desired_angle'] <= -1:
            self.rotate(-1)
            self.ai_moving['desired_angle'] += 1
        else:
            self.fire()
            self.state = 'patrolling'

    def patrolling(self):
        """
        Patrols area for enemies.
        """
        if self.ai_moving['back'] >= 1:
            self.backward()
            self.ai_moving['back'] -= 1
        if self.ai_moving['desired_angle'] >= 1:
            self.rotate(1)
            self.ai_moving['desired_angle'] -= 1
        elif self.ai_moving['desired_angle'] <= -1:
            self.rotate(-1)
            self.ai_moving['desired_angle'] += 1
        else:
            if not self.forward():
                self.ai_moving['back'] = 40
                self.ai_moving['desired_angle'] = 90

    def act(self):
        """
        Tics Artificial Intelligence Algorithms and performs actions
        """
        if self.status['is_on']:
            if self.status['cool_down'] > 0:
                self.status['cool_down'] -= 1
            if self.state_change_frame == 0:
                self.state_change_frame = self.max_state_change_frame
                for player in GAME_DATA.elements.players[:4]:
                    if player.status['is_on']:
                        if self.find_target(player):
                            break
            else:
                if self.state == 'targeting':
                    self.targeting()
                elif self.state == 'patrolling':
                    self.patrolling()
                self.state_change_frame -= 1


class Bullet(object):
    """
    Controls Bullet
    """
    def __init__(self, vector, center, damage=1):
        """
        :param vector: path for bullet
        :param center: starting point for bullet
        :param damage: damage to be dealt on impact
        :param speed: movement speed of bullet
        :param duration: time after which bullet will be destroyed
        """
        self.old_x = 0
        self.old_y = 0
        self.vector = vector
        self.damage = damage
        self.duration = 150
        self.position_debt = (0.0, 0.0)
        if damage > 1:
            self.bullet = HotBulletSprite(center)
        else:
            self.bullet = BulletSprite(center)

    def destroy(self):
        """
        Destroys bullet.
        """
        if self in GAME_DATA.elements.bullets:
            GAME_DATA.elements.bullets.remove(self)
        if self.bullet in GAME_DATA.sprites:
            GAME_DATA.sprites.remove(self.bullet)

    def initial_forward(self):
        """
        Moves bullet forward after it is shot from tank(ignores tank impact
         to not deal damage to shooter), if it hits wall
          :return: True if hit wall, False otherwise
        """
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        (fractional_x, integral_x) = math.modf(vec_x*3+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y*3+debt_y)
        self.bullet.rect.x -= integral_x
        self.bullet.rect.y += integral_y
        walls_hit = pygame.sprite.spritecollide(self.bullet, GAME_DATA.walls, False)
        if walls_hit:
            return True
        self.position_debt = (fractional_x, fractional_y)
        return False

    def forward(self):
        """
        Moves bullet forward, bounces on walls, deals damage on tank impact
        """
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        (fractional_x, integral_x) = math.modf(vec_x*3+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y*3+debt_y)
        self.old_x = self.bullet.rect.x
        self.old_y = self.bullet.rect.y
        self.bullet.rect.x -= integral_x
        self.bullet.rect.y += integral_y
        tanks_hit = pygame.sprite.spritecollide(self.bullet, GAME_DATA.tanks, False)
        for tank in tanks_hit:
            tank.parent.damage(self.damage)
            self.destroy()
        walls_hit = pygame.sprite.spritecollide(self.bullet, GAME_DATA.walls, False)
        if walls_hit:
            diff_x = walls_hit[0].rect.centerx - self.bullet.rect.centerx
            diff_y = walls_hit[0].rect.centery - self.bullet.rect.centery
            if abs(diff_x) > abs(diff_y):
                self.vector = (lambda x: (-x[0], x[1]))(self.vector)
            else:
                self.vector = (lambda x: (x[0], -x[1]))(self.vector)

            self.bullet.rect.x = self.old_x
            self.bullet.rect.y = self.old_y
        self.position_debt = (fractional_x, fractional_y)

    def act(self):
        """
        Moves forward bullet and counts time for bullet to be destroyed
        """
        self.duration -= 1
        if self.duration < 0:
            self.destroy()
        if self.damage == 1:
            self.bullet.animate()
        self.forward()


class Bonus(object):
    """
    Controls Bonus element
    """
    def __init__(self, bonus_type, duration=500):
        """
        :param bonus_type: bonus type(health - additional health,
                                      damage - increased damage,
                                      speed - increased tank speed,
                                      attack_speed - increased attack speed)
        :param duration: duration after which bonus will be destroyed
        """
        self.duration = duration
        self.position_debt = (0.0, 0.0)
        self.bonus_type = bonus_type
        self.bonus = BonusSprite(bonus_type, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    def destroy(self):
        """
        Destroys Bonus.
        """
        if self in GAME_DATA.elements.bonuses:
            GAME_DATA.elements.bonuses.remove(self)
        if self.bonus in GAME_DATA.sprites:
            GAME_DATA.sprites.remove(self.bonus)

    def act(self):
        """
        Counts time for destruction, if collides with tank it gives it bonus.
        """
        self.duration -= 1
        if self.duration < 0:
            self.destroy()
        tanks_hit = pygame.sprite.spritecollide(self.bonus, GAME_DATA.tanks, False)
        for tank in tanks_hit:
            if self.bonus_type == 'health':
                tank.parent.damage(-5)
            elif self.bonus_type == 'damage':
                tank.parent.status['damage_bonus'] = True
            elif self.bonus_type == 'speed':
                tank.parent.status['speed_bonus'] = 1000
            elif self.bonus_type == 'attack_speed':
                tank.parent.status['attack_speed_bonus'] = 10
            self.destroy()

GAME_DATA = GameData()
