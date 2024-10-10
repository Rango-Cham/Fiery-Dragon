import pygame
import sys
from board import Board
from board_factory import EasyBoardFactory, BoardFactory
from animal_factory import EasyAnimalFactory, AnimalFactory
from constants import WIDTH, HEIGHT, BACKGROUND, BACKGROUND_MUSIC, DEFAULT_DIFFICULTY, SAVE_FILE
from gameflow import GameFlow
from pygame import mixer
import json
import os

""" 
Displays the welcome screen, 
Gets user input for number of players
Initialises the game board and gameflow
triggers the start of the game when player clicks start button
"""

# Initializing pygame and the mixer 
pygame.init()
pygame.mixer.init()

# Background music
mixer.music.load(BACKGROUND_MUSIC)
mixer.music.play(-1) # -1 allows the music to play in loop

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 80, 0)


class Button:
    def __init__(self, x, y, width, height, text, color, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

class Incrementer(Button):
    def __init__(self, x, y, width, height, text, color, font_size):
        super().__init__(x, y, width, height, text, color, font_size)

    def draw(self, window):
        super().draw(window)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        window.blit(text_surface, text_rect)


def welcome_screen(window):    

    # Fonts
    font = pygame.font.SysFont(None, 50)

    # Text
    welcome_text = font.render("Welcome to Fiery Dragon", True, WHITE)

    # Player incrementer buttons
    incrementer_width = 30
    incrementer_height = 30
    incrementer_x = WIDTH // 2 - 30
    incrementer_y = HEIGHT // 2 - 60
    incrementer_plus = Incrementer(incrementer_x, incrementer_y, incrementer_width, incrementer_height, "+", GREEN, 30)
    incrementer_minus = Incrementer(incrementer_x + incrementer_width + 10, incrementer_y, incrementer_width, incrementer_height, "-", GREEN, 30)

    # Difficulty buttons
    difficulty_x = WIDTH // 2 - 180 
    difficulty_y = HEIGHT // 2 + 100
    difficulty_width = 100
    difficulty_height = 40
    button_spacing = 20

    easy_button = Button(difficulty_x, difficulty_y, difficulty_width, difficulty_height, "Easy", BLUE, 30)
    medium_button = Button(difficulty_x + difficulty_width + button_spacing, difficulty_y, difficulty_width, difficulty_height, "Medium", BLUE, 30)
    hard_button = Button(difficulty_x + 2 * (difficulty_width + button_spacing), difficulty_y, difficulty_width, difficulty_height, "Hard", BLUE, 30)
    
    # Start button
    start_button_width = 200
    start_button_height = 50
    start_button_x = (WIDTH - start_button_width) // 2
    start_button_y = HEIGHT - 200
    start_button = Button(start_button_x, start_button_y, start_button_width, start_button_height, "START", GREEN, 50)

    # Reload Previous Game button
    # reload_button_width = 280
    # reload_button_height = 40
    # reload_button_x = start_button_x + (start_button_width - reload_button_width) // 2
    # reload_button_y = start_button_y + start_button_height + 15
    # reload_button = Button(reload_button_x, reload_button_y, reload_button_width, reload_button_height, "RELOAD PREVIOUS GAME", DARK_GREEN, 30)

    # Initial player count
    player_count = 2

    # Initial difficulty level
    difficulty = DEFAULT_DIFFICULTY

    # Main loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if incrementer_plus.rect.collidepoint(event.pos):
                    if player_count < 4:
                        player_count += 1
                elif incrementer_minus.rect.collidepoint(event.pos):
                    if player_count > 2:
                        player_count -= 1
                elif easy_button.rect.collidepoint(event.pos):
                    difficulty = "Easy"
                elif medium_button.rect.collidepoint(event.pos):
                    difficulty = "Medium"
                elif hard_button.rect.collidepoint(event.pos):
                    difficulty = "Hard"
                elif start_button.rect.collidepoint(event.pos):
                    # Start the game
                    return player_count, difficulty
                # elif reload_button.rect.collidepoint(event.pos):
                #     # Reload previous game
                #     return "reload"

        # Fill the background
        window.fill(BLACK)

        # Draw text
        text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        window.blit(welcome_text, text_rect)

        # Draw incrementer buttons
        incrementer_plus.draw(window)
        incrementer_minus.draw(window)

        # Draw difficulty buttons
        easy_button.draw(window)
        medium_button.draw(window)
        hard_button.draw(window)

        # Display player count
        player_count_text = font.render(f"Players: {player_count}", True, WHITE)
        player_count_rect = player_count_text.get_rect(midtop=(WIDTH // 2, incrementer_y + incrementer_height + 10))
        window.blit(player_count_text, player_count_rect)

        # Display difficulty level
        difficulty_text = font.render(f"Difficulty: {difficulty}", True, WHITE)
        difficulty_text_rect = difficulty_text.get_rect(midtop=(WIDTH // 2, difficulty_y - 50))
        window.blit(difficulty_text, difficulty_text_rect)

        # Draw start button
        start_button.draw(window)

        # Draw reload previous game button
        # reload_button.draw(window)

        # Update the display
        pygame.display.flip()

def ask_reload_previous_game_screen(window):    
    start_button_width = 200
    start_button_height = 50
    start_button_x = (WIDTH - start_button_width) // 2
    start_button_y = HEIGHT - 200    
    # Reload Previous Game button
    reload_button_width = 280
    reload_button_height = 40
    reload_button_x = start_button_x + (start_button_width - reload_button_width) // 2
    reload_button_y = start_button_y + start_button_height + 15
    reload_button = Button(reload_button_x, reload_button_y, reload_button_width, reload_button_height, "RELOAD PREVIOUS GAME", DARK_GREEN, 30)
    new_game_button = Button(start_button_x, start_button_y, reload_button_width, reload_button_height, "START NEW GAME", GREEN, 30)

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reload_button.rect.collidepoint(event.pos):
                    return "Reload"
                elif new_game_button.rect.collidepoint(event.pos):
                    return "New Game"

        window.fill(BLACK)
        new_game_button.draw(window)
        reload_button.draw(window)
        pygame.display.flip()

def new_game(window, player_count, difficulty):
    """ create new board and game flow"""        
    
    if difficulty == "Easy":
        a_fac = EasyAnimalFactory()
        b_fac = EasyBoardFactory(a_fac)
    else:
        a_fac = AnimalFactory()
        b_fac = BoardFactory(a_fac)    
        
    board = Board(b_fac, difficulty, player_count)    
    game_flow = GameFlow(board, window)
    
    if difficulty == "Easy":
        game_flow.run_easy()
    elif difficulty == "Medium":
        game_flow.run_medium()
    elif difficulty == "Hard":
        game_flow.run_hard()

def previous_game(window):
    with open(SAVE_FILE, 'r') as file:
        gamestate = json.load(file)
        
    board = Board.from_dict(gamestate['board'])
    game_flow = GameFlow(board, window)
    game_flow.curr_player = board.players[gamestate['current_player_id']-1]
    
    difficulty = board.difficulty    
    if difficulty == "Easy":
        game_flow.run_easy()
    elif difficulty == "Medium":
        game_flow.run_medium()
    elif difficulty == "Hard":
        game_flow.run_hard()


def main():
    pygame.init()
    pygame.display.set_caption("Fiery Dragon")
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    if os.path.exists(SAVE_FILE):
        button = ask_reload_previous_game_screen(window)
        
        if button == "Reload":
            previous_game(window)            
            return 
        else:
            os.remove(SAVE_FILE)
        
    # new game
    player_count, difficulty = welcome_screen(window) 
    new_game(window, player_count, difficulty) 




if __name__ == "__main__":
    main()
