import pygame
from sys import exit
import os
from xpbar.XpBar import *
from main_game_screen.Elements import *
from quest_screen.QuestButton import *
from utilities.scene import *
from utilities.SaveManager import *
from utilities import Screen
from quest_screen.QuestLine import *

class QuestScene:
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        
        self.save_manager = SaveManager()
        
        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        
        self.active_scene = Scene.main
        self.quest_line = QuestLine()
    
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                for element in elements.elements:
                    mouse_position = pygame.mouse.get_pos()
                    self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.main
        
        Screen.screen.fill((46, 46, 46))
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        self.quest_line.draw(Screen.screen)
        
        self.quest_button.draw(Screen.screen)
    
    def set_active_scene(self, active_scene: Scene):
        self.active_scene = active_scene
    
    def get_active_scene(self):
        return self.active_scene
    
    def resize_scene(self, new_size: tuple[int, int]):
                    
        self.quest_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.quest_line.resize_questline(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
                    
        self.screen_size = Screen.screen.get_size()
