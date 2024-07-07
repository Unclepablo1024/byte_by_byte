

import pygame

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.sprites = []
        self.load_sprite_sheet(picture_path)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 100)  # Initial position
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 0.1  # Milliseconds per frame
        self.current_frame = 0

    def load_sprite_sheet(self, picture_path):
        sprite_sheet = pygame.image.load(picture_path).convert_alpha()
        sheet_width, sheet_height = sprite_sheet.get_size()

        # Assuming all frames are in a single row
        num_frames = 6  # Number of frames in the sprite sheet
        frame_width = sheet_width // num_frames
        frame_height = sheet_height

        for i in range(num_frames):
            frame_x = i * frame_width
            frame_rect = pygame.Rect(frame_x, 0, frame_width, frame_height)
            frame = sprite_sheet.subsurface(frame_rect)
            self.sprites.append(frame)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
            self.image = self.sprites[self.current_frame]

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
