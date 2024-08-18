import pygame
import os
from background import Background
from enemy import Enemy
import config

def set_level(game, level):
    print(f"Setting level: {level}")
    level_settings = config.LEVELS.get(level)

    if level_settings:
        print(f"Loading background for level {level}: {level_settings['background']}")
        try:
            game.background = Background(str(level_settings["background"]), config.BACKGROUND_SIZE)
        except Exception as e:
            print(f"Error loading background: {str(e)}")
        game.current_enemies = level_settings["enemies"]
        print(f"Enemies for level {level}: {game.current_enemies}")

        # Stop the current music and play the new level's music
        if game.music_player:
            game.music_player.stop_main_music()

        if 'music' in level_settings:
            music_path = level_settings["music"]
            print(f"Attempting to play music for level {level}: {music_path}")
            if os.path.exists(music_path):
                try:
                    game.music_player.play_music(music_path)
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
            game.background = Background(str(config.LEVELS[1]["background"]), config.BACKGROUND_SIZE)
        except Exception as e:
            print(f"Error loading default background: {str(e)}")
        game.current_enemies = config.LEVELS[1]["enemies"]
        if game.music_player:
            game.music_player.stop_main_music()
        if 'music' in config.LEVELS[1]:
            try:
                game.music_player.play_music(config.LEVELS[1]["music"])
                print("Default music started")
            except Exception as e:
                print(f"Error playing default music: {str(e)}")

    game.current_level = level
    print(f"Level set to {game.current_level}")

    # Reset game state for the new level
    game.enemy_count = 0
    game.defeated_enemies = 0  # Reset the defeated enemies count
    game.enemy_group.empty()
    game.all_sprites.remove([sprite for sprite in game.all_sprites if isinstance(sprite, Enemy)])

    # Reset character position
    game.character.rect.x = config.CHARACTER_INITIAL_X
    game.character.rect.y = config.CHARACTER_GROUND_LEVEL
    print(f"Character position reset to ({game.character.rect.x}, {game.character.rect.y})")

    # Reset boss-related state
    game.boss = None
    game.boss_spawned = False
    game.boss_trigger = False
    game.boss_deaths = 0  # Reset boss deaths if necessary

    # Reset enemy spawn timer
    game.enemy_spawn_timer = pygame.time.get_ticks()

    # Check if music is playing
    if pygame.mixer.music.get_busy():
        print("Music is currently playing")
    else:
        print("No music is playing")

    print(f"Level {level} setup complete")






def next_level(game):
    # Function handles the update of levels
    game.current_level += 1
    print(f"Moving to level {game.current_level}")  # Debugging
    if game.current_level > len(config.LEVELS):
        print("You have completed all levels!")
        game.running = False
    else:
        set_level(game, game.current_level)
        print(f"Level set to {game.current_level}")  # Debugging
        game.restart_game()

    # Set boss_trigger back to False
    game.boss_trigger = False


def restart_level(game):
    game.current_question_index = 0
    game.correct_answers = 0
    game.questions = config.get_random_questions(game.total_questions)
    game.health_bar.reset()
    game.current_attempt = 0
    game.waiting_for_answer = False