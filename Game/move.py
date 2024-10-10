from constants import ROWS, COLS
from board_piece import VolcanoCard, VcSquare
from const_piece_positions import CAVE_POSITIONS_EASY as cpe
from position import Position


""" 
move functions that returns updated positions in the 
specified direction based on input
"""


def move_out(pos: Position, difficulty:str) -> Position:
    """
    returns position outside of player's cave based on where 
    they are on the board
    """    
    if difficulty == "Easy":
        if (pos.row, pos.col) == (cpe[1].row,cpe[1].col): #top
            new_pos = move_down(pos)
        elif (pos.row, pos.col) == (cpe[2].row,cpe[2].col): #right
            new_pos = move_left(pos)
        elif (pos.row, pos.col) == (cpe[3].row,cpe[3].col): #down
            new_pos = move_up(pos)
        else: # left
            new_pos = move_right(pos)
    else:
        if pos.col < COLS//2: # at left
            new_pos = move_right(pos)
        elif pos.col > COLS//2: # at right
            new_pos = move_left(pos)            
        
        elif pos.row < ROWS//2: # at top
            new_pos = move_down(pos)
        else:                   # at down
            new_pos = move_up(pos)
    
    return new_pos

def move_in(pos: Position) -> Position:
    """
    used to move player into their cave 
    """    
    if pos.col < COLS//2: # at left
        new_pos = move_left(pos)
    elif pos.col > COLS//2: # at right
        new_pos = move_right(pos)            
    
    elif pos.row < ROWS//2: # at top
        new_pos = move_up(pos)
    else:                   # at down
        new_pos = move_down(pos)
    
    return new_pos

def move_forward(pos: Position, curr_sq:VcSquare, curr_vc:VolcanoCard, next_vc:VolcanoCard) -> Position:
    """ updates input position and returns it 1 step in the forwards direction """
    next = None                    
    for i in range(len(curr_vc.squares)-1):
        if curr_vc.squares[i] == curr_sq:
            next = curr_vc.squares[i+1].position
            break
    if curr_sq == curr_vc.squares[-1]:
        next = next_vc.squares[0].position
    
    pos.update_pos((next.row, next.col))
    return pos

def move_backward(pos: Position, curr_sq:VcSquare, curr_vc:VolcanoCard, prev_vc:VolcanoCard) -> Position:
    """ updates input position and returns it 1 step in the backwards direction """
    next = None
    if curr_sq == curr_vc.squares[0]:
        next = prev_vc.squares[-1].position
        
    else: 
        for i in range(1, len(curr_vc.squares)):
            if curr_sq == curr_vc.squares[i]:
                next = curr_vc.squares[i-1].position
                break     
    pos.update_pos((next.row, next.col))
    return pos

def move_up(pos: Position) -> Position:
    """moves position 1 row up"""
    new = (max(0, pos.row-1), pos.col)
    return Position(new)

def move_down(pos: Position) -> Position:
    """moves position 1 row down"""
    new = (min(ROWS-1, pos.row+1), pos.col)    
    return Position(new)

def move_left(pos: Position) -> Position:
    """moves position 1 column to the left"""
    new = (pos.row, pos.col-1)    
    return Position(new)

def move_right(pos: Position) -> Position:
    """moves position 1 column to the right"""
    new = (pos.row, pos.col+1)     
    return Position(new)