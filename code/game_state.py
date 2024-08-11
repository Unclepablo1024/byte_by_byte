import config
class GameState:
    def __init__(self):
        self.current_level = 1
        self.lives = config.INITIAL_LIVES
        self.boss_deaths = 1
        self.boss_trigger = False
        self.dialogue_shown = False

    def next_level(self):
        self.current_level += 1
        if self.current_level > len(config.LEVELS):
            return False
        return True

    def decrease_life(self):
        self.lives -= 1
        return self.lives > 0

    def reset(self):
        self.current_level = 1
        self.lives = config.INITIAL_LIVES
        self.boss_deaths = 1
        self.boss_trigger = False
        self.dialogue_shown = False