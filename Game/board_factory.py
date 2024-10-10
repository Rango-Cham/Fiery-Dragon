from abc import ABC, abstractmethod
from animal_factory import AbstractAnimalFactory
from board_piece import AbstractBoardPiece
from constants import CHIT_IMGS, CAVE_IMGS, EASY_VOLC_IMGS ,VOLC_IMGS
from const_vc_combinations import EASY_VC_COMBINATIONS, VC_COMBINATIONS
from board_piece import *
from random import shuffle
""" 
A board piece factory that utilizes the animal factory to 
create a set of board pieces.
"""    
class AbstractBoardFactory(ABC):
    def __init__(self, factory:AbstractAnimalFactory) -> None:
        super().__init__()
        self._factory = factory
        
    def create_caves(self, num: int) -> list[AbstractBoardPiece]:
        """ 
        creates a list of caves based on the number of players
        """
        animals = self._factory.create_cave_animals(num)
        caves = []
        for i in range(num):            
            caves.append(Cave(CAVE_IMGS[animals[i].type], animals[i]))            
        return caves

    @abstractmethod
    def create_volcano_cards(self): dict        
    
    def create_chits(self, num:int, difficulty:str) -> list[AbstractBoardPiece]:
        """ 
        creates a list of chit cards.
        """
        animals = self._factory.create_chit_animals(difficulty)
        chits = []
        for i in range(num): 
            img = f'{animals[i][1].type}_{abs(animals[i][0])}'            
            chits.append(Chit(CHIT_IMGS[img], animals[i][0], animals[i][1]))
        return chits 
    
    
class BoardFactory(AbstractBoardFactory):     
    """ 
    creates all the respective pieces along with assigning the correct
    image to display all the animals.
    """
    
    def __init__(self, factory:AbstractAnimalFactory) -> None:
        super().__init__(factory)         
         
    
    def create_volcano_cards(self) -> list[AbstractBoardPiece]:
        """ 
        creates a list of volcano cards with unique combinations
        of animals.
        """
        animals = self._factory.create_vc_animals(VC_COMBINATIONS) # dictionary of combinations
        cards = []
        for k, combi in animals.items():
            cards.append(VolcanoCard(VOLC_IMGS[k], combi, 3))
        
        return cards 


    
class EasyBoardFactory(AbstractBoardFactory):
    def __init__(self, factory: AbstractAnimalFactory) -> None:
        super().__init__(factory) 
    
    def create_volcano_cards(self) -> list[AbstractBoardPiece]:
        # 4 volcano cards, 2 squares each, 8 possible combinations, pick 4 random
        keys = list(EASY_VC_COMBINATIONS.keys())
        shuffle(keys)        
        combi = {}
        for i in range(len(keys)//2):
            combi[keys[i]] = EASY_VC_COMBINATIONS[keys[i]]
        animals = self._factory.create_vc_animals(combi)
        cards = []
        for k, combi in animals.items():
            cards.append(VolcanoCard(EASY_VOLC_IMGS[k], combi, 2))
        
        return cards 

