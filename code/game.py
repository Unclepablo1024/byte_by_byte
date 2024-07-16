import pygame
import sys
import random
from pygame.locals import *
from enemy import Enemy
from background import Background
from healthbar import HealthBar
from music import MusicPlayer
from character import MainCharacter

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Byte by Byte")
        self.clock = pygame.time.Clock()
        self.character = MainCharacter(
            "../sprites/Gangsters_2/Idlefix.png",
            "../sprites/Gangsters_2/Walk.png",
            "../sprites/Gangsters_2/Jump.png",
            "../sprites/Gangsters_2/Run.png",
            "../sprites/Gangsters_2/Hurt.png",
            "../sprites/Gangsters_2/Dead.png"
        )

        self.background = Background("../sprites/backgrounds/City2_pale.png", (800, 600))
        self.all_sprites = pygame.sprite.Group(self.character)
        self.enemy_group = pygame.sprite.Group()
        self.ground_level = 430
        
        # Health Bar
        self.health_bar = HealthBar(100, 200, 20, 600 - 30, 10, (0, 255, 0))

        # Movement Speed
        self.scroll_speed = 5

        # Initialize MusicPlayer
        self.music_player = MusicPlayer()

        # List to track spawned enemies
        self.spawned_enemies = []

        # Spawn timer for enemies
        self.enemy_spawn_timer = pygame.time.get_ticks()

    def run(self):
        self.music_player.play_main_music()  # Start playing the main music
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(60)

        self.music_player.stop_main_music()  # Stop the main music when the game ends
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
        self.all_sprites.update()

        # Spawn enemies randomly
        now = pygame.time.get_ticks()
        if now - self.enemy_spawn_timer > 3000:  # spawn interval in milliseconds
            self.spawn_enemy()
            self.enemy_spawn_timer = now

        # Update enemies
        for enemy in self.enemy_group:
            if pygame.sprite.collide_rect(self.character, enemy):
                enemy.attack()

        # Remove off-screen enemies
        for enemy in self.enemy_group:
            if enemy.rect.right < 0:
                enemy.kill()

    def spawn_enemy(self):
    # Determine enemy type randomly for demonstration
        available_types = ["Homeless_1", "Homeless_2", "Homeless_3"]
        available_types = [type for type in available_types if type not in self.spawned_enemies]

        if available_types:
            enemy_type = random.choice(available_types)
            new_enemy = Enemy(enemy_type, "../sprites/enemies", self.surface.get_width(), 560, self.character)
            self.all_sprites.add(new_enemy)
            self.enemy_group.add(new_enemy)
            self.spawned_enemies.append(enemy_type)


    def draw(self):
        self.surface.fill((0, 0, 0))  # Clear the screen with black
        self.background.draw(self.surface)  # Draw the background
        self.all_sprites.draw(self.surface)  # Draw all sprites
        self.health_bar.draw(self.surface)  # Draw the health bar
        pygame.display.flip()  # Update the display

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
