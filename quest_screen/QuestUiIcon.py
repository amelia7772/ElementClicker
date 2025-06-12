import pygame
from utilities.UiElement import UiElement

class QuestUiIcon(UiElement):
    
    def __init__(self, background_image: pygame.Surface, ui_icon_image: pygame.Surface, position: tuple[int, int], is_quest_available = False):
        self._available_quest_ui_icon = ui_icon_image.copy()
        self._unavailable_quest_ui_icon = ui_icon_image.copy()
        self._unavailable_quest_ui_icon.fill(pygame.color.Color(0,0,0), None, pygame.BLEND_RGBA_MULT)
        if is_quest_available:
            super().__init__([background_image, self._available_quest_ui_icon], [(65,65), (50,50)], is_highlightable = True)
        else:
            super().__init__([background_image, self._unavailable_quest_ui_icon], [(65,65), (50,50)], is_highlightable = True)
        icon_x = position[0] + ((background_image.get_width() / 2) - (ui_icon_image.get_width() / 2))
        icon_y = position[1] + ((background_image.get_height() / 2) - (ui_icon_image.get_height() / 2))
        self.position = position
        self.positions= [position, (icon_x, icon_y)]
    
    def set_background(self, background: pygame.Surface):
        self.images[0] = background.copy()
        self.images_original[0] = background.copy()
    
    def set_quest_available(self, is_quest_available: bool):
        if is_quest_available:
            self.images[1] = self._available_quest_ui_icon
            self.images_original[1] = self._available_quest_ui_icon
        else:
            self.images[1] = self._unavailable_quest_ui_icon
            self.images_original[1] = self._unavailable_quest_ui_icon
    
    def update_position(self, new_position: tuple[int, int]):
        self.position = new_position
        icon_x = self.position[0] + ((self.images[0].get_width() / 2) - (self.images[1].get_width() / 2))
        icon_y = self.position[1] + ((self.images[0].get_height() / 2) - (self.images[1].get_height() / 2))
        self.positions= [new_position, (icon_x, icon_y)]
    
    def draw(self, screen):
        super().draw(screen, self.positions)