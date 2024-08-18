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
from enemy_spawner import spawn_enemy


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
        self.total_questions = 3
        self.enemy_count = 0
        self.defeated_enemies = 0
        self.first_encounter = 0

        #trigger for boss spawn
        self.boss_spawned = False
        self.enemy_spawn_timer = 0

        # Flag for dialogue trigger for levels
        self.level_start_dialog_shown = False

        # Dialogue setup for change level to level
        self.boss_deaths = 0
        self.boss_trigger = False
        self.boss = None

        self.waiting_for_level_change = False
        self.game_completed = False
        

    def init_resources(self):
        # Loads resources like music and sounds
        self.music_player = MusicPlayer()
        self.death_sound = pygame.mixer.Sound(config.DEATH_SOUND_PATH)

    def ask_for_name(self):
        self.name = ask_for_name(self)
    
    def change_level_dialogue(self):
        if self.boss_deaths in [0, 1, 2]:  
            self.show_dialog(f"Zoey: Congratulations! You have completed Level {self.boss_deaths}. Press 'X' to continue to the next level.", auto_hide_seconds=5)
            self.waiting_for_level_change = False
            pygame.event.clear() 
        elif self.boss_deaths == 3:
            self.show_dialog("Zoey: Congratulations! You have completed all 3 levels! Game Over!", auto_hide_seconds=5)
            self.game_completed = True
        else:
            print(f"Unexpected boss_deaths value: {self.boss_deaths}")
        pygame.event.clear()

    def handle_level_change_response(self, key):
        if self.waiting_for_level_change:
            if key == pygame.K_x:
                print(f"Changing to level {self.boss_deaths + 2}")  # +2 because boss_deaths is 0-based
                self.next_level()
        
            self.waiting_for_level_change = False
            self.dialog_box.hide()
            pygame.time.set_timer(pygame.USEREVENT + 3, 0)  # Stop the timer
            pygame.event.clear() 


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

            # Continue with normal enemy spawning until max is reached
            if now - self.enemy_spawn_timer > 3000 and self.enemy_count < config.MAX_ENEMIES and not self.boss_spawned:
                spawn_enemy(self)
                self.enemy_spawn_timer = now

            for enemy in list(self.enemy_group):
                if enemy.is_dead:
                    continue  # Skip processing for dead enemies

                if self.character.is_attacking and self.is_in_attack_range(enemy):
                    enemy.mark_for_damage(pygame.time.get_ticks() + 10)

                # Check for collision with boss and trigger dialogue
                if isinstance(enemy, Boss) and pygame.sprite.collide_rect(self.character, enemy):
                    if not hasattr(self, 'dialog_cooldown') or self.dialog_cooldown <= 0:
                        self.dialog_box.show_dialog("So you are the intern beating all my minions..", auto_hide_seconds= 5) # The auto hide allows to move to next question
                        self.dialog_box.show_dialog("You think you know git?\nLet's test your knowledge! \nAnswer my questions and ill let you pass, Are you ready?! Y/N")
                        self.dialog_cooldown = 5000  # Set cooldown to 5 seconds (adjust as needed)

                # Check for the first encounter with an enemy
                if not hasattr(self, 'first_encounter_triggered') and self.is_in_attack_range(enemy):
                    self.first_encounter_triggered = True
                    self.dialog_box.show_dialog("Zoey Tip: (Use the left mouse button to attack!)", auto_hide_seconds=5)

                    # Add the remaining dialogues to the queue
                    for counter in range(1, 5):
                        self.dialog_box.show_dialog(f"{config.LEVEL_ONE_DIALOGUE[counter]}", auto_hide_seconds=5)
                    break  # Exit the loop after showing the dialog for the first encounter

            # Handle collisions and character movement
            collided = False
            for enemy in list(self.enemy_group):
                if not enemy.is_dead and pygame.sprite.collide_rect(self.character, enemy):
                    if self.character.rect.centerx < enemy.rect.centerx:
                        self.character.stop_movement('right')
                    else:
                        self.character.stop_movement('left')
                    collided = True
                    break

            if not collided:
                self.character.resume_movement()

            # Update background and sprites
            self.background.update(dx)
            self.all_sprites.update()

            # Check character health and handle death
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
                    if not isinstance(enemy, Boss):
                        self.defeated_enemies += 1

            # Spawn Boss if max enemies defeated
            if self.defeated_enemies >= config.MAX_ENEMIES and not self.boss_spawned:
                print("MAX_ENEMIES defeated, spawning Boss!")
                self.spawn_boss()

            # Check for boss defeat and trigger level change
            if self.boss and self.boss.is_dead:
                print("Boss is dead. Triggering level change.")
                self.boss_trigger = True
                self.change_level_dialogue()
                pygame.time.set_timer(pygame.USEREVENT + 3, 10000)  # 10 seconds delay
                self.waiting_for_level_change = True

            # Handle level change dialogue timeout
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 3:
                    if self.waiting_for_level_change:
                        self.change_level_dialogue()
                    pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                    self.waiting_for_level_change = False

    def spawn_boss(self):
        ground_level = self.ground_level
        self.boss = Boss(folder_path="sprites/Bosses/Boss1", screen_width=self.surface.get_width(), ground_level=ground_level, main_character=self.character)
        self.all_sprites.add(self.boss)
        self.enemy_group.add(self.boss)
        self.boss_spawned = True

    def draw_enemy_counter(self):
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 32)
        counter_text = f"{self.defeated_enemies}/{config.MAX_ENEMIES}"
        text_surface = font.render(counter_text, True, (255, 255, 255))
        self.surface.blit(text_surface, (10, 10))


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
        self.draw_enemy_counter()

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