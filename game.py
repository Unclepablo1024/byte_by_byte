import pygame
import sys
from pygame.locals import *
from character import MainCharacter
from background import Background
from healthbar import HealthBar
from dialogue import Dialogue
import config

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Byte by Byte")
        self.clock = pygame.time.Clock()
        self.character = MainCharacter(
            config.IDLE_PICTURE_PATH,
            config.WALK_GIF_PATH,
            config.JUMP_GIF_PATH,
            config.RUN_GIF_PATH,
            config.HURT_GIF_PATH,
            config.DIE_GIF_PATH
        )

        self.background = Background(config.BACKGROUND_IMAGE_PATH, config.BACKGROUND_SIZE)
        self.character_group = pygame.sprite.Group(self.character)

        # Dialogue Box
        self.dialogue = Dialogue(self.surface, config.DIALOGUE_FONT_SIZE)

        # Health Bar
        self.health_bar = HealthBar(100, config.HEALTH_BAR_WIDTH, config.HEALTH_BAR_HEIGHT, 
        config.HEALTH_BAR_X, config.HEALTH_BAR_Y, config.HEALTH_BAR_COLOR)

        # Movement Speed
        self.scroll_speed = config.SCROLL_SPEED

        #Dialogue Visibility
        self.show_dialogue = False

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
            dx = -config.SCROLL_SPEED
            moving = True
        if keys[K_RIGHT]:
            dx = config.SCROLL_SPEED
            moving = True
        if keys[K_UP] and not self.character.is_jumping:
            self.character.jump()
            moving = True
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            if keys[K_LEFT] or keys[K_RIGHT]:
                running = True
                dx *= config.RUN_SPEED_MULTIPLIER  # Increase the speed while sprinting
        if keys[K_h]:
            self.character.hurt()
            self.health_bar.update_health(-5)
            if self.health_bar.current_health <= 0:
                self.character.die()

        if keys[K_d]:
            self.show_dialogue = not self.show_dialogue


        self.character.set_running(running)
        self.character.set_walking(moving and not self.character.is_jumping and not running)
        self.character.move(dx, dy)

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[K_RIGHT] and not self.character.is_dead:
            dx = self.scroll_speed

        self.background.update(dx)
        self.character.update()

    def draw(self):
        self.surface.fill((0, 0, 0))  # Clear the screen with black
        self.background.draw(self.surface)  # Load the background
        self.character_group.draw(self.surface) # Draw the character group on the surface

        # Draw the health bar
        self.health_bar.draw(self.surface)

        if self.show_dialogue:
            self.dialogue.draw()  # Dialogue box

        pygame.display.flip()  # Update the display


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
