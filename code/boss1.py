import pygame
import os

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Define the folder path and image file names
        BOSSES_FOLDER_PATH = os.path.join('sprites', 'Bosses', 'Boss1')

        self.images = {
            "idle": pygame.image.load(os.path.join(BOSSES_FOLDER_PATH, 'Idlefix.png')).convert_alpha(),
            "walk": pygame.image.load(os.path.join(BOSSES_FOLDER_PATH, 'Walk.png')).convert_alpha(),
            "jump": pygame.image.load(os.path.join(BOSSES_FOLDER_PATH, 'Jump.png')).convert_alpha(),
            "run": pygame.image.load(os.path.join(BOSSES_FOLDER_PATH, 'Run.png')).convert_alpha(),
            "hurt": pygame.image.load(os.path.join(BOSSES_FOLDER_PATH, 'Hurt.png')).convert_alpha(),
            "die": pygame.image.load(os.path.join(BOSSES_FOLDER_PATH, 'Dead.png')).convert_alpha()
        }

        # Initialize animation control variables
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
        self.vertical_velocity = 0
        self.gravity = 0.5  # Example value for gravity
        self.jump_strength = 10  # Example value for jump strength
        self.ground_level = 400  # Example ground level
        self.rect.topleft = (100, self.ground_level)  # Example initial position
        self.screen_width = 800  # Example screen width
        self.screen_height = 600  # Example screen height

        # Initialize current animation
        self.image = self.images["idle"]
        self.rect = self.image.get_rect()

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
                self.current_frame = (self.current_frame + 1) % len(self.images["die_frames"])
                self.image = self.images["die_frames"][self.current_frame]
                if self.current_frame == 0:  # Optional: Stop the animation after one loop
                    return
            return

        # Handle hurt animation
        if self.is_hurt:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images["hurt_frames"])
                if self.current_frame == 0:
                    self.is_hurt = False
                self.image = self.images["hurt_frames"][self.current_frame]
            return

        # Handle jumping animation
        if self.is_jumping:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images["jump_frames"])
                if self.current_frame == 0:
                    self.is_jumping = False
                self.image = self.images["jump_frames"][self.current_frame]
            return

        # Handle running animation
        if self.is_running:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images["run_frames"])
                self.image = self.images["run_frames"][self.current_frame]
            return

        # Default to idle animation
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images["idle_frames"])
            self.image = self.images["idle_frames"][self.current_frame]

    def set_walking(self, walking):
        self.is_walking = walking
        if walking:
            self.image = self.images["walk"]
        else:
            self.image = self.images["idle"]

    def set_jumping(self, jumping):
        self.is_jumping = jumping

    def set_running(self, running):
        self.is_running = running

    def set_hurt(self, hurt):
        self.is_hurt = hurt

    def set_dead(self, dead):
        self.is_dead = dead
