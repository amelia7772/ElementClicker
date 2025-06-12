import pygame
import os
import time

pygame.init()

from utilities import Screen

background_image = pygame.image.load(os.path.join("assets", "images" ,"background.png")).convert_alpha()

from main_game_screen.Elements import *
from utilities.scene import *
from main_game_screen.MainScene import *
from quest_screen.QuestScene import *
from utilities.SaveManager import *

Screen.screen.fill((194, 255, 250))

active_scene = Scene.main
save_manager = SaveManager()
save_manager.load_game(Screen.screen)

clock = pygame.time.Clock()
previous_time = time.time()

main_scene = MainScene(background_image)
quest_scene = QuestScene(background_image)

while True:
    dt = time.time() - previous_time
    previous_time = time.time()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            save_manager.save_game()
            exit()
        elif event.type == pygame.VIDEORESIZE and not pygame.display.is_fullscreen():
            main_scene.previous_size = main_scene.screen_size
            quest_scene.previous_size = quest_scene.screen_size
            if event.size[0] >= 800 and event.size[1] >= 400:
                Screen.screen = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            else:
                Screen.screen = pygame.display.set_mode((800,400), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            main_scene.resize_scene(Screen.screen.get_size())
            quest_scene.resize_scene(Screen.screen.get_size())
                
    if pygame.key.get_pressed()[pygame.key.key_code("f11")]:
        if not pygame.display.is_fullscreen():
            main_scene.previous_size = Screen.screen.get_size()
            quest_scene.previous_size = Screen.screen.get_size()
            Screen.screen = pygame.display.set_mode(pygame.display.list_modes()[0])
            Screen.screen = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
        else:
            Screen.screen = pygame.display.set_mode(main_scene.previous_size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            main_scene.previous_size = Screen.monitor_size
            quest_scene.previous_size = Screen.monitor_size
        main_scene.resize_scene(Screen.screen.get_size())
        quest_scene.resize_scene(Screen.screen.get_size())
        
    if active_scene == Scene.main:
        main_scene.update(dt, events)
        active_scene = main_scene.get_active_scene()
        quest_scene.set_active_scene(active_scene)
    elif active_scene == Scene.quest_scene:
        quest_scene.update(events)
        active_scene = quest_scene.get_active_scene()
        main_scene.set_active_scene(active_scene)
    pygame.display.update()
    clock.tick(120)
