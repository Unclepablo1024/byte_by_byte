import pygame
import sys
import random
import os
import config

pygame.init()
pygame.mixer.init()

# Screen setup
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Trivia Challenge")

# Fonts
font_path = config.FONT_PATH
font = config.font
small_font = config.small_font
large_font = config.large_font
title_font = config.title_font

# Sounds
correct_sound = pygame.mixer.Sound(os.path.join("audio", "get_point.wav"))
wrong_sound = pygame.mixer.Sound(os.path.join("audio", "lost-sobbing.wav"))
pygame.mixer.music.load(os.path.join("audio", "supershy.mp3"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Questions
questions = [
    {"question": "What does FIFO stand for in a queue?", "options": ["First In First Out", "First In Last Out"], "answer": "First In First Out"},
    {"question": "What are the primary operations of a queue?", "options": ["Enqueue and Dequeue", "Push and Pop"], "answer": "Enqueue and Dequeue"},
    {"question": "What does LIFO stand for in a stack?", "options": ["Last In First Out", "Last In Last Out"], "answer": "Last In First Out"},
    {"question": "What are the main operations of a stack?", "options": ["Push and Pop", "Insert and Delete"], "answer": "Push and Pop"},
    {"question": "What is the top node of a tree called?", "options": ["Root", "Leaf"], "answer": "Root"},
    {"question": "In a tree, what is a node with no children called?", "options": ["Leaf", "Root"], "answer": "Leaf"},
    {"question": "What is the relationship between parent and child nodes in a tree called?", "options": ["Parent-Child Relationship", "Sibling Relationship"], "answer": "Parent-Child Relationship"},
    {"question": "In a binary tree, how many children can each node have at most?", "options": ["Two", "Three"], "answer": "Two"},
    {"question": "What is the characteristic of a set that does not allow duplicate elements?", "options": ["Uniqueness", "Order"], "answer": "Uniqueness"},
    {"question": "Is the order of elements important in a set?", "options": ["No", "Yes"], "answer": "No"},
    {"question": "In graph theory, what is a sequence of edges connecting two vertices called?", "options": ["Path", "Cycle"], "answer": "Path"},
    {"question": "What is the last node in a singly linked list called?", "options": ["Tail", "Head"], "answer": "Tail"},
    {"question": "How many pointers does a node in a doubly linked list have?", "options": ["Two", "One"], "answer": "Two"}
]

# Game state
score = 0
current_question = 0
FULL_TEXT = "TechWise_Rock"
revealed_text_indices = set()

def draw_button(surface, text, rect, color, hover_color):
    mouse = pygame.mouse.get_pos()

    is_hovered = rect.collidepoint(mouse)

    if is_hovered:
        pygame.draw.rect(surface, hover_color, rect)
    else:
        pygame.draw.rect(surface, color, rect)

    text_color = config.WHITE if color != config.WHITE else config.BLACK
    text_surface = font.render(text, True, text_color)

    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Function to show a question with wrapped text
def show_question(surface, question):
    surface.fill(config.WHITE)
    
    title_surface = title_font.render("Trivia Challenge", True, config.BLUE)
    surface.blit(title_surface, (config.SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 20))
    
    wrapped_question = config.wrap_text(question["question"], font, config.SCREEN_WIDTH - 100)
    y_offset = 100
    for line in wrapped_question:
        question_surface = font.render(line, True, config.BLACK)
        surface.blit(question_surface, (50, y_offset))
        y_offset += question_surface.get_height() + 5

    options = question["options"]
    # random.shuffle(options)

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
        draw_button(surface, option, rect, config.BLUE, config.LIGHT_BLUE)

    score_text = small_font.render(f"Score: {score}", True, config.BLACK)
    surface.blit(score_text, (config.SCREEN_WIDTH - 100, 20))

    progress_text = small_font.render(f"Question {current_question + 1}/13", True, config.BLACK)
    surface.blit(progress_text, (20, 20))

    draw_revealed_text(surface)

    return options, option_rects

def draw_revealed_text(surface):
    global revealed_text_indices
    for i, char in enumerate(FULL_TEXT):
        color = config.LIGHT_BLUE if i not in revealed_text_indices else config.RED
        char_surface = title_font.render(char, True, color)
        char_width = char_surface.get_width()
        surface.blit(char_surface, (config.SCREEN_WIDTH // 2 - len(FULL_TEXT) * char_width // 2 + i * char_width, 450))

def show_result(surface, correct):
    global revealed_text_indices
    result_font = config.large_font
    result_text = "Correct!" if correct else "Incorrect!"
    result_color = config.GREEN if correct else config.RED
    result_surface = result_font.render(result_text, True, result_color)
    screen.blit(result_surface, (config.SCREEN_WIDTH // 2 - result_surface.get_width() // 2, 400))

    if correct:
        next_index = next(i for i in range(len(FULL_TEXT)) if i not in revealed_text_indices)
        revealed_text_indices.add(next_index)

    draw_revealed_text(surface)

    pygame.display.flip()
    pygame.time.delay(1000)

# Game loop
def randomize_all_options(questions):
    for question in questions:
        random.shuffle(question["options"])

randomize_all_options(questions)
clock = pygame.time.Clock()
while True:
    screen.fill(config.WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if current_question < len(questions):
        question = questions[current_question]
        options, option_rects = show_question(screen, question)

        # Handle button clicks
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        for i, rect in enumerate(option_rects):
            if rect.collidepoint(mouse):
                if click[0] == 1:
                    selected_option = options[i]
                    if selected_option == question["answer"]:
                        correct_sound.play()
                        score += 1
                        show_result(screen, True)
                    else:
                        wrong_sound.play()
                        show_result(screen, False)

                    current_question += 1
                    pygame.time.delay(1000)  # Add delay to avoid immediately jumping to next question
                    break

    else:
        screen.fill(config.WHITE)
        game_over_text = title_font.render("Game Over!", True, config.RED)
        final_score_text = large_font.render(f"Final Score: {score}", True, config.BLACK)
        screen.blit(game_over_text, (config.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(final_score_text, (config.SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 300))

        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS