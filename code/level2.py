import pygame
import random
import time
import config
import sys
import os

class Level2:
    def __init__(self, game):
        self.game = game
        self.screen = game.surface
        self.clock = pygame.time.Clock()
        
        # Load images for feedback
        self.correct_image = pygame.image.load(os.path.join(config.PIC_PATH, 'correct.webp'))
        self.wrong_image = pygame.image.load(os.path.join(config.PIC_PATH, 'wrong.webp'))
        image_width, image_height = 440, 300
        self.correct_image = pygame.transform.scale(self.correct_image, (image_width, image_height))
        self.wrong_image = pygame.transform.scale(self.wrong_image, (image_width, image_height))
        
        # Now create the GameState with the images
        self.game_state = self.GameState(self.correct_image, self.wrong_image)
        
        self.dragging_block = None
        self.hint_text = config.small_font.render(
            "Press H for hint | Press Enter to submit code", True, config.BLACK)
        self.level_completed = False
        

    def run(self):
        while not self.game_state.game_completed:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        self.level_completed = True
        print("Level2 completed")
        self.game.is_level2_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mousedown(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouseup(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN and not self.game_state.feedback_image:
            if self.game_state.check_code():
                config.correct_sound.play()
                config.correct_sound.set_volume(0.02)
                self.game_state.score += 1
                self.game_state.show_feedback(self.game_state.correct_image)
                self.game_state.next_level()
            else:
                config.wrong_sound.play()
                config.wrong_sound.set_volume(0.02)
                self.game_state.show_feedback(self.game_state.wrong_image)
                self.game_state.score -= 1
        elif event.key == pygame.K_h:
            self.game_state.show_hint()

    def update(self):
        self.game_state.update_hint()
        self.game_state.update_feedback()
        self.game_state.code_blocks.update()

    def handle_mousedown(self, event):
        if event.button == 1:  # Left mouse button
            for block in self.game_state.code_blocks:
                if block.rect.collidepoint(event.pos):
                    self.dragging_block = block
                    block.dragging = True
                    break

    def handle_mouseup(self, event):
        if event.button == 1 and self.dragging_block:
            self.dragging_block.dragging = False
            for slot in self.game_state.answer_slots:
                if slot.rect.collidepoint(event.pos):
                    if slot.occupied_block:
                        slot.occupied_block.reset_position()
                    slot.occupied_block = self.dragging_block
                    self.dragging_block.rect.topleft = slot.rect.topleft
                    break
            else:
                self.dragging_block.reset_position()
            self.dragging_block = None


    def draw(self):
        self.screen.fill(config.WHITE)
        self.screen.blit(self.hint_text, (config.SCREEN_WIDTH - 700, config.SCREEN_HEIGHT - 50))

        if self.game_state.feedback_image:
            self.screen.blit(self.game_state.feedback_image, (
                config.SCREEN_WIDTH // 2 - self.game_state.feedback_image.get_width() // 2,
                config.SCREEN_HEIGHT // 2 - self.game_state.feedback_image.get_height() // 2))
        else:
            for slot in self.game_state.answer_slots:
                slot.draw(self.screen)

            self.game_state.code_blocks.draw(self.screen)
            level_text = config.large_font.render(f"Level {self.game_state.current_level}", True, config.BLACK)
            self.screen.blit(level_text, (50, 30))
            desc_text = config.small_font.render(self.game_state.get_current_level_description(), True, config.BLACK)
            self.screen.blit(desc_text, (50, 70))
            score_text = config.small_font.render(f"Score: {self.game_state.score}", True, config.BLACK)
            self.screen.blit(score_text, (config.SCREEN_WIDTH - 150, 30))

            if self.game_state.hint_visible:
                self.draw_hint()


        pygame.display.flip()

    def draw_hint(self):
        total_height = len(self.game_state.hint_lines) * config.small_font.get_linesize()
        hint_rect = pygame.Rect(0, 0, config.SCREEN_WIDTH - 40, total_height + 20)
        hint_rect.bottomleft = (20, config.SCREEN_HEIGHT - 300)
        hint_rect.left = (config.SCREEN_WIDTH - hint_rect.width) // 2
        pygame.draw.rect(self.screen, config.HINT_BG_COLOR, hint_rect)
        pygame.draw.rect(self.screen, config.HINT_TEXT_COLOR, hint_rect, 2)

        for i, line in enumerate(self.game_state.hint_lines):
            hint_surface = config.small_font.render(line, True, config.HINT_TEXT_COLOR)
            hint_pos = hint_rect.left + 10, hint_rect.top + 10 + i * config.small_font.get_linesize()
            self.screen.blit(hint_surface, hint_pos)

    def draw_dialog_box(self, message):
        dialog_width, dialog_height = 600, 300
        dialog_x = (config.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (config.SCREEN_HEIGHT - dialog_height) // 2

        pygame.draw.rect(self.screen, config.WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, config.BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        lines = config.wrap_text(message, config.font, dialog_width - 20)
        for i, line in enumerate(lines):
            text_surface = config.font.render(line, True, config.BLACK)
            self.screen.blit(text_surface, (dialog_x + 10, dialog_y + 10 + i * 30))

        pygame.display.flip()

    class Level:
        def __init__(self, level_number, description, code_snippets, correct_order, hint):
            self.level_number = level_number
            self.description = description
            self.code_snippets = code_snippets
            self.correct_order = correct_order
            self.hint = hint

        def generate_code_blocks(self):
            blocks = pygame.sprite.Group()
            y_position = 100
            snippets = self.code_snippets[:]
            random.shuffle(snippets)
            for snippet in snippets:
                block = Level2.CodeBlock(snippet, 50, y_position)
                blocks.add(block)
                y_position += 60
            return blocks

        def check_code(self, game_state):
            for i, slot in enumerate(game_state.answer_slots):
                if slot.occupied_block:
                    if slot.occupied_block.text != self.correct_order[i]:
                        return False
                else:
                    return False
            return True
        
    class GameState:
        def __init__(self, correct_image, wrong_image):
            self.correct_image = correct_image
            self.wrong_image = wrong_image
            self.score = 0
            self.current_level = 1
            self.levels = self.generate_levels()
            self.code_blocks = pygame.sprite.Group()
            self.answer_slots = []
            self.feedback_image = None
            self.feedback_start_time = 0
            self.feedback_duration = 2  # 2 seconds
            self.game_completed = False
            self.hint_visible = False
            self.hint_start_time = 0
            self.hint_duration = 3
            self.hint_lines = []
            self.reset_level()

        def show_feedback(self, image):
            self.feedback_image = image
            self.feedback_start_time = time.time()

        def update_feedback(self):
            if self.feedback_image and time.time() - self.feedback_start_time > self.feedback_duration:
                self.feedback_image = None

        def generate_levels(self):
            return [
                Level2.Level(1, "Define the function signature",
                    ["def fibonacci(n):", "def fib(n):", "def fibonacci_sequence(n):"],
                    ["def fibonacci(n):"],
                    "Start by defining a function that takes a single parameter 'n'."),

                Level2.Level(2, "Implement the base case",
                    ["if n <= 1:", "if n < 2:", "if n == 0 or n == 1:", "    return n", "    return 1", "    return 0"],
                    ["if n <= 1:", "    return n"],
                    "The base case handles the simplest inputs. For Fibonacci, what are these?"),

                Level2.Level(3, "Add the recursive case",
                    ["return fibonacci(n-1) + fibonacci(n-2)", "return fibonacci(n) + fibonacci(n-1)",
                    "return n + fibonacci(n-1)"],
                    ["return fibonacci(n-1) + fibonacci(n-2)"],
                    "The recursive case combines results from smaller subproblems. How do we calculate the nth Fibonacci number?"),

                Level2.Level(4, "Initialize a list for the sequence",
                    ["fib_sequence = []", "fib_sequence = [0, 1]", "fib_sequence = list()"],
                    ["fib_sequence = []"],
                    "We need a list to store our Fibonacci numbers. Start with an empty list."),

                Level2.Level(5, "Create a loop to generate the sequence",
                    ["for i in range(10):", "for i in range(n):", "while len(fib_sequence) < 10:"],
                    ["for i in range(10):"],
                    "We want to generate the first 10 Fibonacci numbers. How should we structure our loop?"),

                Level2.Level(6, "Append Fibonacci numbers to the sequence",
                    ["fib_sequence.append(fibonacci(i))", "fib_sequence.append(i)", "fib_sequence += fibonacci(i)"],
                    ["fib_sequence.append(fibonacci(i))"],
                    "For each iteration, we need to calculate the Fibonacci number and add it to our sequence."),

                Level2.Level(7, "Implement the full function",
                    ["def fibonacci(n):",
                    " if n <= 1:",
                    " return n",
                    " return fibonacci(n-1) + fibonacci(n-2)",
                    "fib_sequence = []",
                    "for i in range(10):",
                    " fib_sequence.append(fibonacci(i))"],
                    ["def fibonacci(n):",
                    " if n <= 1:",
                    " return n",
                    " return fibonacci(n-1) + fibonacci(n-2)",
                    "fib_sequence = []",
                    "for i in range(10):",
                    " fib_sequence.append(fibonacci(i))"],
                    "Use a loop to generate the first 10 numbers of the Fibonacci sequence.")
            ]

        def reset_level(self):
            current_level = self.levels[self.current_level - 1]
            self.code_blocks = current_level.generate_code_blocks()
            self.generate_answer_slots()

        def generate_answer_slots(self):
            self.answer_slots = []
            num_slots = len(self.levels[self.current_level - 1].correct_order)
            for i in range(num_slots):
                self.answer_slots.append(Level2.AnswerSlot(400, 100 + i * 40, 300, 35, i + 1))

        def check_code(self):
            return self.levels[self.current_level - 1].check_code(self)

        def next_level(self):
            if self.current_level < len(self.levels):
                self.current_level += 1
                self.reset_level()
                self.feedback_image = self.correct_image
            else:
                self.game_completed = True
                self.feedback_image = None

        def get_current_level_description(self):
            return self.levels[self.current_level - 1].description

        def get_current_level_hint(self):
            return self.levels[self.current_level - 1].hint

        def show_hint(self):
            self.hint_visible = True
            self.hint_start_time = time.time()
            hint_text = self.get_current_level_hint()
            self.hint_lines = config.wrap_text(hint_text, config.small_font, config.SCREEN_WIDTH - 100)

        def update_hint(self):
            if self.hint_visible:
                if time.time() - self.hint_start_time > self.hint_duration:
                    self.hint_visible = False

    

    class CodeBlock(pygame.sprite.Sprite):
        def __init__(self, text, x, y):
            super().__init__()
            self.text = text
            self.font = config.small_font
            self.color = config.LIGHT_BLUE
            self.text_color = config.BLACK
            self.padding = 5
            self.dragging = False
            self.rect = pygame.Rect(x, y, 0, 0)
            self.original_pos = (x, y)
            self.update_image()

        def update_image(self):
            lines = self.text.split('\n')
            max_width = 0
            rendered_lines = []
            for line in lines:
                text_surface = self.font.render(line.lstrip(), True, self.text_color)
                rendered_lines.append((text_surface, line.count(' ') * 4))
                max_width = max(max_width, text_surface.get_width() + line.count(' ') * 4)

            total_height = sum(line.get_height() for line, _ in rendered_lines)
            self.image = pygame.Surface((max_width + 2 * self.padding, total_height + 2 * self.padding))
            self.image.fill(self.color)

            y_offset = self.padding
            for text_surface, indent in rendered_lines:
                self.image.blit(text_surface, (self.padding + indent, y_offset))
                y_offset += text_surface.get_height()

            new_rect = self.image.get_rect()
            self.rect.size = new_rect.size

        def draw(self, surface):
            surface.blit(self.image, self.rect)

        def update(self):
            if self.dragging:
                self.rect.center = pygame.mouse.get_pos()
            self.update_image()

        def reset_position(self):
            self.rect.topleft = self.original_pos

    class AnswerSlot:
        def __init__(self, x, y, width, height, slot_number):
            self.rect = pygame.Rect(x, y, width, height)
            self.slot_number = slot_number
            self.occupied_block = None

        def draw(self, screen):
            pygame.draw.rect(screen, config.GRAY, self.rect, 2)
            if self.occupied_block:
                self.occupied_block.draw(screen)