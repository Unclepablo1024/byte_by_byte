import pygame
import os
import config
class DialogBox:
    def __init__(self, surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.rect = pygame.Rect((surface.get_width() - width) // 2, (surface.get_height() - height) // 2, width, height)

        self.dialog_image = pygame.image.load(config.DIALOGUE_BOX_IMAGE_PATH)
        self.dialog_image = pygame.transform.scale(self.dialog_image, (width, height))
        self.text_color = pygame.Color('white')
        self.font = pygame.font.Font(config.DIALOG_FONT_PATH, 32)
        self.text = ""
        self.active = False
        self.image = pygame.image.load(os.path.join('../pic','s2.png'))
        self.image = pygame.transform.scale(self.image, (120, 100))
        self.image_rect = self.dialog_image.get_rect(topleft=(self.rect.right - 120, self.rect.top + 100))
        self.typing_speed = 50
        self.last_update_time = pygame.time.get_ticks()
        self.current_char_index = 0
        self.full_text = ""
        self.auto_hide_time = None
        self.user_input = ""
        self.input_font = pygame.font.Font(os.path.join('../fonts','undertalesans.ttf'), 32)
        self.input_color = (0, 0, 255)
        self.input_text = ""
        self.max_attempts = 3  
        self.attempts = 0      
        self.correct_answer = ""
        self.is_question = False 
        

    def show(self, text, auto_hide_seconds=None):
        self.full_text = text
        self.text = ""
        self.current_char_index = 0
        self.active = True
        self.last_update_time = pygame.time.get_ticks()
        if auto_hide_seconds is not None:
            self.auto_hide_time = pygame.time.get_ticks() + (auto_hide_seconds * 1000)
        else:
            self.auto_hide_time = None

    def hide(self):
        self.active = False
        self.auto_hide_time = None
        print("Dialog box hidden")

    def update(self):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        if self.auto_hide_time is not None and current_time >= self.auto_hide_time:
            self.hide()

        if current_time - self.last_update_time > self.typing_speed and self.current_char_index < len(self.full_text):
            self.last_update_time = current_time
            self.text += self.full_text[self.current_char_index]
            self.current_char_index += 1

    def add_char(self, char):
        self.user_input += char

    def backspace(self):
        self.user_input = self.user_input[:-1]

    def get_input(self):
        input_text = self.user_input
        self.user_input = ""
        return input_text
    
    def draw(self):
        if not self.active:
            return

        self.surface.blit(self.dialog_image, self.rect.topleft)
        words = self.text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font.size(test_line)[0] < self.rect.width - 20:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        y = self.rect.top + 10
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            self.surface.blit(text_surface, (self.rect.left + 10, y))
            y += text_surface.get_height() + 5
        self.surface.blit(self.image, self.image_rect)

        if self.active:
            input_surface = self.input_font.render(self.user_input, True, (0, 0, 0))
            input_rect = input_surface.get_rect(bottomleft=(self.rect.left + 10, self.rect.bottom - 10))
            self.surface.blit(input_surface, input_rect)
    
    def set_style(self, background_color, image_path):
        self.background_color = background_color
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))

    def show_dialog(self, message, auto_hide_seconds=None):
        self.show(message, auto_hide_seconds)
        if "Here is Level 1" in message:
            self.set_style((173, 216, 230), os.path.join('sprites','s4.png'))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.backspace()
            elif event.key == pygame.K_RETURN:
                return self.get_input()
            else:
                self.add_char(event.unicode)

