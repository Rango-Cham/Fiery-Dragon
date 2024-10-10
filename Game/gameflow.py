import sys
from constants import WIDTH, HEIGHT, ROWS, COLS, SAVE_FILE
import pygame
from board import Board 
from board_piece import *
import move
from board_factory import EasyBoardFactory
from animal_factory import EasyAnimalFactory
from player import Player
import json
import os

CHIT_UP_TIME = 1000  # amount of time chit remains face up
TURN_LIMIT_TIME = 20000  # 20 seconds turn limit

""" 
Gameflow controls the game loop and the overall flow.
Is based on the template design pattern.
Implements all game logic for the loop.
"""

class GameFlow:
    def __init__(self, board: Board, window: pygame.Surface) -> None:
        self.window = window
        self.board: Board = board  # creates the initial board.
        self.curr_player: Player = self.board.players[0]        
        self.turn_start_time = pygame.time.get_ticks()  # Initialize turn start time
        self.extra_move = False  # Track if the player gets an extra move

    def run_easy(self):
        """The main loop for the easy difficulty where the game runs without a timer."""
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_game()
                    pygame.quit()
                    sys.exit()  # Use sys.exit() for a clean exit

                if not self.is_chit_open():  # ensure 1 chit is flipped at a time
                    self.flip_chit(event)  # -> flips chit & moves/switches player

            # check for any winners
            if self.have_winner():
                self.win_game()
            else:  # update display
                self.unflip_chits()  # -> unflips after some seconds
                self.board.update_board(self.window)
                self.display_current_player()
            
            pygame.display.update()

    def run_medium(self):
        """The main loop for the medium difficulty where the game runs with a resetting timer."""
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_game()
                    pygame.quit()
                    sys.exit()  # Use sys.exit() for a clean exit

                if not self.is_chit_open():  # ensure 1 chit is flipped at a time
                    self.flip_chit(event, reset_timer=True)  # -> flips chit & moves/switches player

            # Check if the turn time limit is exceeded
            if pygame.time.get_ticks() - self.turn_start_time > TURN_LIMIT_TIME:
                self.penalize_player()
                self.switch_player()
                self.turn_start_time = pygame.time.get_ticks()  # Reset turn start time

            # check for any winners
            if self.have_winner():
                self.win_game()
            else:  # update display
                self.unflip_chits()  # -> unflips after some seconds
                self.board.update_board(self.window)
                self.display_current_player()
                self.display_timer()
            
            pygame.display.update()

    def run_hard(self):
        """The main loop for the hard difficulty where the game runs with a non-resetting timer."""
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_game()
                    pygame.quit()
                    sys.exit()  # Use sys.exit() for a clean exit

                if not self.is_chit_open():  # ensure 1 chit is flipped at a time
                    self.flip_chit(event, reset_timer=False)  # -> flips chit & moves/switches player

            # Check if the turn time limit is exceeded
            if pygame.time.get_ticks() - self.turn_start_time > TURN_LIMIT_TIME:
                self.switch_player()
                self.turn_start_time = pygame.time.get_ticks()  # Reset turn start time

            # check for any winners
            if self.have_winner():
                self.win_game()
            else:  # update display
                self.unflip_chits()  # -> unflips after some seconds
                self.board.update_board(self.window)
                self.display_current_player()
                self.display_timer()
            
            pygame.display.update()

    def flip_chit(self, event, reset_timer=False) -> None:
        """Checks if a click was done on a chit.
        Triggers move player if the chit was a match or a pirate dragon.
        Triggers switch player if it was a non-match."""
        if event.type == pygame.MOUSEBUTTONUP:
            for chit in self.board.chits:
                if chit.chit_clicked(event):
                    if self.is_match_or_pirate(chit):
                        print(f"Player clicked {chit.animal.type}")
                        self.move(chit.steps)
                        if reset_timer:
                            self.turn_start_time = pygame.time.get_ticks()  # Reset timer if it's a correct click
                        return
                    elif self.is_bad_pirate(chit):
                        self.move_to_cave()
                        return
                    else:
                        self.switch_player()
                        return
    
    
    def is_chit_open(self) -> bool:
        """Check if any chit is currently flipped open."""
        return any(chit.is_flipped for chit in self.board.chits)
    
    def unflip_chits(self) -> None: 
        """
        Checks if any chit is flipped open, and
        closes them if (some) seconds has passed.        
        """                
        current_time = pygame.time.get_ticks()
        for chit in self.board.chits:
            if chit.is_flipped and current_time - chit.flip_time >= CHIT_UP_TIME:  # Check if it's time to close
                chit.is_flipped = False
    
    def is_match_or_pirate(self, chit:Chit):
        """ 
        returns true if the current chit clicked
        matches the players position, or if its a 
        pirate dragon.
            
        -   updates players' consecutive pirate dragons tracker.
        """
        pos = self.curr_player.curr_position
        square = self.board.board[pos.row][pos.col]
        if square.animal.type == chit.animal.type:
            print(f'Player {self.curr_player.id} was standing on {square.animal.type}')
            self.curr_player.num_pirates_clicked = 0
            return True
        elif chit.animal.type == "PirateDragon":
            self.curr_player.num_pirates_clicked += 1
            return True
        return False
    
    def is_bad_pirate(self, chit:Chit):
        """ 
        returns true if the current chit clicked
        is a bad chit
        """
        if chit.animal.type == "BadChit":
            self.curr_player.num_pirates_clicked += 1
            return True
        return False

    def get_cave_player(self, pos:Position) -> Player:
        """
        returns which players cave the current player is on
        """
        if len(self.board.players) > 2:
            if pos.row < ROWS//2 and pos.col == COLS//2:
                cave_id = 0
            elif pos.row == ROWS//2 and pos.col > COLS//2:
                cave_id = 1
            elif pos.row > ROWS//2 and pos.col == COLS//2:
                cave_id = 2
            else:
                if len(self.board.players) == 4: cave_id = 3
        
        elif len(self.board.players) == 2:
            if pos.row < ROWS//2 and pos.col == COLS//2:
                cave_id = 0
            else:
                cave_id = 1

        return self.board.players[cave_id]

    def move(self, steps:int) -> None:
        """
        Moves the player the specified amount of steps around the board.
        
        Helps player enter and exit their cave when necessary.
        
        Checks if player can reenter their cave to win.
        
        Validates the new position before updating the players position
        
        Checks if player has clicked 2 pirates in a row
        
        Triggers switch player if new position is invalidated or clicked 
        2 pirate dragons in a row.                                
        """
        pos = self.curr_player.curr_position
        new_pos = Position((pos.row,pos.col))

        if steps < 0:   # move backwards.
            if self.curr_player.is_home: # do nothing
                if self.curr_player.num_pirates_clicked >= 2:
                    self.switch_player()
                return 
            
            if self.curr_player.steps_taken == 1:
                self.curr_player.curr_position = move.move_in(pos)
                self.curr_player.steps_taken = 0
                self.curr_player.is_home = True
                self.get_cave_player(self.curr_player.curr_position).cave_occupied = True
                return

            # move backward
            for i in range(abs(steps)):
                sq = self.board.board[new_pos.row][new_pos.col]
                vc = self.board.volcano_cards[sq.id - 1]
                if vc.id == 1:
                    prev_vc = self.board.volcano_cards[len(self.board.volcano_cards) - 1]
                else:
                    prev_vc = self.board.volcano_cards[vc.id - 2]
            
                new_pos = move.move_backward(new_pos, sq, vc, prev_vc)
            
        else:
            if self.curr_player.is_home:
                self.get_cave_player(self.curr_player.curr_position).cave_occupied = False
                new_pos = move.move_out(new_pos, self.board.difficulty)
                steps -= 1
                
            for i in range(steps):  # move forwards
                sq = self.board.board[new_pos.row][new_pos.col]
                vc = self.board.volcano_cards[sq.id - 1]
                if vc.id == len(self.board.volcano_cards):
                    next_vc = self.board.volcano_cards[0]
                else:
                    next_vc = self.board.volcano_cards[vc.id]
                                                   
                if i == steps-1: # (last step for current round)
                    # check if player has went around the board and is near their cave
                    if self.curr_player.steps_taken >= self.board.max_steps-3: # player is at most 3 steps away from cave (including step in)
                        # check if player is exactly outside their cave
                        outside_pos = self.curr_player.initial_position
                        if (new_pos.row, new_pos.col) == (outside_pos.row, outside_pos.col):
                            new_pos = move.move_in(new_pos)
                            self.curr_player.curr_position.update_pos((new_pos.row, new_pos.col))
                            self.curr_player.is_finished = True
                            return # exit early.                                    
                new_pos = move.move_forward(new_pos, sq, vc, next_vc)
        
        # check valid move
        if self.board.is_valid_move(self.curr_player, new_pos):
            # update player pos
            self.curr_player.curr_position = new_pos
            
            # update steps
            self.curr_player.steps_taken += steps
            if self.curr_player.is_home:
                self.curr_player.is_home = False
                self.curr_player.steps_taken += 1 
            
            if self.curr_player.steps_taken < 0: # puts players back in their cave
                self.curr_player.steps_taken = 0
                self.curr_player.is_home = True
                self.get_cave_player(self.curr_player.curr_position).cave_occupied = True
                self.curr_player.curr_position = move.move_in(self.curr_player.initial_position)
            
            ####
            sq = self.board.board[new_pos.row][new_pos.col]
            print(f'Player {self.curr_player.id} now standing on {sq.animal.type}')
            print(f'Player {self.curr_player.id} total steps taken: {self.curr_player.steps_taken}')            
            ####
            if self.curr_player.num_pirates_clicked >= 2:  # if clicked 2 pirates in a row: end turn
                self.switch_player()

        else:
            self.switch_player()

    def move_to_cave(self) -> None:
        """ 
        Moves the player back to their cave.
        """
        # pos = self.curr_player.initial_position
        # new_pos = move.move_in(pos)
        # self.curr_player.curr_position = new_pos
        # self.curr_player.is_home = True
        # self.curr_player.steps_taken = 0
        if self.curr_player.is_home:
            if self.curr_player.num_pirates_clicked >= 2:
                self.switch_player()            
            return
        
        num_of_players = len(self.board.players)
        pos = self.curr_player.curr_position

        if num_of_players > 2:
            if pos.row <= ROWS//2 and pos.col > COLS//2:
                cave_id = 0
            elif pos.row > ROWS//2 and pos.col >= COLS//2:
                cave_id = 1
            elif pos.row >= ROWS//2 and pos.col < COLS//2:
                cave_id = 2
            else:
                if num_of_players==4: 
                    cave_id = 3 
                else: 
                    cave_id = 2
        elif num_of_players == 2:
            if (pos.col == COLS//2 and pos.row > ROWS//2) or (pos.col > COLS//2):
                cave_id = 0
            else:
                cave_id = 1

        # print("target cave id:", cave_id)

        found_empty_cave = False
        while not found_empty_cave:
            cave_player = self.board.players[cave_id]
            if not cave_player.cave_occupied:
                found_empty_cave = True
                pos = cave_player.initial_position
                new_pos = move.move_in(pos)
                self.curr_player.curr_position = new_pos
                self.curr_player.is_home = True
                self.curr_player.steps_taken = 0
                cave_player.cave_occupied = True
                break
            else:
                cave_id -= 1
                if cave_id < 0:
                    cave_id = num_of_players - 1            

        # print("final cave id:", cave_id)
        if self.curr_player.num_pirates_clicked >= 2:
            self.switch_player()            

    def switch_player(self) -> None:
        """updates current player to the next player based on their id"""
        self.curr_player.num_pirates_clicked = 0  # Reset the counter for consecutive clicks
        self.extra_move = False  # Reset extra move flag

        if self.curr_player == self.board.players[-1]:  # if last player,
            self.curr_player = self.board.players[0]  # loop back to first player
        else:
            for i in range(len(self.board.players) - 1):
                if self.board.players[i] == self.curr_player:
                    self.curr_player = self.board.players[i + 1]
                    break

        self.turn_start_time = pygame.time.get_ticks()  # Reset turn start time for new player
    
    def penalize_player(self) -> None:
        """Penalize the current player by moving them back one step."""
        print(f'Player {self.curr_player.id} exceeded the time limit and is penalized')
        self.move(-1)  # Move back one step

    def have_winner(self) -> bool:
        """returns true if a player has won"""
        for p in self.board.players:
            if p.is_finished:
                return True
        return False

    def display_current_player(self):
        """Displays who is the current player onto the window"""
        
        # color = ""        
        if self.curr_player.cave.animal.type == "Spider":
            color = "Yellow"
        elif self.curr_player.cave.animal.type == "Salamander":
            color = "Red"
        elif self.curr_player.cave.animal.type == "BabyDragon":
            color = "Green"
        else: # Bat
            color = "Blue"
        
        # PLAYER_COLORS = {
        #     0: "Red",
        #     1: "Green",
        #     2: "Blue",
        #     3: "Yellow"
        # }
        # color = PLAYER_COLORS.get(self.curr_player.id, "Unknown")
        f_string = color + " Player's Turn"
        display_font = pygame.font.SysFont('None', 32)
        display_text = display_font.render(f_string, True, (255, 255, 255))
        self.window.blit(display_text, (0, 0))



    def display_timer(self):
        """displays the timer onto the window"""
        time_left = TURN_LIMIT_TIME - (pygame.time.get_ticks() - self.turn_start_time)
        time_left = max(0, time_left)
        time_left = time_left // 1000
        f_string = "Time Left: " + str(time_left)
        display_font = pygame.font.SysFont('None', 32)
        display_text = display_font.render(f_string, True, (255, 255, 255))
        self.window.blit(display_text, (WIDTH - 150, 0))

    def win_game(self):
        "displays the win screen till player closes display"
        
        win_text = "Player " + str(self.curr_player.id) + " wins!"
        display_font = pygame.font.SysFont('None', 32)
        display_text = display_font.render(win_text, True, (255, 255, 255))
        text_rect = display_text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)

        self.board.update_board(self.window)  # draws winner in their cave
        self.display_current_player()
        pygame.display.update()
        
        pygame.time.wait(1000)  # so can see player in their cave

        while True:
            self.window.fill('Black')
            self.window.blit(display_text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    if os.path.exists(SAVE_FILE): # delete old save file if exists.
                        os.remove(SAVE_FILE)
                    
                    pygame.quit()
                    sys.exit()  # Use sys.exit() for a clean exit
            pygame.display.update()


#===============================    
    def save_game(self):                 
        save = {
            'board': self.board.to_dict(),
            'current_player_id': self.curr_player.id
        }
        
        with open(SAVE_FILE, 'w') as file:
            json.dump(save, file)

if __name__ == "__main__":
    
    
    pygame.init()
    pygame.display.set_caption("Fiery Dragon")
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Initializing the board and game flow for different difficulty
    difficulty = "Medium"  # Change this to "Easy", "Medium", or "Hard"
    if difficulty == "Easy":
        b = Board(EasyBoardFactory(EasyAnimalFactory()), "Easy", 4)
        gf = GameFlow(b, window)
        gf.run_easy()
    elif difficulty == "Medium":
        b = Board(EasyBoardFactory(EasyAnimalFactory()), "Medium", 4)
        gf = GameFlow(b, window)
        gf.run_medium()
    elif difficulty == "Hard":
        b = Board(EasyBoardFactory(EasyAnimalFactory()), "Hard", 4)
        gf = GameFlow(b, window)
        gf.run_hard()      
    
    pass
