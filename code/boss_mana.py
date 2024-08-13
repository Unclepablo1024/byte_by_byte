import pygame
from boss1 import Boss


class GameManager:
    def __init__(self):
        self.enemies_defeated = 0
        self.Boss = None

    def add_boss(self, boss):
        self.Boss = boss

    def defeat_enemy(self):
        self.enemies_defeated += 1
        if self.enemies_defeated >= 5 and self.Boss:
            self.Boss.set_walking(True)  # Start boss walking out
    def update(self):
         if self.Boss:
             self.Boss.update()