import pygame
import config

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.main_sound = pygame.mixer.Sound(config.MAIN_SOUND_PATH)
        self.main_sound.set_volume(0.1)

    def play_main_music(self):
        self.main_sound.play(loops=-1)

    def stop_main_music(self):
        self.main_sound.stop()
