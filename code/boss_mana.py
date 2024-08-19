import pygame
import config
from boss1 import Boss1


class GameManager:
    def __init__(self):
        self.enemies_defeated = 0
        self.Boss = None

    def add_boss(self, boss):
        self.Boss = boss

    def defeat_enemy(self):
        self.enemies_defeated += 1
        if self.enemies_defeated >= config.MAX_ENEMIES and self.Boss:
            self.Boss.set_walking(True)  # Start boss walking out
    def update(self):
         if self.Boss:
             self.Boss.update()


class Boss_HealthBar:
    def __init__(self, max_health=config.HEALTH_BAR_MAX_HEALTH, width=config.HEALTH_BAR_WIDTH,
                 height=config.HEALTH_BAR_HEIGHT,
                 x=config.HEALTH_BAR_X, y=config.HEALTH_BAR_Y, color=config.HEALTH_BAR_COLOR):
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def update_health(self, amount):
        self.current_health = max(0, min(self.max_health, self.current_health + amount))
        print(f"Updated health: {self.current_health}")

    

    def is_depleted(self):
        return self.current_health <= 0

    def draw(self, screen):
        # Calculate the proportion of health left
        health_ratio = self.current_health / self.max_health
        # Update the color based on health ratio (green to red)
        self.color = (255 * (1 - health_ratio), 255 * health_ratio, 0)
        # Draw the background bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # Draw the current health bar
        current_width = self.width * health_ratio
        pygame.draw.rect(screen, self.color, (self.x, self.y, current_width, self.height))