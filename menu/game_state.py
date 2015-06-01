"""
Module for game screen screen.
"""
from functools import partial
from game_core.game_data import AITank

__author__ = 'Tomasz Rzepka'

import pygame
import sys
from menu.configs import CONFIGURATION, SCREEN_HEIGHT, SCREEN_WIDTH
from menu.state import State

class Game(State):
    """
    Game screeen state
    """
    def __init__(self, screen, game_data, bg_color=(0, 0, 0)):
        """
        Generates initial screen
        :param screen: PyGame screen
        :param game_data: data of game session
        :param bg_color: background color
        :return:
        """
        super(Game, self).__init__(screen, bg_color)
        self.status_font = pygame.font.SysFont("monospace", 20)
        self.status_font.set_bold(True)
        self.game_data = game_data

    def stop_game(self, result_id=-1):
        """
        Stops state and returns to previous one
        :param result_id: result of stopping _gamegame(winning player id)
        """
        self.screen.fill((0, 0, 0))
        self.game_data.clear()
        if result_id != -1:
            if result_id < 5:
                result = self.status_font.render("Player %d won" \
                                                 % result_id, 1, (0, 250, 0))
            else:
                result = self.status_font.render("You LOST", 1, (250, 0, 0))
            self.screen.blit(result, ((SCREEN_WIDTH / 2) - (result.get_rect().width / 2), 20))
        pygame.display.flip()
        self.mainloop = False

    def run(self):
        """
        Base loop for state
        """
        clock = pygame.time.Clock()
        self.mainloop = True
        while self.mainloop:
            self.screen.fill((0, 100, 0))
            clock.tick(100)
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
                self.stop_game(result)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.item_selection(event.key)
                elif event.type == pygame.KEYUP:
                    self.release_key(event.key)

            pygame.display.flip()

    def item_selection(self, key):
        """
        Interprets press key user actions
        :param key: key to be interpreted
        """
        for player_id, player_key in enumerate(CONFIGURATION.player_key_list):
            if key == player_key.up_key:
                self.game_data.elements.players[player_id].set_action_drive(
                    self.game_data.elements.players[player_id].forward)
            if key == player_key.down:
                self.game_data.elements.players[player_id].set_action_drive(
                    self.game_data.elements.players[player_id].backward)
            if key == player_key.left:
                self.game_data.elements.players[player_id].set_action_rotate(
                    partial(self.game_data.elements.players[player_id].rotate, 1))
            if key == player_key.right:
                self.game_data.elements.players[player_id].set_action_rotate(
                    partial(self.game_data.elements.players[player_id].rotate, -1))
            if key == player_key.action:
                self.game_data.elements.players[player_id].fire()
        if key == pygame.K_ESCAPE:
            self.stop_game()

    def release_key(self, key):
        """
        Interprets release key user actions
        :param key: key to be interpreted
        """
        for player_id, player_key in enumerate(CONFIGURATION.player_key_list):
            if key == player_key.up_key or key == player_key.down:
                self.game_data.elements.players[player_id].set_action_drive(
                    self.game_data.elements.players[player_id].none_action)
            elif key == player_key.left or key == player_key.right:
                self.game_data.elements.players[player_id].set_action_rotate(
                    self.game_data.elements.players[player_id].none_action)

    def update_state(self):
        """
        opdates state of game
        :return: -1 if game should not end, otherwise id of winning player
        """
        result_players = ""
        result_ai = ""
        alive = 0
        alive_players = 0
        alive_id = 0
        for i, player in enumerate(self.game_data.elements.players):
            if player.status['is_on']:
                alive_id = i + 1
                alive += 1
                if isinstance(player, AITank):
                    result_ai += "computer %d: %d hp    " % (i+1, player.status['health'])
                else:
                    alive_players += 1
                    result_players += "player %d: %d hp    " % (i+1, player.status['health'])
        status_players = self.status_font.render(result_players, 1, (80, 20, 20))
        status_ai = self.status_font.render(result_ai, 1, (80, 20, 20))
        self.screen.blit(status_players, (10, 10))
        self.screen.blit(status_ai, (10, SCREEN_HEIGHT-40))
        if alive < 2 or alive_players == 0:
            return alive_id
        return -1
