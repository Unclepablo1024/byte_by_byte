import os
import random
import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Character settings
CHARACTER_INITIAL_X = 50
CHARACTER_GROUND_LEVEL = SCREEN_HEIGHT - 160  # Assuming character height is 128
CHARACTER_GRAVITY = 1
CHARACTER_JUMP_STRENGTH = -20
FRAME_RATE = 100  # Milliseconds per frame

# Movement speed
SCROLL_SPEED = 5
RUN_SPEED_MULTIPLIER = 2

# Paths

FONT_PATH = os.path.join("fonts", "determinationmono.ttf")
AUDIO_PATH = os.path.join("audio")
BASE_SPRITES_PATH = os.path.join("sprites")
LOGO_PATH = os.path.join("logo", "icon.png")
PIC_PATH = os.path.join("pic")

# Background settings
BACKGROUND_IMAGE_PATH = os.path.join(BASE_SPRITES_PATH, 'backgrounds', 'City2_pale.png')
BACKGROUND_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Character sprites
IDLE_PICTURE_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Idlefix.png')
WALK_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Walk.png')
JUMP_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Jump.png')
RUN_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Run.png')
HURT_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Hurt.png')
DIE_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Dead.png')
ATTACK_1_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Attack_1.png')
ATTACK_2_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Attack_2.png')
ATTACK_3_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Attack_3.png')

# Health bar settings
HEALTH_BAR_MAX_HEALTH = 200
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_X = 600 - 30
HEALTH_BAR_Y = 30
HEALTH_BAR_COLOR = (0, 255, 0)

LIFE_ICON_PATH = os.path.join(BASE_SPRITES_PATH, 'Life_icon.png')
LIFE_ICON_SIZE = 52
LIFE_ICON_SPACING = 1
INITIAL_LIVES = 3

# Dialogue settings
DIALOGUE_FONT_SIZE = 32
DIALOGUE_TEXT_COLOR = (255, 255, 255)
DIALOGUE_BOX_IMAGE_PATH = os.path.join(BASE_SPRITES_PATH, 'Dialouge', 'Dialouge boxes', 'BetterDialouge1.png')
DIALOG_COOLDOWN_TIME = 2000  # 2 seconds cooldown


LEVELS = {
    1: {
        "background": os.path.join(BASE_SPRITES_PATH, "backgrounds", "City2_pale.png"),
        "enemies": ["Homeless_1", "Homeless_2", "Homeless_3"],
        "music": os.path.join(AUDIO_PATH, 'western.mp3'),
        "max_enemies": 5
    },
    2: {
        "background": os.path.join(BASE_SPRITES_PATH, "backgrounds", "City3.png"),
        "enemies": ["Homeless_1", "Homeless_2", "Homeless_3", "Robot_1", "Robot_2", "Robot_3"],
        "music": os.path.join(AUDIO_PATH, 'cyberpunk.mp3'),
        "max_enemies": 10
    },
    3: {
        "background": os.path.join(BASE_SPRITES_PATH, "backgrounds", "City4.png"),
        "enemies": ["Homeless_1", "Homeless_2", "Homeless_3", "Robot_1", "Robot_2", "Robot_3", "Vampire_1", "Vampire_3", "Dog", "Cat"],
        "music": os.path.join(AUDIO_PATH, 'bleach.mp3'),
        "max_enemies": 20
    }
}

# Enemy settings
ENEMY_TYPES = ["Homeless_1", "Homeless_2", "Homeless_3"]
ENEMY_SPRITES_PATH = os.path.join(BASE_SPRITES_PATH, 'enemies')

MAX_ENEMIES = 5

ENEMY_POSITION = 565
# Attack animations paths
ATTACK_1_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Attack_1.png')
ATTACK_2_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Attack_2.png')
ATTACK_3_GIF_PATH = os.path.join(BASE_SPRITES_PATH, 'Gangsters_2', 'Attack_3.png')
ATTACK_RANGE = 80

# Attack sounds path
ATTACK_1_SOUNDS_PATH =os.path.join(AUDIO_PATH, 'attack1.mp3')
ATTACK_2_SOUNDS_PATH =os.path.join(AUDIO_PATH, 'attack2.mp3')
ATTACK_3_SOUNDS_PATH =os.path.join(AUDIO_PATH, 'attack3.wav')

# Music and sound settings
DEATH_SOUND_PATH = os.path.join(AUDIO_PATH, 'pain-scream.wav')
MAIN_SOUND_PATH = os.path.join(AUDIO_PATH, 'western.mp3')

