import pygame
import random
import time
import config
import sys
import os
from boss3 import Boss3

class Level3:
    def __init__(self, game):
        self.game = game
        self.screen = game.surface
        self.clock = pygame.time.Clock()
        
        # Initialize game state
        self.score = 0
        self.current_question = 0
        self.FULL_TEXT = "TechWise_Rock"
        self.revealed_text_indices = set()
        self.game_completed = False

        # Load sound effects
        self.correct_sound = config.correct_sound
        self.wrong_sound = config.wrong_sound
        
        self.excellent_image = config.excellent_image
        

        # Questions
        self.questions = [
            {"question": "What does FIFO stand for in a queue?", "options": ["First In First Out", "First In Last Out"], "answer": "First In First Out"},
            {"question": "What are the primary operations of a queue?", "options": ["Enqueue and Dequeue", "Push and Pop"], "answer": "Enqueue and Dequeue"}
            # ,
            # {"question": "What does LIFO stand for in a stack?", "options": ["Last In First Out", "Last In Last Out"], "answer": "Last In First Out"},
            # {"question": "What are the main operations of a stack?", "options": ["Push and Pop", "Insert and Delete"], "answer": "Push and Pop"},
            # {"question": "What is the top node of a tree called?", "options": ["Root", "Leaf"], "answer": "Root"},
            # {"question": "In a tree, what is a node with no children called?", "options": ["Leaf", "Root"], "answer": "Leaf"},
            # {"question": "What is the relationship between parent and child nodes in a tree called?", "options": ["Parent-Child Relationship", "Sibling Relationship"], "answer": "Parent-Child Relationship"},
            # {"question": "In a binary tree, how many children can each node have at most?", "options": ["Two", "Three"], "answer": "Two"},
            # {"question": "What is the characteristic of a set that does not allow duplicate elements?", "options": ["Uniqueness", "Order"], "answer": "Uniqueness"},
            # {"question": "Is the order of elements important in a set?", "options": ["No", "Yes"], "answer": "No"},
            # {"question": "In graph theory, what is a sequence of edges connecting two vertices called?", "options": ["Path", "Cycle"], "answer": "Path"},
            # {"question": "What is the last node in a singly linked list called?", "options": ["Tail", "Head"], "answer": "Tail"},
            # {"question": "How many pointers does a node in a doubly linked list have?", "options": ["Two", "One"], "answer": "Two"}
        ]
        
        self.randomize_all_options()

    def randomize_all_options(self):
        for question in self.questions:
            random.shuffle(question["options"])

    def run(self):
        while self.current_question < len(self.questions):
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        self.show_finished_text()
        self.game_completed = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click()

    def handle_click(self):
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                selected_option = self.options[i]
                if selected_option == self.questions[self.current_question]["answer"]:
                    self.correct_sound.play()
                    self.score += 1
                    self.show_result(True)
                else:
                    self.wrong_sound.play()
                    self.show_result(False)
                
                self.current_question += 1
                pygame.time.delay(1000)  # Add delay to avoid immediately jumping to next question
                break

    def draw(self):
        self.screen.fill(config.WHITE)
        if self.current_question < len(self.questions):
            self.options, self.option_rects = self.show_question(self.questions[self.current_question])
        self.draw_revealed_text()
        pygame.display.flip()

    def show_question(self, question):
        self.screen.fill(config.WHITE)
        
        title_surface = config.title_font.render("Trivia Challenge", True, config.BLUE)
        self.screen.blit(title_surface, (config.SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 20))
        
        wrapped_question = config.wrap_text(question["question"], config.font, config.SCREEN_WIDTH - 100)
        y_offset = 100
        for line in wrapped_question:
            question_surface = config.font.render(line, True, config.BLACK)
            self.screen.blit(question_surface, (50, y_offset))
            y_offset += question_surface.get_height() + 5

        options = question["options"]
        option_rects = []
        option_width = 350  
        option_height = 80  
        space_between = 50   
        base_x = (config.SCREEN_WIDTH - 2 * option_width - space_between) // 2  
        base_y = 200  

        for i, option in enumerate(options):
            x = base_x + (i % 2) * (option_width + space_between)
            y = base_y + (i // 2) * (option_height + 10)  
            rect = pygame.Rect(x, y, option_width, option_height)
            option_rects.append(rect)
            self.draw_button(option, rect, config.BLUE, config.LIGHT_BLUE)

        score_text = config.small_font.render(f"Score: {self.score}", True, config.BLACK)
        self.screen.blit(score_text, (config.SCREEN_WIDTH - 100, 20))

        progress_text = config.small_font.render(f"Question {self.current_question + 1}/13", True, config.BLACK)
        self.screen.blit(progress_text, (20, 20))

        return options, option_rects

    def draw_button(self, text, rect, color, hover_color):
        mouse = pygame.mouse.get_pos()

        is_hovered = rect.collidepoint(mouse)
        button_color = hover_color if is_hovered else color

        pygame.draw.rect(self.screen, button_color, rect)

        text_color = config.WHITE if color != config.WHITE else config.BLACK
        text_surface = config.font.render(text, True, text_color)

        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_revealed_text(self):
        for i, char in enumerate(self.FULL_TEXT):
            color = config.LIGHT_BLUE if i not in self.revealed_text_indices else config.RED
            char_surface = config.title_font.render(char, True, color)
            char_width = char_surface.get_width()
            self.screen.blit(char_surface, (config.SCREEN_WIDTH // 2 - len(self.FULL_TEXT) * char_width // 2 + i * char_width, 450))

    def show_result(self, correct):
        if correct:
            next_index = next(i for i in range(len(self.FULL_TEXT)) if i not in self.revealed_text_indices)
            self.revealed_text_indices.add(next_index)
        else:
            wrong_image = config.wrong_image
            self.screen.blit(wrong_image, (config.SCREEN_WIDTH // 2 - wrong_image.get_width() // 2, (config.SCREEN_HEIGHT - wrong_image.get_height()) // 2))
            pygame.display.flip()
            pygame.time.delay(1000)
        self.draw_revealed_text()

        result_text = "Correct!" if correct else "Incorrect!"
        result_color = config.GREEN if correct else config.RED
        result_surface = config.large_font.render(result_text, True, result_color)
        self.screen.blit(result_surface, (config.SCREEN_WIDTH // 2 - result_surface.get_width() // 2, 400))
        

        pygame.display.flip()
        pygame.time.delay(1000)

    def show_finished_text(self):
        self.screen.fill(config.WHITE)
        finished_text = config.title_font.render("Finished!!", True, config.RED)
        final_score_text = config.large_font.render(f"Final Score: {self.score}", True, config.BLACK)
        final_score_text_rect = final_score_text.get_rect(midtop=(config.SCREEN_WIDTH // 2, 5))
        self.screen.blit(self.excellent_image, (config.SCREEN_WIDTH // 2 - self.excellent_image.get_width() // 2, config.SCREEN_HEIGHT // 2 - self.excellent_image.get_height() // 2))
        self.screen.blit(finished_text, final_score_text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        self.game.boss_deaths = 3

        self.game.is_level3_active = False
