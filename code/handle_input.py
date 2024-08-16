import pygame
import sys
from pygame.locals import *
import config

def ask_for_name(self):
        # Function that asks the player for their name
        self.surface.fill((0, 0, 0))
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 60)
        prompt_text = 'Enter your name:'
        prompt_surface = font.render(prompt_text, True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2 - 50))
        self.surface.blit(prompt_surface, prompt_rect)
        pygame.display.flip()
        self.name = self.get_user_input()
        self.dialog_box.show(
            f" Zoey: {self.name}!! \n We cannot work with you, You're "
            f"fired! Don't come back until \n you've learned to code!",
            auto_hide_seconds=9)

def handle_player_input(self, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            self.character.hurt()
            self.health_bar.update_health(-5)
            if self.health_bar.current_health <= 0:
                self.handle_character_death()
        
        elif self.waiting_for_level_change:
            if event.key == pygame.K_x:
                print(f"Changing to level {self.boss_deaths + 2}")  
                self.next_level()
                self.waiting_for_level_change = False
                self.dialog_box.hide()
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)  
            

def handle_continuous_input(game):
    # Handle continuous input (e.g., movement keys held down)
    keys = pygame.key.get_pressed()
    moving = False
    running = False
    dx, dy = 0, 0
    if keys[K_LEFT]:
        dx = -1  # Decreased speed
        moving = True
    if keys[K_RIGHT]:
        dx = 1  # Decreased speed
        moving = True
    if keys[K_UP] and not game.character.is_jumping:
        game.character.jump()
        moving = True
    if keys[K_LSHIFT] or keys[K_RSHIFT]:
        if keys[K_LEFT] or keys[K_RIGHT]:
            running = True
            dx *= config.RUN_SPEED_MULTIPLIER

    game.character.set_running(running)
    game.character.set_walking(moving and not game.character.is_jumping and not running)
    game.character.move(dx, dy)

def get_user_input(game):
    input_text = ""
    font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 60)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.unicode.isprintable() and len(event.unicode) == 1:
                    input_text += event.unicode

        game.surface.fill((0, 0, 0))
        prompt_text = 'Enter your name:'
        prompt_surface = font.render(prompt_text, True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(
            center=(game.surface.get_width() / 2, game.surface.get_height() / 2 - 50))
        game.surface.blit(prompt_surface, prompt_rect)
        input_surface = font.render(input_text, True, (255, 255, 255))
        input_rect = input_surface.get_rect(
            center=(game.surface.get_width() / 2, game.surface.get_height() / 2 + 50))
        game.surface.blit(input_surface, input_rect)
        pygame.display.flip()
        game.clock.tick(60)
