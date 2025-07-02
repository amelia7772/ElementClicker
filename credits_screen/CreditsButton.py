import pygame
from utilities.UiElement import *

class CreditsButton(UiElement):
    def __init__(self, background: pygame.Surface, icon_image: pygame.Surface):
        super().__init__([background, icon_image], [(65, 65), (50, 50)], True)
    
    def draw(self, screen: pygame.Surface):
        background_x = 0
        background_y = 0
        icon_x = background_x + ((self.images[0].get_width() / 2) - (self.images[1].get_width() / 2))
        icon_y = background_y + ((self.images[0].get_height() / 2) - (self.images[1].get_height() / 2))
        super().draw(screen, [(background_x, background_y), (icon_x, icon_y)])