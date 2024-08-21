import pygame
import config
import os

def game_over(surface):
    print("Game Over")
    font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 160)
    text = font.render('GAME OVER', True, (186, 85, 211))
    text_rect = text.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2))
    surface.blit(text, text_rect)
    
    pygame.display.flip()
    pygame.time.wait(500)

def show_ending_screen(surface):
    ending_image = pygame.image.load(os.path.join(config.PIC_PATH, 'ending.png'))    
    ending_image = pygame.transform.scale(ending_image, (surface.get_width(), surface.get_height()))  
    surface.blit(ending_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(3000)

def ask_to_play_again(surface, game):
    font = pygame.font.Font(config.GAME_OVER_FONT_PATH, 60)
    text = font.render('Play again? (Y/N)', True, (255, 255, 255))
    text_rect = text.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 + 100))
    surface.blit(text, text_rect)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    print("Restarting game...")  # Debug Print
                    waiting_for_input = False
                    game.restart_game()
                elif event.key == pygame.K_n:
                    print("Exiting Game...")  # Debug Print
                    waiting_for_input = False
                    show_ending_screen(surface)  
                    game.running = False 