import pygame
import config


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load images from config paths
        self.images = {
            "idle": [pygame.image.load(config.IDLE_PATH).convert_alpha()],
            "walk": [pygame.image.load(config.WALK_PATH).convert_alpha()],
            "jump": [pygame.image.load(config.JUMP_PATH).convert_alpha()],
            "run": [pygame.image.load(config.RUN_PATH).convert_alpha()],
            "hurt": [pygame.image.load(config.HURT_PATH).convert_alpha()],
            "die": [pygame.image.load(config.DIE_PATH).convert_alpha()]
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
        self.rect = pygame.Rect(100, self.ground_level, self.images["idle"][0].get_width(), self.images["idle"][0].get_height())  # Initialize rect
        self.screen_width = 800  # Example screen width
        self.screen_height = 600  # Example screen height

        # Initialize current animation
        self.image = self.images["idle"][0]

        # Initialize big boss walking out state
        self.walking_out = False


    def update(self):
        now = pygame.time.get_ticks()

        if self.walking_out:
            # Move boss out of the screen to the left
            self.rect.x -= 5  # Adjust speed as needed
            if self.rect.right < 0:  # If the boss is completely off-screen
                self.kill()  # Remove boss from all groups
            return

        # Handle other animations
        if self.is_dead:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images["die"])
                self.image = self.images["die"][self.current_frame]
                if self.current_frame == 0:  # Optional: Stop the animation after one loop
                    return
            return

        if self.is_hurt:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images["hurt"])
                if self.current_frame == 0:
                    self.is_hurt = False
                self.image = self.images["hurt"][self.current_frame]
            return

        if self.is_jumping:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images["jump"])
                if self.current_frame == 0:
                    self.is_jumping = False
                self.image = self.images["jump"][self.current_frame]
            return

        if self.is_running:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images["run"])
                self.image = self.images["run"][self.current_frame]
            return

        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images["idle"])
            self.image = self.images["idle"][self.current_frame]

    def set_walking(self, walking):
        self.is_walking = walking
        if walking:
            self.image = self.images["walk"][0]
            self.walking_out = True  # Start walking out
        else:
            self.image = self.images["idle"][0]

    def set_jumping(self, jumping):
        self.is_jumping = jumping

    def set_running(self, running):
        self.is_running = running

    def set_hurt(self, hurt):
        self.is_hurt = hurt

    def set_dead(self, dead):
        self.is_dead = dead
