import pygame
import os
from utilities import Screen

class LoadingScene:
    def __init__(self, background_image: pygame.Surface):
        self.game_icon = pygame.image.load(os.path.join("assets", "images" ,"wood log 16-bit.png")).convert_alpha()
        self.background_image = background_image.copy()
        self.margin_between_icon_and_loading_text = 50.0
        self.game_icon = pygame.transform.scale(self.game_icon, (100,100))
        self.game_icon_position = ((float(Screen.screen.get_width()) / 2.0) - 50, (float(Screen.screen.get_height()) / 2.0) - 50 - (self.margin_between_icon_and_loading_text / 2.0))
        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)
        self.number_of_loading_dots = 1
        self.loading_text_one_dot = self.pixelated_font.render("Loading.", False, (255,255,255)).convert_alpha()
        self.loading_text_two_dots = self.pixelated_font.render("Loading..", False, (255,255,255)).convert_alpha()
        self.loading_text_three_dots = self.pixelated_font.render("Loading...", False, (255,255,255)).convert_alpha()
        self.loading_text_position_one_dot = ((float(Screen.screen.get_width()) / 2.0) - (float(self.loading_text_one_dot.get_width()) / 2.0), (float(Screen.screen.get_height()) / 2.0) - self.loading_text_one_dot.get_height() + 50 + (self.margin_between_icon_and_loading_text / 2.0))
        self.loading_text_position_two_dots = ((float(Screen.screen.get_width()) / 2.0) - (float(self.loading_text_two_dots.get_width()) / 2.0), (float(Screen.screen.get_height()) / 2.0) - self.loading_text_two_dots.get_height() + 50 +  (self.margin_between_icon_and_loading_text / 2.0))
        self.loading_text_position_three_dots = ((float(Screen.screen.get_width()) / 2.0) - (float(self.loading_text_three_dots.get_width()) / 2.0), (float(Screen.screen.get_height()) / 2.0) - self.loading_text_three_dots.get_height() + 50 + (self.margin_between_icon_and_loading_text / 2.0))

    def update(self):
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        Screen.screen.blit(self.game_icon, self.game_icon_position)
        if self.number_of_loading_dots == 1:
            Screen.screen.blit(self.loading_text_one_dot, self.loading_text_position_one_dot)
        elif self.number_of_loading_dots == 2:
            Screen.screen.blit(self.loading_text_two_dots, self.loading_text_position_two_dots)
        else:
            Screen.screen.blit(self.loading_text_three_dots, self.loading_text_position_three_dots)