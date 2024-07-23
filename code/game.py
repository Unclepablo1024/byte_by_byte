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
import config

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Byte by Byte")
        self.clock = pygame.time.Clock()
        self.running = True
        self.init_resources()
        self.restart_game()

    def init_resources(self):
        self.music_player = MusicPlayer()
        self.dialog_box = DialogBox(self.surface, 600, 151)
        self.death_sound = pygame.mixer.Sound(config.DEATH_SOUND_PATH)
    
    def show_dialog(self, message):
        self.dialog_box.show(message)

    def restart_game(self):
        self.character = MainCharacter(
            config.IDLE_PICTURE_PATH,
            config.WALK_GIF_PATH,
            config.JUMP_GIF_PATH,
            config.RUN_GIF_PATH,
            config.HURT_GIF_PATH,
            config.DIE_GIF_PATH
        )
        self.background = Background(config.BACKGROUND_IMAGE_PATH, config.BACKGROUND_SIZE)
        self.all_sprites = pygame.sprite.Group(self.character)
        self.enemy_group = pygame.sprite.Group()
        self.ground_level = config.CHARACTER_GROUND_LEVEL
        self.health_bar = HealthBar(config.HEALTH_BAR_MAX_HEALTH, config.HEALTH_BAR_WIDTH, config.HEALTH_BAR_HEIGHT, config.HEALTH_BAR_X, config.HEALTH_BAR_Y, config.HEALTH_BAR_COLOR)
        self.life_icons = []
        self.lives = config.INITIAL_LIVES
        self.scroll_speed = config.SCROLL_SPEED
        self.dialog_cooldown = 0
        self.dialog_cooldown_time = config.DIALOG_COOLDOWN_TIME  # 2sec cooldown
        self.death_timer = None  # initialize death timer
        self.spawned_enemies = []
        self.enemy_spawn_timer = pygame.time.get_ticks()

        life_icon_path = config.LIFE_ICON_PATH
        life_icon_size = config.LIFE_ICON_SIZE
        life_icon_spacing = config.LIFE_ICON_SPACING

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
            self.dialog_box.update()  # update dialog box
            self.draw()  
            self.dialog_box.draw()  # draw dialog box
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
                dx *= config.RUN_SPEED_MULTIPLIER # Increase the speed while sprinting

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
                        self.show_dialog(f"Welcome to Level 1....\nNow we will have some task for you. \nAre you ready?!")
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
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 160)
        text = font.render('GAME OVER', True, (186, 85, 211))
        text_rect = text.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2))
        self.surface.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(500)  # Wait for 0.5 second
        # Ask if the user wants to play again
        self.ask_to_play_again()

    def ask_to_play_again(self):
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 60)
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
