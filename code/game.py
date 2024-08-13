import pygame
import sys
import os
from pygame.locals import *
import boss_mana
from boss1 import Boss
from enemy import Enemy
from background import Background
from healthbar import HealthBar, LifeIcon
from music import MusicPlayer
from character import MainCharacter
from dialog import DialogBox
import config
import event
from game_over import game_over, ask_to_play_again
from change_level import set_level, next_level, restart_level
from handle_input import ask_for_name, handle_player_input, handle_continuous_input, get_user_input
from restart import restart_game
from dialog_response import handle_dialog_response, ask_next_question, check_answer, set_timer
from enemy_spawner import spawn_enemy, draw_enemy_counter


# Initialize game and its components
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        icon = pygame.image.load(config.LOGO_PATH)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Byte by Byte")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level = 1
        self.current_enemies = config.LEVELS[self.current_level]["enemies"]
        self.spawned_enemies = []
        self.name = ""
        self.init_resources()
        self.max_enemies = config.MAX_ENEMIES  # Ensure this line is here
        self.dialog_box = DialogBox(self.surface, 600, 200)  # Moved this line up
        self.restart_game()

        self.current_question_index = 0
        self.current_attempt = 0
        self.attempts = 0
        self.max_attempts = 3
        self.questions = config.get_random_questions(5)
        self.waiting_for_answer = False
        self.correct_answers = 0
        self.total_questions = 5
        self.enemy_count = 0
        self.first_encounter = 0

        # Flag for dialogue trigger for levels
        self.dialogue_shown = False

        # Dialogue setup for change level to level
        self.boss_deaths = 1
        self.boss_trigger = False
        

    def init_resources(self):
        # Loads resources like music and sounds
        self.music_player = MusicPlayer()
        self.death_sound = pygame.mixer.Sound(config.DEATH_SOUND_PATH)

    def ask_for_name(self):
        self.name = ask_for_name(self)
    
    def change_level_dialogue(self):
        if self.boss_deaths in [1, 2, 3]:
            self.show_dialog(f"You have completed Level {self.boss_deaths}, press 'x' to continue!", auto_hide_seconds=5)

    def set_level(self, level):
        set_level(self, level)

    def next_level(self):
        next_level(self)

    def run(self):
        self.ask_for_name()
        while self.running:
            pygame.event.pump()  # Pump the event queue
            event.handle_events(self)  # Process input events
            self.update()  # Update game logic
            self.draw()  # Draw everything on the screen
            pygame.display.flip()  # Update display
            self.clock.tick(60)  # Maintain 60 FPS
        self.music_player.stop_main_music()
        pygame.quit()
        sys.exit()

    def show_dialog(self, message, auto_hide_seconds=None):
        self.dialog_box.show(message, auto_hide_seconds)
        pygame.event.clear()

    def handle_player_input(self, event):
        handle_player_input(self, event)

    def handle_continuous_input(self):
        handle_continuous_input(self)

    def get_user_input(self):
        return get_user_input(self)

    def restart_level(self):
        restart_level(self)
    

    def handle_dialog_response(self, response):
        handle_dialog_response(self, response)

    def ask_next_question(self):
        ask_next_question(self)

    def check_answer(self, response):
        return check_answer(self, response)

    def set_timer(self):
        set_timer(self)

    def revive_character(self):
        if self.lives > 0:
            print(f"Reviving character, lives remaining: {self.lives}")
            self.character.revive()
            self.update_life_icons()
        else:
            self.game_over()

    def die_gracefully(self):
        print("Graceful death initiated")
        while not self.character.is_dead:
            pass  # Wait until the character is dead
        pygame.time.wait(1500)  # Wait for 1.5 seconds

    def handle_character_death(self):
        self.lives -= 1
        self.character.die()
        self.death_sound.play()
        # self.die_gracefully()  # Wait for death animation to complete
        self.revive_character()

    def update_life_icons(self):
        print("Updating life icons")
        self.life_icons = self.life_icons[:self.lives]

        # Revives the character and resets game
        self.character.revive()
        self.health_bar.reset()
        self.death_timer = None

    def update(self):
        self.dialog_box.update()
        dx = 0

        if not self.dialog_box.active:
            keys = pygame.key.get_pressed()
            if keys[K_RIGHT] and not self.character.is_dead:
                dx = self.scroll_speed
            if keys[K_LEFT] and not self.character.is_dead:
                dx = -self.scroll_speed
            self.character.move(dx, 0)
            now = pygame.time.get_ticks()

            if now - self.enemy_spawn_timer > 3000 and len(self.enemy_group) != self.max_enemies:
                spawn_enemy(self)
                self.enemy_spawn_timer = now

            for enemy in self.enemy_group:
                if enemy.is_dead:
                    continue  # Skip processing for dead enemies

                if self.character.is_attacking and self.is_in_attack_range(enemy):
                    enemy.mark_for_damage(pygame.time.get_ticks() + 10)

                # Check for the first encounter with an enemy
                if not hasattr(self, 'first_encounter_triggered') and self.is_in_attack_range(enemy):
                    self.first_encounter_triggered = True
                    self.dialog_box.show_dialog("TIP -- (Use the left mouse button to attack!)", auto_hide_seconds=5)
                    self.dialog_box.set_style((3,3,3), os.path.join("pic", "s2.png"))

                    # Add the remaining dialogues to the queue
                    for counter in range(1, 5):
                        self.dialog_box.show_dialog(f"{config.LEVEL_ONE_DIALOGUE[counter]}", auto_hide_seconds=5)
                    break  # Exit the loop after showing the dialog for the first encounter

            collided = False
            for enemy in self.enemy_group:
                if not enemy.is_dead and pygame.sprite.collide_rect(self.character, enemy):
                    if self.character.rect.centerx < enemy.rect.centerx:
                        self.character.stop_movement('right')
                    else:
                        self.character.stop_movement('left')
                    collided = True
                    break

            if not collided:
                self.character.resume_movement()

            self.background.update(dx)
            self.all_sprites.update()

            if self.character.health_bar.is_depleted():
                print("Character health depleted, calling handle_character_death")
                self.handle_character_death()

            if self.character.is_dead:
                current_time = pygame.time.get_ticks()
                if self.lives > 0 and current_time - self.death_timer >= 1000:  # 1000 milliseconds = 1 second
                    self.revive_character()
                elif self.lives == 0 and current_time - self.death_timer >= 1000:  # 1 second delay before game over
                    self.game_over()

            # Remove enemies that have finished their death animation and increase the counter
            for enemy in list(self.enemy_group):
                if enemy.is_dead and enemy.current_frame == len(enemy.dead_images) - 1:
                    self.enemy_group.remove(enemy)
                    self.enemy_count += 1

            # Check for boss defeat and trigger level change
            # if self.boss_trigger:
            # if self.enemy_count == config.MAX_ENEMIES:  #line changed to trigger when all enemies die, change to this line to be based on the boss if self.boss_trigger:
            # if self.enemy_count == config.MAX_ENEMIES:
                # self.change_level_dialogue()
                
            if boss_mana.Boss_HealthBar == HealthBar.is_depleted:
                self.boss_trigger = True
                self.change_level_dialogue()


    def is_in_attack_range(self, enemy):
        distance = abs(self.character.rect.centerx - enemy.rect.centerx)
        return distance < config.ATTACK_RANGE  # Smaller range for attack detection

    def draw(self):
        # Draw all game elements: background, sprites, health bar, dialog box, etc.
        self.surface.fill((0, 0, 0))
        self.background.draw(self.surface)
        self.all_sprites.draw(self.surface)
        self.character.health_bar.draw(self.surface)  # Ensure health bar is drawn here

        # Draw the enemy spawn counter
        draw_enemy_counter(self)

        for enemy in self.enemy_group:
            enemy.draw_rectangle(self.surface)

        for i in range(self.lives):
            self.life_icons[i].draw(self.surface)

        self.dialog_box.draw()
        pygame.display.flip()

  
    def game_over(self):
        game_over(self.surface)
        ask_to_play_again(self.surface, self)
    
    def restart_game(self):
        restart_game(self)


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