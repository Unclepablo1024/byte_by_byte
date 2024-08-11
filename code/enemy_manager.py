import pygame
import random
import os
import config
from enemy import Enemy


class EnemyManager:
    def __init__(self, surface, character, max_enemies, all_sprites):
        self.surface = surface
        self.character = character
        self.max_enemies = max_enemies
        self.enemy_group = pygame.sprite.Group()
        self.all_sprites = all_sprites
        self.enemy_count = 0
        self.enemy_spawn_timer = pygame.time.get_ticks()
        self.current_enemies = []

    def set_current_enemies(self, enemies):
        self.current_enemies = enemies

    def spawn_enemy(self):
        if self.enemy_count + 1 >= self.max_enemies:
            return

        try:
            enemy_type = random.choice(self.current_enemies)
            new_enemy = Enemy(enemy_type, os.path.join('../sprites', 'enemies'), self.surface.get_width(), 560, self.character)
            self.enemy_group.add(new_enemy)
            self.all_sprites.add(new_enemy)
        except FileNotFoundError as e:
            print(f"Error spawning enemy: {e}")

    def update_enemies(self, dialog_box):
        now = pygame.time.get_ticks()
        if now - self.enemy_spawn_timer > 3000 and len(self.enemy_group) < self.max_enemies:
            self.spawn_enemy()
            self.enemy_spawn_timer = now

        for enemy in self.enemy_group:
            if enemy.is_dead:
                continue

            if enemy.attack and not dialog_box.dialogue_shown:
                dialog_box.show("The enemy is attacking! Prepare yourself!", auto_hide_seconds=3)

            if self.character.is_attacking and self.is_in_attack_range(enemy):
                enemy.mark_for_damage(pygame.time.get_ticks() + 10)

        for enemy in list(self.enemy_group):
            if enemy.is_dead and enemy.current_frame == len(enemy.dead_images) - 1:
                self.enemy_group.remove(enemy)
                self.enemy_count += 1

    def is_in_attack_range(self, enemy):
        distance = abs(self.character.rect.centerx - enemy.rect.centerx)
        return distance < config.ATTACK_RANGE

    def draw_enemy_counter(self, surface):
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 32)
        counter_text = f"{self.enemy_count + 0}/{self.max_enemies}"
        text_surface = font.render(counter_text, True, (255, 255, 255))
        surface.blit(text_surface, (10, 10))

    def draw(self, surface):
        self.enemy_group.draw(surface)
        for enemy in self.enemy_group:
            enemy.draw_rectangle(surface)
    
