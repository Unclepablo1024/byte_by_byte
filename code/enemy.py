import pygame
import random
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, folder_path, screen_width, ground_level, main_character):
        super().__init__()
        self.folder_path = folder_path
        self.enemy_type = enemy_type
        self.walk_images = self.load_images("Walk.png")
        self.attack_images = self.load_images("Attack_1.png")
        self.dead_images = self.load_images("Dead.png")
        self.image = self.walk_images[0]
        self.rect = self.image.get_rect()
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # milliseconds per frame
        self.health = 100
        self.current_frame = 0
        self.state = "walking"
        self.is_dead = False
        self.screen_width = screen_width
        self.ground_level = ground_level
        self.main_character = main_character
        self.direction = -1  # -1 for left, 1 for right
        self.attack_distance = 50
        self.speed = 2
        self.reset_position()

    def load_images(self, action):
        images = []
        image_path = os.path.join(self.folder_path, self.enemy_type, action)
        image = pygame.image.load(image_path).convert_alpha()
        width, height = image.get_size()
        frame_height = height
        for i in range(width // frame_height):
            frame_rect = pygame.Rect(i * frame_height, 0, frame_height, frame_height)
            frame = image.subsurface(frame_rect)
            images.append(frame)
        return images

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
                    self.current_frame = (self.current_frame + 1) % len(self.attack_images)
                    self.image = self.attack_images[self.current_frame]
                elif self.state == "walking":
                    self.current_frame = (self.current_frame + 1) % len(self.walk_images)
                    self.image = self.walk_images[self.current_frame]

            self.image = pygame.transform.flip(self.image, self.direction == 1, False)
            
            new_rect = self.image.get_rect()
            new_rect.bottom = self.ground_level
            new_rect.centerx = self.rect.centerx
            self.rect = new_rect

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.bottom = self.ground_level  # 確保敵人保持在地面上

    def reset_position(self):
        self.rect.bottom = self.ground_level
        self.rect.left = self.screen_width + random.randint(50, 200)
        self.state = "walking"
        self.current_frame = 0
        self.image = self.walk_images[self.current_frame]
        self.direction = -1

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
        self.image = self.dead_images[self.current_frame]
        self.rect.bottom = self.ground_level  # 確保敵人死亡時仍在地面上