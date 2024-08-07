import pygame
import config
from healthbar import HealthBar


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, idle_picture_path, walk_gif_path, jump_gif_path, run_gif_path, hurt_gif_path, die_gif_path,
                 attack_1_gif_path, attack_2_gif_path, attack_3_gif_path):
        super().__init__()
        self.idle_image = pygame.image.load(idle_picture_path).convert_alpha()
        self.walk_frames = self.load_gif_frames(walk_gif_path)
        self.jump_frames = self.load_gif_frames(jump_gif_path)
        self.run_frames = self.load_gif_frames(run_gif_path)
        self.hurt_frames = self.load_gif_frames(hurt_gif_path)
        self.die_frames = self.load_gif_frames(die_gif_path)
        self.attack_animations = [
            self.load_gif_frames(attack_1_gif_path),
            self.load_gif_frames(attack_2_gif_path),
            self.load_gif_frames(attack_3_gif_path)
        ]
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-150, -150)
        self.health_bar = HealthBar()
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.current_frame = 0
        self.is_walking = False
        self.is_jumping = False
        self.is_running = False
        self.is_hurt = False
        self.is_dead = False
        self.is_attacking = False
        self.attack_index = 0
        self.attack_damage = 10
        self.vertical_velocity = 0
        self.gravity = config.CHARACTER_GRAVITY
        self.jump_strength = config.CHARACTER_JUMP_STRENGTH
        self.ground_level = config.CHARACTER_GROUND_LEVEL
        self.rect.topleft = (config.CHARACTER_INITIAL_X, self.ground_level)
        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.blocked_direction = None

    def load_gif_frames(self, gif_path):
        gif = pygame.image.load(gif_path).convert_alpha()
        gif_width, gif_height = gif.get_size()
        frames = []
        for i in range(gif_width // gif_height):
            frame_rect = pygame.Rect(i * gif_height, 0, gif_height, gif_height)
            frame = gif.subsurface(frame_rect)
            frames.append(frame)
        return frames

    def update(self):
        now = pygame.time.get_ticks()
        if self.is_dead:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = min(self.current_frame + 1, len(self.die_frames) - 1)
                self.image = self.die_frames[self.current_frame]
            return

        if self.is_hurt:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.hurt_frames)
                if self.current_frame == 0:
                    self.is_hurt = False
                self.image = self.hurt_frames[self.current_frame]
            return

        if self.is_jumping:
            self.vertical_velocity += self.gravity
            self.rect.y += self.vertical_velocity
            if self.rect.y >= self.ground_level:
                self.rect.y = self.ground_level
                self.is_jumping = False
                self.vertical_velocity = 0

            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
                self.image = self.jump_frames[self.current_frame]

        elif self.is_running:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.image = self.run_frames[self.current_frame]

        elif self.is_walking:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame]

        elif self.is_attacking:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_animations[self.attack_index])
                if self.current_frame == 0:
                    self.is_attacking = False
                self.image = self.attack_animations[self.attack_index][self.current_frame]

        else:
            self.image = self.idle_image

    def move(self, dx, dy):
        if self.is_dead:
            return

        if (self.blocked_direction == 'right' and dx > 0) or (self.blocked_direction == 'left' and dx < 0):
            dx = 0  # Prevent movement in the blocked direction

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if 0 <= new_x <= self.screen_width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= self.ground_level:
            self.rect.y = new_y

    def jump(self):
        if not self.is_jumping and not self.is_dead:
            self.is_jumping = True
            self.current_frame = 0
            self.image = self.jump_frames[self.current_frame]
            self.vertical_velocity = self.jump_strength

    def hurt(self, damage):
        if not self.is_dead:
            self.is_hurt = True
            self.health_bar.update_health(-damage)
            if self.health_bar.current_health <= 0:
                self.die()
            else:
                self.image = self.hurt_frames[0]

    def stop_hurt(self):
        self.is_hurt = False

    def die(self):
        self.is_dead = True
        self.current_frame = 0
        self.image = self.die_frames[self.current_frame]

    def revive(self):
        self.is_dead = False
        self.health_bar.reset()
        self.image = self.idle_image
        self.rect.topleft = (100, 430)  # Reset to starting position
        self.is_jumping = False  # Reset jumping state

    def stop_movement(self, direction):
        self.blocked_direction = direction

    def resume_movement(self):
        self.blocked_direction = None

    def set_running(self, running):
        self.is_running = running

    def set_walking(self, walking):
        self.is_walking = walking

    def attack(self):
        if not self.is_attacking and not self.is_dead and not self.is_hurt and not self.is_jumping:
            self.is_attacking = True
            self.attack_index = (self.attack_index + 1) % len(self.attack_animations)
            self.current_frame = 0
