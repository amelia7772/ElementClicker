import pygame
import math
from typing import Union, Sequence, Tuple

class Ellipse(pygame.Rect):
    
    def __init__(self, left: float, top: float, width: float, height: float):
        super().__init__(left, top, width, height)
        self.float_left = left
        self.float_top = top
        self.float_width = width
        self.float_height = height
        
    
    def point_on_ellipse_from_angle(self, angle: float):
        if angle ==  (math.pi / 2):
            return ((self.float_left + (self.float_width / 2)), self.float_top)
        if angle ==  -(math.pi / 2):
            return ((self.float_left + (self.float_width / 2)), self.float_top + self.float_height)
        if angle ==  (math.pi) or angle ==  -(math.pi):
            return (self.float_left, self.float_top + (self.float_height / 2))
        if angle == 0:
            return (self.float_left + self.float_width, self.float_top + (self.float_height / 2))
        absolute_value_x = ((self.float_width / 2) * (self.float_height / 2)) / (math.sqrt((self.float_height / 2) ** 2 + (((self.float_width / 2) ** 2) * (math.tan(angle) ** 2))))
        absolute_value_y = ((self.float_width / 2) * (self.float_height / 2)) / (math.sqrt((self.float_width / 2) ** 2 + (((self.float_height / 2) ** 2) / (math.tan(angle) ** 2))))
        
        if angle >= -(math.pi / 2) and angle <= (math.pi / 2):
            return ((self.float_left + (self.float_width / 2)) + absolute_value_x, (self.float_top + (self.float_height / 2)) + absolute_value_y)
        return ((self.float_left + (self.float_width / 2)) - absolute_value_x, (self.float_top + (self.float_height / 2)) - absolute_value_y)
    
    def collide_point(self, point_x: float, point_y: float):
        distance_to_center_x = ((point_x - (self.float_left + (self.float_width / 2))) ** 2) / ((self.float_width / 2) ** 2)
        distance_to_center_y = ((point_y - (self.float_top + (self.float_height / 2))) ** 2) / ((self.float_height / 2) ** 2)
        return (distance_to_center_x + distance_to_center_y) <= 1
    
    def draw(self, screen: pygame.Surface, color: Union[pygame.color.Color, int, str, Tuple[int, int, int], Tuple[int, int, int, int], Sequence[int]], width: int = 0):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.ellipse(surface, color, surface.get_rect(), width)
        screen.blit(surface, self.topleft)