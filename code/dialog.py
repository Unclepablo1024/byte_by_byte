import pygame

class DialogBox:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = pygame.Rect((screen.get_width() - width) // 2, (screen.get_height() - height) // 2, width, height)
        self.color = pygame.Color('white')
        self.text_color = pygame.Color('black')
        self.font = pygame.font.Font("../fonts/undertalesans.ttf", 32)
        self.text = ""
        self.active = False
        # import pic path
        self.image = pygame.image.load('../pic/s3.png')
        # init image rect
        self.image_rect = self.image.get_rect(topleft=(self.rect.right - 130, self.rect.top + 80))
        self.typing_speed = 50  # Number of milliseconds between characters
        self.last_update_time = pygame.time.get_ticks()
        self.current_char_index = 0
        
        

    def show(self, text):
        self.full_text = text
        self.text = ""
        self.current_char_index = 0
        self.current_text = ""  #init current_text
        self.active = True
        self.last_update_time = pygame.time.get_ticks()


    def hide(self):
        self.active = False
        print("Dialog box hidden")  # Debug print

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.hide()
            print("Dialog closed by pressing Q")  # Debug print
            return True
        return False

    def update(self):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.typing_speed and self.current_char_index < len(self.full_text):
            self.last_update_time = current_time
            self.text += self.full_text[self.current_char_index]
            self.current_char_index += 1

    def draw(self):
        if not self.active:
            return
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, self.text_color, self.rect, 2)

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
        
        words = self.current_text.split('\n')
        y = self.rect.top + 10
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surface, (self.rect.left + 10, y))
            y += text_surface.get_height() + 5

        # Draw the image in the top-right corner
        self.screen.blit(self.image, self.image_rect)