# Game over settings
GAME_OVER_FONT_PATH = os.path.join(FONT_PATH)

#Congrats page ending setting
congrats_image = pygame.image.load(os.path.join(PIC_PATH, 'congrats.png'))

# Dialog settings
DIALOG_FONT_PATH = os.path.join(FONT_PATH)
DIALOGUE_FONT_SIZE = 24
DIALOG_COOLDOWN_TIME = 2000  # 2 seconds in milliseconds


# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

BOSSES1_FOLDER_PATH = os.path.join(BASE_SPRITES_PATH, 'Bosses', 'Boss1')
BOSSES2_FOLDER_PATH = os.path.join(BASE_SPRITES_PATH, 'Bosses', 'Boss2')
BOSSES3_FOLDER_PATH = os.path.join(BASE_SPRITES_PATH, 'Bosses', 'Boss3')
IDLE_PATH = os.path.join(BOSSES1_FOLDER_PATH, 'Idlefix.png')
WALK_PATH = os.path.join(BOSSES1_FOLDER_PATH, 'Walk.png')
JUMP_PATH = os.path.join(BOSSES1_FOLDER_PATH, 'Jump.png')
RUN_PATH = os.path.join(BOSSES1_FOLDER_PATH, 'Run.png')
HURT_PATH = os.path.join(BOSSES1_FOLDER_PATH, 'Hurt.png')
DIE_PATH = os.path.join(BOSSES1_FOLDER_PATH, 'Dead.png')

# Load common fonts
font = pygame.font.Font(FONT_PATH, 24)
large_font = pygame.font.Font(FONT_PATH, 36)
small_font = pygame.font.Font(FONT_PATH, 18)
title_font = pygame.font.Font(FONT_PATH, 48)

# Load common sounds
correct_sound = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "get_point.wav"))
wrong_sound = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "lost-sobbing.wav"))
hit_sound = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "hit.wav"))
duck_sound = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "duck.wav"))
congra_sound = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "cheer.wav"))
congra_sound.set_volume(0.2)

# Load common pic
fight_image = pygame.image.load(os.path.join(BASE_SPRITES_PATH, 'fight.png'))
bang_image = pygame.image.load(os.path.join(BASE_SPRITES_PATH, 'bang.png'))
congra_image = pygame.image.load(os.path.join(PIC_PATH, 'congra.png'))
coffee_image = pygame.image.load(os.path.join(PIC_PATH, 'coffee.png'))
noway_image = pygame.image.load(os.path.join(PIC_PATH, 'anoway.png'))
awesome_image = pygame.image.load(os.path.join(PIC_PATH, 'awesome.jpg'))
excellent_image = pygame.image.load(os.path.join(PIC_PATH, 'fexcellent.png'))
ending_image = pygame.image.load(os.path.join(PIC_PATH, 'ending.png'))
wrong_image = pygame.image.load(os.path.join(PIC_PATH, 'fwrong.png'))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
HINT_BG_COLOR = (255, 255, 200)
HINT_TEXT_COLOR = (0, 100, 0)
LIGHT_GRAY = (200, 200, 200)

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


#level 1 dialog
LEVEL_ONE_DIALOGUE =  {1:"You: What do I do know!? I lost my job and know nothing about coding", 2: "Enemy: Spare Change!",
    3:"You: Sorry man I don't have any..", 4:"Enemy: We will see about that, guys!! Take his money.",
    5:"Zoey Tip: Click your right mouse button to atack enemies.", 6:" Enemy: Our leader will show you who is boss."}


LEVEL_TWO_DIALOGUE = {
    1: "You: A futuristic city? How did I end up here?",
    2: "Enemy: You thought you could escape us? Think again.",
    3: "You: Seriously? You followed me here too?",
    4: "Enemy: We don't work alone. Meet our new friend, the robot!",
    5: "Robot: Target acquired. Initiating Fibonacci sequence challenge.",
    6: "You: Guess I'll have to code my way out of this one!"
}

LEVEL_THREE_DIALOGUE = {
    1: "You: This place just keeps getting crazier... Now it's swarming with enemies!",
    2: "Enemy: We’ve got new allies. Meet the vampires, dogs, and cats!",
    3: "Vampire: Your blood won’t save you from the data structures we command.",
    4: "You: Great, now I have to deal with vampires and their pets?",
    5: "Dog: Woof! Fetch the data, or face the consequences.",
    6: "You: Alright, let's see how well you handle my coding skills!"
}

def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    while words:
        line_words = []
        while words:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > max_width:
                break
        lines.append(' '.join(line_words))
    return lines