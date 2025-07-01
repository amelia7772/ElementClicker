import pygame
import struct
from xpbar.XpBar import *
from main_game_screen.Elements import *
from quest_screen.QuestLine import *
from marketplace_screen import Money
class SaveManager:
    def __init__(self):
        pass
    
    def save_game(self):
        save_file = open("save.bin", 'wb')
        buffer = bytes()
        for element in elements.elements:
            buffer += struct.pack('<1i', element.element_resource_amount)
        buffer += struct.pack('<2i', xp_bar.xp_amount, xp_bar.level)
        for element in elements.elements:
            buffer += struct.pack('<1b', element.is_available)
        for quest in quests:
            buffer += struct.pack('<1b', quest.is_completed)
        buffer += struct.pack('<d', Money.money)
        print(buffer)
        if save_file.writable():
            save_file.write(buffer)
        save_file.close()
    
    def load_game(self, screen:pygame.Surface):
        try:
            save_file = open("save.bin", 'rb')
            if save_file.readable():
                print(((len(elements.elements) + 2) * 4) + len(elements.elements) + len(quests) + 8)
                buffer = save_file.read(((len(elements.elements) + 2) * 4) + len(elements.elements) + len(quests) + 8)
                resources = struct.unpack(f'<{len(elements.elements) + 2}i{len(elements.elements) + len(quests)}bd', buffer)
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
                for quest in quests:
                    quest_line.set_quest_completed(quest.id, resources[counter])
                    counter += 1
            Money.money = resources[counter]
            save_file.close()
        except FileExistsError:
            print("FileExistsError")
        except FileNotFoundError:
            print("FileNotFoundError")
        except struct.error:
            print("struct.error")
