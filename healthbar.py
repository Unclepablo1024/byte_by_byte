import pygame


class HealthBar:
    def __init__(self, max_health, width, height, x, y, color):
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def update_health(self, amount):
        self.current_health = max(0, min(self.max_health, self.current_health + amount))

    def draw(self, screen):
        # Draw the background bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # Draw the current health bar
        current_width = self.width * (self.current_health / self.max_health)
        pygame.draw.rect(screen, self.color, (self.x, self.y, current_width, self.height))
