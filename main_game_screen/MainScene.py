import pygame
import os
from xpbar.XpBar import *
from main_game_screen.Elements import *
from crafting.CraftingManager import *
from quest_screen.QuestButton import *
from utilities.Scene import *
from utilities.SaveManager import *
from utilities import Screen
from marketplace_screen.MarketplaceButton import MarketplaceButton

class MainScene:
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        self.marketplace_button = MarketplaceButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"marketplace button icon.png")).convert_alpha())

        self.active_scene = Scene.main

        reevaluate_recipes_waiting_time()

        for element in elements.elements:
            element.reposition_elements()

        xp_bar.reposition_xp_elements(Screen.screen)

        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        self.rock_timer = 0

        self.element_explanation_message_displayed = -1
        self.selected_element_to_be_produced_by_factories = [-1, -1, -1, -1, -1, -1]
        self.crafting_amounts = [0 for i in range(0, len(crafting_timers))]
    
    def update(self, dt, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                for element in elements.elements:
                    element.is_highlighted = element._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                counter = 0
                for element in elements.elements:
                    if element.is_highlighted and not element.is_element_pressed():
                        element.set_element_is_pressed(True)
                        self.selected_element_to_be_produced_by_factories[element.element_tier - 1] = counter
                        if get_recipe_for(ElementType(counter)).waiting_time > 0 and is_craftable(get_recipe_for(ElementType(counter))):
                            element._crafting_prorgress = 0.0
                            element._is_element_currently_being_crafted = True
                            self.crafting_amounts[counter] = 1
                    counter += 1
                self.element_explanation_message_displayed = -1
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
                if self.marketplace_button.is_highlighted and not self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(True)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                is_no_element_highlighted = True
                counter = 0
                for element in elements.elements:
                    if element.is_highlighted and not (self.element_explanation_message_displayed == counter):
                        self.element_explanation_message_displayed = counter
                        is_no_element_highlighted = False
                    counter += 1
                if is_no_element_highlighted:
                    self.element_explanation_message_displayed = -1
            elif event.type == pygame.MOUSEBUTTONUP:
                counter = 0
                for element in elements.elements:
                    if element.is_element_pressed() and crafting_timers[counter] == -1:
                        if is_craftable(get_recipe_for(ElementType(counter))):
                            craft(get_recipe_for(ElementType(counter)), Screen.screen)
                            for k in range(0, len(elements.elements)):
                                elements.elements[k]._is_element_craftable = is_craftable(get_recipe_for(ElementType(k)))
                            reevaluate_recipes_waiting_time()
                        if crafting_timers[counter] == -1:
                            element.set_element_is_pressed(False)
                    counter += 1
                if self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.quest_scene
                if self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.marketplace_scene
            elif event.type == pygame.MOUSEWHEEL:
                zoom_speed = event.y * 0.1
                for element in elements.elements:
                    if event.y >= 0:
                        if element._ratio_of_change_in_width <= 2 and element._ratio_of_change_in_height <= 2:
                            element.resize_elements(1.0 + zoom_speed, 1.0 + zoom_speed, 1.0 + zoom_speed)
                    else:
                        if element._ratio_of_change_in_width >= 0.5 and element._ratio_of_change_in_height >= 0.5:
                            element.resize_elements(1.0 + zoom_speed, 1.0 + zoom_speed, 1.0 + zoom_speed)
            
        movement_speed = 6 * dt * 60
        
        if pygame.key.get_pressed()[pygame.key.key_code("w")]:
            for element in elements.elements:
                if element.offset[1] + (1 * movement_speed) <= 1200:
                    element.reposition_elements_with_offset((0, 1.0 * movement_speed))
        if pygame.key.get_pressed()[pygame.key.key_code("s")]:
            for element in elements.elements:
                if element.offset[1] + (-1 * movement_speed) <= 1200:
                    element.reposition_elements_with_offset((0, -1.0 * movement_speed))
        if pygame.key.get_pressed()[pygame.key.key_code("a")]:
            for element in elements.elements:
                if element.offset[0] + (1 * movement_speed)<= 1200:
                    element.reposition_elements_with_offset((1.0 * movement_speed, 0))
        if pygame.key.get_pressed()[pygame.key.key_code("d")]:
            for element in elements.elements:
                if element.offset[0] + (-1 * movement_speed) <= 1200:
                    element.reposition_elements_with_offset((-1.0 * movement_speed, 0))
        
        elements.reevaluate_availability(xp_bar.level)  
        
        Screen.screen.fill((46, 46, 46))
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        elements.draw(Screen.screen)
        
        if self.element_explanation_message_displayed >=0:
            if elements.elements[self.element_explanation_message_displayed].is_available:
                elements.elements[self.element_explanation_message_displayed].element_explanation_message.draw(Screen.screen)
        
        xp_bar.draw(Screen.screen)
        
        self.quest_button.draw(Screen.screen)
        self.marketplace_button.draw(Screen.screen)
    
    def set_active_scene(self, active_scene: Scene):
        self.active_scene = active_scene
        
        mouse_position = pygame.mouse.get_pos()
        for element in elements.elements:
            element.is_highlighted = element._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
        self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
        self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
    
    def get_active_scene(self):
        return self.active_scene
    
    def resize_scene(self, new_size: tuple[int,int]):
        ratio_of_change_in_size = max(new_size[0] / self.previous_size[0], new_size[1] / self.previous_size[1])
                    
        for element in elements.elements:
            element.resize_elements(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]),ratio_of_change_in_size)
                    
        xp_bar.resize_xp_elements(Screen.screen, float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        
        self.quest_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.marketplace_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))

        self.screen_size = Screen.screen.get_size()
                    
        for element in elements.elements:
            element.reposition_elements()
                    
        xp_bar.reposition_xp_elements(Screen.screen)
