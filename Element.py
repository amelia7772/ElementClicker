import pygame

class Element(pygame.sprite.Sprite):
    def __init__(self, image_path: str):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self._element_image_original = self.image.copy()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self._element_image_rect_original_size = self.rect.size