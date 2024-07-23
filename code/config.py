import os

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Character settings
CHARACTER_INITIAL_X = 50
CHARACTER_GROUND_LEVEL = SCREEN_HEIGHT - 155  # Assuming character height is 128
CHARACTER_GRAVITY = 1
CHARACTER_JUMP_STRENGTH = -15
FRAME_RATE = 100  # Milliseconds per frame

# Movement speed
SCROLL_SPEED = 5
RUN_SPEED_MULTIPLIER = 2

# Background settings
BACKGROUND_IMAGE_PATH = "../sprites/backgrounds/City2_pale.png"
BACKGROUND_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Character sprites
IDLE_PICTURE_PATH = "../sprites/Gangsters_2/Idlefix.png"
WALK_GIF_PATH = "../sprites/Gangsters_2/Walk.png"
JUMP_GIF_PATH = "../sprites/Gangsters_2/Jump.png"
RUN_GIF_PATH = "../sprites/Gangsters_2/Run.png"
HURT_GIF_PATH = "../sprites/Gangsters_2/Hurt.png"
DIE_GIF_PATH = "../sprites/Gangsters_2/Dead.png"

# Health bar settings
HEALTH_BAR_MAX_HEALTH = 100
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_X = 600 - 30
HEALTH_BAR_Y = 30
HEALTH_BAR_COLOR = (0, 255, 0)

# Life icon settings
LIFE_ICON_PATH = "../sprites/life_icon.png"
LIFE_ICON_SIZE = 52
LIFE_ICON_SPACING = 1
INITIAL_LIVES = 3

# Dialogue settings
DIALOGUE_FONT_SIZE = 32
DIALOGUE_TEXT_COLOR = (255, 255, 255)
DIALOGUE_BOX_IMAGE_PATH = os.path.join('sprites', 'Dialouge', 'Dialouge boxes', 'BetterDialouge1.png')
DIALOG_COOLDOWN_TIME = 2000  # 2 seconds cooldown

# Enemy settings
ENEMY_TYPES = ["Homeless_1", "Homeless_2", "Homeless_3"]
ENEMY_SPRITES_PATH = "../sprites/enemies"

# Music and sound settings
DEATH_SOUND_PATH = "../audio/pain-scream.wav"
MAIN_SOUND_PATH = "../audio/western.mp3"


# Game over settings
GAME_OVER_FONT_PATH = "../fonts/determinationsans.ttf"




# import os

# # Screen settings
# from os import path


# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600

# # Characters settings
# CHARACTER_INITIAL_X = 70
# CHARACTER_GROUND_LEVEL = SCREEN_HEIGHT - 170 # Assuming character height is 128
# CHARACTER_GRAVITY = 1
# CHARACTER_JUMP_STRENGTH = -15
# FRAME_RATE = 100 # Miliseconds per frame

# # Movement speed
# SCROLL_SPEED = 5
# RUN_SPEED_MULTIPLIER = 2

# # Background settings
# BACKGROUND_IMAGE_PATH = "sprites/backgrounds/City2_pale.png"
# BACKGROUND_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# # Character sprites
# IDLE_PICTURE_PATH = "sprites/Gangsters_2/Idlefix.png"
# WALK_GIF_PATH = "sprites/Gangsters_2/Walk.png"
# JUMP_GIF_PATH = "sprites/Gangsters_2/Jump.png"
# RUN_GIF_PATH = "sprites/Gangsters_2/Run.png"
# HURT_GIF_PATH = "sprites/Gangsters_2/Hurt.png" 
# DIE_GIF_PATH = "sprites/Gangsters_2/Dead.png"

# # Health bar settings
# HEALTH_BAR_MAX_HEALTH = 100
# HEALTH_BAR_WIDTH = 200
# HEALTH_BAR_HEIGHT = 20
# HEALTH_BAR_X = 600 - 30
# HEALTH_BAR_Y = 10
# HEALTH_BAR_COLOR = (0, 255, 0)

# # Dialogue settings
# DIALOGUE_FONT_SIZE = 24
# DIALOGUE_TEXT_COLOR = (255, 255, 255)
# DIALOGUE_BOX_IMAGE_PATH = os.path.join('sprites', 'Dialouge', 'Dialouge boxes', 'BetterDialouge1.png')