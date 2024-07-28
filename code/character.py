import pygame
import config

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, idle_picture_path, walk_gif_path, jump_gif_path, run_gif_path, hurt_gif_path, die_gif_path):
        super().__init__()
        # Load images
        self.idle_image = pygame.image.load(idle_picture_path).convert_alpha()
        self.walk_frames = self.load_gif_frames(walk_gif_path)
        self.jump_frames = self.load_gif_frames(jump_gif_path)
        self.run_frames = self.load_gif_frames(run_gif_path)
        self.hurt_frames = self.load_gif_frames(hurt_gif_path)
        self.die_frames = self.load_gif_frames(die_gif_path)
        
        self.hurt_frames = self.load_gif_frames(hurt_gif_path)
        self.die_frames = self.load_gif_frames(die_gif_path)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        
        # Animation control variables
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Milliseconds per frame
        self.current_frame = 0
        
        # Movement and state variables
        self.is_walking = False
        self.is_jumping = False
        self.is_running = False
        self.is_hurt = False
        self.is_dead = False
        
        # Physics variables
        self.is_hurt = False
        self.is_dead = False
        self.vertical_velocity = 0
        self.gravity = config.CHARACTER_GRAVITY  # Gravity force
        self.jump_strength = config.CHARACTER_JUMP_STRENGTH  # Initial jump force
        self.ground_level = config.CHARACTER_GROUND_LEVEL  # Y position of the ground
        self.rect.topleft = (config.CHARACTER_INITIAL_X, self.ground_level)  # Initial position
        self.screen_width = config.SCREEN_WIDTH # Screen width
        self.screen_height = config.SCREEN_HEIGHT # Screen height

    def load_gif_frames(self, gif_path):
        gif = pygame.image.load(gif_path).convert_alpha()
        gif_width, gif_height = gif.get_size()
        frame_height = gif_height
        frames = []

        for i in range(gif_width // frame_height):
            frame_rect = pygame.Rect(i * frame_height, 0, frame_height, frame_height)
            frame = gif.subsurface(frame_rect)
            frames.append(frame)

        return frames

    def update(self):
        now = pygame.time.get_ticks()
        
        # Handle death animation
        if self.is_dead:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = min(self.current_frame + 1, len(self.die_frames) - 1)
                self.image = self.die_frames[self.current_frame]
            return
        
        # Handle hurt animation
        if self.is_hurt:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.hurt_frames)
                if self.current_frame == 0:
                    self.is_hurt = False
                self.image = self.hurt_frames[self.current_frame]
            return
        
        # Handle jumping animation
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
        
        # Handle running animation
        elif self.is_running:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.image = self.run_frames[self.current_frame]
        
        # Handle walking animation
        elif self.is_walking:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame]
        
        # Default to idle animation
        else:
            self.image = self.idle_image

    def move(self, dx, dy):
        if self.is_dead:
            return
        
    def move(self, dx, dy):
        if self.is_dead:
            return
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Check boundaries for the character
        if 0 <= new_x <= self.screen_width - self.rect.width:
            self.rect.x = new_x
        
        if 0 <= new_y <= self.ground_level:
            self.rect.y = new_y

    def set_walking(self, walking):
        self.is_walking = walking

    def set_running(self, running):
        self.is_running = running

    def jump(self):
        if not self.is_jumping and not self.is_dead:
            self.is_jumping = True
            self.current_frame = 0
            self.image = self.jump_frames[self.current_frame]
            self.vertical_velocity = self.jump_strength

    def hurt(self):
        if not self.is_dead:
            self.is_hurt = True
            self.current_frame = 0
            self.image = self.hurt_frames[self.current_frame]

    def stop_hurt(self):
        self.is_hurt = False

    def die(self):
        self.is_dead = True
        self.current_frame = 0
        self.image = self.die_frames[self.current_frame]

    def revive(self):
        self.is_dead = False
        self.image = self.idle_image
        self.rect.topleft = (100, 430)  # Reset to starting position or any appropriate position
        # Reset other necessary states here
        
    def reset(self):
        self.is_dead = False
        self.rect.bottom = 560

    def hurt(self):
        if not self.is_dead:
            self.is_hurt = True
            self.current_frame = 0
            self.image = self.hurt_frames[self.current_frame]

    def stop_hurt(self):
        self.is_hurt = False

    def die(self):
        self.is_dead = True
        self.current_frame = 0
        self.image = self.die_frames[self.current_frame]
