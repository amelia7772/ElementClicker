import pygame

class UiElement:
    def __init__(self, images: list[pygame.Surface], sizes: list[tuple[float, float]]):
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
    
    def resize_quest_button(self, change_in_width: float, change_in_height: float):
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
        
        self._ratio_of_non_preservative_change_in_width *= change_in_width
        self._ratio_of_non_preservative_change_in_height *= change_in_height
        
    def draw(self, screen: pygame.Surface, positions: list[tuple[int, int]]):
        for i in range(0, len(self.images)):
            screen.blit(self.images[i], positions[i])