from abc import ABC

""" 
Animal abstract class and its child classes with a 
unique attribute.
"""


class Animal(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.type = None
    
    @classmethod
    def from_dict(cls, animal:str):
        if animal == "Bat":
            return Bat()
        elif animal == "Salamander":
            return Salamander()
        elif animal == "Spider":
            return Spider()
        elif animal == "BabyDragon":
            return BabyDragon()
        elif animal == "PirateDragon":
            return PirateDragon()
        elif animal == "BadChit":
            return BadChit()

class Bat(Animal):
    def __init__(self) -> None:
        super().__init__()         
        self.type = "Bat"

class Salamander(Animal):
    def __init__(self) -> None:
        super().__init__() 
        self.type = "Salamander"
        
class Spider(Animal):
    def __init__(self) -> None:
        super().__init__() 
        self.type = "Spider"
        
class BabyDragon(Animal):
    def __init__(self) -> None:
        super().__init__() 
        self.type = "BabyDragon"
        
class PirateDragon(Animal):
    def __init__(self) -> None:
        super().__init__() 
        self.type = "PirateDragon"

class BadChit(Animal):
    def __init__(self) -> None:
        super().__init__() 
        self.type = "BadChit"