"""Game State"""
from functools import partial
from game_core.game_data import AITank

__author__ = 'Tomasz Rzepka'

import pygame
import sys
from configs import config, SCREEN_HEIGHT, SCREEN_WIDTH

class Game:
    def __init__(self, screen, game_data, bg_color=(0, 0, 0)):
        self.status_font = pygame.font.SysFont("monospace", 20)
        self.status_font.set_bold(True)
        self.screen = screen
        self.bg_color = bg_color
        self.game_data = game_data
        self.clock = pygame.time.Clock()
        self.mouse_is_visible = False
        self.mainloop = False

    def stop(self, result_id=-1):
        self.screen.fill((0, 0, 0))
        self.game_data.clear()
        if result_id != -1:
            if result_id < 5:
                result = self.status_font.render("Player %d won" \
                                                 % result_id, 1, (0, 250, 0))
            else:
                result = self.status_font.render("You LOST", 1, (250, 0, 0))
            self.screen.blit(result, ((SCREEN_WIDTH / 2) \
                                      - (result.get_rect().width / 2), 20))

        pygame.display.flip()
        self.mainloop = False

    def mouse_visibility(self):
        """set mouse visibility"""
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def run(self):
        """mainloop"""
        self.mainloop = True
        while self.mainloop:
            self.screen.fill((0, 100, 0))
            self.clock.tick(100)
            for player in self.game_data.elements.players:
                player.act()
            for bullet in self.game_data.elements.bullets:
                bullet.act()
            for bonus in self.game_data.elements.bonuses:
                bonus.act()
            self.game_data.try_spawn_bonus()
            self.mouse_visibility()
            self.game_data.sprites.draw(self.screen)
            result = self.update_state()
            if result > 0:
                self.stop(result)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.press_key(event.key)
                elif event.type == pygame.KEYUP:
                    self.release_key(event.key)

            pygame.display.flip()

    def press_key(self, key):
        for player_id, player_key in enumerate(config.player_key_list):
            if key == player_key.up:
                self.game_data.elements.players[player_id].set_action_drive\
                    (self.game_data.elements.players[player_id].forward)
            if key == player_key.down:
                self.game_data.elements.players[player_id].set_action_drive\
                    (self.game_data.elements.players[player_id].backward)
            if key == player_key.left:
                self.game_data.elements.players[player_id].set_action_rotate\
                    (partial(self.game_data.elements.players[player_id].rotate,\
                             1))
            if key == player_key.right:
                self.game_data.elements.players[player_id].set_action_rotate\
                    (partial(self.game_data.elements.players[player_id].rotate,\
                             -1))
            if key == player_key.action:
                self.game_data.elements.players[player_id].fire()
        if key == pygame.K_ESCAPE:
            self.stop()

    def release_key(self, key):  # hardcoded for debug purposes
        for player_id, player_key in enumerate(config.player_key_list):
            if key == player_key.up or key == player_key.down:
                self.game_data.elements.players[player_id].set_action_drive\
                    (self.game_data.elements.players[player_id].none_action)
            elif key == player_key.left or key == player_key.right:
                self.game_data.elements.players[player_id].set_action_rotate\
                    (self.game_data.elements.players[player_id].none_action)

    def update_state(self):
        result_players = ""
        result_ai = ""
        alive = 0
        alive_players = 0
        alive_id = 0
        for i, player in enumerate(self.game_data.elements.players):
            if player.status['is_on']:
                alive_id = i + 1
                alive += 1
                if type(player) is AITank:
                    result_ai += "computer %d: %d hp    " \
                                 % (i+1, player.status['health'])
                else:
                    alive_players += 1
                    result_players += "player %d: %d hp    " \
                                      % (i+1, player.status['health'])
        status_players = self.status_font.render(result_players, 1, \
                                                 (80, 20, 20))
        status_ai = self.status_font.render(result_ai, 1, (80, 20, 20))
        self.screen.blit(status_players, (10, 10))
        self.screen.blit(status_ai, (10, SCREEN_HEIGHT-40))
        if alive < 2 or alive_players == 0:
            return alive_id
        return -1
