import pygame
import os
from utilities import Screen
from utilities.Scene import Scene
from quest_screen.QuestButton import QuestButton
from marketplace_screen.MarketplaceButton import MarketplaceButton

class MarketplaceScene:
    
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        self.marketplace_button = MarketplaceButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"marketplace button icon.png")).convert_alpha())
        
        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        
        self.active_scene = Scene.main
    
    def reposition_ui(self):
        pass
    
    def update(self, dt, events):
        Screen.screen.fill((46, 46, 46))
        
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))

            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
                if self.marketplace_button.is_highlighted and not self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(True)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.main
                if self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.marketplace_scene
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        self.quest_button.draw(Screen.screen)
        self.marketplace_button.draw(Screen.screen)
    
    def set_active_scene(self, active_scene: Scene):
        self.active_scene = active_scene
        
    
    def get_active_scene(self):
        return self.active_scene
    
    def resize_scene(self, new_size: tuple[int,int]):
        self.quest_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.marketplace_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))

        self.screen_size = Screen.screen.get_size()
        self.reposition_ui()
