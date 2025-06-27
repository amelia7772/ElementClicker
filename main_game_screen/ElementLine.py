import pygame
from main_game_screen.Element import Element
from main_game_screen.ElementText import ElementText
import math
import os
from utilities.Ellipse import Ellipse
from main_game_screen.ElementExplanationMessage import ElementExplanationMessage
from utilities.BigNumberMap import order_of_magnitude_to_symbol_map

class ElementLine(pygame.sprite.Group):
    def __init__(self, position: tuple[float, float], element_tier: int,element_image_path: str, background: pygame.Surface, element_explanation_message: ElementExplanationMessage):
        super().__init__()
        self.element_resource_amount = 0
        self.position = position
        self._initial_position = position
        self.element_tier = element_tier
        self.is_available = False
        self._element_image = Element(element_image_path)
        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)
        self._element_text = ElementText(self.pixelated_font, self.element_resource_amount)
        self.add(self._element_image, self._element_text)
        self._is_element_button_pressed = False
        self._is_element_button_hovered_over = False
        self._is_element_pressed = False
        
        self._crafting_prorgress_ellipse_empty: list[pygame.Rect, float] = [pygame.Rect(0,0, self._element_image.rect.width + 25, self._element_image.rect.height + 25), 5.0]
        self._crafting_prorgress_ellipse_empty[0].center = self._element_image.rect.center
        
        self._hightliter_ellipse = Ellipse(self._element_image.rect.left, self._element_image.rect.top, self._element_image.rect.width, self._element_image.rect.height)
        
        self._hightliter_ellipse.float_width = self._crafting_prorgress_ellipse_empty[0].size[0]
        self._hightliter_ellipse.float_height = self._crafting_prorgress_ellipse_empty[0].size[1]
        self._hightliter_ellipse.size = self._crafting_prorgress_ellipse_empty[0].size
        
        self._hightliter_ellipse.center = self._element_image.rect.center
        self._hightliter_ellipse.float_top = float(self._hightliter_ellipse.top)
        self._hightliter_ellipse.float_left = float(self._hightliter_ellipse.left)
        
        self._is_element_currently_being_crafted = False
        self._crafting_prorgress = 0.0
        
        self._ratio_of_change_in_width = 1.0
        self._ratio_of_change_in_height = 1.0
        
        self._ratio_of_non_preservative_change_in_width = 1.0
        self._ratio_of_non_preservative_change_in_height = 1.0
        
        self._element_image_rect_float_size: tuple[float, float] = (float(self._element_image.rect.size[0]), float(self._element_image.rect.size[1]))
        self._element_text_rect_float_size: tuple[float, float] = (float(self._element_text.rect.size[0]), float(self._element_text.rect.size[1]))
        
        self.offset: tuple[float,float] = (0,0)
        
        self.is_highlighted = False
        self._hightliter_ellipse_color = (150,150,150,100)
        self._element_background = background.copy()
        self._element_background_original = background.copy()
        self._element_background = pygame.transform.scale(self._element_background_original, self._crafting_prorgress_ellipse_empty[0].size)
        
        self.element_explanation_message = element_explanation_message
        self.element_explanation_message.rect.bottomleft = self._crafting_prorgress_ellipse_empty[0].topright
        self._element_explanation_message_rect_float_size: tuple[float, float] = self.element_explanation_message.rect.size
        
        self._is_element_craftable = False
        self._non_craftable_image = Element(element_image_path)
        self._non_craftable_image.image.fill(pygame.color.Color(0,0,0, 150), None, pygame.BLEND_RGBA_SUB)
        self._non_craftable_image._element_image_original = self._non_craftable_image.image.copy()
        
    def reposition_elements(self):
        element_line_of_objects_rect = pygame.Rect(0,0,0,0)
        element_line_of_objects_rect.size = (self._element_image_rect_float_size[0] + self._element_text_rect_float_size[0]  + 10 * self._ratio_of_change_in_width, max(self._element_image_rect_float_size[1], self._element_text_rect_float_size[1]))
        element_line_of_objects_rect.center = (self.position[0] + self.offset[0], self.position[1] + self.offset[1])
            
        self._element_image.rect.topleft = element_line_of_objects_rect.topleft
        self._hightliter_ellipse.center = self._element_image.rect.center
        self._hightliter_ellipse.float_top = float(self._hightliter_ellipse.top)
        self._hightliter_ellipse.float_left = float(self._hightliter_ellipse.left)
        self._element_text.rect.top = self._element_image.rect.top
        self._element_text.rect.left = self._element_image.rect.right + 20 * self._ratio_of_change_in_width
        
        self._non_craftable_image.rect = self._element_image.rect.copy()
        
        self._crafting_prorgress_ellipse_empty[0].center = self._element_image.rect.center
        self._crafting_prorgress_ellipse_empty[1] = 5 * ((self._ratio_of_change_in_width +  self._ratio_of_change_in_height) / 2)
        self.element_explanation_message.rect.bottomleft = (self._crafting_prorgress_ellipse_empty[0].right - (20 * self._ratio_of_change_in_width), self._crafting_prorgress_ellipse_empty[0].top + (20 * self._ratio_of_change_in_width))
        
    def reposition_elements_with_offset(self, offset: tuple[float, float]):
        self.offset = (self.offset[0] + offset[0], self.offset[1] + offset[1])
        element_line_of_objects_rect = pygame.Rect(0,0,0,0)
        element_line_of_objects_rect.size = (self._element_image_rect_float_size[0] + self._element_text_rect_float_size[0]  + 10 * self._ratio_of_change_in_width, max(self._element_image_rect_float_size[1], self._element_text_rect_float_size[1]))
        element_line_of_objects_rect.center = (self.position[0] + round(self.offset[0]), self.position[1] + round(self.offset[1]))
            
        self._element_image.rect.topleft = element_line_of_objects_rect.topleft
        self._hightliter_ellipse.center = self._element_image.rect.center
        self._hightliter_ellipse.float_top = float(self._hightliter_ellipse.top)
        self._hightliter_ellipse.float_left = float(self._hightliter_ellipse.left)
        self._element_text.rect.top = self._element_image.rect.top
        self._element_text.rect.left = self._element_image.rect.right + 20 * self._ratio_of_change_in_width
        
        self._non_craftable_image.rect = self._element_image.rect.copy()
        
        self._crafting_prorgress_ellipse_empty[0].center = self._element_image.rect.center
        self._crafting_prorgress_ellipse_empty[1] = 5 * ((self._ratio_of_change_in_width +  self._ratio_of_change_in_height) / 2)
        self.element_explanation_message.rect.bottomleft = (self._crafting_prorgress_ellipse_empty[0].right - (20 * self._ratio_of_change_in_width), self._crafting_prorgress_ellipse_empty[0].top + (20 * self._ratio_of_change_in_width))
    
    def scale_rect_without_changing_aspect_ratio(self, rect_size: tuple[float, float], original_rect_size: tuple[float, float], change_in_width: float, change_in_height: float):
        if rect_size[0] == 0 or rect_size[1] == 0:
            return rect_size
        original_ratio_of_width_to_height = float(rect_size[0]) / float(rect_size[1])
        original_ratio_of_height_to_width = float(rect_size[1]) / float(rect_size[0])
        
        non_preservative_scaled_rect_size = (original_rect_size[0]  * self._ratio_of_non_preservative_change_in_width * change_in_width, original_rect_size[1] * self._ratio_of_non_preservative_change_in_height * change_in_height)
        scaled_ratio_of_width_to_height = float(non_preservative_scaled_rect_size[0]) / float(non_preservative_scaled_rect_size[1])
        if original_ratio_of_width_to_height == scaled_ratio_of_width_to_height:
            return non_preservative_scaled_rect_size
        if original_ratio_of_width_to_height > scaled_ratio_of_width_to_height:
            return (non_preservative_scaled_rect_size[0], non_preservative_scaled_rect_size[0] * original_ratio_of_height_to_width)
        return (non_preservative_scaled_rect_size[1] * original_ratio_of_width_to_height, non_preservative_scaled_rect_size[1])
        
    
    def resize_elements(self, change_in_width: float, change_in_height: float,ratio_of_change_in_size: float):
        original_ratio_of_width_to_height = float(self._element_image_rect_float_size[0]) / float(self._element_image_rect_float_size[1])
        original_ratio_of_height_to_width = float(self._element_image_rect_float_size[1]) / float(self._element_image_rect_float_size[0])
        
        non_preservative_scaled_rect_size = (self._element_image._element_image_rect_original_size[0] * self._ratio_of_non_preservative_change_in_width * change_in_width, self._element_image._element_image_rect_original_size[1] * self._ratio_of_non_preservative_change_in_height * change_in_height)
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
        
        self.position = (self._initial_position[0] * self._ratio_of_change_in_width, self._initial_position[1] * self._ratio_of_change_in_height)
        
        self._element_image_rect_float_size = self.scale_rect_without_changing_aspect_ratio(self._element_image_rect_float_size, (float(self._element_image._element_image_rect_original_size[0]), float(self._element_image._element_image_rect_original_size[1])), change_in_width, change_in_height)
        self._element_text_rect_float_size = self.scale_rect_without_changing_aspect_ratio(self._element_text_rect_float_size, (float(self._element_text._element_text_original.get_rect().size[0]), float(self._element_text._element_text_original.get_rect().size[1])), change_in_width, change_in_height)
        
        self._element_explanation_message_rect_float_size = self.scale_rect_without_changing_aspect_ratio(self._element_explanation_message_rect_float_size, (float(self.element_explanation_message.original_size[0]), float(self.element_explanation_message.original_size[1])), change_in_width, change_in_height)
        self._element_image.rect.size = (round(self._element_image_rect_float_size[0]), round(self._element_image_rect_float_size[1]))
        self._element_text.rect.size = (round(self._element_text_rect_float_size[0]), round(self._element_text_rect_float_size[1]))
        self.element_explanation_message.rect.size = (round(self._element_explanation_message_rect_float_size[0]), round(self._element_explanation_message_rect_float_size[1]))
        
        self._non_craftable_image.rect = self._element_image.rect.copy()
        
        self._crafting_prorgress_ellipse_empty[0] = pygame.Rect((0,0), self.scale_rect_without_changing_aspect_ratio(self._crafting_prorgress_ellipse_empty[0].size, (self._element_image._element_image_rect_original_size[0] + 25, self._element_image._element_image_rect_original_size[1] + 25), change_in_width, change_in_height))
        self._crafting_prorgress_ellipse_empty[0].center = self._element_image.rect.center
        self._crafting_prorgress_ellipse_empty[1] = 5 * ((self._ratio_of_change_in_width +  self._ratio_of_change_in_height) / 2)
        self._hightliter_ellipse.float_width = self._crafting_prorgress_ellipse_empty[0].size[0]
        self._hightliter_ellipse.float_height = self._crafting_prorgress_ellipse_empty[0].size[1]
        self._hightliter_ellipse.size = self._crafting_prorgress_ellipse_empty[0].size
        
        self._element_image.image = pygame.transform.scale(self._element_image._element_image_original, self._element_image.rect.size)
        self._non_craftable_image.image = pygame.transform.scale(self._non_craftable_image._element_image_original, self._non_craftable_image.rect.size)
        self._element_text.image = pygame.transform.scale(self._element_text._element_text_original, self._element_text.rect.size)
        
        self._ratio_of_non_preservative_change_in_width *= change_in_width
        self._ratio_of_non_preservative_change_in_height *= change_in_height
        
        self._element_background = pygame.transform.scale(self._element_background_original, self._crafting_prorgress_ellipse_empty[0].size)
        
        self.element_explanation_message.image = pygame.transform.scale(self.element_explanation_message.original_image, self.element_explanation_message.rect.size)
        
        self.reposition_elements()
    
    def set_element_is_pressed(self, _is_element_pressed: bool):
        self._is_element_pressed = _is_element_pressed
        if _is_element_pressed:
            self._hightliter_ellipse_color = (99,99,99,100)
        else:
            self._hightliter_ellipse_color = (150,150,150,100)
    
    def is_element_pressed(self):
        return self._is_element_pressed
    
    def __calculate_order_of_magnitude__(self, number: int):
        order_of_magnitude = 0
        while number > 0:
            number = number // 10
            if number > 0:
                order_of_magnitude += 1
        return order_of_magnitude
    
    def increase_element_amount(self, amount_of_increase: int, screen: pygame.Surface):
        self.element_resource_amount += amount_of_increase
        previous_size = self._element_text._element_text_original.get_rect().size
        
        resource_amount = self.element_resource_amount
        symbol = ""
        order_of_magnitude_of_resource_amount = self.__calculate_order_of_magnitude__(resource_amount)
        if order_of_magnitude_of_resource_amount >= 3:
            symbol = order_of_magnitude_to_symbol_map[order_of_magnitude_of_resource_amount - (order_of_magnitude_of_resource_amount % 3)]
            non_rounded_resource_amount = float(resource_amount) / (10.0 ** (order_of_magnitude_of_resource_amount - (order_of_magnitude_of_resource_amount % 3)))
            resource_amount = round(non_rounded_resource_amount, 2 - self.__calculate_order_of_magnitude__(int(non_rounded_resource_amount)))
        self._element_text.image = self.pixelated_font.render(str(resource_amount) + symbol, False, "White").convert_alpha()
        self._element_text._element_text_original = self._element_text.image.copy()
        
        self._element_text.rect.size = self._element_text.image.get_rect().size
        self._element_text_rect_float_size = (self._element_text_rect_float_size[0] * (float(self._element_text.rect.size[0]) / float(previous_size[0])), self._element_text_rect_float_size[1])
        self._element_text.rect.size = (float(self._element_text_rect_float_size[0]), float(self._element_text_rect_float_size[1]))
        self._element_text.image = pygame.transform.scale(self._element_text._element_text_original, self._element_text.rect.size)
        self.reposition_elements()
    
    def is_element_button_pressed(self):
        return self._is_element_button_pressed
    
    def is_element_button_hovered_over(self):
        return self._is_element_button_hovered_over
    
    def draw(self, screen: pygame.Surface):
        screen_rect = screen.get_rect()
        if self.is_available:
            if self._element_image.rect.colliderect(screen_rect):
                screen.blit(self._element_background, self._crafting_prorgress_ellipse_empty[0])
                if self._is_element_craftable:
                    screen.blit(self._element_image.image, self._element_image.rect)
                else:
                    screen.blit(self._non_craftable_image.image, self._non_craftable_image.rect)
            if self._element_text.rect.colliderect(screen_rect):
                screen.blit(self._element_text.image, self._element_text.rect)
            if self._hightliter_ellipse.colliderect(screen_rect) and (self.is_highlighted or self._is_element_pressed):
                self._hightliter_ellipse.draw(screen, self._hightliter_ellipse_color)
            if self._is_element_currently_being_crafted and self._crafting_prorgress_ellipse_empty[0].colliderect(screen_rect):
                stroke_width = round(self._crafting_prorgress_ellipse_empty[1])
                pygame.draw.ellipse(screen,"#999999", self._crafting_prorgress_ellipse_empty[0], stroke_width)
                pygame.draw.arc(screen,"#00ff00", self._crafting_prorgress_ellipse_empty[0], math.pi / 2, 2 * math.pi * self._crafting_prorgress + math.pi / 2, stroke_width)
        #else:
        #    if self._element_image.rect.colliderect(screen_rect):
        #        screen.blit(self._element_background, self._crafting_prorgress_ellipse_empty[0])
