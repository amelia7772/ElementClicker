import pygame
from utilities.BigNumberMap import order_of_magnitude_to_symbol_map


class ElementText(pygame.sprite.Sprite):
    def __init__(self, font: pygame.font.Font, resource_amount: int):
        super().__init__()
        symbol = ""
        order_of_magnitude_of_resource_amount = self.__calculate_order_of_magnitude__(resource_amount)
        if order_of_magnitude_of_resource_amount >= 3:
            symbol = order_of_magnitude_to_symbol_map[order_of_magnitude_of_resource_amount - (order_of_magnitude_of_resource_amount % 3)]
            resource_amount = round(float(resource_amount) / (10.0 ** order_of_magnitude_of_resource_amount), 2)
        self.image = font.render(str(resource_amount) + symbol, False, "White").convert_alpha()
        self._element_text_original = self.image.copy()
        self.rect = self.image.get_rect()
        self._element_text_rect_original_size = self.rect.size
    
    def __calculate_order_of_magnitude__(self, number: int):
        order_of_magnitude = 0
        while number > 0:
            number = number // 10
            if number > 0:
                order_of_magnitude += 1
        return order_of_magnitude
