import pygame
import os

def check_images():
    images = [
        "sprites/Gangsters_2/Idlefix.png",
        "sprites/Gangsters_2/Walk.png",
        "sprites/Gangsters_2/Jump.png",
        "sprites/Gangsters_2/Run.png",
        "sprites/Gangsters_2/Hurt.png",
        "sprites/Gangsters_2/Dead.png",
        "sprites/backgrounds/City2_pale.png",
        "sprites/life_icon.png",
        # 其他圖像文件...
    ]

    for image_path in images:
        try:
            image = pygame.image.load(image_path)
            print(f"Loaded {image_path} successfully")
        except Exception as e:
            print(f"Error loading {image_path}: {e}")

if __name__ == "__main__":
    pygame.init()
    check_images()
    pygame.quit()