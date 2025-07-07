import pygame
from utilities.UiElement import *
from utilities import Screen

class QuestButton(UiElement):
    def __init__(self, background: pygame.Surface, icon_image: pygame.Surface):
        background_resized = pygame.transform.scale(background, (83, 83))
        #icon_image_resized = pygame.transform.scale(icon_image, (50, 50))
        super().__init__([background_resized, icon_image], [(83, 83), (64, 64)], True)
        self._hightliter_ellipse.topleft = (Screen.screen.get_width() - self.images[0].get_width(), Screen.screen.get_height() - self.images[0].get_height())
        self._hightliter_ellipse.float_top = float(self._hightliter_ellipse.top)
        self._hightliter_ellipse.float_left = float(self._hightliter_ellipse.left)
        
    def draw(self, screen: pygame.Surface):
        background_x = screen.get_width() - self.images[0].get_width()
        background_y = screen.get_height() - self.images[0].get_height()
        icon_x = background_x + ((self.images[0].get_width() / 2) - (self.images[1].get_width() / 2))
        icon_y = background_y + ((self.images[0].get_height() / 2) - (self.images[1].get_height() / 2))
        super().draw(screen, [(background_x, background_y), (icon_x, icon_y)])
