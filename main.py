import pygame, sys
from pygame.locals import *

# Function to extract frames from a sprite sheet
def extract_frames(sheet, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

# Main character class
class Main_character(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.sprites = []
        # Load the sprite sheet
        sprite_sheet = pygame.image.load(picture_path).convert_alpha()
        # Extract frames
        frame_width = 80
        frame_height = 128
        num_frames = 6
        self.sprites = extract_frames(sprite_sheet, frame_width, frame_height, num_frames)
        # Set the initial image to the first frame
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 100)  # Initial position
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Milliseconds per frame


# Initialize Pygame and create the display
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Byte by Byte")

# We associate the sprites to the a group
character = Main_character("sprites/Gangsters_2/Idle.png")
character_group = pygame.sprite.Group()
character_group.add(character)

class Game:
    def __init__(self) -> None:
        self.running = True
        self.surface = screen
        self.clock = pygame.time.Clock()

    def run(self):
        # Game Loop
        while self.running:
            # Handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        print("Key UP")
                    elif event.key == K_DOWN:
                        print("Key DOWN")
                    elif event.key == K_LEFT:
                        print("Key LEFT")
                    elif event.key == K_RIGHT:
                        print("Key RIGHT")

            self.surface.fill((0, 0, 0))  # Clear the screen with black
            character_group.draw(self.surface) # Draw the character group on the surface
            pygame.display.flip() # Update the display

            # Render at 60 FPS
            self.clock.tick(60)

        print("Quitting...")
        pygame.quit()
        raise SystemExit

def main() -> None:
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
