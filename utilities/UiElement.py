import pygame
from utilities.Ellipse import *

class UiElement:
    def __init__(self, images: list[pygame.Surface], sizes: list[tuple[float, float]], is_highlightable = False):
        self.is_highlightable = is_highlightable
        self.images: list[pygame.Surface] = []
        self.sizes: list[tuple[float, float]] = []
        
        for i in range(0, len(images)):
            self.images.append(images[i].copy())
        
        for i in range(0, len(sizes)):
            self.sizes.append((sizes[i][0], sizes[i][1]))
        
        self.images_original: list[pygame.Surface] = []
        
        for i in range(0, len(images)):
            self.images_original.append(images[i].copy())
        
        self.sizes_original: list[tuple[float, float]] = []
        for i in range(0, len(sizes)):
            self.sizes_original.append((sizes[i][0], sizes[i][1]))
        
        for i in range(0, len(images)):
            self.images[i] = pygame.transform.scale(self.images[i], sizes[i])
        
        self._ratio_of_change_in_width = 1.0
        self._ratio_of_change_in_height = 1.0
        
        self._ratio_of_non_preservative_change_in_width = 1.0
        self._ratio_of_non_preservative_change_in_height = 1.0
        
        self._is_ui_element_pressed = False
        self._is_ui_element_button_pressed = False
        self._is_ui_element_button_hovered_over = False
        
        if is_highlightable:
            self._hightliter_ellipse = Ellipse(0, 0, self.images[0].get_width(), self.images[0].get_height())
            self._hightliter_ellipse_color = (150,150,150,100)
            self.is_highlighted = False

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
    
    def resize_ui_element(self, change_in_width: float, change_in_height: float):
        original_ratio_of_width_to_height = float(self.sizes_original[0][0]) / float(self.sizes_original[0][1])
        original_ratio_of_height_to_width = float(self.sizes_original[0][1]) / float(self.sizes_original[0][0])
        
        non_preservative_scaled_rect_size = (self.sizes_original[0][0] * self._ratio_of_non_preservative_change_in_width * change_in_width, self.sizes_original[0][1] * self._ratio_of_non_preservative_change_in_height * change_in_height)
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
        
        for i in range(0, len(self.sizes)):
            self.sizes[i] = self.scale_rect_without_changing_aspect_ratio(self.sizes[i], (float(self.sizes_original[i][0]), float(self.sizes_original[i][1])), change_in_width, change_in_height)
        
        for i in range(0, len(self.images)):
            self.images[i] = pygame.transform.scale(self.images_original[i], self.sizes[i])
        
        self._hightliter_ellipse.float_width = self.images[0].get_width()
        self._hightliter_ellipse.float_height = self.images[0].get_height()
        self._hightliter_ellipse.size = (self.images[0].get_width(), self.images[0].get_height())
        
        self._ratio_of_non_preservative_change_in_width *= change_in_width
        self._ratio_of_non_preservative_change_in_height *= change_in_height
    
    def set_ui_element_is_pressed(self, _is_ui_element_pressed: bool):
        self._is_ui_element_pressed = _is_ui_element_pressed
        if _is_ui_element_pressed:
            self._hightliter_ellipse_color = (99,99,99,100)
        else:
            self._hightliter_ellipse_color = (150,150,150,100)
    
    def is_ui_element_pressed(self):
        return self._is_ui_element_pressed
    
    def is_ui_element_button_pressed(self):
        return self._is_ui_element_button_pressed
    
    def is_ui_element_button_hovered_over(self):
        return self._is_ui_element_button_hovered_over
    
    def draw(self, screen: pygame.Surface, positions: list[tuple[int, int]]):
        for i in range(0, len(self.images)):
            screen.blit(self.images[i], positions[i])
        if self.is_highlightable:
            self._hightliter_ellipse.topleft = (positions[0][0], positions[0][1])
            self._hightliter_ellipse.float_top = float(self._hightliter_ellipse.top)
            self._hightliter_ellipse.float_left = float(self._hightliter_ellipse.left)
            if self._hightliter_ellipse.colliderect(screen.get_rect()) and (self.is_highlighted or self._is_ui_element_pressed):
                self._hightliter_ellipse.draw(screen,self._hightliter_ellipse_color)