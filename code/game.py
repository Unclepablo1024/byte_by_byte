import subprocess

import pygame
import sys
import os
from pygame.locals import *
import boss_mana
from boss1 import Boss1
from boss2 import Boss2
from level2 import Level2

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

        self.waiting_for_boss2_response = False
        self.level2 = None
        self.is_level2_active = False
        
    def init_resources(self):
        # Loads resources like music and sounds
        self.music_player = MusicPlayer()
        self.death_sound = pygame.mixer.Sound(config.DEATH_SOUND_PATH)

    def ask_for_name(self):
        self.name = ask_for_name(self)

    def change_level_dialogue(self):
        if self.boss_deaths in [0, 1, 2]:
            self.show_dialog(f" You have completed Level {self.boss_deaths}. Press 'X' to continue to the next level.",
                             auto_hide_seconds=7)
            self.waiting_for_level_change = False
            pygame.event.clear()
        elif self.boss_deaths == 3:
            self.show_dialog("Congratulations! You have completed all 3 levels! Game Over!", auto_hide_seconds=5)
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

    def start_level2(self):
        self.is_level2_active = True
        self.level2 = Level2(self)
        print("Level2 started")

    def end_level2(self):
        self.is_level2_active = False
        self.level2 = None
    

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
                if self.level2.game_state.game_completed:
                    self.is_level2_active = False
                    self.level2 = None
                    print("Level2 completed, returning to main game")
                else:
                    self.level2.run()
            else:
                self.update()
                self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
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
            self.show_coffee_picture()
        else:
            self.dialog_box.show("Please answer Y or N")
        self.waiting_for_boss2_response = False


    def show_coffee_picture(self):
        coffee_image = pygame.image.load("../pic/coffee.jpg")
        coffee_image = pygame.transform.scale(coffee_image, (self.surface.get_width(), self.surface.get_height()))  
        self.surface.blit(coffee_image, (0, 0))  
        pygame.display.flip()
        self.dialog_box.show_dialog("Enjoy your coffee! After that, keep going!", auto_hide_seconds=4)


    def update(self):
        if self.is_level2_active:
            return 

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.waiting_for_boss2_response:
                    if event.key == pygame.K_y:
                        print("Y key pressed for Boss2 response")
                        self.handle_boss2_dialog_response('y')
                        self.waiting_for_boss2_response = False
                    elif event.key == pygame.K_n:
                        print("N key pressed for Boss2 response")
                        self.handle_boss2_dialog_response('n')
                        self.waiting_for_boss2_response = False
                    pygame.event.clear()
                elif self.dialog_box.active:
                    if event.key == pygame.K_y:
                        self.handle_dialog_response('y')
                    elif event.key == pygame.K_n:
                        self.handle_dialog_response('n')
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

            # 繼續正常的敵人生成,直到達到最大數量
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
                    self.dialog_box.show_dialog(
                        "Haha! You think you know git?\nLets test your knowledge then!\nAre you ready?! Y/N")
                    break

                if isinstance(enemy, Boss2) and pygame.sprite.collide_rect(self.character, enemy):
                    print("Collision with Boss2 detected.")
                    self.dialog_box.show_dialog(
                        "Level 2: This challenge will be tougher!\nPrepare yourself for a new set of questions.\nAre you ready?! Y/N")
                    self.waiting_for_boss2_response = True
                    break

            # 處理碰撞和角色移動
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

            # 更新背景和精靈
            self.background.update(dx)
            self.all_sprites.update()

            # 檢查角色健康狀況並處理死亡
            if self.character.health_bar.is_depleted():
                print("Character health depleted, calling handle_character_death")
                self.handle_character_death()

            if self.character.is_dead:
                current_time = pygame.time.get_ticks()
                if self.lives > 0 and current_time - self.death_timer >= 1000:
                    self.revive_character()
                elif self.lives == 0 and current_time - self.death_timer >= 1000:
                    self.game_over()

            # 移除已完成死亡動畫的敵人並增加計數器
            for enemy in list(self.enemy_group):
                if enemy.is_dead and enemy.current_frame == len(enemy.dead_images) - 1:
                    self.enemy_group.remove(enemy)
                    if not isinstance(enemy, Boss1) and not isinstance(enemy, Boss2):
                        self.defeated_enemies += 1

            # 如果達到最大敵人數量,生成Boss
            if self.defeated_enemies >= config.MAX_ENEMIES and not self.boss_spawned:
                print("MAX_ENEMIES defeated, spawning Boss!")
                self.spawn_boss()

            # 檢查Boss是否被擊敗並觸發關卡變更
            if self.boss and self.boss.is_dead:
                print("Boss is dead. Triggering level change.")
                self.boss_trigger = True
                self.change_level_dialogue()
                pygame.time.set_timer(pygame.USEREVENT + 3, 10000)  # 10秒延遲
                self.waiting_for_level_change = True

    def spawn_boss(self):
        ground_level = self.ground_level

        if self.boss_deaths == 0:
            self.boss = Boss1(folder_path="../sprites/Bosses/Boss1", screen_width=self.surface.get_width(),
                              ground_level=ground_level, main_character=self.character)
        elif self.boss_deaths == 1:
            self.boss = Boss2(folder_path="../sprites/Bosses/Boss2", screen_width=self.surface.get_width(),
                              ground_level=ground_level, main_character=self.character)
        # elif self.boss_deaths == 2:
        #     self.boss = Boss3(folder_path="../sprites/Bosses/Boss3", screen_width=self.surface.get_width(),
        #                       ground_level=ground_level, main_character=self.character)

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
