import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OOP Matching Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font
font = pygame.font.Font(None, 24)

# Sound Effects
match_sound = pygame.mixer.Sound("../audio/get_point.wav")
no_match_sound = pygame.mixer.Sound("../audio/lost-sobbing.wav")

class Block:
    def __init__(self, x, y, width, height, text, category, pair_id):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.category = category
        self.pair_id = pair_id
        self.selected = False
        self.matched = False

    def draw(self, surface):
        if self.matched:
            color = GREEN
        elif self.selected:
            color = LIGHT_BLUE
        else:
            color = WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        words = self.text.split()
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + " " + word)[0] <= self.rect.width - 10:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        y_offset = 10
        for line in lines:
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(midtop=(self.rect.centerx, self.rect.y + y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += 30

class Game:
    def __init__(self):
        self.blocks = []
        self.selected_blocks = []
        self.score = 0
        self.create_blocks()
        self.feedback_text = ""
        self.feedback_color = BLACK
        self.feedback_time = 0

    def create_blocks(self):
        concepts = [
            ("Class", "A blueprint describing common features and behaviors of objects"),
            ("Attributes", "Features of an object: name, age, breed, etc."),
            ("Methods", "Actions an object can perform: bark(), run(), eat()"),
            ("Object", "An instance of a class, representing a specific entity"),
            ("Inheritance", "Creating a new class based on an existing class, inheriting its properties"),
            ("Encapsulation", "Bundling data and methods that work on that data within a single unit"),
            ("Polymorphism", "Objects of different types can be accessed through the same interface"),
            ("Constructor", "Special method for initializing new objects when they are created")
        ]
        pair_id = 0
        for i, (concept, description) in enumerate(concepts):
            x = (i % 4) * 300 + 10
            y = (i // 4) * 200 + 10
            self.blocks.append(Block(x, y, 280, 90, concept, "concept", pair_id))
            self.blocks.append(Block(x, y + 100, 280, 90, description, "description", pair_id))
            pair_id += 1
        random.shuffle(self.blocks)

        # Assign new positions after shuffling
        for i, block in enumerate(self.blocks):
            block.rect.x = (i % 4) * 300 + 10
            block.rect.y = (i // 4) * 200 + 10

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
        return True

    def handle_click(self, pos):
        for block in self.blocks:
            if block.rect.collidepoint(pos) and not block.matched:
                if block not in self.selected_blocks:
                    block.selected = True
                    self.selected_blocks.append(block)
                    if len(self.selected_blocks) == 2:
                        self.check_match()
                break

    def check_match(self):
        block1, block2 = self.selected_blocks
        if block1.pair_id == block2.pair_id and block1.category != block2.category:
            self.feedback_text = "Match found!"
            self.feedback_color = GREEN
            self.score += 1
            block1.matched = True
            block2.matched = True
            match_sound.play()
        else:
            self.feedback_text = "No match."
            self.feedback_color = RED
            block1.selected = False
            block2.selected = False
            no_match_sound.play()
        self.feedback_time = time.time()
        self.selected_blocks.clear()

    def draw(self):
        screen.fill(WHITE)
        for block in self.blocks:
            block.draw(screen)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 760))
        
        if time.time() - self.feedback_time < 2:  # Show feedback for 2 seconds
            feedback_surface = font.render(self.feedback_text, True, self.feedback_color)
            screen.blit(feedback_surface, (WIDTH // 2 - feedback_surface.get_width() // 2, 730))
        
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
