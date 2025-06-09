import pygame
from sys import exit
import struct
import os
import time

pygame.init()
monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode((800, 400), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
pygame.display.set_caption("Element Clicker")
logo_image = pygame.image.load(os.path.join("assets", "images" ,"icon.png")).convert_alpha()
pygame.display.set_icon(logo_image)
background_image = pygame.image.load(os.path.join("assets", "images" ,"background.png")).convert_alpha()


from XpBar import *
from Elements import *
from CraftingTable import *
from QuestButton import *

quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())

screen.fill((194, 255, 250))
previous_time = time.time()

try:
    save_file = open("save.bin", 'rb')
    if save_file.readable():
        buffer = save_file.read(((len(elements.elements) + 2) * 4) + len(elements.elements))
        resources = struct.unpack(f'{len(elements.elements) + 2}i{len(elements.elements)}b', buffer)
        counter = 0
        for element in elements.elements:
            element.increase_element_amount(resources[counter], screen)
            counter += 1
        xp_bar.set_xp(resources[counter], screen)
        counter += 1
        xp_bar.set_level(resources[counter], screen)
        counter += 1
        for element in elements.elements:
            element.is_available = resources[counter]
            counter += 1
    save_file.close()
except FileExistsError:
    print("FileExistsError")
except FileNotFoundError:
    print("FileNotFoundError")
except struct.error:
    print("struct.error")

reevaluate_recipes_waiting_time()

clock = pygame.time.Clock()

for element in elements.elements:
    element.reposition_elements()

xp_bar.reposition_xp_elements(screen)

screen_size = screen.get_size()
global rock_timer
rock_timer = 0

element_explanation_message_displayed = -1

