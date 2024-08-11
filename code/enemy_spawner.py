import pygame
import random
import os
from enemy import Enemy
import config


def spawn_enemy(self):
    # Check if the dialog box is active
    if self.dialog_box.active:
        print("Dialog box is active, delaying enemy spawn.")
        return  # Exit the function without spawning an enemy

    if self.enemy_count + 1 >= self.max_enemies:
        return  # Stop spawning if max enemies are reached

    try:
        enemy_type = random.choice(self.current_enemies)
        print(f"Selected enemy type: {enemy_type}")
        new_enemy = Enemy(enemy_type, os.path.join(config.BASE_SPRITES_PATH, 'enemies'), self.surface.get_width(), 560,
                            self.character)
        self.enemy_group.add(new_enemy)
        self.all_sprites.add(new_enemy)
        # Do not increment enemy_count here; it should only increment on enemy death
    except FileNotFoundError as e:
        print(f"Error spawning enemy: {e}")

def draw_enemy_counter(self):
    font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 32)  # Adjust the font size as needed
    counter_text = f"{self.enemy_count + 0}/{self.max_enemies}"
    text_surface = font.render(counter_text, True, (255, 255, 255))  # White text
    self.surface.blit(text_surface, (10, 10))