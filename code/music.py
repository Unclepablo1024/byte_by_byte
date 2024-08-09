import pygame
import config
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.main_sound = None
        self.current_level_sound = None
        self.volume = 0.1


    def stop_main_music(self):
        if self.main_sound:
            self.main_sound.stop()
            print("Main music stopped")

    def play_music(self, music_path):
        self.stop_main_music()
        if self.current_level_sound:
            self.current_level_sound.stop()
        
        if not os.path.exists(music_path):
            print(f"Music file not found: {music_path}")
            return

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            print(f"Level music started: {music_path}")
        except pygame.error as e:
            print(f"Error playing level music: {e}")

    def set_volume(self, volume):
        self.volume = volume
        if self.main_sound:
            self.main_sound.set_volume(volume)
        if self.current_level_sound:
            self.current_level_sound.set_volume(volume)