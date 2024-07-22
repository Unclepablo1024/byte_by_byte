import pygame
import sys
import random
from pygame.locals import *
from enemy import Enemy
from background import Background
from healthbar import HealthBar, LifeIcon
from music import MusicPlayer
from character import MainCharacter
from dialog import DialogBox

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Byte by Byte")
        self.clock = pygame.time.Clock()
        self.running = True
        self.init_resources()
        self.restart_game()

    def init_resources(self):
        self.music_player = MusicPlayer()
        self.dialog_box = DialogBox(self.surface, 600, 150)
        self.death_sound = pygame.mixer.Sound("../audio/pain-scream.wav")

    def restart_game(self):
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
        self.health_bar = HealthBar(100, 200, 20, 600 - 30, 30, (0, 255, 0))
        self.life_icons = []
        self.lives = 5
        self.scroll_speed = 5
        self.dialog_cooldown = 0
        self.dialog_cooldown_time = 2000  # 2sec cooldown
        self.death_timer = None  # initialize death timer
        self.spawned_enemies = []
        self.enemy_spawn_timer = pygame.time.get_ticks()

        life_icon_path = "../sprites/life_icon.png"
        life_icon_size = 52  
        life_icon_spacing = 1

        health_bar_x = self.health_bar.x
        health_bar_y = self.health_bar.y
        health_bar_height = self.health_bar.height

        for i in range(self.lives):
            icon_x = health_bar_x + i * (life_icon_size + life_icon_spacing) * 0.7
            icon_y = health_bar_y - health_bar_height - 20
            icon = LifeIcon(icon_x, icon_y, life_icon_size, life_icon_size, life_icon_path)
            self.life_icons.append(icon)
        
    
    def run(self):
        self.music_player.play_main_music()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        self.music_player.stop_main_music()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.dialog_box.active:
                if self.dialog_box.handle_event(event):
                    print("Dialog closed")  # Debug print
            elif event.type == pygame.KEYDOWN:
                self.handle_player_input(event)

        if not self.dialog_box.active:
            self.handle_continuous_input()

    def handle_player_input(self, event):
        if event.key == pygame.K_h:
            self.character.hurt()
            self.health_bar.update_health(-5)  # Decrease health by 5 units
            if self.health_bar.current_health <= 0:
                self.handle_character_death()

    def handle_continuous_input(self):
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

    def revive_character(self):
        self.character.revive()
        self.health_bar.reset()
        self.death_timer = None
        
    def handle_character_death(self):
        if not self.character.is_dead:
            print("Character is dying")  # Debug print
            self.lives -= 1
            self.character.die()
            self.death_sound.play()  # Play death sound here
            if self.lives > 0:
                self.death_timer = pygame.time.get_ticks()
            else:
                self.death_timer = pygame.time.get_ticks() + 1000  # Additional time to show death animation

    def update(self):
        if not self.dialog_box.active:
            keys = pygame.key.get_pressed()
            dx = 0
            if keys[K_RIGHT] and not self.character.is_dead:
                dx = self.scroll_speed

            self.background.update(dx)
            self.all_sprites.update()

            now = pygame.time.get_ticks()
            if now - self.enemy_spawn_timer > 3000:
                self.spawn_enemy()
                self.enemy_spawn_timer = now

            # update cooldown time
            if self.dialog_cooldown > 0:
                self.dialog_cooldown -= self.clock.get_time()
                if self.dialog_cooldown < 0:
                    self.dialog_cooldown = 0

            for enemy in self.enemy_group:
                if pygame.sprite.collide_rect(self.character, enemy):
                    if self.dialog_cooldown == 0:
                        enemy.attack()
                        self.show_dialog(f"Enemy {enemy.enemy_type} is attacking!")
                        self.dialog_cooldown = self.dialog_cooldown_time

            for enemy in self.enemy_group:
                if enemy.rect.right < 0:
                    enemy.kill()

            if self.health_bar.is_depleted() and not self.character.is_dead:
                self.handle_character_death()

            if self.character.is_dead:
                current_time = pygame.time.get_ticks()
                if self.lives > 0 and current_time - self.death_timer >= 1000:  # 1000 milliseconds = 3 seconds
                    self.revive_character()
                elif self.lives == 0 and current_time - self.death_timer >= 1000:  # 1 second delay before game over
                    self.game_over()

    def spawn_enemy(self):
        available_types = ["Homeless_1", "Homeless_2", "Homeless_3"]
        available_types = [type for type in available_types if type not in self.spawned_enemies]

        if available_types:
            enemy_type = random.choice(available_types)
            new_enemy = Enemy(enemy_type, "../sprites/enemies", self.surface.get_width(), 560, self.character)
            self.all_sprites.add(new_enemy)
            self.enemy_group.add(new_enemy)
            self.spawned_enemies.append(enemy_type)

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.background.draw(self.surface)
        self.all_sprites.draw(self.surface)
        self.health_bar.draw(self.surface)
        for i in range(self.lives):
            self.life_icons[i].draw(self.surface)
        self.dialog_box.draw()
        pygame.display.flip()
        
    def game_over(self):
        print("Game Over")  # Debug print
        font = pygame.font.Font("../fonts/determinationsans.ttf", 160)
        text = font.render('GAME OVER', True, (186, 85, 211))
        text_rect = text.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2))
        self.surface.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(500)  # Wait for 0.5 second
        # Ask if the user wants to play again
        self.ask_to_play_again()

    def ask_to_play_again(self):
        font = pygame.font.Font("../fonts/determinationsans.ttf", 60)
        text = font.render('Play again? (Y/N)', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2 + 100))
        self.surface.blit(text, text_rect)
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        waiting_for_input = False
                        self.restart_game()
                    elif event.key == pygame.K_n:
                        waiting_for_input = False
                        self.running = False

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
