import pygame
import random
import os
from enemy import Enemy
import config

def spawn_enemy(game):
    if game.dialog_box.active or game.boss_spawned:
        print("Dialog box is active or boss has spawned, delaying enemy spawn.")
        return

    if game.enemy_count >= config.MAX_ENEMIES:
        return

    try:
        enemy_type = random.choice(game.current_enemies)
        print(f"Selected enemy type: {enemy_type}")
        new_enemy = Enemy(enemy_type, os.path.join(config.BASE_SPRITES_PATH, 'enemies'),
                          game.surface.get_width(), config.ENEMY_POSITION,
                          game.character)
        game.enemy_group.add(new_enemy)
        game.all_sprites.add(new_enemy)
        game.enemy_count += 1
        print(f"Enemy spawned. Total count: {game.enemy_count}")
    except FileNotFoundError as e:
        print(f"Error spawning enemy: {e}")



