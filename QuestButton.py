import pygame

class QuestButton:
    def __init__(self, background: pygame.Surface, icon_image: pygame.Surface):
        self.background = background.copy()
        self.icon_image = icon_image.copy()
        
        self.background_original = background.copy()
        self.icon_image_original = icon_image.copy()
        
        self.background = pygame.transform.scale(self.background, (65, 65))
        self.icon_image = pygame.transform.scale(self.icon_image, (50, 50))
        self.background_size = (65.0, 65.0)
        self.icon_image_size = (50.0, 50.0)
        
        self.background_original_size = (65.0, 65.0)
        self.icon_image_original_size = (50.0, 50.0)
        
        self._ratio_of_change_in_width = 1.0
        self._ratio_of_change_in_height = 1.0
        
        self._ratio_of_non_preservative_change_in_width = 1.0
        self._ratio_of_non_preservative_change_in_height = 1.0
    
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
    
    def resize_quest_button(self, screen: pygame.Surface, change_in_width: float, change_in_height: float):
        original_ratio_of_width_to_height = float(self.background_original_size[0]) / float(self.background_original_size[1])
        original_ratio_of_height_to_width = float(self.background_original_size[1]) / float(self.background_original_size[0])
        
        non_preservative_scaled_rect_size = (self.background_original_size[0] * self._ratio_of_non_preservative_change_in_width * change_in_width, self.background_original_size[1] * self._ratio_of_non_preservative_change_in_height * change_in_height)
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
        
        self.background_size = self.scale_rect_without_changing_aspect_ratio(self.background_size, (float(self.background_original_size[0]), float(self.background_original_size[1])), change_in_width, change_in_height)
        self.icon_image_size = self.scale_rect_without_changing_aspect_ratio(self.icon_image_size, (float(self.icon_image_original_size[0]), float(self.icon_image_original_size[1])), change_in_width, change_in_height)
        
        self.background = pygame.transform.scale(self.background_original, self.background_size)
        self.icon_image = pygame.transform.scale(self.icon_image_original, self.icon_image_size)
        
        self._ratio_of_non_preservative_change_in_width *= change_in_width
        self._ratio_of_non_preservative_change_in_height *= change_in_height
    
    def draw(self, screen: pygame.Surface):
        background_x = screen.get_width() - self.background.get_width()
        background_y = screen.get_height() - self.background.get_height()
        icon_x = background_x + ((self.background.get_width() / 2) - (self.icon_image.get_width() / 2))
        icon_y = background_y + ((self.background.get_height() / 2) - (self.icon_image.get_height() / 2))
        screen.blit(self.background, (background_x,background_y))
        screen.blit(self.icon_image, (icon_x,icon_y))