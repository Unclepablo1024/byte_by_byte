import pygame
from character import MainCharacter
from background import Background
from healthbar import HealthBar, LifeIcon
import config

def restart_level(game):
    # The function restarts the current level and all relevant level variables
    game.current_question_index = 0
    game.correct_answers = 0
    game.questions = config.get_random_questions(game.total_questions)
    game.health_bar.reset()
    game.current_attempt = 0
    game.waiting_for_answer = False

def restart_game(game):
    # This function restarts the game, including character, background, etc.
    game.character = MainCharacter(
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
    game.background = Background(config.BACKGROUND_IMAGE_PATH, config.BACKGROUND_SIZE)
    game.all_sprites = pygame.sprite.Group(game.character)
    game.enemy_group = pygame.sprite.Group()
    game.ground_level = config.CHARACTER_GROUND_LEVEL
    game.health_bar = HealthBar(config.HEALTH_BAR_MAX_HEALTH, config.HEALTH_BAR_WIDTH, config.HEALTH_BAR_HEIGHT,
                                config.HEALTH_BAR_X, config.HEALTH_BAR_Y, config.HEALTH_BAR_COLOR)
    game.life_icons = []
    game.lives = config.INITIAL_LIVES
    game.scroll_speed = config.SCROLL_SPEED - 1  # Decrease player speed
    game.dialog_cooldown = 0
    game.dialog_cooldown_time = config.DIALOG_COOLDOWN_TIME
    game.death_timer = None
    game.spawned_enemies = []
    game.enemy_spawn_timer = pygame.time.get_ticks()

    # Sets life icons when restarting
    life_icon_path = config.LIFE_ICON_PATH
    life_icon_size = config.LIFE_ICON_SIZE
    life_icon_spacing = config.LIFE_ICON_SPACING

    # Sets the health bar when restarting
    health_bar_x = game.health_bar.x
    health_bar_y = game.health_bar.y
    health_bar_height = game.health_bar.height
    for i in range(game.lives):
        icon_x = health_bar_x + i * (life_icon_size + life_icon_spacing) * 0.7
        icon_y = health_bar_y - health_bar_height - 20
        icon = LifeIcon(icon_x, icon_y, life_icon_size, life_icon_size, life_icon_path)
        game.life_icons.append(icon)

    game.set_level(game.current_level)  # Ensure the correct background is set