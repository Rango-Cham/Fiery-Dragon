from position import Position
from board_piece import Cave
import pygame 
from move import move_out


class Player:
    def __init__(self, cave: Cave, image:str, difficulty:str):        
        """ 
        initializes player at their assigned caves position.
        """
        self.id = cave.id
        self.cave = cave        
        
        self.image = pygame.image.load(image) 
        self._image_path = image
        self.curr_position = Position((cave.position.row, cave.position.col))
        cp = Position((cave.position.row, cave.position.col))
        self.initial_position = move_out(cp, difficulty)  # get position outside cave
                
        self.is_home = True
        
        self.num_pirates_clicked = 0  # Track consecutive Pirate Dragon clicks
        
        self.steps_taken = 0    # to track if player has made a round around the board.
                                # max number of steps = no. vol cards * no. squares + 2(step in and out the cave)
        
        self.is_finished = False    # track if player has won the game

        self.cave_occupied = True  # Track if player has found an empty cave
        
        
    def to_dict(self):
        return {
            'id': self.id,            
            'image': self._image_path,
            'curr_position': (self.curr_position.row, self.curr_position.col),            
            'is_home': self.is_home,
            'num_pirates_clicked': self.num_pirates_clicked,
            'steps_taken': self.steps_taken,
            'is_finished': self.is_finished,
            'cave_occupied': self.cave_occupied
        }
    
    @classmethod
    def from_dict(cls, cave:Cave, data:dict, difficulty:str):        
        player = cls(cave, data['image'], difficulty)
        player.id = data['id']
        player.curr_position = Position(data['curr_position'])
        player.is_home = data['is_home']
        player.num_pirates_clicked = data['num_pirates_clicked']
        player.steps_taken = data['steps_taken']
        player.is_finished = data['is_finished']
        player.cave_occupied = data['cave_occupied']
        return player