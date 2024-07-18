import sys
import pygame
from pygame.locals import *
import os
from character import MainCharacter
from background import Background
from healthbar import HealthBar

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.running = True
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Byte by Byte")
        self.clock = pygame.time.Clock()
        self.character = MainCharacter(
        "sprites/Gangsters_2/Idlefix.png",
        "sprites/Gangsters_2/Walk.png",
        "sprites/Gangsters_2/Jump.png",
        "sprites/Gangsters_2/Run.png",
        "sprites/Gangsters_2/Hurt.png",
        "sprites/Gangsters_2/Dead.png"
    )

# Define Screen
        self.background = Background("sprites/backgrounds/City2_pale.png", (800, 600))
        self.character_group = pygame.sprite.Group(self.character)

        # Health Bar
        self.health_bar = HealthBar(100, 200, 20, 600 - 30, 10, (0, 255, 0))

        # Movement Speed
        self.scroll_speed = 5
        self.font = pygame.font.SysFont('Arial', 24)

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
            if keys[K_h]:
                self.character.hurt()
                self.health_bar.update_health(-5)
                if self.health_bar.current_health <= 0:
                    self.character.die()
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

#Dialouge Box
    def draw(self):
        self.surface.fill((0, 0, 0))  # Clear the screen with black
        self.background.draw(self.surface)  # Draw the background
        self.character_group.draw(self.surface)  # Draw the character group

    # Draw the health bar
        self.health_bar.draw(self.surface)

    # Draw the dialogue box
        image_path = os.path.join('sprites', 'Dialouge', 'Dialouge boxes', 'BetterDialouge1.png')
        dialouge_box = pygame.image.load(image_path)
        self.surface.blit(dialouge_box,(100,100))
        dialouge_text = "Greetings Player!"

    #Font and text
        text_surface = self.render_text(dialouge_text, (255, 255, 255))  # White color
        self.surface.blit(text_surface, (150, 125))  # Adjust the position as needed
        #Font of the text
        pygame.display.flip()
    def render_text(self,text, color):
        text_surface = self.font.render(text, True, color)
        return text_surface

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()

    pygame.display.flip()



