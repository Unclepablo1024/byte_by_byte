import config
from background import Background
import os
import pygame

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.current_level = 1
        self.background = None  
        self.set_level(1)  

    def set_level(self, level):
        print(f"Setting level: {level}")
        level_settings = config.LEVELS.get(level)
        if level_settings:
            print(f"Loading background for level {level}: {level_settings['background']}")
            try:
                self.background = Background(str(level_settings["background"]), config.BACKGROUND_SIZE)
            except Exception as e:
                print(f"Error loading background: {str(e)}")
            self.game.enemy_manager.set_current_enemies(level_settings["enemies"])
            print(f"Enemies for level {level}: {self.game.enemy_manager.current_enemies}")

            if self.game.music_player:
                self.game.music_player.stop_main_music()

            if 'music' in level_settings:
                music_path = level_settings["music"]
                print(f"Attempting to play music for level {level}: {music_path}")
                if os.path.exists(music_path):
                    try:
                        self.game.music_player.play_music(music_path)
                        print(f"Music started for level {level}")
                    except Exception as e:
                        print(f"Error playing music: {str(e)}")
                else:
                    print(f"Music file not found: {music_path}")
            else:
                print(f"No music specified for level {level}")
        else:
            print(f"Level {level} not found in configuration. Using default level 1 settings.")
            try:
                self.background = Background(str(config.LEVELS[1]["background"]), config.BACKGROUND_SIZE)
            except Exception as e:
                print(f"Error loading default background: {str(e)}")
            self.game.enemy_manager.set_current_enemies(config.LEVELS[1]["enemies"])
            if self.game.music_player:
                self.game.music_player.stop_main_music()
            if 'music' in config.LEVELS[1]:
                try:
                    self.game.music_player.play_music(config.LEVELS[1]["music"])
                    print("Default music started")
                except Exception as e:
                    print(f"Error playing default music: {str(e)}")

        self.current_level = level
        print(f"Level set to {self.current_level}")

        # Reset character position
        self.game.character.rect.x = config.CHARACTER_INITIAL_X
        self.game.character.rect.y = config.CHARACTER_GROUND_LEVEL
        print(f"Character position reset to ({self.game.character.rect.x}, {self.game.character.rect.y})")

        # Reset enemy spawn timer
        self.game.enemy_manager.enemy_spawn_timer = pygame.time.get_ticks()

        print(f"Level {level} setup complete")

    def next_level(self):
        self.current_level += 1
        print(f"Moving to level {self.current_level}")
        if self.current_level > len(config.LEVELS):
            print("You have completed all levels!")
            return False
        else:
            self.set_level(self.current_level)
            print(f"Level set to {self.current_level}")
            return True

    def draw_background(self, surface):
        if self.background:
            self.background.draw(surface)