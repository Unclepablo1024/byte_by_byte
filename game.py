import pygame, sys
from pygame.locals import *
from character import MainCharacter

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Byte by Byte")
        self.clock = pygame.time.Clock()
        self.character = MainCharacter("sprites/Gangsters_2/Idle.png")
        self.character_group = pygame.sprite.Group(self.character)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.character.move(0, -5)
                elif event.key == K_DOWN:
                    self.character.move(0, 5)
                elif event.key == K_LEFT:
                    self.character.move(-5, 0)
                elif event.key == K_RIGHT:
                    self.character.move(5, 0)

    def update(self):
        self.character.update()

    def draw(self):
        self.surface.fill((0, 0, 0))  # Clear the screen with black
        self.character_group.draw(self.surface)  # Draw the character group on the surface
        pygame.display.flip()  # Update the display

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
