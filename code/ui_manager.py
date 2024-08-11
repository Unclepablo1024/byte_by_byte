import pygame
import sys
import random
from pygame.locals import *
import config
from character import MainCharacter
from background import Background
from dialog import DialogBox
from music import MusicPlayer
from enemy_manager import EnemyManager
from game_over import GameOver
from game_state import GameState
from input_handler import InputHandler
from level_manager import LevelManager
from ui_manager import UIManager

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        icon = pygame.image.load('../logo/icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Byte by Byte")

        self.clock = pygame.time.Clock()
        self.running = True
        self.name = ""
        self.init_resources()
        self.restart_game()

    def init_resources(self):
        self.music_player = MusicPlayer()
        self.death_sound = pygame.mixer.Sound(config.DEATH_SOUND_PATH)

    def restart_game(self):
        self.character = MainCharacter(
            config.IDLE_PICTURE_PATH,
            config.WALK_GIF_PATH,
            config.JUMP_GIF_PATH,
            config.RUN_GIF_PATH,
            config.HURT_GIF_PATH,
            config.DIE_GIF_PATH,
            config.ATTACK_1_GIF_PATH,
            config.ATTACK_2_GIF_PATH,
            config.ATTACK_3_GIF_PATH
        )
        self.all_sprites = pygame.sprite.Group(self.character)
        self.game_state = GameState()
        self.level_manager = LevelManager(self)
        self.ui_manager = UIManager(self.surface, self.character)
        self.enemy_manager = EnemyManager(self.surface, self.character, config.MAX_ENEMIES, self.all_sprites)
        self.dialog_box = DialogBox(self.surface, 600, 200)
        self.input_handler = InputHandler(self)
        self.game_over_screen = GameOver(self.surface)

        self.scroll_speed = config.SCROLL_SPEED - 1
        self.dialog_cooldown = 0
        self.dialog_cooldown_time = config.DIALOG_COOLDOWN_TIME
        self.death_timer = None

        self.level_manager.set_level(self.game_state.current_level)

    def run(self):
        self.ask_for_name()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        self.music_player.stop_main_music()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.USEREVENT + 1:
                self.dialog_box.hide()
            elif event.type == pygame.KEYDOWN:
                self.input_handler.handle_player_input(event)

        if not self.dialog_box.active:
            self.input_handler.handle_continuous_input()

    def update(self):
        self.dialog_box.update()
        dx = self.input_handler.handle_continuous_input()

        if not self.dialog_box.active:
            self.character.move(dx, 0)
            self.enemy_manager.update_enemies(self.dialog_box)
            self.level_manager.background.update(dx)
            self.all_sprites.update()

            if self.character.health_bar.is_depleted():
                self.handle_character_death()

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.level_manager.draw_background(self.surface)
        self.all_sprites.draw(self.surface)
        self.ui_manager.draw()
        self.enemy_manager.draw(self.surface)
        self.enemy_manager.draw_enemy_counter(self.surface)
        self.dialog_box.draw()

    def handle_character_death(self):
        if not self.game_state.decrease_life():
            self.game_over()
        else:
            self.character.die()
            self.death_sound.play()
            self.death_timer = pygame.time.get_ticks()
            self.ui_manager.update_life_icons(self.game_state.lives)

    def game_over(self):
        self.game_over_screen.show()
        if self.game_over_screen.ask_to_play_again():
            self.restart_game()
        else:
            self.running = False

    def ask_for_name(self):
        # Implement the name input logic here
        pass

    def next_level(self):
        if self.level_manager.next_level():
            self.restart_game()
        else:
            self.running = False

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()