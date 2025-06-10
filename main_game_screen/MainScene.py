import pygame
from sys import exit
import os
import time
from xpbar.XpBar import *
from main_game_screen.Elements import *
from crafting.CraftingManager import *
from quest_screen.QuestButton import *
from utilities.scene import *
from utilities.SaveManager import *
from utilities import Screen

class MainScene:
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        
        self.save_manager = SaveManager()
        
        self.active_scene = Scene.main

        reevaluate_recipes_waiting_time()

        for element in elements.elements:
            element.reposition_elements()

        xp_bar.reposition_xp_elements(Screen.screen)

        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        self.rock_timer = 0

        self.element_explanation_message_displayed = -1
    
    def update(self, dt, monitor_size):
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
                    element.is_highlighted = element._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                    self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                counter = 0
                for element in elements.elements:
                    if element.is_highlighted and not element.is_element_pressed():
                        element.set_element_is_pressed(True)
                        if get_recipe_for(ElementType(counter)).waiting_time > 0 and is_craftable(get_recipe_for(ElementType(counter))):
                            element._crafting_prorgress = 0.0
                            element._is_element_currently_being_crafted = True
                    counter += 1
                self.element_explanation_message_displayed = -1
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
            
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
                            reevaluate_recipes_waiting_time()
                        if crafting_timers[counter] == -1:
                            element.set_element_is_pressed(False)
                    counter += 1
                if self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.quest_scene
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
        
        counter = 0
        for crafting_timer in crafting_timers:
            recipe = get_recipe_for(ElementType(counter))
            if crafting_timer >= 0:
                if (time.time() - crafting_timer) >= recipe.waiting_time:
                    if len(recipe.ingredients[0]) != 0:
                        for ingredient in recipe.ingredients:
                            if ingredient[2]:
                                elements.elements[int(ingredient[0])].increase_element_amount(-ingredient[1], Screen.screen)
                    elements.elements[int(recipe.result[0])].increase_element_amount(recipe.result[1], Screen.screen)
                    reevaluate_recipes_waiting_time()
                    xp_bar.increase_xp(recipe.resulting_xp, Screen.screen)
                    crafting_timers[counter] = -1
                    elements.elements[int(recipe.result[0])].set_element_is_pressed(False)
                    elements.elements[int(recipe.result[0])]._is_element_currently_being_crafted = False
                    elements.elements[int(recipe.result[0])]._crafting_prorgress = 0.0
                else:
                    elements.elements[int(recipe.result[0])]._crafting_prorgress = (time.time() - crafting_timer) / float(recipe.waiting_time)
            counter += 1
        
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
    
    def set_active_scene(self, active_scene: Scene):
        self.active_scene = active_scene
    
    def get_active_scene(self):
        return self.active_scene