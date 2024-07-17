import pygame
from pygame.locals import *
import os


#Not needed os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Byte By Byte")

# Define colors of Screen
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Player properties
player_x = 400
player_y = 500
player_speed = 5

# Enemy properties
enemy_x = 400
enemy_y = 100
enemy_speed = 3

running = True
clock = pygame.time.Clock()

#Dialouge Box
image_path = os.path.join('sprites', 'Dialouge', 'Dialouge boxes', 'Dialouge1ish.png')

dialouge_box = pygame.image.load(image_path)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Player movement
    if keys[K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[K_RIGHT] and player_x < screen_width - 50:
        player_x += player_speed

    # Update enemy position
    enemy_y += enemy_speed
    if enemy_y > screen_height:
        enemy_y = -50

    # Check collision
    # if pygame.Rect(player_x, player_y, 50, 50).colliderect(pygame.Rect(enemy_x, enemy_y, 50, 50)):
    #     screen.fill(BLACK)
    #     draw_dialogue_box(screen, "Collision detected!")
    #     pygame.display.flip()
    #     pygame.time.wait(2000)  # Wait for 2 seconds
    #     running = False

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (player_x, player_y, 50, 50))
    pygame.draw.rect(screen, WHITE, (enemy_x, enemy_y, 50, 50))
    screen.blit(dialouge_box, (100, 100))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
