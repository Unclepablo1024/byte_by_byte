import pygame
import os


class Dialogue:
    def __init__(self, surface):
        self.surface = surface  # Clear the screen with black
        self.font = pygame.font.Font(None, 32)

    def draw(self):
        self.draw_dialogue_box("Greetings Player!",(100, 100))


    # Draw the dialogue box
    def draw_dialogue_box(self, dialogue_text, position):
        image_path = os.path.join('sprites', 'Dialouge', 'Dialouge boxes', 'BetterDialouge1.png')
        dialogue_box = pygame.image.load(image_path).convert_alpha()
        self.surface.blit(dialogue_box, position)

        # Font of text
        text_surface = self.render_text(dialogue_text, (255, 255, 255))
        text_position = (position[0] + 50, position[1] + 25)
        self.surface.blit(text_surface, text_position)

    def render_text(self, text, color):
        text_surface = self.font.render(text, True, color)
        return text_surface

