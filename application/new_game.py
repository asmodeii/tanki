"""
Module for game creation screen state
"""
__author__ = 'Tomasz Rzepka, Pawel Kalecinski'

import pygame
from application.state import State
from game_core import GAME_DATA
from functools import partial
from application.game_state import Game
from application.configs import SCREEN_WIDTH, SCREEN_HEIGHT
from application.menu_item import ORANGE


class NewGame(State):
    """
    Game creation screen state.
    """
    def __init__(self, screen, bg_color=(0, 0, 0)):
        """
        Generates initial screen
        :param screen: Pygame screen to write on
        :param bg_color: background color
        """
        super(NewGame, self).__init__(screen, bg_color, "Assets/tanks2.jpg")
        self.npc_tanks_number = 0
        self.game_data = GAME_DATA
        player_strings = self.generate_players_strings()
        funcs = (("Create Game", self.create_new_game),
                 (player_strings[0], partial(self.change_player_state, 0)),
                 (player_strings[1], partial(self.change_player_state, 1)),
                 (player_strings[2], partial(self.change_player_state, 2)),
                 (player_strings[3], partial(self.change_player_state, 3)),
                 (self.generate_npc_tanks_string(), self.change_npc_tanks_number),
                 ("Back", self.stop))
        self.initialize(funcs)

    def create_new_game(self):
        """
        If there is enough players creates new game state and starts it
        """
        tank_count = 0
        for player in self.game_data.elements.players:
            if player.status['is_on']:
                tank_count += 1
        tank_count += self.npc_tanks_number
        if tank_count > 1:
            self.game_data.add_npcs(self.npc_tanks_number)
            self.game_data.initiate()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
            game = Game(screen, self.game_data)
            game.run()
            pygame.display.flip()

    def generate_players_strings(self):
        """
        :return: list of strings describing which players are enabled
        """
        strings = []
        for i, player in enumerate(self.game_data.elements.players):
            if player.status['is_on']:
                strings.append("Player %d  ON" % i)
            else:
                strings.append("Player %d  OFF" % i)
        return strings

    def generate_player_string(self, player_id):
        """
        :param player_id: if of player that status is being checked
        :return: string describing if player is enabled
        """
        if self.game_data.elements.players[player_id].status['is_on']:
            return "Player %d  ON" % player_id
        else:
            return "Player %d  OFF" % player_id

    def generate_npc_tanks_string(self):
        """
        :return: string describing how many non player characters are enabled
        """
        return "NPC Tanks: %d" % self.npc_tanks_number

    def change_npc_tanks_number(self):
        """
        Changes number of NPCs (0...4)
        """
        self.npc_tanks_number = (self.npc_tanks_number + 1) % 5
        self.items[5].text = self .generate_npc_tanks_string()

    def change_player_state(self, player_id):
        """
        Enables tank if not enabled or cycles through available tanks or sets off
        :param player_id: id of player to be changed
        """
        if self.game_data.elements.players[player_id].status['is_on']:
            if 0 <= self.game_data.elements.players[player_id].tank.tank_id < 3:
                self.game_data.elements.players[player_id].tank.change_image(
                    self.game_data.elements.players[player_id].tank.tank_id+1)
            else:
                self.game_data.elements.players[player_id].turn_off()
        else:
            self.game_data.elements.players[player_id].turn_on()
        self.items[player_id+1].text = self.generate_player_string(player_id)

    def update_screen(self):
        """
        draws screen elements representing settings
        """
        strings = self.generate_players_strings()
        for i, string in enumerate(strings):
            self.items[i+1].text = string
        for i, player in enumerate(self.game_data.elements.players):
            if i > 4:
                break
            if player.status['is_on']:
                (position_x, position_y) = self.items[i+1].position
                if i % 2:
                    self.screen.blit(player.tank.image, (position_x
                                                         + self.items[i+1].get_width(),
                                                         position_y-30))
                else:
                    self.screen.blit(player.tank.image, (position_x-50,
                                                         position_y-30))

    def run(self):
        """
        Base loop for state
        """
        clock = pygame.time.Clock()
        if self.bg_img is not None:
            bg_rect = self.bg_img.get_rect()
        self.mainloop = True
        while self.mainloop:
            clock.tick(100)

            for item in self.items:
                item.set_italic(False)
                item.set_color(item.base_font_color)
            self.get_input()
            if self.curr_item is not None:
                self.items[self.curr_item].set_italic(True)
                self.items[self.curr_item].set_color(ORANGE)

            if self.bg_img is not None:
                self.screen.blit(self.bg_img, ((SCREEN_WIDTH - bg_rect.width) / 2,
                                               (SCREEN_HEIGHT - bg_rect.height) / 2))
            self.mouse_visibility()
            self.draw_items()
            self.update_screen()
            pygame.display.flip()
