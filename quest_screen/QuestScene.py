import pygame
from sys import exit
import os
from xpbar.XpBar import *
from main_game_screen.Elements import *
from quest_screen.QuestButton import *
from utilities.scene import *
from utilities.SaveManager import *
from utilities import Screen

class QuestScene:
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        
        self.save_manager = SaveManager()
        
        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        
        self.active_scene = Scene.main
    
    def update(self, monitor_size):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.save_manager.save_game()
                exit()
            elif event.type == pygame.VIDEORESIZE and not pygame.display.is_fullscreen():
                if event.size[0] >= 800 and event.size[1] >= 400:
                    self.previous_size = self.screen_size
                    Screen.screen = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

                    ratio_of_change_in_size = max(Screen.screen.get_size()[0] / self.previous_size[0], Screen.screen.get_size()[1] / self.previous_size[1])
                    
                    for element in elements.elements:
                        element.resize_elements(float(Screen.screen.get_size()[0]) / float(self.previous_size[0]), float(Screen.screen.get_size()[1]) / float(self.previous_size[1]),ratio_of_change_in_size)
                    
                    xp_bar.resize_xp_elements(Screen.screen, float(Screen.screen.get_size()[0]) / float(self.previous_size[0]), float(Screen.screen.get_size()[1]) / float(self.previous_size[1]))
                    self.quest_button.resize_ui_element(float(Screen.screen.get_size()[0]) / float(self.previous_size[0]), float(Screen.screen.get_size()[1]) / float(self.previous_size[1]))
                    
                    self.screen_size = Screen.screen.get_size()
                    
                    for element in elements.elements:
                        element.reposition_elements()
                    
                    xp_bar.reposition_xp_elements(Screen.screen)
                    
                else:
                    self.previous_size = self.screen_size
                    Screen.screen = pygame.display.set_mode((800,400), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                    ratio_of_change_in_size = max(Screen.screen.get_size()[0] / self.previous_size[0], Screen.screen.get_size()[1] / self.previous_size[1])
                    
                    for element in elements.elements:
                        element.resize_elements(float(Screen.screen.get_size()[0]) / float(self.previous_size[0]), float(Screen.screen.get_size()[1]) / float(self.previous_size[1]),ratio_of_change_in_size)
                    
                    xp_bar.resize_xp_elements(Screen.screen, float(Screen.screen.get_size()[0]) / float(self.previous_size[0]), float(Screen.screen.get_size()[1]) / float(self.previous_size[1]))
                    self.quest_button.resize_ui_element(float(Screen.screen.get_size()[0]) / float(self.previous_size[0]), float(Screen.screen.get_size()[1]) / float(self.previous_size[1]))
                    
                    self.screen_size = Screen.screen.get_size()
                    
                    for element in elements.elements:
                        element.reposition_elements()
                    
                    xp_bar.reposition_xp_elements(Screen.screen)
            elif event.type == pygame.MOUSEMOTION:
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
        
        if pygame.key.get_pressed()[pygame.key.key_code("f11")]:
            if not pygame.display.is_fullscreen():
                self.previous_size = Screen.screen.get_size()
                Screen.screen = pygame.display.set_mode(pygame.display.list_modes()[0])
                Screen.screen = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)

                ratio_of_change_in_size = max(monitor_size[0] / self.previous_size[0], monitor_size[1] / self.previous_size[1])
                    
                for element in elements.elements:
                    element.resize_elements(float(monitor_size[0]) / float(self.previous_size[0]), float(monitor_size[1]) / float(self.previous_size[1]),ratio_of_change_in_size)
                    
                xp_bar.resize_xp_elements(Screen.screen, float(monitor_size[0]) / float(self.previous_size[0]), float(monitor_size[1]) / float(self.previous_size[1]))
                self.quest_button.resize_ui_element(float(monitor_size[0]) / float(self.previous_size[0]), float(monitor_size[1]) / float(self.previous_size[1]))
                    
                self.screen_size = Screen.screen.get_size()
                    
                for element in elements.elements:
                    element.reposition_elements()
                    
                xp_bar.reposition_xp_elements(Screen.screen)
            else:
                Screen.screen = pygame.display.set_mode(self.previous_size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

                ratio_of_change_in_size = max(self.previous_size[0] / monitor_size[0], self.previous_size[1] / monitor_size[1])
                    
                for element in elements.elements:
                    element.resize_elements(float(self.previous_size[0]) / float(monitor_size[0]), float(self.previous_size[1]) / float(monitor_size[1]),ratio_of_change_in_size)
                    
                xp_bar.resize_xp_elements(Screen.screen, float(self.previous_size[0]) / float(monitor_size[0]), float(self.previous_size[1]) / float(monitor_size[1]))
                self.quest_button.resize_ui_element(float(self.previous_size[0]) / float(monitor_size[0]), float(self.previous_size[1]) / float(monitor_size[1]))
                
                self.screen_size = Screen.screen.get_size()
                    
                for element in elements.elements:
                    element.reposition_elements()
                    
                xp_bar.reposition_xp_elements(Screen.screen)
        
        Screen.screen.fill((46, 46, 46))
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        self.quest_button.draw(Screen.screen)
    
    def set_active_scene(self, active_scene: Scene):
        self.active_scene = active_scene
    
    def get_active_scene(self):
        return self.active_scene