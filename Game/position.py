from constants import SQUARE_SIZE


"""
Position keeps track of its row and column in the boards internal matrix
and the display coordinates for the screen.
"""

class Position:   
    def __init__(self, row_col:tuple[int,int]):
        """ 
        row, col are the indexes in the 2d array,
        x_y are the coordinates on the display screen
        """
        self.row = row_col[0] # y
        self.col = row_col[1] # x
        self.x_y = (self.col*SQUARE_SIZE[0], self.row*SQUARE_SIZE[1])

    def update_pos(self, row_col:tuple[int,int]) -> None:
        self.row = row_col[0] 
        self.col = row_col[1] 
        self.x_y = (self.col*SQUARE_SIZE[0], self.row*SQUARE_SIZE[1])
    

    def __str__(self):
        return f"{self.x_y}"
    