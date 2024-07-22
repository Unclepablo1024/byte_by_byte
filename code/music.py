import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.main_sound = pygame.mixer.Sound('../audio/western.mp3')
        self.main_sound.set_volume(0.5)

    def play_main_music(self):
        self.main_sound.play(loops=-1)

    def stop_main_music(self):
        self.main_sound.stop()
