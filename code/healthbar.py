import pygame
import config

class HealthBar:
    def __init__(self, max_health= config.HEALTH_BAR_MAX_HEALTH, width = config.HEALTH_BAR_WIDTH, height = config.HEALTH_BAR_HEIGHT, 
    x = config.HEALTH_BAR_X, y = config.HEALTH_BAR_Y, color = config.HEALTH_BAR_COLOR):
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def update_health(self, amount):
        self.current_health = max(0, min(self.max_health, self.current_health + amount))
    
    def reset(self):
        self.current_health = self.max_health
    
    def is_depleted(self):
        return self.current_health <= 0

    def draw(self, screen):
        # Draw the background bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # Draw the current health bar
        current_width = self.width * (self.current_health / self.max_health)
        pygame.draw.rect(screen, self.color, (self.x, self.y, current_width, self.height))

class LifeIcon:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)