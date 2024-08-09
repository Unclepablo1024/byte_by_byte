import pygame
import config
import os


class Boss(pygame.sprite.Sprite):
    def __init__(self, folder_path, screen_width, ground_level, main_character):
        super().__init__("Boss1", folder_path, screen_width, ground_level, main_character)
        self.boss_walk_images = self.load_images("Walk.png")
        self.boss_attack_images = self.load_images("Attack.png")
        self.boss_dead_images = self.load_images("Dead.png")
        self.image = self.boss_walk_images[0]
        self.state = "walking"
        self.attack_distance = 100  # Boss might have a different attack distance
        self.special_ability_ready = True

    def update(self):
        now = pygame.time.get_ticks()
        if self.main_character and not self.is_dead:
            player_x = self.main_character.rect.centerx
            enemy_x = self.rect.centerx
            distance = abs(player_x - enemy_x)

            if distance < self.attack_distance:
                self.attack()
                self.direction = 1 if player_x > enemy_x else -1
            else:
                self.stop_attack()
                self.direction = -1

            if self.state == "walking":
                self.move(self.speed * self.direction, 0)

            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.state == "attacking":
                    self.current_frame = (self.current_frame + 1) % len(self.boss_attack_images)
                    self.image = self.boss_attack_images[self.current_frame]
                elif self.state == "walking":
                    self.current_frame = (self.current_frame + 1) % len(self.boss_walk_images)
                    self.image = self.boss_walk_images[self.current_frame]

            self.image = pygame.transform.flip(self.image, self.direction == 1, False)

            new_rect = self.image.get_rect()
            new_rect.bottom = self.ground_level
            new_rect.centerx = self.rect.centerx
            self.rect = new_rect

    def attack(self):
        if self.state != "attacking":
            self.state = "attacking"
            self.current_frame = 0

    def stop_attack(self):
        if self.state != "walking":
            self.state = "walking"
            self.current_frame = 0

    def die(self):
        self.is_dead = True
        self.current_frame = 0
        self.image = self.boss_dead_images[self.current_frame]
        self.rect.bottom = self.ground_level

    # Add any special abilities or behaviors here
    def special_ability(self):
        if self.special_ability_ready:
            # Implement the special ability logic
            self.special_ability_ready = False
            # Cooldown or special effect here
