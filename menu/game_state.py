from functools import partial

__author__ = 'Tomasz Rzepka'

import pygame
import sys
from configs import config

class Game:
    def __init__(self, screen, game_data, bg_color=(0, 0, 0)):
        self.screen = screen
        self.bg_color = bg_color
        self.game_data = game_data
        self.clock = pygame.time.Clock()
        self.mouse_is_visible = False
        self.mainloop = False

    def stop(self):
        self.screen.fill((0, 0, 0))
        self.game_data.clear()
        self.mainloop = False

    def mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def run(self):
        self.mainloop = True
        while self.mainloop:
            self.screen.fill((0, 100, 0))
            self.clock.tick(100)
            for player in self.game_data.players:
                player.act()
            for bullet in self.game_data.bullets:
                bullet.act()
            for bonus in self.game_data.bonuses:
                bonus.act()
            self.game_data.try_spawn_bonus()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.press_key(event.key)
                elif event.type == pygame.KEYUP:
                    self.release_key(event.key)

            self.mouse_visibility()
            self.game_data.sprites.draw(self.screen)
            pygame.display.flip()

    def press_key(self, key):
        for player_id, player_key in enumerate(config.player_key_list):
            if key == player_key.up:
                self.game_data.players[player_id].set_action_drive(self.game_data.players[player_id].forward)
            if key == player_key.down:
                self.game_data.players[player_id].set_action_drive(self.game_data.players[player_id].backward)
            if key == player_key.left:
                self.game_data.players[player_id].set_action_rotate(partial(self.game_data.players[player_id].rotate, 1))
            if key == player_key.right:
                self.game_data.players[player_id].set_action_rotate(partial(self.game_data.players[player_id].rotate, -1))
            if key == player_key.action:
                self.game_data.players[player_id].fire()
        if key == pygame.K_ESCAPE:
            self.stop()

    def release_key(self, key):  # hardcoded for debug purposes
        for player_id, player_key in enumerate(config.player_key_list):
            if key == player_key.up or key == player_key.down:
                self.game_data.players[player_id].set_action_drive(self.game_data.players[player_id].none_action)
            elif key == player_key.left or key == player_key.right:
                self.game_data.players[player_id].set_action_rotate(self.game_data.players[player_id].none_action)
