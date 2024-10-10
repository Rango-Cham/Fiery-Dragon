import os
SAVE_FILE = 'savegame.json'

DEFAULT_DIFFICULTY = "Medium"
HEIGHT, WIDTH = 780, 850

ROWS, COLS = 15, 15
SQUARE_SIZE = (WIDTH//COLS, HEIGHT//ROWS)
BACKGROUND = "Black"

            # (normal, pirates, new)
NUM_EASY_CHITS = (8, 2, 0) #10
NUM_MID_CHITS = (12, 3, 1) #16
NUM_HARD_CHITS = (9, 4, 3) #16
# NUM_HARD_CHITS = (21, 6, 5) #32

MIN_CAVE = 2 
MAX_CAVE = 4

# Define directory paths
IMAGE_DIR = "images"
# HARD_VC_DIR = "hard_vc_imgs"
MID_VC_DIR = "mid_vc_imgs"
EASY_VC_DIR = "easy_vc_imgs"
MUSIC_DIR = "music"

BACKGROUND_MUSIC = os.path.join(MUSIC_DIR, "Thunder-Unison-Action-Dramatic-Epic-Music-chosic.wav")

CHIT_BACK = os.path.join(IMAGE_DIR, "chit_back.png")

CHIT_IMGS = {
    'BabyDragon_1': os.path.join(IMAGE_DIR, "BabyDragon_1.png"),
    'BabyDragon_2': os.path.join(IMAGE_DIR, "BabyDragon_2.png"),
    'BabyDragon_3': os.path.join(IMAGE_DIR, "BabyDragon_3.png"),
    'Bat_1': os.path.join(IMAGE_DIR, "Bat_1.png"),
    'Bat_2': os.path.join(IMAGE_DIR, "Bat_2.png"),
    'Bat_3': os.path.join(IMAGE_DIR, "Bat_3.png"),
    'Salamander_1': os.path.join(IMAGE_DIR, "Salamander_1.png"),
    'Salamander_2': os.path.join(IMAGE_DIR, "Salamander_2.png"),
    'Salamander_3': os.path.join(IMAGE_DIR, "Salamander_3.png"),
    'Spider_1': os.path.join(IMAGE_DIR, "Spider_1.png"),
    'Spider_2': os.path.join(IMAGE_DIR, "Spider_2.png"),
    'Spider_3': os.path.join(IMAGE_DIR, "Spider_3.png"),
    'PirateDragon_1': os.path.join(IMAGE_DIR, "PirateDragon_1.png"),
    'PirateDragon_2': os.path.join(IMAGE_DIR, "PirateDragon_2.png"),    
    'BadChit_0': os.path.join(IMAGE_DIR, "BadChit_0.png"),
}

CAVE_IMGS = {
    "BabyDragon": os.path.join(IMAGE_DIR, "cave_babyDragon.png"),
    "Bat": os.path.join(IMAGE_DIR, "cave_bat.png"),
    "Salamander": os.path.join(IMAGE_DIR, "cave_salamander.png"),
    "Spider": os.path.join(IMAGE_DIR, "cave_spider.png")
}

EASY_VOLC_IMGS = {
    1: os.path.join(EASY_VC_DIR, "img01.png"),
    2: os.path.join(EASY_VC_DIR, "img02.png"),
    3: os.path.join(EASY_VC_DIR, "img03.png"),
    4: os.path.join(EASY_VC_DIR, "img04.png"),
    5: os.path.join(EASY_VC_DIR, "img05.png"),
    6: os.path.join(EASY_VC_DIR, "img06.png"),
    7: os.path.join(EASY_VC_DIR, "img07.png"),
    8: os.path.join(EASY_VC_DIR, "img08.png"),
}
VOLC_IMGS = {
    1: os.path.join(MID_VC_DIR, "img1.png"),
    2: os.path.join(MID_VC_DIR, "img2.png"),
    3: os.path.join(MID_VC_DIR, "img3.png"),
    4: os.path.join(MID_VC_DIR, "img4.png"),
    5: os.path.join(MID_VC_DIR, "img5.png"),
    6: os.path.join(MID_VC_DIR, "img6.png"),
    7: os.path.join(MID_VC_DIR, "img7.png"),
    8: os.path.join(MID_VC_DIR, "img8.png"),
}
# HARD_VOLC_IMGS = {
#     1: os.path.join(HARD_VC_DIR, "img11.png"),
#     2: os.path.join(HARD_VC_DIR, "img22.png"),
#     3: os.path.join(HARD_VC_DIR, "img33.png"),
#     4: os.path.join(HARD_VC_DIR, "img44.png"),
#     5: os.path.join(HARD_VC_DIR, "img55.png"),
#     6: os.path.join(HARD_VC_DIR, "img66.png"),
#     7: os.path.join(HARD_VC_DIR, "img77.png"),
#     8: os.path.join(HARD_VC_DIR, "img88.png"),
# }

PLAYER_IMGS = {
    1: os.path.join(IMAGE_DIR, "player_yellow.png"), # Spider
    2: os.path.join(IMAGE_DIR, "player_red.png"), # Salamander
    3: os.path.join(IMAGE_DIR, "player_green.png"), # Baby Dragon
    4: os.path.join(IMAGE_DIR, "player_blue.png"), # Bat
}
