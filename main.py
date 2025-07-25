import pygame
import os
import time
import threading
from sys import exit
pygame.init()

from utilities import Screen

background_image = pygame.image.load(os.path.join("assets", "images" ,"background.png")).convert_alpha()

global is_loaded
is_loaded = False

def load_screen(background_image: pygame.Surface):
    from loading_screen.LoadingScene import LoadingScene
    clock = pygame.time.Clock()
    loading_scene = LoadingScene(background_image)
    timer_for_loading_dots = 0.0
    previous_time = 0.0
    while not is_loaded:
        dt = time.time() - previous_time
        previous_time = time.time()
        timer_for_loading_dots += dt
        if (timer_for_loading_dots * 1000.0) > 300:
            loading_scene.number_of_loading_dots = ((timer_for_loading_dots * 1000.0) // 300.0) + 1
        if timer_for_loading_dots >= 1.0:
            timer_for_loading_dots = 0.0
            loading_scene.number_of_loading_dots = 1
        loading_scene.update()
        pygame.display.flip()
        clock.tick(120)
    del loading_scene
    del clock

loading_screen_thread = threading.Thread(target=load_screen, args=(background_image,))
loading_screen_thread.start()

from main_game_screen.Elements import *
from utilities.Scene import *
from main_game_screen.MainScene import *
from quest_screen.QuestScene import *
from utilities.SaveManager import *
from quest_screen.QuestLine import *
from marketplace_screen.MarketplaceScene import *
from settings_screen.SettingsScene import *
from credits_screen.CreditScene import *
from utilities.Events import *

Screen.screen.fill((194, 255, 250))

active_scene = Scene.main
save_manager = SaveManager()
save_manager.load_game(Screen.screen)

clock = pygame.time.Clock()
previous_time = time.time()

main_scene = MainScene(background_image)
quest_scene = QuestScene(background_image)
marketplace_scene = MarketplaceScene(background_image)
settings_scene = SettingsScene(background_image)
credits_scene = CreditsScene(background_image)

timer_for_saving_game = 0.0
timers_for_factories = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

for i in range(0, len(elements.elements)):
    elements.elements[i]._is_element_craftable = is_craftable(get_recipe_for(ElementType(i)))

def evaluate_crafting_timers(crafting_amounts: list[int] = [1 for i in range(0, len(crafting_timers))]):
    counter = 0
    for crafting_timer in crafting_timers:
        recipe = get_recipe_for(ElementType(counter))
        if crafting_timer >= 0:
            if (time.time() - crafting_timer) >= recipe.waiting_time:
                if len(recipe.ingredients[0]) != 0:
                    for ingredient in recipe.ingredients:
                        if ingredient[2]:
                            elements.elements[int(ingredient[0])].increase_element_amount(-(ingredient[1] * crafting_amounts[counter]), Screen.screen)
                elements.elements[int(recipe.result[0])].increase_element_amount(recipe.result[1] * crafting_amounts[counter], Screen.screen)
                for k in range(0, len(elements.elements)):
                    elements.elements[k]._is_element_craftable = is_craftable(get_recipe_for(ElementType(k)))
                reevaluate_recipes_waiting_time()
                xp_bar.increase_xp(recipe.resulting_xp * crafting_amounts[counter], Screen.screen)
                crafting_timers[counter] = -1
                crafting_amounts[counter] = 0
                elements.elements[int(recipe.result[0])].set_element_is_pressed(False)
                elements.elements[int(recipe.result[0])]._is_element_currently_being_crafted = False
                elements.elements[int(recipe.result[0])]._crafting_prorgress = 0.0
                for quest in quests:
                    if (quest.condition(elements.elements, xp_bar.level)) and (not quest.is_completed):
                        quest_line.set_quest_completed(quest.id, True)
            else:
                elements.elements[int(recipe.result[0])]._crafting_prorgress = (time.time() - crafting_timer) / float(recipe.waiting_time)
        counter += 1
    return crafting_amounts

def check_for_automatic_crafting(timers_for_factories, crafting_amounts: list[int] = [1 for i in range(0, len(crafting_timers))]):
    factories_indices: list[int] = [int(ElementType.factory_tier_one), int(ElementType.factory_tier_two), int(ElementType.factory_tier_three)]
    for i in range(0, len(factories_indices)):
        if elements.elements[factories_indices[i]].element_resource_amount >= 1:
            if main_scene.selected_element_to_be_produced_by_factories[i] >= 0:
                number_of_items_crafted = 1
                delay = 1
                amount_of_times_decreasing_delay = elements.elements[factories_indices[i]].element_resource_amount
                if amount_of_times_decreasing_delay >= 3:
                    number_of_items_crafted += amount_of_times_decreasing_delay // 3
                    amount_of_times_decreasing_delay = amount_of_times_decreasing_delay % 3
                for j in range(1, amount_of_times_decreasing_delay):
                    delay -= (delay * 0.10)
                recipe = get_recipe_for(ElementType(main_scene.selected_element_to_be_produced_by_factories[i]))
                if timers_for_factories[i] >= delay or elements.elements[ElementType(main_scene.selected_element_to_be_produced_by_factories[i])]._is_element_currently_being_crafted:
                    timers_for_factories[i] = 0.0
                    elements.elements[main_scene.selected_element_to_be_produced_by_factories[i]].set_element_is_pressed(True)
                    if recipe.waiting_time > 0 and is_craftable(recipe):
                        elements.elements[main_scene.selected_element_to_be_produced_by_factories[i]]._crafting_prorgress = 0.0
                        elements.elements[main_scene.selected_element_to_be_produced_by_factories[i]]._is_element_currently_being_crafted = True
                        if crafting_amounts[main_scene.selected_element_to_be_produced_by_factories[i]] == 0:
                            crafting_amounts[main_scene.selected_element_to_be_produced_by_factories[i]] = number_of_items_crafted
                    if elements.elements[main_scene.selected_element_to_be_produced_by_factories[i]].is_element_pressed() and crafting_timers[main_scene.selected_element_to_be_produced_by_factories[i]] == -1:
                            for j in range(0, number_of_items_crafted):
                                if is_craftable(recipe):
                                    craft(recipe, Screen.screen)
                            reevaluate_recipes_waiting_time()
                            if crafting_timers[main_scene.selected_element_to_be_produced_by_factories[i]] == -1:
                                elements.elements[main_scene.selected_element_to_be_produced_by_factories[i]].set_element_is_pressed(False)
                else:
                    timers_for_factories[i] += dt
    return timers_for_factories, crafting_amounts

def evaluate_game_event(game_event: Event, marketplace_scene: MarketplaceScene):
    if game_event == Event.update_marketplace_goods_availability:
        for goods_line in marketplace_scene.goods_lines:
            goods_line.update_availability()
    if game_event == Event.money_amount_decrease:
        for goods_line in marketplace_scene.goods_lines:
            goods_line.resize_ui_elements()
    return marketplace_scene

is_loaded = True

while True:
    dt = time.time() - previous_time
    previous_time = time.time()
    timer_for_saving_game += dt
    if timer_for_saving_game >= 5:
        save_manager.save_game()
        timer_for_saving_game = 0.0
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            save_manager.save_game()
            exit()
        elif event.type == pygame.VIDEORESIZE and not pygame.display.is_fullscreen():
            main_scene.previous_size = main_scene.screen_size
            quest_scene.previous_size = quest_scene.screen_size
            marketplace_scene.previous_size = marketplace_scene.screen_size
            settings_scene.previous_size = settings_scene.screen_size
            credits_scene.previous_size = credits_scene.screen_size
            if event.size[0] >= 800 and event.size[1] >= 400:
                Screen.screen = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            else:
                Screen.screen = pygame.display.set_mode((800,400), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            main_scene.resize_scene(Screen.screen.get_size())
            quest_scene.resize_scene(Screen.screen.get_size())
            marketplace_scene.resize_scene(Screen.screen.get_size())
            settings_scene.resize_scene(Screen.screen.get_size())
            credits_scene.resize_scene(Screen.screen.get_size())
                
    if pygame.key.get_pressed()[pygame.key.key_code("f11")]:
        if not pygame.display.is_fullscreen():
            main_scene.previous_size = Screen.screen.get_size()
            quest_scene.previous_size = Screen.screen.get_size()
            marketplace_scene.previous_size = Screen.screen.get_size()
            settings_scene.previous_size = Screen.screen.get_size()
            credits_scene.previous_size = Screen.screen.get_size()
            Screen.screen = pygame.display.set_mode(pygame.display.list_modes()[0])
            Screen.screen = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
        else:
            Screen.screen = pygame.display.set_mode(main_scene.previous_size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            main_scene.previous_size = Screen.monitor_size
            quest_scene.previous_size = Screen.monitor_size
            marketplace_scene.previous_size = Screen.monitor_size
            settings_scene.previous_size = Screen.monitor_size
            credits_scene.previous_size = Screen.monitor_size
        main_scene.resize_scene(Screen.screen.get_size())
        quest_scene.resize_scene(Screen.screen.get_size())
        marketplace_scene.resize_scene(Screen.screen.get_size())
        settings_scene.resize_scene(Screen.screen.get_size())
        credits_scene.resize_scene(Screen.screen.get_size())
    
    for event in game_events:
        marketplace_scene = evaluate_game_event(event, marketplace_scene)
    game_events.clear()
    
    timers_for_factories, main_scene.crafting_amounts = check_for_automatic_crafting(timers_for_factories, main_scene.crafting_amounts)
    main_scene.crafting_amounts = evaluate_crafting_timers(main_scene.crafting_amounts)
    if active_scene == Scene.main:
        main_scene.update(dt, events)
        active_scene = main_scene.get_active_scene()
        quest_scene.set_active_scene(active_scene)
        marketplace_scene.set_active_scene(active_scene)
        settings_scene.set_active_scene(active_scene)
        credits_scene.set_active_scene(active_scene)
        if active_scene == Scene.marketplace_scene:
            marketplace_scene.redraw()
    elif active_scene == Scene.quest_scene:
        quest_scene.update(dt, events)
        active_scene = quest_scene.get_active_scene()
        main_scene.set_active_scene(active_scene)
        marketplace_scene.set_active_scene(active_scene)
        settings_scene.set_active_scene(active_scene)
        credits_scene.set_active_scene(active_scene)
        if active_scene == Scene.marketplace_scene:
            marketplace_scene.redraw()
    elif active_scene == Scene.marketplace_scene:
        marketplace_scene.update(dt, events)
        active_scene = marketplace_scene.get_active_scene()
        main_scene.set_active_scene(active_scene)
        quest_scene.set_active_scene(active_scene)
        settings_scene.set_active_scene(active_scene)
        credits_scene.set_active_scene(active_scene)
    elif active_scene == Scene.settings_scene:
        settings_scene.update(dt, events)
        active_scene = settings_scene.get_active_scene()
        main_scene.set_active_scene(active_scene)
        quest_scene.set_active_scene(active_scene)
        marketplace_scene.set_active_scene(active_scene)
        credits_scene.set_active_scene(active_scene)
        if active_scene == Scene.marketplace_scene:
            marketplace_scene.redraw()
    elif active_scene == Scene.credits_scene:
        credits_scene.update(dt, events)
        active_scene = credits_scene.get_active_scene()
        main_scene.set_active_scene(active_scene)
        quest_scene.set_active_scene(active_scene)
        marketplace_scene.set_active_scene(active_scene)
        settings_scene.set_active_scene(active_scene)
        if active_scene == Scene.marketplace_scene:
            marketplace_scene.redraw()
    
    pygame.display.flip()
    clock.tick(120)
