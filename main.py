import pygame, sys
from pygame.locals import *


#Main character class

class Main_character(pygame.sprite.Sprite):
   
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()


# We associate the sprites to the a group
character = Main_character("sprites/Gangsters_2/Idle.png")
character_group = pygame.sprite.Group()
character_group.add(character)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Byte by Byte")
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
