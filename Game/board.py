import pygame
from random import shuffle 
from position import Position 
from constants import ROWS, COLS, PLAYER_IMGS, BACKGROUND, NUM_EASY_CHITS,NUM_MID_CHITS
from player import Player
from board_factory import AbstractBoardFactory
from const_piece_positions import VOLC_POSITIONS_EASY, VOLC_POSITIONS, CHIT_POSITIONS_EASY, CHIT_POSITIONS, CAVE_POSITIONS_EASY, CAVE_POSITIONS
from board_piece import *
""" 
Board class creates all necessary cards and the player instances,
it randomizes the position of each card to give variety each game,
& displays and updates the game window.
"""


class Board:        
    
    def __init__(self, factory:AbstractBoardFactory|None, difficulty:str, num_players:int=2) -> None:
        """ 
        - utilises abstract factory to create all board pieces instances
        - creates a 2d array as an internal representation of each piece's location
        - creates player instances based on num_players        
        """     
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.vc_positions = VOLC_POSITIONS_EASY
            self.chit_positions = CHIT_POSITIONS_EASY
            self.cave_positions = CAVE_POSITIONS_EASY
        else:
            self.vc_positions = VOLC_POSITIONS
            self.chit_positions = CHIT_POSITIONS
            self.cave_positions = CAVE_POSITIONS
                        
        if factory is None:  # for reload game            
            return        
        
        # create the board pieces according to difficulty.
        if difficulty == "Easy":
            self.chits = factory.create_chits(sum(NUM_EASY_CHITS), difficulty)
            self.volcano_cards = factory.create_volcano_cards()            
                        
        else:            
            self.chits = factory.create_chits(sum(NUM_MID_CHITS), difficulty)             
            self.volcano_cards = factory.create_volcano_cards()            
            
        self.caves = factory.create_caves(num_players)
        # --------------------------------------------
        # max number of steps player can take around the board:
        self.max_steps = len(self.volcano_cards) * len(self.volcano_cards[0].squares) + 2 # (step in and out of cave)
        
        # assign randomized positions to each piece
        self.__assign_piece_positions()
        
        # 2d internal representation of the board.
        self.board = self.__create_board()    
        
        # create list of player instances and initialises the first player
        self.players = self.__create_players()
    
            
    def __assign_piece_positions(self) -> dict:
        """shuffles the lists of cards and assigns a position to each"""
        
        # chits
        keys = list(self.chit_positions.keys())
        # shuffle(self.chits)        
        for i in range(len(self.chits)):
            self.chits[i].position = self.chit_positions[keys[i]]
            self.chits[i].id = keys[i]
        
        # caves. 
        # if 2 players, their caves will be opposite each other,         
        # else follow clockwise direction.
        if len(self.caves) == 2:
            self.caves[0].position = self.cave_positions[1]
            self.caves[0].id = 1
            self.caves[1].position = self.cave_positions[3]
            self.caves[1].id = 2
        else:
            for i in range(len(self.caves)):
                self.caves[i].position = self.cave_positions[i+1]
                self.caves[i].id = i+1
        
        # volcano cards.
        keys = list(self.vc_positions.keys())
        shuffle(self.volcano_cards)
        for i in range(len(self.volcano_cards)):
            self.volcano_cards[i].id = keys[i]
            self.volcano_cards[i].set_square_positions(self.vc_positions[keys[i]])            
                                  
    def __create_board(self) -> list[list]:
        # 2d array
        board = [[0]*COLS for _ in range(ROWS)]
        
        # add caves, chits, vc->squares        
        for cave in self.caves:
            pos = cave.position
            board[pos.row][pos.col] = cave

        for vc in self.volcano_cards:
            for square in vc.squares:
                pos = square.position
                board[pos.row][pos.col] = square
        
        for chit in self.chits:
            pos = chit.position
            board[pos.row][pos.col] = chit

        return board
    
    def __create_players(self) -> list[Player]:
        """ 
        creates player instances and assigns them an image and cave.
        """
        players = [] 
        for i in range(len(self.caves)):
            if self.caves[i].animal.type == "Spider":
                image = PLAYER_IMGS[1]
            elif self.caves[i].animal.type == "Salamander":
                image = PLAYER_IMGS[2]
            elif self.caves[i].animal.type == "BabyDragon":
                image = PLAYER_IMGS[3]
            else: # bat
                image = PLAYER_IMGS[4]
                
            p = Player(self.caves[i], image, self.difficulty)
            players.append(p)         
        return players
    
    def __draw_caves(self,window) -> None:        
        """draws all caves onto the window"""
        for cave in self.caves:            
            window.blit(cave.image, cave.position.x_y)
    
    def __draw_chits(self, window) -> None:
        """ 
        draws all chits onto the window.
        """
        for chit in self.chits:
            if not chit.is_flipped:
                window.blit(chit.unflipped_image, chit.position.x_y)
            else:
                window.blit(chit.flipped_image, chit.position.x_y)    
                   
    def draw_players(self, window) -> None:
        """
        draws all players on the window
        """
        for p in self.players:
            window.blit(p.image, p.curr_position.x_y)
    
    def __draw_vol_cards(self, window) -> None: 
        if self.difficulty == "Easy":
            top, down = (240, 100), (240, 510)
            left, right = (140, 185), (570, 185)            
            pos = [top, right, down, left]
            
            rotation = 0
            for i in range(len(pos)):
                img = pygame.transform.rotozoom(self.volcano_cards[i].image, rotation, 1)
                window.blit(img, pos[i])
                rotation -= 90
                                                    
        else:   # medium / hard
            top, down = (312, 100),(312,610)
            left, right = (100,285), (640,285)
            tl, bl = (110,100), (112,460)
            tr, br = (490,104), (488,460)
      
            pos = [top, tr, right, br, down, bl, left, tl]
            
            rotation = 0        
            for i in range(len(pos)):            
                img = pygame.transform.rotozoom(self.volcano_cards[i].image, rotation, 1)
                window.blit(img, pos[i])
                rotation -= 45   
        
    
    def draw_board(self, window:pygame.Surface) -> None:       
        """ 
        draws all board pieces on the window
        """
        # public method to draw all board cards on the window        
        self.__draw_chits(window)
                
        self.__draw_vol_cards(window)
        
        # draw caves on top of volcano cards:
        self.__draw_caves(window)     
    
    def update_board(self, window) -> None:
        """
        redraws the board with players in their updated positions(if any).
        """                           
        window.fill(BACKGROUND)
        self.draw_board(window)
        self.draw_players(window) 
    
    
    def is_valid_move(self, curr_player:Player, new:Position) -> bool:
        """ 
        Checks if the potential new position is a valid move for the 
        player based on their number of steps taken
        Invalid moves: 
        - new position contains another player,
        - new position causes player to pass their cave after making 1 round
        """       
        # check if new_pos match current_pos of other players:
        for player in self.players:
            if player == curr_player:
                continue
            p_pos = player.curr_position
            if (p_pos.row, p_pos.col) == (new.row, new.col):
                return False
  
        # check if player is close to making 1 round around the board,
            # check if the new position would pass thier cave.
        if curr_player.steps_taken >= self.max_steps-3: # (max number of steps that can be made each turn is 3)
            if self.__player_passed_cave(curr_player):
                return False                                                                               
        return True
    
    def __player_passed_cave(self, player:Player) -> bool:
        if player.steps_taken >= self.max_steps:
            return True
        return False
    
    
    
    def to_dict(self):        
        return {
            'difficulty':   self.difficulty,
            'chits':        [chit.to_dict() for chit in self.chits],
            'vol_cards':    [vc.to_dict() for vc in self.volcano_cards],
            'caves':        [cave.to_dict() for cave in self.caves],
            'max_steps': self.max_steps,            
            'players': [p.to_dict() for p in self.players]
        }
        
        
    @classmethod
    def from_dict(cls, data:dict):
        board = cls(None, data['difficulty'])
        
        board.chits = [Chit.from_dict(chit) for chit in data['chits']]
        board.volcano_cards = [VolcanoCard.from_dict(vc) for vc in data['vol_cards']]                
        board.caves = [Cave.from_dict(cave) for cave in data['caves']]
        
        board.board = board.__create_board()
        
        board.max_steps = data['max_steps']
        players = []
        for i in range(len(board.caves)):
            players.append(Player.from_dict(board.caves[i], data['players'][i], board.difficulty))
        board.players = players        
        
        return board