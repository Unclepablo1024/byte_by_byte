import pygame
from pygame.locals import *


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


            # Render screen

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