while True:
    dt = time.time() - previous_time
    previous_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            save_file = open("save.bin", 'wb')
            buffer = bytes()
            for element in elements.elements:
                buffer += struct.pack('1i', element.element_resource_amount)
            buffer += struct.pack('2i', xp_bar.xp_amount, xp_bar.level)
            for element in elements.elements:
                buffer += struct.pack('1b', element.is_available)
            if save_file.writable():
                save_file.write(buffer)
            save_file.close()
            exit()
        elif event.type == pygame.VIDEORESIZE and not pygame.display.is_fullscreen():
            if event.size[0] >= 800 and event.size[1] >= 400:
                previous_size = screen_size
                screen = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

                ratio_of_change_in_size = max(screen.get_size()[0] / previous_size[0], screen.get_size()[1] / previous_size[1])
                
                for element in elements.elements:
                    element.resize_elements(float(screen.get_size()[0]) / float(previous_size[0]), float(screen.get_size()[1]) / float(previous_size[1]),ratio_of_change_in_size)
                
                xp_bar.resize_xp_elements(screen, float(screen.get_size()[0]) / float(previous_size[0]), float(screen.get_size()[1]) / float(previous_size[1]))
                quest_button.resize_quest_button(float(screen.get_size()[0]) / float(previous_size[0]), float(screen.get_size()[1]) / float(previous_size[1]))
                
                screen_size = screen.get_size()
                
                for element in elements.elements:
                    element.reposition_elements()
                
                xp_bar.reposition_xp_elements(screen)
                
            else:
                previous_size = screen_size
                screen = pygame.display.set_mode((800,400), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                ratio_of_change_in_size = max(screen.get_size()[0] / previous_size[0], screen.get_size()[1] / previous_size[1])
                
                for element in elements.elements:
                    element.resize_elements(float(screen.get_size()[0]) / float(previous_size[0]), float(screen.get_size()[1]) / float(previous_size[1]),ratio_of_change_in_size)
                
                xp_bar.resize_xp_elements(screen, float(screen.get_size()[0]) / float(previous_size[0]), float(screen.get_size()[1]) / float(previous_size[1]))
                quest_button.resize_quest_button(float(screen.get_size()[0]) / float(previous_size[0]), float(screen.get_size()[1]) / float(previous_size[1]))
                
                screen_size = screen.get_size()
                
                for element in elements.elements:
                    element.reposition_elements()
                
                xp_bar.reposition_xp_elements(screen)
        elif event.type == pygame.MOUSEMOTION:
            for element in elements.elements:
                mouse_position = pygame.mouse.get_pos()
                element.is_highlighted = element._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            counter = 0
            for element in elements.elements:
                if element.is_highlighted and not element.is_element_pressed():
                    element.set_element_is_pressed(True)
                    if get_recipe_for(ElementType(counter)).waiting_time > 0 and is_craftable(get_recipe_for(ElementType(counter))):
                        element._crafting_prorgress = 0.0
                        element._is_element_currently_being_crafted = True
                counter += 1
            element_explanation_message_displayed = -1
        
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
            is_no_element_highlighted = True
            counter = 0
            for element in elements.elements:
                if element.is_highlighted and not (element_explanation_message_displayed == counter):
                    element_explanation_message_displayed = counter
                    is_no_element_highlighted = False
                counter += 1
            if is_no_element_highlighted:
                element_explanation_message_displayed = -1
        elif event.type == pygame.MOUSEBUTTONUP:
            counter = 0
            for element in elements.elements:
                if element.is_element_pressed() and crafting_timers[counter] == -1:
                    if is_craftable(get_recipe_for(ElementType(counter))):
                        craft(get_recipe_for(ElementType(counter)), screen)
                        reevaluate_recipes_waiting_time()
                    if crafting_timers[counter] == -1:
                        element.set_element_is_pressed(False)
                counter += 1
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
            previous_size = screen.get_size()
            screen = pygame.display.set_mode(pygame.display.list_modes()[0])
            screen = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)

            ratio_of_change_in_size = max(monitor_size[0] / previous_size[0], monitor_size[1] / previous_size[1])
                
            for element in elements.elements:
                element.resize_elements(float(monitor_size[0]) / float(previous_size[0]), float(monitor_size[1]) / float(previous_size[1]),ratio_of_change_in_size)
                
            xp_bar.resize_xp_elements(screen, float(monitor_size[0]) / float(previous_size[0]), float(monitor_size[1]) / float(previous_size[1]))
                
            screen_size = screen.get_size()
                
            for element in elements.elements:
                element.reposition_elements()
                
            xp_bar.reposition_xp_elements(screen)
        else:
            screen = pygame.display.set_mode(previous_size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

            ratio_of_change_in_size = max(previous_size[0] / monitor_size[0], previous_size[1] / monitor_size[1])
                
            for element in elements.elements:
                element.resize_elements(float(previous_size[0]) / float(monitor_size[0]), float(previous_size[1]) / float(monitor_size[1]),ratio_of_change_in_size)
                
            xp_bar.resize_xp_elements(screen, float(previous_size[0]) / float(monitor_size[0]), float(previous_size[1]) / float(monitor_size[1]))
                
            screen_size = screen.get_size()
                
            for element in elements.elements:
                element.reposition_elements()
                
            xp_bar.reposition_xp_elements(screen)
    
    counter = 0
    for crafting_timer in crafting_timers:
        recipe = get_recipe_for(ElementType(counter))
        if crafting_timer >= 0:
            if (time.time() - crafting_timer) >= recipe.waiting_time:
                if len(recipe.ingredients[0]) != 0:
                    for ingredient in recipe.ingredients:
                        if ingredient[2]:
                            elements.elements[int(ingredient[0])].increase_element_amount(-ingredient[1], screen)
                elements.elements[int(recipe.result[0])].increase_element_amount(recipe.result[1], screen)
                reevaluate_recipes_waiting_time()
                xp_bar.increase_xp(recipe.resulting_xp, screen)
                crafting_timers[counter] = -1
                elements.elements[int(recipe.result[0])].set_element_is_pressed(False)
                elements.elements[int(recipe.result[0])]._is_element_currently_being_crafted = False
                elements.elements[int(recipe.result[0])]._crafting_prorgress = 0.0
            else:
                elements.elements[int(recipe.result[0])]._crafting_prorgress = (time.time() - crafting_timer) / float(recipe.waiting_time)
        counter += 1
    
    elements.reevaluate_availability(xp_bar.level)  
    

    screen.fill((46, 46, 46))
    
    for x in range(0, screen.get_width(), background_image.get_width()):
        for y in range(0, screen.get_height(), background_image.get_height()):
            screen.blit(background_image, (x,y))
    
    elements.draw(screen)
    
    if element_explanation_message_displayed >=0:
        if elements.elements[element_explanation_message_displayed].is_available:
            elements.elements[element_explanation_message_displayed].element_explanation_message.draw(screen)
    
    xp_bar.draw(screen)
    quest_button.draw(screen)
    pygame.display.update()
    clock.tick(120)
