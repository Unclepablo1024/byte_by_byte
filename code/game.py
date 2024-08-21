import pygame
import sys
import os
from pygame.locals import *
from boss1 import Boss1
from boss2 import Boss2
from boss3 import Boss3
from level2 import Level2
from level3 import Level3
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
        self.minigame_process = None
        self.current_question_index = 0
        self.current_attempt = 0
        self.attempts = 0
        self.max_attempts = 3
        self.questions = config.get_random_questions(5)
        self.waiting_for_answer = False
        self.correct_answers = 0
        self.total_questions = 1
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

        self.waiting_for_boss1_response = False
        self.waiting_for_boss2_response = False
        self.level2 = None
        self.is_level2_active = False
        self.boss2_defeated = False

        self.waiting_for_boss3_response = False
        self.level3 = None
        self.is_level3_active = False
        self.boss3_defeated = False
        self.coffee_image = config.coffee_image
        self.noway_image = config.noway_image

        
    def init_resources(self):
        # Loads resources like music and sounds
        self.music_player = MusicPlayer()
        self.death_sound = pygame.mixer.Sound(config.DEATH_SOUND_PATH)

    def ask_for_name(self):
        return ask_for_name(self)
    
    def handle_dialog_response(self, response):
        return handle_dialog_response(self, response)

    def change_level_dialogue(self):
        if self.boss_deaths in [1, 2]:  
            self.show_dialog(f"You have completed Level {self.current_level}. Press 'X' to continue to the next level.", auto_hide_seconds=10)
            self.waiting_for_level_change = True
        elif self.boss_deaths >= 3:
            self.show_dialog("Congratulations! You have completed all 3 levels! Game Over!", auto_hide_seconds=10)
            self.game_completed = True
        else:
            print(f"Unexpected boss_deaths value: {self.boss_deaths}")
        pygame.event.clear()   

    def start_level2(self):
        self.is_level2_active = True
        self.level2 = Level2(self)
        print("Level2 started")

    def end_level2(self):
        self.is_level2_active = False
        self.level2 = None

    def start_level3(self):
        self.is_level3_active = True
        self.level3 = Level3(self)
        print("Level3 started")

    def end_level3(self):
        self.is_level3_active = False
        self.level3 = None

    def set_level(self, level):
        set_level(self, level)

    def next_level(self):
        next_level(self)

    def run(self):
        self.ask_for_name()
        while self.running:
            pygame.event.pump()
            event.handle_events(self)
            
            if self.is_level2_active:
                if self.level2 is None:
                    self.level2 = Level2(self)
                
                self.level2.run()
                
                if self.level2.game_state.game_completed:
                    self.is_level2_active = False
                    print("Level2 completed, returning to main game")
                    self.show_boss_defeated_dialog("Boss 2")
                    self.level2 = None

            if self.is_level3_active:
                if self.level3 is None:
                    self.level3 = Level3(self)
                
                self.level3.run()
                
                if self.level3.game_completed:
                    self.is_level3_active = False
                    print("Level3 completed, returning to main game")
                    self.show_boss_defeated_dialog("Boss 3")
                    self.level3 = None
            else:
                self.update()
                self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        self.music_player.stop_main_music()
        pygame.quit()
        sys.exit()

    def show_boss_defeated_dialog(self, boss_name):
        dialog_text = f"{boss_name} has been defeated! Congratulations!"
        self.show_dialog(dialog_text, auto_hide_seconds=5)
        self.boss_trigger = True
        self.boss_deaths += 1  
        pygame.time.delay(1000)  
        self.change_level_dialogue()

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

    def handle_boss2_dialog_response(self, response):
        print(f"Boss2 dialog response received: {response}")
        if response.lower() == 'y':
            self.start_level2()
        elif response.lower() == 'n':
            self.surface.blit(self.noway_image, ((self.surface.get_width() - self.noway_image.get_width()) // 2,
                                             (self.surface.get_height() - self.noway_image.get_height()) // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
        else:
            self.dialog_box.show("Please answer Y or N")
        self.waiting_for_boss2_response = False

    def handle_boss3_dialog_response(self, response):
        print(f"Boss3 dialog response received: {response}")
        if response.lower() == 'y':
            self.start_level3()
        elif response.lower() == 'n':
            self.surface.blit(self.coffee_image, ((self.surface.get_width() - self.coffee_image.get_width()) // 2,
                                             (self.surface.get_height() - self.coffee_image.get_height()) // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
        else:
            self.dialog_box.show("Please answer Y or N")
        self.waiting_for_boss3_response = False

        
    def update(self):
        if self.is_level2_active:
            self.level2.run()
            if self.level2.game_state.game_completed:
                self.is_level2_active = False
                self.handle_level2_completion()
                self.level2 = None
                self.boss = None  
                self.boss_spawned = False 
            return 

        if self.is_level3_active:
            self.level3.run()
            if self.level3.game_state.game_completed:
                self.is_level3_active = False
                self.handle_level3_completion()
                self.level3 = None
                self.boss = None  
                self.boss_spawned = False  
            return 
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.waiting_for_level_change:
                    if event.key == pygame.K_y:
                        self.next_level()
                        self.waiting_for_level_change = False
                        self.dialog_box.hide()
                        pygame.event.clear()
                    elif event.key == pygame.K_n:
                        self.show_dialog("You have chosen to stay on the current level.", auto_hide_seconds=3)
                        pygame.event.clear()
                if self.waiting_for_boss2_response:
                    if event.key == pygame.K_y:
                        print("Y key pressed for Boss2 response")
                        self.handle_boss2_dialog_response('y')
                        self.waiting_for_boss2_response = False
                    elif event.key == pygame.K_n:
                        self.handle_boss2_dialog_response('n')
                        self.waiting_for_boss2_response = False

                if self.waiting_for_boss3_response:
                    if event.key == pygame.K_y:
                        print("Y key pressed for Boss3 response")
                        self.handle_boss3_dialog_response('y')
                        self.waiting_for_boss_response = False
                    elif event.key == pygame.K_n:
                        self.handle_boss3_dialog_response('n')
                        self.waiting_for_boss3_response = False

            
            elif event.type == pygame.USEREVENT + 3:
                if self.waiting_for_level_change:
                    self.change_level_dialogue()
                    pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                    self.waiting_for_level_change = False

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
         
            if now - self.enemy_spawn_timer > 3000 and self.enemy_count < config.MAX_ENEMIES and not self.boss_spawned:
                spawn_enemy(self)
                self.enemy_spawn_timer = now

            for enemy in list(self.enemy_group):
                if enemy.is_dead:
                    continue

                if self.character.is_attacking and self.is_in_attack_range(enemy):
                    enemy.mark_for_damage(pygame.time.get_ticks() + 10)

                if not hasattr(self, 'first_encounter_triggered') and self.is_in_attack_range(enemy):
                    self.first_encounter_triggered = True
                    self.dialog_box.show_dialog("TIP: (Use the left mouse button to attack!)", auto_hide_seconds=5)
                    for counter in range(1, 5):
                        self.dialog_box.show_dialog(f"{config.LEVEL_ONE_DIALOGUE[counter]}", auto_hide_seconds=5)
                    break

                if isinstance(enemy, Boss1) and pygame.sprite.collide_rect(self.character, enemy):
                    if not self.waiting_for_boss1_response:
                        self.dialog_box.show_dialog(
                            "Haha! You think you know git?\nLets test your knowledge then!\nAre you ready?! Y/N")
                        self.waiting_for_answer = False
                        self.waiting_for_boss1_response = True

                if isinstance(enemy, Boss2) and pygame.sprite.collide_rect(self.character, enemy):
                    print("Collision with Boss2 detected.")
                    if not self.waiting_for_boss2_response:
                        self.dialog_box.show_dialog(
                            "Level 2: This challenge will be tougher!\nPrepare yourself for a new set of questions.\nAre you ready?! Y/N")
                        self.waiting_for_boss2_response = True
                        break

                if isinstance(enemy, Boss3) and pygame.sprite.collide_rect(self.character, enemy):
                    print("Collision with Boss3 detected.")
                    if not self.waiting_for_boss2_response:
                        self.dialog_box.show_dialog(
                            "Level 3: This the final test.\nAre you ready?! Y/N")
                        self.waiting_for_boss3_response = True
                        break
        
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
            
            self.background.update(dx)
            self.all_sprites.update()
            
            if self.character.health_bar.is_depleted():
                print("Character health depleted, calling handle_character_death")
                self.handle_character_death()

            if self.character.is_dead:
                current_time = pygame.time.get_ticks()
                if self.lives > 0 and current_time - self.death_timer >= 1000:
                    self.revive_character()
                elif self.lives == 0 and current_time - self.death_timer >= 1000:
                    self.game_over()
            
            for enemy in list(self.enemy_group):
                if enemy.is_dead and enemy.current_frame == len(enemy.dead_images) - 1:
                    self.enemy_group.remove(enemy)
                    if not isinstance(enemy, Boss1) and not isinstance(enemy, Boss2):
                        self.defeated_enemies += 1
            
            if self.defeated_enemies >= config.MAX_ENEMIES and not self.boss_spawned:
                print("MAX_ENEMIES defeated, spawning Boss!")
                self.spawn_boss()
          
            if self.boss and self.boss.is_dead:
                print("Boss is dead. Triggering level change.")
                self.boss_trigger = True
                # self.boss_deaths += 1
                self.show_boss_defeated_dialog(f"Boss {self.boss_deaths}")
                self.waiting_for_level_change = True

    def spawn_boss(self):
        ground_level = self.ground_level

        if self.current_level == 2:
            self.boss = Boss2(config.BOSSES2_FOLDER_PATH, screen_width=self.surface.get_width(),
                            ground_level=ground_level, main_character=self.character)
        elif self.current_level == 3:
            self.boss = Boss3(config.BOSSES3_FOLDER_PATH, screen_width=self.surface.get_width(),
                            ground_level=ground_level, main_character=self.character)
        else:
            self.boss = Boss1(config.BOSSES1_FOLDER_PATH, screen_width=self.surface.get_width(),
                            ground_level=ground_level, main_character=self.character)

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

        # Draw additional level-specific elements if Level 2 is active
        if self.is_level2_active:
            self.level2.draw(self.surface)

        if self.is_level3_active:
            self.level3.draw(self.surface)
        
        # Update the display
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
