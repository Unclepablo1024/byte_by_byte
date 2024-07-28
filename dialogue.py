import pygame
import os
import config


class Dialogue:
    def __init__(self, surface, font_size = config.DIALOGUE_FONT_SIZE):
        self.surface = surface  # Clear the screen with black
        self.font = pygame.font.Font(None, font_size)
        self.dialogue_box_image_path = config.DIALOGUE_BOX_IMAGE_PATH
        self.text_color = config.DIALOGUE_TEXT_COLOR
        self.current_text = "Greetings Player!" # Default text
        self.dialogue_position = (100, 100) # Default Position for Dialogue Box
        self.dialogues = {} # Dictionary to store different dialogue
    def draw(self):
        self.draw_dialogue_box(self.current_text, self.dialogue_position)

    # Draw the dialogue box
    def draw_dialogue_box(self, dialogue_text, position):
        dialogue_box = pygame.image.load(self.dialogue_box_image_path).convert_alpha()
        self.surface.blit(dialogue_box, position)

        # Font of text
        text_surface = self.render_text(dialogue_text, (255, 255, 255))
        text_position = (position[0] + 50, position[1] + 25)
        self.surface.blit(text_surface, text_position)

    def render_text(self, text, color):
        text_surface = self.font.render(text, True, color)
        return text_surface

    def update_text(self, new_text):
        self.current_text = new_text

    def add_dialogue(self, key, dialogue_text):
        self.dialogues[key] = dialogue_text

    def get_dialogue(self, key):
        return self.dialogues.get(key, "Dialogue not Found")

    def set_dialogue(self, key):
        self.current_text = self.get_dialogue(key)
    def update_dialogue_position(self, new_position):
        self.dialogue_position = new_position





