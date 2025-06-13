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
    
    def update(self, dt, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                for quest in quests:
                    quest.quest_ui_icon.is_highlighted = quest.quest_ui_icon._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
                for quest in quests:
                    if quest.quest_ui_icon.is_highlighted and not quest.quest_ui_icon.is_ui_element_pressed():
                        quest.quest_ui_icon.set_ui_element_is_pressed(True)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.main
                for quest in quests:
                    if quest.quest_ui_icon.is_ui_element_pressed():
                        quest.quest_ui_icon.set_ui_element_is_pressed(False)
            
            elif event.type == pygame.MOUSEWHEEL:
                zoom_speed = event.y * 0.1
                if event.y >= 0:
                    if quest_line._ratio_of_change_in_width <= 2 and quest_line._ratio_of_change_in_height <= 2:
                        quest_line.resize_questline(1.0 + zoom_speed, 1.0 + zoom_speed)
                else:
                    if quest_line._ratio_of_change_in_width >= 0.5 and quest_line._ratio_of_change_in_height >= 0.5:
                        quest_line.resize_questline(1.0 + zoom_speed, 1.0 + zoom_speed)
        
        movement_speed = 6 * dt * 60
        
        if pygame.key.get_pressed()[pygame.key.key_code("w")]:
            if quest_line.position_offset[1] + (1 * movement_speed) <= 1200:
                quest_line.set_position((quest_line.position_offset[0], quest_line.position_offset[1] + (1.0 * movement_speed)))
        if pygame.key.get_pressed()[pygame.key.key_code("s")]:
            if quest_line.position_offset[1] + (-1 * movement_speed) <= 1200:
                quest_line.set_position((quest_line.position_offset[0], quest_line.position_offset[1] - (1.0 * movement_speed)))
        if pygame.key.get_pressed()[pygame.key.key_code("a")]:
            if quest_line.position_offset[0] + (1 * movement_speed)<= 1200:
                quest_line.set_position((quest_line.position_offset[0] + (1.0 * movement_speed), quest_line.position_offset[1]))
        if pygame.key.get_pressed()[pygame.key.key_code("d")]:
            if quest_line.position_offset[0] + (-1 * movement_speed) <= 1200:
                quest_line.set_position((quest_line.position_offset[0] + (-1.0 * movement_speed), quest_line.position_offset[1]))
        
        Screen.screen.fill((46, 46, 46))
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        quest_line.draw(Screen.screen)
        
        self.quest_button.draw(Screen.screen)
    
    def set_active_scene(self, active_scene: Scene):
        self.active_scene = active_scene
    
    def get_active_scene(self):
        return self.active_scene
    
    def resize_scene(self, new_size: tuple[int, int]):
                    
        self.quest_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        quest_line.resize_questline(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
                    
        self.screen_size = Screen.screen.get_size()
