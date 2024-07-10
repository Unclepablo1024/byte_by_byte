import pygame
import sys
from pygame.locals import *
from character import MainCharacter
from background import Background


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Byte by Byte")
        self.clock = pygame.time.Clock()
        self.character = MainCharacter(
            "sprites/Gangsters_2/Idlefix.png",
            "sprites/Gangsters_2/Walk.png",
            "sprites/Gangsters_2/Jump.png",
            "sprites/Gangsters_2/Run.png"  # Update sprint animation path
        )

        self.background = Background("sprites/backgrounds/City2_pale.png", (800, 600))
        self.character_group = pygame.sprite.Group(self.character)

        #Movement Speed
        self.scroll_speed = 5

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

        keys = pygame.key.get_pressed()
        moving = False
        running = False
        dx, dy = 0, 0
        if keys[K_LEFT]:
            dx = -2
            moving = True
        if keys[K_RIGHT]:
            dx = 2
            moving = True
        if keys[K_UP] and not self.character.is_jumping:
            self.character.jump()
            moving = True
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            if keys[K_LEFT] or keys[K_RIGHT]:
                running = True
                dx *= 2  # Increase the speed while sprinting

        self.character.set_running(running)
        self.character.set_walking(moving and not self.character.is_jumping and not running)
        self.character.move(dx, dy)

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[K_RIGHT]:
            dx = self.scroll_speed

        self.background.update(dx)
        self.character.update()

    def draw(self):
        self.surface.fill((0, 0, 0))  # Clear the screen with black
        self.background.draw(self.surface) #Loading first map into the game
        self.character_group.draw(self.surface)  # Draw the character group on the surface
        pygame.display.flip()  # Update the display


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
