import pygame
from pygame.locals import *

class InputHandler:
    def __init__(self, game):
        self.game = game

    def handle_player_input(self, event):
        if event.key == pygame.K_1:
            self.game.character.hurt()
            self.game.health_bar.update_health(-5)
            if self.game.health_bar.current_health <= 0:
                self.game.handle_character_death()
        elif event.key == pygame.K_5:
            self.game.next_level()

    def handle_continuous_input(self):
        keys = pygame.key.get_pressed()
        moving = False
        running = False
        dx, dy = 0, 0
        if keys[K_LEFT]:
            dx = -1
            moving = True
        if keys[K_RIGHT]:
            dx = 1
            moving = True
        if keys[K_UP] and not self.game.character.is_jumping:
            self.game.character.jump()
            moving = True
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            if keys[K_LEFT] or keys[K_RIGHT]:
                running = True
                dx *= config.RUN_SPEED_MULTIPLIER

        self.game.character.set_running(running)
        self.game.character.set_walking(moving and not self.game.character.is_jumping and not running)
        self.game.character.move(dx, dy)

        return dx