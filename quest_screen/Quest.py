import pygame
import os
from quest_screen.QuestUiIcon import QuestUiIcon

class Quest:
    def __init__(self, id: int, name: str, ui_icon_path: str, description: str, condition, parent_quests = [], is_available = False,is_rewarded = False, reward = None):
        self.id = id
        self.name = name
        self._uncompleted_quest_background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images" ,"quest background.png")).convert_alpha(), (65, 65))
        self.quest_ui_icon = QuestUiIcon(self._uncompleted_quest_background,pygame.transform.scale(pygame.image.load(ui_icon_path).convert_alpha(), (50,50)), (0,0), is_available)
        self._completed_quest_background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images" ,"completed quest background.png")).convert_alpha(), (65, 65))
        self.description = description
        self.condition = condition
        self.parent_quests = parent_quests
        self.is_available = is_available
        self.is_rewarded = is_rewarded
        self.reward = reward
        self.is_completed = False