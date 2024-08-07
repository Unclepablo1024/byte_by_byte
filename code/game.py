import pygame
import sys
import os
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
        self.name = ""
        self.init_resources()
        self.restart_game()
        self.dialog_box = DialogBox(self.surface, 600, 200)
        self.current_question_index = 0
        self.current_attempt = 0
        self.attempts = 0
        self.max_attempts = 3
        self.questions = config.get_random_questions(5)
        self.waiting_for_answer = False
        self.correct_answers = 0
        self.total_questions = 5

    def init_resources(self):
        self.music_player = MusicPlayer()
        self.death_sound = pygame.mixer.Sound(config.DEATH_SOUND_PATH)

    def ask_for_name(self):
        self.surface.fill((0, 0, 0))
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 60)
        prompt_text = 'Enter your name:'
        prompt_surface = font.render(prompt_text, True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2 - 50))
        self.surface.blit(prompt_surface, prompt_rect)
        pygame.display.flip()

        self.name = self.get_user_input()
        self.dialog_box.show(
            f" {self.name}!!\nThat's it! You're fired! Don't come back until\nyou've learned something!",
            auto_hide_seconds=7)

    def handle_dialog_response(self, response):
        if self.current_question_index == 0 and not self.waiting_for_answer:
            if response.lower() == 'y':
                self.waiting_for_answer = True
                self.ask_next_question()
            elif response.lower() == 'n':
                self.dialog_box.show(f"Austin!! {self.name} is not ready!!! Come here to help!", auto_hide_seconds=7)
            return

        if self.waiting_for_answer:
            if self.check_answer(response):
                self.correct_answers += 1
                self.dialog_box.show(
                    f"Good job! You've answered {self.correct_answers} out of {self.total_questions} questions correctly.",
                    auto_hide_seconds=6)
                self.current_attempt = 0
                self.current_question_index += 1
                self.waiting_for_answer = False
                pygame.time.set_timer(pygame.USEREVENT + 2, 3000)
            else:
                self.current_attempt += 1
                self.health_bar.update_health(-10)

                if self.current_attempt >= self.max_attempts:
                    correct_answer = self.questions[self.current_question_index]["answer"]
                    self.dialog_box.show(f"Oh no! The correct answer was: {correct_answer}", auto_hide_seconds=5)
                    self.current_attempt = 0
                    self.waiting_for_answer = False
                    self.current_question_index += 1
                    pygame.time.set_timer(pygame.USEREVENT + 2, 5000)
                else:
                    attempts_left = self.max_attempts - self.current_attempt
                    self.dialog_box.show(f"Wrong! Attempts left: {attempts_left}. Please try again!",
                                         auto_hide_seconds=3)
                    self.set_timer()

    def set_timer(self):
        pygame.time.set_timer(pygame.USEREVENT + 2, 3000)

    def ask_next_question(self):
        if self.current_question_index < self.total_questions:
            question = self.questions[self.current_question_index]["question"]
            self.dialog_box.show(f"No# {self.current_question_index + 1}: {question}")
            self.waiting_for_answer = True
        else:
            if self.correct_answers == self.total_questions:
                self.dialog_box.show(
                    "Congratulations! You've answered all 5 questions correctly. You've passed Level One!",
                    auto_hide_seconds=5)
            else:
                self.dialog_box.show(
                    f"You've only answered {self.correct_answers} out of {self.total_questions} questions correctly. You need to answer all 5 questions correctly to pass. Try again!",
                    auto_hide_seconds=5)
                self.restart_level()
            self.waiting_for_answer = False

    def restart_level(self):
        self.current_question_index = 0
        self.correct_answers = 0
        self.questions = config.get_random_questions(self.total_questions)
        self.health_bar.reset()
        self.current_attempt = 0
        self.waiting_for_answer = False

    def check_answer(self, response):
        correct_answer = self.questions[self.current_question_index]["answer"]
        print(
            f"Checking answer: '{response.strip().lower()}' against correct answer: '{correct_answer.strip().lower()}'")
        return response.strip().lower() == correct_answer.strip().lower()

    def get_user_input(self):
        input_text = ""
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 60)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        return input_text
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        input_text += event.unicode

                    self.surface.fill((0, 0, 0))

                    prompt_text = 'Enter your name:'
                    prompt_surface = font.render(prompt_text, True, (255, 255, 255))
                    prompt_rect = prompt_surface.get_rect(
                        center=(self.surface.get_width() / 2, self.surface.get_height() / 2 - 50))
                    self.surface.blit(prompt_surface, prompt_rect)

                    input_surface = font.render(input_text, True, (255, 255, 255))
                    input_rect = input_surface.get_rect(
                        center=(self.surface.get_width() / 2, self.surface.get_height() / 2 + 50))
                    self.surface.blit(input_surface, input_rect)

                    pygame.display.flip()

            self.clock.tick(30)

    def restart_game(self):
        self.character = MainCharacter(
            config.IDLE_PICTURE_PATH,
            config.WALK_GIF_PATH,
            config.JUMP_GIF_PATH,
            config.RUN_GIF_PATH,
            config.HURT_GIF_PATH,
            config.DIE_GIF_PATH,
            config.ATTACK_1_GIF_PATH,
            config.ATTACK_2_GIF_PATH,
            config.ATTACK_3_GIF_PATH
        )
        self.background = Background(config.BACKGROUND_IMAGE_PATH, config.BACKGROUND_SIZE)
        self.all_sprites = pygame.sprite.Group(self.character)
        self.enemy_group = pygame.sprite.Group()
        self.ground_level = config.CHARACTER_GROUND_LEVEL
        self.health_bar = HealthBar(config.HEALTH_BAR_MAX_HEALTH, config.HEALTH_BAR_WIDTH, config.HEALTH_BAR_HEIGHT,
                                    config.HEALTH_BAR_X, config.HEALTH_BAR_Y, config.HEALTH_BAR_COLOR)
        self.lives = config.INITIAL_LIVES
        self.scroll_speed = config.SCROLL_SPEED - 1  # Decrease player speed
        self.dialog_cooldown = 0
        self.dialog_cooldown_time = config.DIALOG_COOLDOWN_TIME
        self.death_timer = None
        self.spawned_enemies = []
        self.enemy_spawn_timer = pygame.time.get_ticks()
        self.update_life_icons()

    def update_life_icons(self):
        self.life_icons = []
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
        self.ask_for_name()
        self.music_player.play_main_music()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        self.music_player.stop_main_music()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.USEREVENT + 1:
                self.dialog_box.hide()

            if event.type == pygame.USEREVENT + 2:
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                if self.current_question_index < len(self.questions):
                    self.ask_next_question()
                else:
                    self.dialog_box.show("Congratulations! You've completed all questions for Level One.",
                                         auto_hide_seconds=5)

            if event.type == pygame.USEREVENT + 3:
                self.revive_character()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    response = self.dialog_box.get_input()
                    print(f"Dialog response received: {response}")
                    self.handle_dialog_response(response)
                elif event.key == pygame.K_BACKSPACE:
                    self.dialog_box.backspace()
                elif event.key == pygame.K_1:
                    self.handle_player_input(event)
                else:
                    self.dialog_box.add_char(event.unicode)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.character.attack()

        if not self.dialog_box.active:
            self.handle_continuous_input()

    def show_dialog(self, message, auto_hide_seconds=None):
        self.dialog_box.show(message, auto_hide_seconds)

    def handle_player_input(self, event):
        if event.key == pygame.K_1:
            self.character.hurt()
            self.health_bar.update_health(-5)
            if self.health_bar.is_depleted():
                self.handle_character_death()

    def handle_continuous_input(self):
        keys = pygame.key.get_pressed()
        moving = False
        running = False
        dx, dy = 0, 0
        if keys[K_LEFT]:
            dx = -1  # Decreased speed
            moving = True
        if keys[K_RIGHT]:
            dx = 1  # Decreased speed
            moving = True
        if keys[K_UP] and not self.character.is_jumping:
            self.character.jump()
            moving = True
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            if keys[K_LEFT] or keys[K_RIGHT]:
                running = True
                dx *= config.RUN_SPEED_MULTIPLIER

        self.character.set_running(running)
        self.character.set_walking(moving and not self.character.is_jumping and not running)
        self.character.move(dx, dy)

    def revive_character(self):
        # Reset the character's state
        self.character.is_dead = False
        self.character.is_attacking = False
        self.character.health = config.HEALTH_BAR_MAX_HEALTH
        self.character.rect.topleft = (config.CHARACTER_INITIAL_X, config.CHARACTER_GROUND_LEVEL)
        self.character.health_bar.reset()
        # Update life icons and respawn if lives are remaining
        self.update_life_icons()
        if self.lives > 0:
            self.all_sprites.add(self.character)

    def handle_character_death(self):
        if not self.character.is_dead:
            print("Character is dying")
            self.lives -= 1
            self.character.die()
            self.death_sound.play()
            self.update_life_icons()
            if self.lives > 0:
                pygame.time.set_timer(pygame.USEREVENT + 3, 2000)  # Set a timer to respawn character after 2 seconds
            else:
                self.game_over()

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
            if now - self.enemy_spawn_timer > 3000:
                self.spawn_enemy()
                self.enemy_spawn_timer = now

            for enemy in self.enemy_group:
                if self.character.is_attacking and self.is_in_attack_range(enemy):
                    enemy.mark_for_damage(pygame.time.get_ticks() + 0.0001)

            collided = False
            for enemy in self.enemy_group:
                if pygame.sprite.collide_rect(self.character, enemy):
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

        if self.character.health_bar.is_depleted() and not self.character.is_dead:
            self.handle_character_death()

        # Ensure the health bar is drawn
        self.character.health_bar.draw(self.surface)

    def is_in_attack_range(self, enemy):
        distance = abs(self.character.rect.centerx - enemy.rect.centerx)
        return distance < config.ATTACK_RANGE  # Smaller range for attack detection

    def spawn_enemy(self):
        if len(self.enemy_group) < 10:  # Limit total number of enemies to 10
            enemy_type = random.choice(config.ENEMY_TYPES)
            new_enemy = Enemy(enemy_type, os.path.join('sprites', 'enemies'), self.surface.get_width(), 560,
                              self.character)
            self.all_sprites.add(new_enemy)
            self.enemy_group.add(new_enemy)

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.background.draw(self.surface)
        self.all_sprites.draw(self.surface)
        self.character.health_bar.draw(self.surface)  # Ensure health bar is drawn here
        for enemy in self.enemy_group:
            enemy.draw_rectangle(self.surface)
        for i in range(self.lives):
            if i < len(self.life_icons):
                self.life_icons[i].draw(self.surface)
        self.dialog_box.draw()
        pygame.display.flip()

    def game_over(self):
        print("Game Over")
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 160)
        text = font.render('GAME OVER', True, (186, 85, 211))
        text_rect = text.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2))
        self.surface.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(500)
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
