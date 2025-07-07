import pygame
import os
from xpbar.XpBar import *
from main_game_screen.Elements import *
from quest_screen.QuestButton import *
from utilities.Scene import *
from utilities.SaveManager import *
from utilities import Screen
from quest_screen.QuestLine import *
from marketplace_screen.MarketplaceButton import MarketplaceButton
from settings_screen.SettingsButton import SettingsButton
from credits_screen.CreditsButton import CreditsButton

class QuestScene:
    
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        self.marketplace_button = MarketplaceButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"marketplace button icon.png")).convert_alpha())
        self.setting_buttons = SettingsButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"settings button icon.png")).convert_alpha())
        self.credits_buttons = CreditsButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"credits button icon.png")).convert_alpha())
        
        self.is_mouse_dragging_on_the_background = False
        
        self.previous_mouse_position = (0, 0)
        
        self.movement_target_position = (quest_line.position_offset[0], quest_line.position_offset[1])
        
        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        
        self.active_scene = Scene.main
    
    def update_movement(self, dt):
        if quest_line.position_offset[0] != self.movement_target_position[0] \
        or quest_line.position_offset[1] != self.movement_target_position[1]:
            if (self.movement_target_position[0] - quest_line.position_offset[0]) > 0:
                movement_in_the_x_axis = max(-3, min(3, 3 * dt * 60.0 * float(self.movement_target_position[0] - quest_line.position_offset[0])))
            elif (self.movement_target_position[0] - quest_line.position_offset[0]) < 0:
                movement_in_the_x_axis = -max(-3, min(3, 3 * dt * 60.0 * abs(float(self.movement_target_position[0] - quest_line.position_offset[0]))))
            else:
                movement_in_the_x_axis = 0.0
            if (self.movement_target_position[1] - quest_line.position_offset[1]) > 0:
                movement_in_the_y_axis = max(-3, min(3, 3 * dt * 60.0 * float(self.movement_target_position[1] - quest_line.position_offset[1])))
            elif (self.movement_target_position[1] - quest_line.position_offset[1]) < 0:
                movement_in_the_y_axis = -max(-3, min(3, 3 * dt * 60.0 * abs(float(self.movement_target_position[1] - quest_line.position_offset[1]))))
            else:
                movement_in_the_y_axis = 0.0
                
            if quest_line.position_offset[0] > self.movement_target_position[0]:
                if (quest_line.position_offset[0] + movement_in_the_x_axis) < self.movement_target_position[0]:
                    movement_in_the_x_axis = float(self.movement_target_position[0] - quest_line.position_offset[0])
            else:
                if (quest_line.position_offset[0] + movement_in_the_x_axis) > self.movement_target_position[0]:
                    movement_in_the_x_axis = float(self.movement_target_position[0] - quest_line.position_offset[0])
            
            if quest_line.position_offset[1] > self.movement_target_position[1]:
                if (quest_line.position_offset[1] + movement_in_the_y_axis) < self.movement_target_position[1]:
                    movement_in_the_y_axis = float(self.movement_target_position[1] - quest_line.position_offset[1])
            else:
                if (quest_line.position_offset[1] + movement_in_the_y_axis) > self.movement_target_position[1]:
                    movement_in_the_y_axis = float(self.movement_target_position[1] - quest_line.position_offset[1])
                
            movement_vector = (movement_in_the_x_axis, movement_in_the_y_axis)
            quest_line.set_position((int(quest_line.position_offset[0] + movement_vector[0]), int(quest_line.position_offset[1] + movement_vector[1])))
    
    def update(self, dt, events):
        mouse_position = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.setting_buttons.is_highlighted = self.setting_buttons._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.credits_buttons.is_highlighted = self.credits_buttons._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                for quest in quests:
                    quest.quest_ui_icon.is_highlighted = quest.quest_ui_icon._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                
                if self.is_mouse_dragging_on_the_background:
                    if (quest_line.position_offset[0] + (mouse_position[0] - self.previous_mouse_position[0])) <= 1200 \
                            and (quest_line.position_offset[1] + (mouse_position[1] - self.previous_mouse_position[1])) <= 1200:
                                quest_line.set_position((quest_line.position_offset[0] + (mouse_position[0] - self.previous_mouse_position[0]), \
                                quest_line.position_offset[1] + (mouse_position[1] - self.previous_mouse_position[1])))
                    self.previous_mouse_position = (mouse_position[0], mouse_position[1])
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                is_any_ui_element_pressed = False
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
                    is_any_ui_element_pressed = True
                if self.marketplace_button.is_highlighted and not self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(True)
                    is_any_ui_element_pressed = True
                if self.setting_buttons.is_highlighted and not self.setting_buttons.is_ui_element_pressed():
                    self.setting_buttons.set_ui_element_is_pressed(True)
                    is_any_ui_element_pressed = True
                if self.credits_buttons.is_highlighted and not self.credits_buttons.is_ui_element_pressed():
                    self.credits_buttons.set_ui_element_is_pressed(True)
                    is_any_ui_element_pressed = True
                for quest in quests:
                    if quest.quest_ui_icon.is_highlighted and not quest.quest_ui_icon.is_ui_element_pressed():
                        quest.quest_ui_icon.set_ui_element_is_pressed(True)
                        is_any_ui_element_pressed = True
                
                if not is_any_ui_element_pressed:
                    self.previous_mouse_position = (mouse_position[0], mouse_position[1])
                    self.is_mouse_dragging_on_the_background = True
                else:
                    self.is_mouse_dragging_on_the_background = False
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_mouse_dragging_on_the_background:
                    self.is_mouse_dragging_on_the_background = False
                
                was_any_quest_ui_icon_pressed = False
                if self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.main
                if self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.marketplace_scene
                if self.setting_buttons.is_ui_element_pressed():
                    self.setting_buttons.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.settings_scene
                if self.credits_buttons.is_ui_element_pressed():
                    self.credits_buttons.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.credits_scene
                for quest in quests:
                    if quest.quest_ui_icon.is_ui_element_pressed():
                        quest.quest_ui_icon.set_ui_element_is_pressed(False)
                        quest_line.display_quest_explanation_message(quest.id)
                        was_any_quest_ui_icon_pressed = True
                if not was_any_quest_ui_icon_pressed:
                    quest_line._displayed_quest_descriptions_quest_index = -1
            
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
            movement_target_y = min(1200, self.movement_target_position[1] + (1 * movement_speed))
            self.movement_target_position = (self.movement_target_position[0], movement_target_y)
        if pygame.key.get_pressed()[pygame.key.key_code("s")]:
            movement_target_y = max(-1200, self.movement_target_position[1] - (1 * movement_speed))
            self.movement_target_position = (self.movement_target_position[0], movement_target_y)
        if pygame.key.get_pressed()[pygame.key.key_code("a")]:
            movement_target_x = min(1200, self.movement_target_position[0] + (1 * movement_speed))
            self.movement_target_position = (movement_target_x, self.movement_target_position[1])
        if pygame.key.get_pressed()[pygame.key.key_code("d")]:
            movement_target_x = max(-1200, self.movement_target_position[0] - (1 * movement_speed))
            self.movement_target_position = (movement_target_x, self.movement_target_position[1])
        
        Screen.screen.fill((46, 46, 46))
        
        self.update_movement(dt)
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        quest_line.draw(Screen.screen)
        
        self.quest_button.draw(Screen.screen)
        self.marketplace_button.draw(Screen.screen)
        self.setting_buttons.draw(Screen.screen)
        self.credits_buttons.draw(Screen.screen)
    
    def set_active_scene(self, active_scene: Scene):
        if self.active_scene != active_scene:
            mouse_position = pygame.mouse.get_pos()
            self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.setting_buttons.is_highlighted = self.setting_buttons._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.credits_buttons.is_highlighted = self.credits_buttons._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            for quest in quests:
                quest.quest_ui_icon.is_highlighted = quest.quest_ui_icon._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.active_scene = active_scene
    
    def get_active_scene(self):
        return self.active_scene
    
    def resize_scene(self, new_size: tuple[int, int]):
        self.quest_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.marketplace_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.setting_buttons.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.credits_buttons.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))

        quest_line.resize_questline(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
                    
        self.movement_target_position = (quest_line.position_offset[0], quest_line.position_offset[1])
        
        self.screen_size = Screen.screen.get_size()
