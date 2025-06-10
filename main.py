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
    if active_scene == Scene.main:
        main_scene.update(dt, Screen.monitor_size)
        active_scene = main_scene.get_active_scene()
        quest_scene.set_active_scene(active_scene)
    elif active_scene == Scene.quest_scene:
        quest_scene.update(Screen.monitor_size)
        active_scene = quest_scene.get_active_scene()
        main_scene.set_active_scene(active_scene)
    pygame.display.update()
    clock.tick(120)