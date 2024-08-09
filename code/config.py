import os
import random

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Character settings
CHARACTER_INITIAL_X = 50
CHARACTER_GROUND_LEVEL = SCREEN_HEIGHT - 155  # Assuming character height is 128
CHARACTER_GRAVITY = 1
CHARACTER_JUMP_STRENGTH = -20
FRAME_RATE = 100  # Milliseconds per frame

# Movement speed
SCROLL_SPEED = 5
RUN_SPEED_MULTIPLIER = 2

# Background settings
BACKGROUND_IMAGE_PATH = os.path.join('sprites', 'backgrounds', 'City2_pale.png')
BACKGROUND_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Character sprites
IDLE_PICTURE_PATH = os.path.join('sprites', 'Gangsters_2', 'Idlefix.png')
WALK_GIF_PATH = os.path.join('sprites', 'Gangsters_2', 'Walk.png')
JUMP_GIF_PATH = os.path.join('sprites', 'Gangsters_2', 'Jump.png')
RUN_GIF_PATH = os.path.join('sprites', 'Gangsters_2', 'Run.png')
HURT_GIF_PATH = os.path.join('sprites', 'Gangsters_2', 'Hurt.png')
DIE_GIF_PATH = os.path.join('sprites', 'Gangsters_2', 'Dead.png')

# Health bar settings
HEALTH_BAR_MAX_HEALTH = 20
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_X = 600 - 30
HEALTH_BAR_Y = 30
HEALTH_BAR_COLOR = (0, 255, 0)

LIFE_ICON_PATH = os.path.join('sprites', 'Life_icon.png')
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
ENEMY_SPRITES_PATH = os.path.join('sprites', 'enemies')

# Attack animations paths
ATTACK_1_GIF_PATH = os.path.join('sprites', 'Gangsters_2', 'Attack_1.png')
ATTACK_2_GIF_PATH = os.path.join('sprites', 'Gangsters_2', 'Attack_2.png')
ATTACK_3_GIF_PATH = os.path.join('sprites', 'Gangsters_2', 'Attack_3.png')
ATTACK_RANGE = 80
# Music and sound settings
DEATH_SOUND_PATH = os.path.join('audio', 'pain-scream.wav')
MAIN_SOUND_PATH = os.path.join('audio', 'western.mp3')

# Game over settings
GAME_OVER_FONT_PATH = os.path.join('fonts', 'determinationsans.ttf')

# Dialog settings
DIALOG_FONT_PATH = os.path.join('fonts', 'determinationsans.ttf')
DIALOGUE_FONT_SIZE = 24
DIALOG_COOLDOWN_TIME = 2000  # 2 seconds in milliseconds

# Level one question
LEVEL_ONE_QUESTIONS = [
    {"question": "What is the command to create a new Git repository?", "answer": "git init"},
    {"question": "What command is used to stage changes in Git?", "answer": "git add"},
    {"question": "Which command is used to commit changes in Git?", "answer": "git commit"},
    {"question": "What command shows the current status of your Git repository?", "answer": "git status"},
    {"question": "What command is used to switch between branches in Git?", "answer": "git checkout"},
    {"question": "What command creates a new branch in Git?", "answer": "git branch"},
    {"question": "What command is used to list all branches in a Git repository?", "answer": "git branch"},
    {"question": "What command is used to merge branches in Git?", "answer": "git merge"},
    {"question": "What command is used to download changes from a remote repository?", "answer": "git pull"},
    {"question": "What command is used to upload local changes to a remote repository?", "answer": "git push"},
    {"question": "What command shows the commit history in Git?", "answer": "git log"},
    {"question": "What is the hidden folder called that Git uses to store its data?", "answer": ".git"},
    {"question": "What command is used to clone a repository in Git?", "answer": "git clone"},
    {"question": "What file is used to specify which files Git should ignore?", "answer": ".gitignore"},
]


def get_random_questions(n=5):
    return random.sample(LEVEL_ONE_QUESTIONS, min(n, len(LEVEL_ONE_QUESTIONS)))
