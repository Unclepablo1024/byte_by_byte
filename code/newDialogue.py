import pygame
import os
import config

class NewDialogue:
    def __init__(self, surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.active = False
        self.text = ""
        self.user_input = "" # Store user input
        self.font = pygame.font.Font(config.DIALOG_FONT_PATH, 24)
        self.dialog_image = pygame.image.load(config.DIALOGUE_BOX_IMAGE_PATH)
        self.dialog_image = pygame.transform.scale(self.dialog_image, (width, height))
        self.image_rect = self.dialog_image.get_rect(center =(self.surface.get_width() / 2, self.surface.get_height() - self.height / 2))


    def show(self, text, auto_hide_seconds = None):
        self.text = text
        self.user_input = ""
        self.active = True
        if auto_hide_seconds:
            pygame.time.set_timer(pygame.USEREVENT + 1, auto_hide_seconds * 1000)

    def hide(self):
        self.active = False

    def draw(self):
        if self.active:
            #Draw Dialogue Box img
            self.surface.blit(self.dialog_image, self.image_rect)

            #Render the Text and draw it on surface
            words = self.text.split(' ')
            lines = []
            line = []
            for word in words:
                test_line = line + [word]
                test_line_surface = self.font.render(' '.join(test_line), True, (255, 255, 255))
                if test_line_surface.get_width() > self.width - 20:
                    lines.append(line)
                    line = [word]
                else:
                    line = test_line
            lines.append(line)

            y_offset = self.image_rect.y + 20
            for line in lines:
                line_surface = self.font.render(' '.join(line), True, (255, 255, 255))
                self.surface.blit(line_surface, (self.image_rect.x + 10, y_offset))
                y_offset += line_surface.get_height()

    def update(self):
        pass # for any future updates

    def get_input(self):
        return self.user_input # returns the user input
    def backspace(self):
        self.user_input = self.text[:-1]

    def add_char(self, char):
        self.user_input += char

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.backspace()
            elif event.key == pygame.K_RETURN:
                return self.get_input()
            else:
                self.add_char(event.unicode)





