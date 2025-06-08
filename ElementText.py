import pygame

class ElementText(pygame.sprite.Sprite):
    def __init__(self, font: pygame.font.Font, resource_amount: int):
        super().__init__()
        self.image = font.render(str(resource_amount), False, "White").convert_alpha()
        self._element_text_original = self.image.copy()
        self.rect = self.image.get_rect()
        self._element_text_rect_original_size = self.rect.size