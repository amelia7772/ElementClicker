from main_game_screen.Elements import *
from main_game_screen.ElementType import ElementType
import pygame
import os

class XpBar:
    def __init__(self):
        self.xp_amount = 0
        self.level = 0
        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)

        self.xp_text = self.pixelated_font.render("XP", False, "White").convert_alpha()
        self.xp_text_original = self.xp_text.copy()
        self.xp_text_rect = self.xp_text.get_rect()

        self.empty_xp_bar = pygame.Rect(0,0,200,20)
        self.full_xp_bar = pygame.Rect(0,0,self.empty_xp_bar.width * ((self.xp_amount) / ((self.level ** 2) * 5 + 10)),20)

        self.xp_number_text = self.pixelated_font.render(str(self.xp_amount), False, "White").convert_alpha()
        self.xp_number_text_original = self.xp_number_text.copy()
        self.xp_number_text_rect = self.xp_number_text.get_rect()

        self.level_text = self.pixelated_font.render(str(self.level), False, "White").convert_alpha()
        self.level_text_original = self.level_text.copy()
        self.level_text_rect = self.level_text.get_rect()
        
        self.xp_text_rect.size = self.xp_text.get_size()
        self.xp_number_text_rect.size = self.xp_number_text.get_size()
        self.level_text_rect.size = self.level_text.get_size()

        self.xp_text_rect_original_size = self.xp_text_rect.size
        self.empty_xp_bar_original_size = self.empty_xp_bar.size
        self.full_xp_bar_original_size = self.full_xp_bar.size
        self.xp_number_text_rect_original_size = self.xp_number_text_rect.size
        self.level_text_rect_original_size = self.level_text_rect.size
        
        self._xp_text_rect_float_size: tuple[float, float] = (float(self.xp_text_rect.size[0]), float(self.xp_text_rect.size[1]))
        self._empty_xp_bar_rect_float_size: tuple[float, float] = (float(self.empty_xp_bar.size[0]), float(self.empty_xp_bar.size[1]))
        self._full_xp_bar_rect_float_size: tuple[float, float] = (float(self.full_xp_bar.size[0]), float(self.full_xp_bar.size[1]))
        self._xp_number_text_rect_float_size: tuple[float, float] = (float(self.xp_number_text_rect.size[0]), float(self.xp_number_text_rect.size[1]))
        self._level_text_rect_float_size: tuple[float, float] = (float(self.level_text_rect.size[0]), float(self.level_text_rect.size[1]))
        
        self._ratio_of_change_in_width = 1.0
        self._ratio_of_change_in_height = 1.0
        
        self._ratio_of_non_preservative_change_in_width = 1.0
        self._ratio_of_non_preservative_change_in_height = 1.0
        
        self.highlighting_surface = pygame.Surface((pygame.Vector2(self.xp_text_rect.midleft).distance_to(self.xp_number_text_rect.midright) + (pygame.display.get_surface().get_width() / 25),pygame.Vector2(self.xp_number_text_rect.midbottom).distance_to(self.level_text_rect.midtop)), pygame.SRCALPHA)
        self.highlighting_surface.fill((0,0,0,100))
        self.highlighting_surface_rect = self.highlighting_surface.get_rect(left = self.xp_text_rect.left - (pygame.display.get_surface().get_width() / 50), top= self.level_text_rect.top)


    def reposition_xp_elements(self, screen: pygame.Surface):
        xp_line_of_objects_rect = pygame.Rect(0,0,0,0)
        xp_line_of_objects_rect.size = (max(self.xp_text_rect.size[0] + (screen.get_rect().size[0] / 100) + self.empty_xp_bar.size[0] + self.xp_number_text_rect.size[0] + (screen.get_rect().size[0] / 50), self.level_text_rect.size[0]), max(self.xp_text_rect.size[1], self.empty_xp_bar.size[1], self.xp_number_text_rect.size[1]) + self.level_text_rect.size[1])
        xp_line_of_objects_rect.centerx = screen.get_rect().centerx
        xp_line_of_objects_rect.bottom = screen.get_rect().bottom
    
        self.empty_xp_bar.centerx = xp_line_of_objects_rect.centerx
        self.xp_text_rect.right = self.empty_xp_bar.left - (screen.get_rect().size[0] / 100)
        self.xp_text_rect.bottom = xp_line_of_objects_rect.bottom
        self.empty_xp_bar.centery = self.xp_text_rect.centery
        self.full_xp_bar.x = self.empty_xp_bar.x
        self.full_xp_bar.y = self.empty_xp_bar.y
        self.xp_number_text_rect.midleft = self.empty_xp_bar.midright
        self.xp_number_text_rect.left += (screen.get_rect().size[0] / 50)
        self.level_text_rect.midbottom = self.empty_xp_bar.midtop

    def scale_rect_without_changing_aspect_ratio(self, rect_size: tuple[float, float], original_rect_size: tuple[float, float], change_in_width: float, change_in_height: float):
        if rect_size[0] == 0 or rect_size[1] == 0:
            return (float(rect_size[0]), float(rect_size[1]))
        original_ratio_of_width_to_height = float(rect_size[0]) / float(rect_size[1])
        original_ratio_of_height_to_width = float(rect_size[1]) / float(rect_size[0])
        
        non_preservative_scaled_rect_size = (original_rect_size[0] * self._ratio_of_non_preservative_change_in_width * change_in_width, original_rect_size[1] * self._ratio_of_non_preservative_change_in_height * change_in_height)
        scaled_ratio_of_width_to_height = float(non_preservative_scaled_rect_size[0]) / float(non_preservative_scaled_rect_size[1])
        if original_ratio_of_width_to_height == scaled_ratio_of_width_to_height:
            return non_preservative_scaled_rect_size
        if original_ratio_of_width_to_height > scaled_ratio_of_width_to_height:
            return (non_preservative_scaled_rect_size[0], non_preservative_scaled_rect_size[0] * original_ratio_of_height_to_width)
        return (non_preservative_scaled_rect_size[1] * original_ratio_of_width_to_height, non_preservative_scaled_rect_size[1])
        
    def resize_xp_elements(self, screen: pygame.Surface, change_in_width: float, change_in_height: float):
        original_ratio_of_width_to_height = float(self.xp_text_rect_original_size[0]) / float(self.xp_text_rect_original_size[1])
        original_ratio_of_height_to_width = float(self.xp_text_rect_original_size[1]) / float(self.xp_text_rect_original_size[0])
        
        non_preservative_scaled_rect_size = (self.xp_text_rect_original_size[0] * self._ratio_of_non_preservative_change_in_width * change_in_width, self.xp_text_rect_original_size[1] * self._ratio_of_non_preservative_change_in_height * change_in_height)
        scaled_ratio_of_width_to_height = float(non_preservative_scaled_rect_size[0]) / float(non_preservative_scaled_rect_size[1])
                
        self._ratio_of_change_in_width = self._ratio_of_non_preservative_change_in_width
        self._ratio_of_change_in_height = self._ratio_of_non_preservative_change_in_height
        
        if original_ratio_of_width_to_height == scaled_ratio_of_width_to_height:
            self._ratio_of_change_in_width *= change_in_width
            self._ratio_of_change_in_height *= change_in_height
        elif original_ratio_of_width_to_height > scaled_ratio_of_width_to_height:
            self._ratio_of_change_in_width *= change_in_width
            self._ratio_of_change_in_height *= change_in_width * original_ratio_of_height_to_width
        else:
            self._ratio_of_change_in_width *= change_in_height * original_ratio_of_width_to_height
            self._ratio_of_change_in_height *= change_in_height
        
        self._xp_text_rect_float_size = self.scale_rect_without_changing_aspect_ratio(self._xp_text_rect_float_size, (float(self.xp_text_rect_original_size[0]), float(self.xp_text_rect_original_size[1])), change_in_width, change_in_height)
        self._empty_xp_bar_rect_float_size = self.scale_rect_without_changing_aspect_ratio(self._empty_xp_bar_rect_float_size, (float(self.empty_xp_bar_original_size[0]), float(self.empty_xp_bar_original_size[1])), change_in_width, change_in_height)
        self._full_xp_bar_rect_float_size = (self._empty_xp_bar_rect_float_size[0] * ((self.xp_amount) / ((self.level ** 2) * 5 + 10)), self._empty_xp_bar_rect_float_size[1])  
        self._xp_number_text_rect_float_size = self.scale_rect_without_changing_aspect_ratio(self._xp_number_text_rect_float_size, (float(self.xp_number_text_original.get_rect().size[0]), float(self.xp_number_text_original.get_rect().size[1])), change_in_width, change_in_height)
        self._level_text_rect_float_size = self.scale_rect_without_changing_aspect_ratio(self._level_text_rect_float_size, (float(self.level_text_original.get_rect().size[0]), float(self.level_text_original.get_rect().size[1])), change_in_width, change_in_height)
        
        
        self.xp_text_rect.size = (round(self._xp_text_rect_float_size[0]), round(self._xp_text_rect_float_size[1]))
        self.empty_xp_bar.size = (round(self._empty_xp_bar_rect_float_size[0]), round(self._empty_xp_bar_rect_float_size[1]))
        self.full_xp_bar.size = (round(self._full_xp_bar_rect_float_size[0]), round(self._full_xp_bar_rect_float_size[1]))
        self.xp_number_text_rect.size = (round(self._xp_number_text_rect_float_size[0]), round(self._xp_number_text_rect_float_size[1]))
        self.level_text_rect.size = (round(self._level_text_rect_float_size[0]), round(self._level_text_rect_float_size[1]))
                
        self.xp_text = pygame.transform.scale(self.xp_text_original, self.xp_text_rect.size)
        self.xp_number_text = pygame.transform.scale(self.xp_number_text_original, self.xp_number_text_rect.size)
        self.level_text = pygame.transform.scale(self.level_text_original, self.level_text_rect.size)
        
        self._ratio_of_non_preservative_change_in_width *= change_in_width
        self._ratio_of_non_preservative_change_in_height *= change_in_height
        
        self.reposition_xp_elements(screen)
        
    def increase_xp(self, amount_of_increase: int, screen: pygame.Surface):
        self.ratio_of_change_in_size = max(screen.get_size()[0] / 800, screen.get_size()[1] / 400)
        
        self.xp_amount += amount_of_increase
                
        while self.xp_amount >= (self.level ** 2) * 5 + 10:
            self.xp_amount -= (self.level ** 2) * 5 + 10
            self.level += 1
            
            previous_size = self.level_text_original.get_rect().size
            
            self.level_text = self.pixelated_font.render(str(self.level), False, "White").convert_alpha()
            self.level_text_original = self.level_text.copy()
            self.level_text_rect = self.level_text.get_rect()
            
            self._level_text_rect_float_size = (self._level_text_rect_float_size[0] * (float(self.level_text_rect.size[0]) / float(previous_size[0])), self._level_text_rect_float_size[1])
            self.level_text_rect.size = (round(self._level_text_rect_float_size[0]), round(self._level_text_rect_float_size[1]))
            
            self.level_text = pygame.transform.scale(self.level_text_original, self.level_text_rect.size)
            elements.reevaluate_availability(self.level)
        
        previous_size = self.xp_number_text_original.get_rect().size
        
        self.xp_number_text = self.pixelated_font.render(str(self.xp_amount), False, "White").convert_alpha()
        self.xp_number_text_original = self.xp_number_text.copy()
        self.xp_number_text_rect = self.xp_number_text.get_rect()
        
        self._xp_number_text_rect_float_size = (self._xp_number_text_rect_float_size[0] * (float(self.xp_number_text_rect.size[0]) / float(previous_size[0])), self._xp_number_text_rect_float_size[1])
        self.xp_number_text_rect.size = (round(self._xp_number_text_rect_float_size[0]), round(self._xp_number_text_rect_float_size[1]))
        
        self.xp_number_text = pygame.transform.scale(self.xp_number_text_original, self.xp_number_text_rect.size)
                
        self._full_xp_bar_rect_float_size = (self._empty_xp_bar_rect_float_size[0] * ((self.xp_amount) / ((self.level ** 2) * 5 + 10)), self._full_xp_bar_rect_float_size[1])  
        self.full_xp_bar.size = (round(self._full_xp_bar_rect_float_size[0]), round(self._full_xp_bar_rect_float_size[1]))
        
        self.reposition_xp_elements(screen)
    
    def set_xp(self, amount_of_xp: int, screen: pygame.Surface):
        self.xp_amount = amount_of_xp
        
        previous_size = self.xp_number_text_original.get_rect().size
        self.ratio_of_change_in_size = max(screen.get_size()[0] / 800, screen.get_size()[1] / 400)
        self.xp_number_text = self.pixelated_font.render(str(self.xp_amount), False, "White").convert_alpha()
        self.xp_number_text_original = self.xp_number_text.copy()
        self.xp_number_text_rect = self.xp_number_text.get_rect()
        
        self._xp_number_text_rect_float_size = (self._xp_number_text_rect_float_size[0] * (float(self.xp_number_text_rect.size[0]) / float(previous_size[0])), self._xp_number_text_rect_float_size[1])
        self.xp_number_text_rect.size = (round(self._xp_number_text_rect_float_size[0]), round(self._xp_number_text_rect_float_size[1]))
        self.xp_number_text = pygame.transform.scale(self.xp_number_text_original, self.xp_number_text_rect.size)
        
        self._full_xp_bar_rect_float_size = (self._empty_xp_bar_rect_float_size[0] * ((self.xp_amount) / ((self.level ** 2) * 5 + 10)), self._full_xp_bar_rect_float_size[1])  
        self.full_xp_bar.size = (round(self._full_xp_bar_rect_float_size[0]), round(self._full_xp_bar_rect_float_size[1]))
        
        self.reposition_xp_elements(screen)
    
    def set_level(self, amount_of_level: int, screen: pygame.Surface):
        self.ratio_of_change_in_size = max(screen.get_size()[0] / 800, screen.get_size()[1] / 400)
        self.level = amount_of_level
        
        previous_size = self.level_text_original.get_rect().size
        
        self.level_text = self.pixelated_font.render(str(self.level), False, "White").convert_alpha()
        self.level_text_original = self.level_text.copy()
        self.level_text_rect = self.level_text.get_rect()
        
        self._level_text_rect_float_size = (self._level_text_rect_float_size[0] * (float(self.level_text_rect.size[0]) / float(previous_size[0])), self._level_text_rect_float_size[1])
        self.level_text_rect.size = (round(self._level_text_rect_float_size[0]), round(self._level_text_rect_float_size[1]))
        
        self.level_text = pygame.transform.scale(self.level_text_original, self.level_text_rect.size)
        elements.reevaluate_availability(self.level)
        
        self._full_xp_bar_rect_float_size = (self._empty_xp_bar_rect_float_size[0] * ((self.xp_amount) / ((self.level ** 2) * 5 + 10)), self._full_xp_bar_rect_float_size[1])  
        self.full_xp_bar.size = (round(self._full_xp_bar_rect_float_size[0]), round(self._full_xp_bar_rect_float_size[1]))
        
        self.reposition_xp_elements(screen)
    
    def draw(self, screen: pygame.Surface):
        self.highlighting_surface = pygame.Surface((pygame.Vector2(self.xp_text_rect.midleft).distance_to(self.xp_number_text_rect.midright) + (screen.get_width() / 25),pygame.Vector2(self.xp_number_text_rect.midbottom).distance_to(self.level_text_rect.midtop)), pygame.SRCALPHA)
        self.highlighting_surface.fill((0,0,0,100))
        self.highlighting_surface_rect = self.highlighting_surface.get_rect(left = self.xp_text_rect.left - (screen.get_width() / 50), top= self.level_text_rect.top)
        
        screen.blit(self.highlighting_surface, self.highlighting_surface_rect)
        screen.blit(self.xp_text, self.xp_text_rect)
        pygame.draw.rect(screen, "#999999", self.empty_xp_bar)
        pygame.draw.rect(screen, "#00ff00", self.full_xp_bar)
        screen.blit(self.xp_number_text, self.xp_number_text_rect)
        screen.blit(self.level_text, self.level_text_rect)

xp_bar = XpBar()