from abc import ABC
import pygame
from animal import Animal, BabyDragon
from position import Position
from constants import CHIT_BACK, SQUARE_SIZE

""" 
Abstract board piece class & its child classes: Volcano Card, Cave & Chit.
Eeach card knows their location, image & the animal(s) displayed on them.
"""

class AbstractBoardPiece(ABC):
    def __init__(self, image:str, animal:Animal) -> None:
        super().__init__()         
        self.animal = animal 
        self.image = pygame.image.load(image)
        self._image_path = image
        self.id = None 
        self.position = None # id & position to be set in board
        
    def to_dict(self):
        return {            
            'image': self._image_path,
            'animal': self.animal.type,
        }
        
    @classmethod
    def from_dict(cls, data:dict):
        return cls(data['image'], Animal.from_dict(data['animal']))

class Cave(AbstractBoardPiece):    
    def __init__(self, image: str, animal: Animal) -> None:
        super().__init__(image, animal)                    
    
    def to_dict(self):
        parent_dict = super().to_dict()  # Call parent class's to_dict method
        chit_dict = {
            'id': self.id,
            'position': (self.position.row, self.position.col),            
        }
        # Combine dictionaries
        parent_dict.update(chit_dict)
        return parent_dict
    
    
    @classmethod
    def from_dict(cls, data: dict):
        cave = super().from_dict(data)
        cave.id = data['id']
        cave.position = Position(data['position'])
        return cave
    
class Chit(AbstractBoardPiece): 
    def __init__(self, image: str, steps:int, animal: Animal) -> None:
        super().__init__(image, animal)
        self.steps = steps
        self.flipped_image = pygame.image.load(image)
        self.unflipped_image = pygame.image.load(CHIT_BACK)
        
        self.is_flipped = False     # Initially all chits are closed
        self.flip_time = 0          # Timestamp when the chit was flipped open
    
    def chit_clicked(self, event) -> bool:
        """ 
        flips the chit if a player clicks on it,
        records the timestamp when it was clicked.
        """
        rect = pygame.Rect(self.position.x_y, SQUARE_SIZE)
        if rect.collidepoint(event.pos):
            if not self.is_flipped:  # Flip only if it's not already flipped
                self.is_flipped = True
                self.flip_time = pygame.time.get_ticks()  # Record the time it was flipped open
                return True
        return False

    def to_dict(self):
        parent_dict = super().to_dict() 
        chit_dict = {
            'id': self.id,
            'position': (self.position.row, self.position.col),
            'steps': self.steps,            
            'is_flipped': self.is_flipped,
            'flip_time': self.flip_time
        }
        
        parent_dict.update(chit_dict)
        return parent_dict

    @classmethod
    def from_dict(cls, data: dict):
        # chit = super().from_dict(data)
        chit = cls(data['image'], data['steps'], Animal.from_dict(data['animal']))
        chit.id = data['id']
        chit.position = Position(data['position'])
        chit.is_flipped = data['is_flipped']
        chit.flip_time = data['flip_time']
        
        return chit
        
class VolcanoCard(AbstractBoardPiece):
    def __init__(self, image: str, animals: list[Animal], num_squares:int) -> None:
        super().__init__(image, None)
        squares = []
        for i in range(num_squares):
            squares.append(VcSquare(animals[i]))
        self.squares = squares
                
    def set_square_positions(self, positions:list[Position]):
        """ sets the positions to each square"""
        for i in range(len(positions)):
            self.squares[i].position = positions[i]
            self.squares[i].id = self.id
    
    def to_dict(self):                
        vc_dict = {
            'image': self._image_path,
            'id': self.id,    
            'animals': [sq.animal.type for sq in self.squares],
            'positions': [(sq.position.row, sq.position.col) for sq in self.squares]            
        }        
        return vc_dict
    
    @classmethod
    def from_dict(cls, data: dict):
        animals = [Animal.from_dict(animal) for animal in data['animals']]        
        positions = [Position(pos) for pos in data['positions']]
        
        vc = cls(data['image'], animals, len(positions))
        vc.id = data['id']
        vc.set_square_positions(positions)
        
        return vc
        
class VcSquare(VolcanoCard):
    """ 
    created only by Volcano Card class, so that each individual position 
    on a volcano card can be known and accessed.
    """
    def __init__(self, animal: Animal) -> None:        
        self.id = None  
        self.animal = animal
        self.position = None
        
        
if __name__ == "__main__":
    cave = Cave("images/cave_babyDragon.png", BabyDragon())
    cave.position = Position((1,2))
    print(cave.to_dict())
    pass 