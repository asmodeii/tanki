__author__ = 'Tomasz Rzepka, Pawel Kalecinski'

from game_menu import GameMenu
import pygame
import sys
from menu_item import RED, ORANGE, MenuItem
from game_core import GameData
from functools import partial
from game_state import Game
from configs import SCREEN_WIDTH, SCREEN_HEIGHT

class NewGame:
    def __init__(self, screen, bg_color=(0, 0, 0)):
        self.screen = screen
        self.bg_color = bg_color
        self.bg_img = pygame.image.load("Assets/tanks2.jpg")
        self.bg_rect = self.bg_img.get_rect()
        font = 'Assets/armalite.ttf'
        font_size = 50
        self.font_color = RED
        self.npc_tanks_number = 0
        self.game_data = GameData()
        player_strings = self.generate_players_strings()
        self.funcs = (("Create Game", self.create_new_game),
                      (player_strings[0], partial(self.change_player_state, 0)),
                      (player_strings[1], partial(self.change_player_state, 1)),
                      (player_strings[2], partial(self.change_player_state, 2)),
                      (player_strings[3], partial(self.change_player_state, 3)),
                      (self.generate_npc_tanks_string(), self.change_npc_tanks_number),
                      ("Back", self.stop))
        self.mainloop = False
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.items = []
        self.clock = pygame.time.Clock()

        for index, item in enumerate(self.funcs):
            (key, func) = item
            menu_item = MenuItem(key, font, font_size, self.font_color)
            height_text = len(self.funcs) * menu_item.height
            position_x = (self.scr_width / 2) - (menu_item.width / 2)
            position_y = 0
            if index == 0:
                position_y -= 30
            if index == len(self.funcs) - 1:
                position_y += 30
            position_y += (self.scr_height / 2) - (height_text / 2) + \
                          ((index * 2) + index * menu_item.height)
            menu_item.set_position(position_x, position_y)
            menu_item.func = func
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def create_new_game(self):
        tank_count = 0
        for i, player in enumerate(self.game_data.players):
            if player.is_on:
                tank_count += 1
        tank_count += self.npc_tanks_number
        if tank_count > 0:
            self.game_data.add_npcs(self.npc_tanks_number)
            self.game_data.initiate()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
            cr = Game(screen, self.game_data)
            cr.run()

    def generate_players_strings(self):
        strings = []
        for i, player in enumerate(self.game_data.players):
            if player.is_on:
                strings.append("Player %d  ON" % i)
            else:
                strings.append("Player %d  OFF" % i)
        return strings

    def generate_player_string(self, player_id):
        if self.game_data.players[player_id].is_on:
            return "Player %d  ON" % player_id
        else:
            return "Player %d  OFF" % player_id

    def generate_npc_tanks_string(self):
        return "NPC Tanks: %d" % self.npc_tanks_number

    def change_npc_tanks_number(self):
        self.npc_tanks_number = (self.npc_tanks_number + 1) % 5
        self.items[5].text = self .generate_npc_tanks_string()

    def change_player_state(self, player_id):
        if self.game_data.players[player_id].is_on:
            if 0 <= self.game_data.players[player_id].tank.tank_id < 3:
                self.game_data.players[player_id].tank.change_image(self.game_data.players[player_id].tank.tank_id+1)
            else:
                self.game_data.players[player_id].turn_off()
        else:
            self.game_data.players[player_id].turn_on()
        self.items[player_id+1].text = self.generate_player_string(player_id)

    def stop(self):
        self.screen.fill((0, 0, 0))
        self.mainloop = False

    def mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def item_selection(self, key):
        print(key)
        for item in self.items:
            item.set_italic(False)
            item.set_color(self.font_color)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0
            elif key == pygame.K_ESCAPE:
                self.stop()
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                self.items[self.cur_item].func()

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_color(ORANGE)



    @staticmethod
    def mouse_select(item, mouse_pos):
        if item.mouse_selection(mouse_pos):
            item.set_color(ORANGE)
            item.set_italic(True)
        else:
            item.set_color(RED)
            item.set_italic(False)

    def run(self):
        self.mainloop = True
        while self.mainloop:
            self.clock.tick(100)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.item_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.mouse_selection(mouse_pos):
                            item.func()

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.mouse_visibility()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.bg_img, ((SCREEN_WIDTH - self.bg_rect.width) / 2,
                                           (SCREEN_HEIGHT - self.bg_rect.height) / 2))

            for item in self.items:
                if self.mouse_is_visible:
                    mouse_pos = pygame.mouse.get_pos()
                    self.mouse_select(item, mouse_pos)
                self.screen.blit(item.label, item.position)

            for i, player in enumerate(self.game_data.players):
                if i > 4:
                    break
                if player.is_on:
                    if i % 2:
                        self.screen.blit(player.tank.image, (self.items[i+1].position_x+self.items[i+1].width,
                                                             self.items[i+1].position_y-30))
                    else:
                        self.screen.blit(player.tank.image, (self.items[i+1].position_x-50, self.items[i+1].position_y-30))
            pygame.display.flip()
