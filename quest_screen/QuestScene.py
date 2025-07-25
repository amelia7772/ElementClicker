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
        
        self.background_ui_icon = UiElement([self.background_image.copy()], [(float(self.background_image.get_width()), float(self.background_image.get_height()))])
        
        self.is_mouse_dragging_on_the_background = False
        
        self.previous_mouse_position = (0, 0)
        
        self.movement_target_position = (quest_line.position_offset[0], quest_line.position_offset[1])
        
        self.movement_change = pygame.Vector2(0.0, 0.0)
        
        self.ratio_of_zooming = 1.0
        
        self.world_size = (2400.0, 2400.0)
        
        self.resize_ui_buttons()
        
        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        
        self.active_scene = Scene.main
    
    def update_movement(self, dt):
        movement_speed = 9.0 * dt * 60.0 * self.ratio_of_zooming
        
        if pygame.key.get_pressed()[pygame.key.key_code("w")]:
            self.movement_change.y += 1 * movement_speed * (Screen.screen.get_height() / 400.0)
        if pygame.key.get_pressed()[pygame.key.key_code("s")]:
            self.movement_change.y -= 1 * movement_speed * (Screen.screen.get_height() / 400.0)
        if pygame.key.get_pressed()[pygame.key.key_code("a")]:
            self.movement_change.x += 1 * movement_speed * (Screen.screen.get_width() / 800.0)
        if pygame.key.get_pressed()[pygame.key.key_code("d")]:
            self.movement_change.x -= 1 * movement_speed * (Screen.screen.get_width() / 800.0)
        
        if not (self.movement_change.x == 0.0 and self.movement_change.y == 0.0):
            self.movement_change.normalize()
        
            self.movement_target_position = (max((-(self.world_size[0] / 2.0) * self.ratio_of_zooming + (float(Screen.screen.get_width()) - (float(Screen.screen.get_width()) * self.ratio_of_zooming))), min(((self.world_size[0] / 2.0) * self.ratio_of_zooming), self.movement_target_position[0] + int(self.movement_change.x))),\
                max((-(self.world_size[1] / 2.0) * self.ratio_of_zooming + (float(Screen.screen.get_height()) - (float(Screen.screen.get_height()) * self.ratio_of_zooming))), min(((self.world_size[1] / 2.0) * self.ratio_of_zooming), self.movement_target_position[1] + int(self.movement_change.y))))
        
            self.movement_change.x = 0.0
            self.movement_change.y = 0.0
        
        if quest_line.position_offset[0] != self.movement_target_position[0] \
        or quest_line.position_offset[1] != self.movement_target_position[1]:
            if (self.movement_target_position[0] - quest_line.position_offset[0]) > 0:
                movement_in_the_x_axis = max(5, min(20, 3 * dt * 60.0 * float(self.movement_target_position[0] - quest_line.position_offset[0])))
            elif (self.movement_target_position[0] - quest_line.position_offset[0]) < 0:
                movement_in_the_x_axis = -max(5, min(20, 3 * dt * 60.0 * abs(float(self.movement_target_position[0] - quest_line.position_offset[0]))))
            else:
                movement_in_the_x_axis = 0.0
            if (self.movement_target_position[1] - quest_line.position_offset[1]) > 0:
                movement_in_the_y_axis = max(5, min(20, 3 * dt * 60.0 * float(self.movement_target_position[1] - quest_line.position_offset[1])))
            elif (self.movement_target_position[1] - quest_line.position_offset[1]) < 0:
                movement_in_the_y_axis = -max(5, min(20, 3 * dt * 60.0 * abs(float(self.movement_target_position[1] - quest_line.position_offset[1]))))
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
    
    def resize_ui_buttons(self):
        self.quest_button.resize_ui_element(75.0 / float(self.quest_button.sizes[0][0]), 75.0 / float(self.quest_button.sizes[0][1]))
        self.marketplace_button.resize_ui_element(75.0 / float(self.marketplace_button.sizes[0][0]), 75.0 / float(self.marketplace_button.sizes[0][1]))
        self.setting_buttons.resize_ui_element(75.0 / float(self.setting_buttons.sizes[0][0]), 75.0 / float(self.setting_buttons.sizes[0][1]))
        self.credits_buttons.resize_ui_element(75.0 / float(self.credits_buttons.sizes[0][0]), 75.0 / float(self.credits_buttons.sizes[0][1]))
    
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
                    self.movement_target_position = (max((-(self.world_size[0] / 2.0) * self.ratio_of_zooming + (float(Screen.screen.get_width()) - (float(Screen.screen.get_width()) * self.ratio_of_zooming))), min(((self.world_size[0] / 2.0) * self.ratio_of_zooming), self.movement_target_position[0] + int(mouse_position[0] - self.previous_mouse_position[0]))),\
                        max((-(self.world_size[1] / 2.0) * self.ratio_of_zooming + (float(Screen.screen.get_height()) - (float(Screen.screen.get_height()) * self.ratio_of_zooming))), min(((self.world_size[1] / 2.0) * self.ratio_of_zooming), self.movement_target_position[1] + int(mouse_position[1] - self.previous_mouse_position[1]))))
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
                    self.movement_target_position = (quest_line.position_offset[0], quest_line.position_offset[1])
                
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
                new_ratio_of_zooming = round(self.ratio_of_zooming + zoom_speed, 1)
                if ((event.y > 0) and (new_ratio_of_zooming <= 2.0))\
                or ((event.y < 0) and (new_ratio_of_zooming >= 0.5)):
                    quest_line.resize_questline(new_ratio_of_zooming / self.ratio_of_zooming, new_ratio_of_zooming / self.ratio_of_zooming)
                    self.background_ui_icon.resize_ui_element(new_ratio_of_zooming / self.ratio_of_zooming, new_ratio_of_zooming / self.ratio_of_zooming)
                    self.ratio_of_zooming = new_ratio_of_zooming
                    
        Screen.screen.fill((46, 46, 46))
        
        self.update_movement(dt)
        
        for x in range(-int(self.background_ui_icon.sizes[0][0]), Screen.screen.get_width() + int(self.background_ui_icon.sizes[0][0]), int(self.background_ui_icon.sizes[0][0])):
            for y in range(-int(self.background_ui_icon.sizes[0][1]), Screen.screen.get_height() + int(self.background_ui_icon.sizes[0][1]), int(self.background_ui_icon.sizes[0][1])):
                self.background_ui_icon.draw(Screen.screen, [(x + (quest_line.position_offset[0] % int(self.background_ui_icon.sizes[0][0])),y + (quest_line.position_offset[1] % int(self.background_ui_icon.sizes[0][1])))])
        
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

        new_ratio_of_zoom = max(0.5, min(2.0, self.ratio_of_zooming * (float(new_size[0]) / float(self.previous_size[0]))))
        
        quest_line.resize_questline(new_ratio_of_zoom / self.ratio_of_zooming, new_ratio_of_zoom / self.ratio_of_zooming)
        
        self.background_ui_icon.resize_ui_element(new_ratio_of_zoom / self.ratio_of_zooming, new_ratio_of_zoom / self.ratio_of_zooming)
        
        self.movement_target_position = (quest_line.position_offset[0], quest_line.position_offset[1])
        
        self.screen_size = Screen.screen.get_size()
