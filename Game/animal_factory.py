from abc import ABC, abstractmethod
from animal import *
from random import shuffle, choice
from const_vc_combinations import *
from constants import NUM_EASY_CHITS, NUM_HARD_CHITS, NUM_MID_CHITS

ANIMALS = {
    1: Bat,
    2: Spider,
    3: Salamander,
    4: BabyDragon,
}

""" 
An animal factory that creates animal instances for a set of cards.
"""
    
class AbstractAnimalFactory(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    def create_cave_animals(self, num_caves:int) -> list:  
        """ 
        returns a list of animals for each cave
        """      
        animals = list(ANIMALS.values())
        shuffle(animals)    # shuffle here, so that there is variation every game if there's less than 4 players
        cave_animals = []
        for i in range(num_caves):            
            cave_animals.append(animals[i]())
        return cave_animals
        
    def create_vc_animals(self, combinations:dict) -> dict:
        """ 
        creates animal instances for each combination
        """
        combi = {}
        for k, c in combinations.items():
            combi[k] = [animal() for animal in c]
        return combi
    
    @abstractmethod
    def create_chit_animals(self, difficulty): list
    
class AnimalFactory(AbstractAnimalFactory):
    def __init__(self) -> None:
        super().__init__() 
    
    def create_chit_animals(self, difficulty):
        """ 
        returns a list of tuples containing 1,2,3 of each animal (except pirate dragons)
        """
        animals = []               
        
        if difficulty == "Medium":
            num_chits = NUM_MID_CHITS
        elif difficulty == "Hard":
            num_chits = NUM_HARD_CHITS            
            
        key, steps = 1, 1
        for i in range(num_chits[0]):
            if key == max(ANIMALS.keys()) +1 :
                key = 1
                steps += 1
            
            animals.append((steps, ANIMALS[key]()))            
            key += 1
        
        # pirates
        for i in range(num_chits[1]):
            animals.append((choice([-1,-2]), PirateDragon()))
        
        # bad chit
        for i in range(num_chits[2]):
            animals.append((0, BadChit()))
                        
        return animals 
               
   

class EasyAnimalFactory(AbstractAnimalFactory):
    def __init__(self) -> None:
        super().__init__()
        
    def create_chit_animals(self, difficulty):
        # 10 chits, 8 normal(1,2 of each animal)
        chits = []
        
        for animal in ANIMALS.values():
            chits.append((1, animal()))
            chits.append((2, animal()))
        
        # pirates
        for i in range(NUM_EASY_CHITS[1]):
            chits.append((-1, PirateDragon()))
        
        # new chits
        for i in range(NUM_EASY_CHITS[2]):
            chits.append((0, BadChit())) # change to new chit later
        
        return chits


if __name__ == "__main__":
    
    # b = EasyAnimalFactory()
    # c = b.create_chit_animals()
    # print(len(c))
    print(max(ANIMALS.keys()))
    pass 
    