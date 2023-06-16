import pygame
from typing import Tuple

class button:
    def __init__(self, x, y, width, height, text='', action = '', color=(176, 176, 176),
                 text_color = (255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action  # shortened string for what button does
        self.color = color
        self.text_color = text_color

    def draw(self, window, outline: Tuple[int] = None) -> None:
        """Draws the button onto a specified window.

        Optional parameter for a tuple of RGB color values, to add a colored
        outline for the button.
        """
        if outline:
            pygame.draw.rect(window, outline,
            (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        
        pygame.draw.rect(window, self.color,
                        (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('arial', 30)
            text = font.render(self.text, 1, self.text_color)
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                     self.y + (self.height / 2 - text.get_height() / 2)))
    
    def isOver(self, pos: Tuple[int]) -> bool:
        """Returns True if pos, representing current mouse position, is hovering
        over this button.
        
        Returns False otherwise.
        """
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False