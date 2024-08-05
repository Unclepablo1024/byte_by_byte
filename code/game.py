# Imports needed for game functioning
import pygame
import sys
import os
import random
from pygame.locals import *
from boss1 import Boss
from enemy import Enemy
from background import Background
from healthbar import HealthBar, LifeIcon
from music import MusicPlayer
from character import MainCharacter
from dialog import DialogBox
import config

# Initialize game and its components
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        # load icon and sets caption for screen
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Byte by Byte")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level = 1   # identifies current level
        self.name = ""           # Player Name
        self.init_resources()    # Loads resources like music and sounds
        self.restart_game()      # restarts the game in terms of character or enemies

        #Dialog interaction setup
        self.dialog_box = DialogBox(self.surface, 600, 200)
        self.current_question_index = 0
        self.current_attempt = 0
        self.attempts = 0  # Initialize attempts
        self.max_attempts = 3
        self.questions = config.get_random_questions(5)
        self.waiting_for_answer = False  # New flag to track if we're waiting for an answer
        self.correct_answers = 0  # New variable to track correct answers
        self.total_questions = 5  # Total number of questions to pass the level

    def init_resources(self):
        # Loads resources like music and sounds
        self.music_player = MusicPlayer()
        self.death_sound = pygame.mixer.Sound(config.DEATH_SOUND_PATH)
    
    def ask_for_name(self):
        # Function that asks the player for their name
        self.surface.fill((0, 0, 0))
        font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 60)
        prompt_text = 'Enter your name:'
        prompt_surface = font.render(prompt_text, True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2 - 50))
        self.surface.blit(prompt_surface, prompt_rect)
        pygame.display.flip()
        self.name = self.get_user_input()
        self.show_dialog(f"Hello {self.name}!\nLet's have fun in Byte by Byte world:)", auto_hide_seconds=4)

    def handle_dialog_response(self, response):
        # Handle the player's responses during Dialogue
        if self.current_question_index == 0 and not self.waiting_for_answer:
            if response.lower() == 'y':
                self.waiting_for_answer = True
                self.ask_next_question()
            elif response.lower() == 'n':
                self.show_dialog(f"Austin!! {self.name} is not ready!!! Come here to help!", auto_hide_seconds=4)
            return

        if self.waiting_for_answer:
            if self.check_answer(response):
                self.correct_answers += 1
                self.show_dialog(f"Good job! You've answered {self.correct_answers} out of {self.total_questions} questions correctly.", auto_hide_seconds=7)
                self.current_attempt = 0
                self.current_question_index += 1
                self.waiting_for_answer = False
                pygame.time.set_timer(pygame.USEREVENT + 2, 3000)
            else:
                self.current_attempt += 1
                self.health_bar.update_health(-10)
                
                if self.current_attempt >= self.max_attempts:
                    # Provide the correct answer after three wrong attempts
                    correct_answer = self.questions[self.current_question_index]["answer"]
                    self.show_dialog(f"Oh no! The correct answer was: {correct_answer}", auto_hide_seconds=5)
                    self.current_attempt = 0
                    self.waiting_for_answer = False
                    self.current_question_index += 1
                    pygame.time.set_timer(pygame.USEREVENT + 2, 5000)  # Give more time to read the correct answer
                else:
                    # Inform the player of remaining attempts
                    attempts_left = self.max_attempts - self.current_attempt
                    self.show_dialog(f"Wrong! Attempts left: {attempts_left}. Please try again!", auto_hide_seconds=3)
                    self.set_timer()

    def set_timer(self):
        #set a timer for dialog or question handling
        pygame.time.set_timer(pygame.USEREVENT + 2, 3000)

    def ask_next_question(self):
        # presents the next question to player
        if self.current_question_index < self.total_questions:
            question = self.questions[self.current_question_index]["question"]
            self.show_dialog(f"No# {self.current_question_index + 1}: {question}")
            self.waiting_for_answer = True
        else:
            # ALL questions have been answered, we ca move to the next level or not
            if self.correct_answers == self.total_questions:
                self.show_dialog("Congratulations! You've answered all 5 questions correctly. You've passed Level One!", auto_hide_seconds=5)
                # Here you can add code to move to the next level or end the game
            else:
                self.show_dialog(f"You've only answered {self.correct_answers} out of {self.total_questions} questions correctly. You need to answer all 5 questions correctly to pass. Try again!", auto_hide_seconds=6)
                self.restart_level()
            self.waiting_for_answer = False

    def restart_level(self):
        # The function restarts the current level and all relevant level variables
        self.current_question_index = 0
        self.correct_answers = 0
        self.questions = config.get_random_questions(self.total_questions)
        self.health_bar.reset()
        self.current_attempt = 0
        self.waiting_for_answer = False

    def check_answer(self, response):
        # It validates the users answers to be correct or not
        correct_answer = self.questions[self.current_question_index]["answer"]
        print(f"Checking answer: '{response.strip().lower()}' against correct answer: '{correct_answer.strip().lower()}'")  # Debug print
        return response.strip().lower() == correct_answer.strip().lower()

    
    def get_user_input(self):
        # The function captures the players input
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
                    prompt_rect = prompt_surface.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2 - 50))
                    self.surface.blit(prompt_surface, prompt_rect)
                    
                    input_surface = font.render(input_text, True, (255, 255, 255))
                    input_rect = input_surface.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2 + 50))
                    self.surface.blit(input_surface, input_rect)
                    
                    pygame.display.flip() # updates the display
        
            self.clock.tick(30) # Limit input processing to 30 FPS

    def restart_game(self):
        # this function restarts the game, including character, Background ..etc
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

        #Sets life icons when restarting
        life_icon_path = config.LIFE_ICON_PATH
        life_icon_size = config.LIFE_ICON_SIZE
        life_icon_spacing = config.LIFE_ICON_SPACING

        #Sets the healthbar when restarting
        health_bar_x = self.health_bar.x
        health_bar_y = self.health_bar.y
        health_bar_height = self.health_bar.height

        for i in range(self.lives):
            icon_x = health_bar_x + i * (life_icon_size + life_icon_spacing) * 0.7
            icon_y = health_bar_y - health_bar_height - 20
            icon = LifeIcon(icon_x, icon_y, life_icon_size, life_icon_size, life_icon_path)
            self.life_icons.append(icon)
            
        self.set_level(self.current_level)  # Ensure the correct background is set

    def set_level(self, level):
    # The function handles the change of the level 
        print(f"Setting level: {level}")  # Debug
        level_settings = config.LEVELS.get(level)
        if level_settings:
            print(f"Loading background for level {level}: {level_settings['background']}")  # Debug
            self.background = Background(str(level_settings["background"]), config.BACKGROUND_SIZE)
        else:
            print(f"Level {level} not found in configuration.") # Debug
            self.background = Background(str(config.LEVELS[1]["background"]), config.BACKGROUND_SIZE)
    
    def run(self):
        # Main game loop, it processes inputs, updates game state.. etc
        self.ask_for_name()
        self.music_player.play_main_music()
        while self.running:
            self.handle_events() #process input events
            self.update() #updates game logic
            self.draw() #draws everything on the screen
            pygame.display.flip() #updates display
            self.clock.tick(60) #Maintains 60 FPS
        self.music_player.stop_main_music()
        pygame.quit()
        sys.exit()

    def handle_events(self):
    #the function handles all game events
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
                    self.show_dialog("Congratulations! You've completed all questions for Level One.", auto_hide_seconds=5)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    response = self.dialog_box.get_input()
                    print(f"Dialog response received: {response}")  # Debug print
                    self.handle_dialog_response(response)
                elif event.key == pygame.K_BACKSPACE:
                    self.dialog_box.backspace()

                #TEST CODE added key bindings to specific events
                elif event.key == pygame.K_1:
                    self.handle_player_input(event) #Damage input
                elif event.key == pygame.K_5:
                    self.handle_player_input(event) #Change level key binding

                else:
                    self.dialog_box.add_char(event.unicode)
                    

        if not self.dialog_box.active:
            self.handle_continuous_input()

    def show_dialog(self, message, auto_hide_seconds=None):
        self.dialog_box.show(message, auto_hide_seconds)

    def handle_player_input(self, event):
        # Handle specific player input for actions like hurting the character or changing levels
        if event.key == pygame.K_1:
            self.character.hurt()
            self.health_bar.update_health(-5)  # Decrease health by 5 units
            if self.health_bar.current_health <= 0:
                self.handle_character_death()

        #Handles the level change 
        if event.key == pygame.K_5:
            print("5 key pressed - attempting to move to next level")  # Debug output
            self.next_level()

    def handle_continuous_input(self):
        # Handle continuous input (e.g., movement keys held down)
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

    def next_level(self): 
        #Function handles the update of levels 
        self.current_level += 1
        print(f"Moving to level {self.current_level}")  # Debugging
        if self.current_level > len(config.LEVELS):
            print("You have completed all levels!")
            self.running = False
        else:
            self.set_level(self.current_level)
            print(f"Level set to {self.current_level}")  # Debugging
            self.restart_game()

    def revive_character(self):
        # Revives the character and resets game
        self.character.revive()
        self.health_bar.reset()
        self.death_timer = None
        
    def handle_character_death(self):
        # creates changes to character when receiving damage until death
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
        # Update game state: manage dialog box, check input, spawn enemies, etc.
        self.dialog_box.update()
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
                        self.show_dialog(f"Here is Level 1....\nYou need to answer at least 5 questions correctly to pass..\nAre you ready?! Y/N")
                        self.dialog_cooldown = self.dialog_cooldown_time

            for enemy in self.enemy_group:
                if enemy.rect.right < 0:
                    enemy.kill()

            if self.health_bar.is_depleted() and not self.character.is_dead:
                self.handle_character_death()

            if self.character.is_dead:
                current_time = pygame.time.get_ticks()
                if self.lives > 0 and current_time - self.death_timer >= 1000:  # 1000 milliseconds = 1 second
                    self.revive_character()
                elif self.lives == 0 and current_time - self.death_timer >= 1000:  # 1 second delay before game over
                    self.game_over()

    def spawn_enemy(self):
    # Spawn enemies randomly from available types, ensuring no duplicates
        available_types = ["Homeless_1", "Homeless_2", "Homeless_3"]
        available_types = [type for type in available_types if type not in self.spawned_enemies]

        if available_types:
            enemy_type = random.choice(available_types)
            new_enemy = Enemy(enemy_type, os.path.join('sprites','enemies'), self.surface.get_width(), 560, self.character)
            self.all_sprites.add(new_enemy)
            self.enemy_group.add(new_enemy)
            self.spawned_enemies.append(enemy_type)

    def draw(self):
    # Draw all game elements: background, sprites, health bar, dialog box. etc
        self.surface.fill((0, 0, 0))
        self.background.draw(self.surface)
        self.all_sprites.draw(self.surface)
        self.health_bar.draw(self.surface)
        for i in range(self.lives):
            self.life_icons[i].draw(self.surface)
        self.dialog_box.draw()
        pygame.display.flip()
        
    def game_over(self):
        # Displays the game over screen once all lives have been used
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
        # Prompts the question to play again once user dies
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
