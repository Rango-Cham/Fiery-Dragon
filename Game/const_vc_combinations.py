from animal import *
EASY_VC_COMBINATIONS = {
    1: [BabyDragon, Salamander],
    2: [BabyDragon, Spider],
    3: [Salamander, BabyDragon],
    4: [Salamander, Bat],
    5: [Spider, Bat],
    6: [Spider, BabyDragon],
    7: [Bat, Salamander],
    8: [Bat, Spider]
}
VC_COMBINATIONS = {
    1: [BabyDragon, Bat, Spider],    
    2: [BabyDragon, Salamander, Bat],
    3: [Salamander, Spider, Bat],
    4: [Salamander, BabyDragon, Spider],
    5: [Spider, Salamander, BabyDragon],
    6: [Spider, Bat, Salamander],
    7: [Bat, Spider, BabyDragon],
    8: [Bat, BabyDragon, Salamander],
}
# HARD_VC_COMBINATIONS = {
#     1: list(MID_VC_COMBINATIONS[1]) + list(EASY_VC_COMBINATIONS[1]),
#     2: list(MID_VC_COMBINATIONS[2]) + list(EASY_VC_COMBINATIONS[2]),
#     3: list(MID_VC_COMBINATIONS[3]) + list(EASY_VC_COMBINATIONS[3]),
#     4: list(MID_VC_COMBINATIONS[4]) + list(EASY_VC_COMBINATIONS[4]),
#     5: list(MID_VC_COMBINATIONS[5]) + list(EASY_VC_COMBINATIONS[5]),
#     6: list(MID_VC_COMBINATIONS[6]) + list(EASY_VC_COMBINATIONS[6]),
#     7: list(MID_VC_COMBINATIONS[7]) + list(EASY_VC_COMBINATIONS[7]),
#     8: list(MID_VC_COMBINATIONS[8]) + list(EASY_VC_COMBINATIONS[8]),    
# }

