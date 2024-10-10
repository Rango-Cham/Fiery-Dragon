from position import Position
from constants import ROWS, COLS

CAVE_POSITIONS_EASY = {        
    1: Position((1,6)),  # top
    2: Position((6,13)), # right
    3: Position((13,8)), # down
    4: Position((8,1)), # left    
}

CAVE_POSITIONS = {        
    1: Position((1,COLS//2)),  # top
    2: Position((ROWS//2, COLS-2)), # right
    3: Position((ROWS-2,COLS//2)), # down
    4: Position((ROWS//2,1)), # left    
}

# CAVE_POSITIONS_HARD = {        
#     1: Position((1, 1)),  # top left
#     2: Position((1, 13)), # top right
#     3: Position((13, 1)), # down left
#     4: Position((13, 13)), # down right
# }


CHIT_POSITIONS_EASY = {
    1: Position((5, 6)),  
    2: Position((5, 8)),   
    3: Position((6, 5)),   
    4: Position((6, 7)),   
    5: Position((6, 9)),   
    6: Position((7, 6)),   
    7: Position((7, 8)),  
    8: Position((8, 5)),   
    9: Position((8, 7)),   
    10: Position((8, 9))
}

CHIT_POSITIONS = {
    1: Position((5, 5)),  
    2: Position((5, 7)),   
    3: Position((5, 9)),   
    4: Position((6, 4)),   
    5: Position((6, 6)),   
    6: Position((6, 8)),   
    7: Position((6, 10)),  
    8: Position((7, 5)),   
    9: Position((7, 9)),   
    10: Position((8, 4)), 
    11: Position((8, 6)),  
    12: Position((8, 8)),  
    13: Position((8, 10)), 
    14: Position((9, 5)),  
    15: Position((9, 7)),  
    16: Position((9, 9)),  
}

# CHIT_POSITIONS_HARD = {
#     1: Position((3, 6)),  
#     2: Position((3, 8)),   
#     3: Position((4, 5)),   
#     4: Position((4, 7)),   
#     5: Position((4, 9)),   
#     6: Position((5, 4)),   
#     7: Position((5, 6)),  
#     8: Position((5, 8)),   
#     9: Position((5, 10)),   
#     10: Position((6, 3)), 
#     11: Position((6, 5)),  
#     12: Position((6, 7)),  
#     13: Position((6, 9)), 
#     14: Position((6, 11)),  
#     15: Position((7, 4)),  
#     16: Position((7, 6)),  
#     17: Position((7, 8)),  
#     18: Position((7, 10)),   
#     19: Position((8, 3)),   
#     20: Position((8, 5)),   
#     21: Position((8, 7)),   
#     22: Position((8, 9)),   
#     23: Position((8, 11)),  
#     24: Position((9, 4)),   
#     25: Position((9, 6)),   
#     26: Position((9, 8)), 
#     27: Position((9, 10)),  
#     28: Position((10, 5)),  
#     29: Position((10, 7)), 
#     30: Position((10, 9)),  
#     31: Position((11, 6)),  
#     32: Position((11, 8))
# }

VOLC_POSITIONS_EASY = {
    1: [Position((2,6)),Position((2,8))],
    2: [Position((6,12)),Position((8,12))],
    3: [Position((12,8)),Position((12,6))],
    4: [Position((8,2)),Position((6,2))]
}

VOLC_POSITIONS = { # clockwise  # these are positions of each VC square
    1: [Position((2,6)),Position((2,7)),Position((2,8))],
    2: [Position((3,9)),Position((4,10)),Position((5,11))],
    3: [Position((6,12)),Position((7,12)),Position((8,12))],
    4: [Position((9,11)),Position((10,10)),Position((11,9))],
    5: [Position((12,8)),Position((12,7)),Position((12,6))],
    6: [Position((11,5)),Position((10,4)),Position((9,3))],
    7: [Position((8,2)),Position((7,2)),Position((6,2))],
    8: [Position((5,3)),Position((4,4)),Position((3,5))],
}

# VOLC_POSITIONS_HARD = { # clockwise  # these are positions of each VC square
#     1: [Position((2,6)),Position((2,7)),Position((2,8))],
#     2: [Position((3,9)),Position((4,10)),Position((5,11))],
#     3: [Position((6,12)),Position((7,12)),Position((8,12))],
#     4: [Position((9,11)),Position((10,10)),Position((11,9))],
#     5: [Position((12,8)),Position((12,7)),Position((12,6))],
#     6: [Position((11,5)),Position((10,4)),Position((9,3))],
#     7: [Position((8,2)),Position((7,2)),Position((6,2))],
#     8: [Position((5,3)),Position((4,4)),Position((3,5))],
# }