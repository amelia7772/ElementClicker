import pygame
import os
from quest_screen.Quest import Quest
from main_game_screen.ElementType import *
from utilities.UiElement import UiElement

global quests
quests: list[Quest] = []
class QuestLine:
    
    def __init__(self):
        quests.append(Quest(0,"Start Your Adventure", os.path.join("assets", "images" ,"wood log 16-bit.png"), "Collect a wooden log", lambda elements, level: elements[int(ElementType.wood)].element_resource_amount >= 1, [], True))
        quests.append(Quest(1,"you really hate your hands, don't you?", os.path.join("assets", "images" ,"rock.png"), "Collect 15 rocks", lambda elements, level: elements[int(ElementType.rock)].element_resource_amount >= 15, [quests[0]]))
        quests.append(Quest(2,"burn your enemies with the fires of your passion!!\nor make smores, your choice really", os.path.join("assets", "images" ,"fire 16-bit.png"), "Collect a 9 fires", lambda elements, level: elements[int(ElementType.fire)].element_resource_amount >= 9, [quests[0]]))
        quests.append(Quest(3,"The Iron Age", os.path.join("assets", "images" ,"iron ingot 16-bit.png"), "Collect an iron bar", lambda elements, level: elements[int(ElementType.iron)].element_resource_amount >= 1, [quests[1], quests[2]]))
        self.vertical_margin = 20
        self.horizontal_margin = 100
        self.position_offset = (0,0)
        self.arrows_size = (4, 12, 8)
        self.calculate_quests_positions_in_the_quest_line()
        self.set_position((200,125))
    
    def set_position(self, new_position: tuple[int, int]):
        for i in range(0, len(self.quests_positions)):
            self.quests_positions[i] = (self.quests_positions[i][0] - self.position_offset[0], self.quests_positions[i][1] - self.position_offset[1])
        self.position_offset = new_position
        for i in range(0, len(self.quests_positions)):
            self.quests_positions[i] = (self.quests_positions[i][0] + self.position_offset[0], self.quests_positions[i][1] + self.position_offset[1])
    
    def resize_questline(self, change_in_width: float, change_in_height: float):
        for i in range(0, len(quests)):
            quests[i].quest_ui_icon.resize_ui_element(change_in_width, change_in_height)
        self.arrows_size = (self.arrows_size[0] * change_in_height, self.arrows_size[1] * change_in_width, self.arrows_size[2] * change_in_width)
        self.vertical_margin *= change_in_height
        self.horizontal_margin *= change_in_width
        self.position_offset = (self.position_offset[0] * change_in_width, self.position_offset[1] * change_in_height)
        self.calculate_quests_positions_in_the_quest_line()
        
    def calculate_quests_positions_in_the_quest_line(self):
        self.quests_positions: list[tuple[int, int]] = []
        previous_position_offset = self.position_offset
        self.position_offset = (0,0)
        last_parent_quest = -1
        previous_last_parent_quest = last_parent_quest
        number_of_quests_in_current_column = 0
        x, y = 0, 0
        for i in range(0, len(quests)):
            previous_last_parent_quest = last_parent_quest
            if len(quests[i].parent_quests) > 0:
                for parent_quest in quests[i].parent_quests:
                    last_parent_quest = max(last_parent_quest, parent_quest.id)
            if (last_parent_quest > previous_last_parent_quest) or (i == (len(quests) - 1)):
                if number_of_quests_in_current_column % 2 == 0:
                    y += self.vertical_margin / 2
                    y += (number_of_quests_in_current_column / 2) * quests[i].quest_ui_icon.images[0].get_height()
                    y += ((number_of_quests_in_current_column / 2) - 1) * self.vertical_margin
                    self.quests_positions.append((x,y))
                else:
                    y += quests[i].quest_ui_icon.images[0].get_height() / 2
                    y += (number_of_quests_in_current_column // 2) * quests[i].quest_ui_icon.images[0].get_height()
                    y += (number_of_quests_in_current_column // 2) * self.vertical_margin
                    self.quests_positions.append((x,y))
                    
                for n in range(1, number_of_quests_in_current_column):
                    y -= quests[i].quest_ui_icon.images[0].get_height()
                    y -= self.vertical_margin
                    self.quests_positions.append((x,y))
                number_of_quests_in_current_column = 0
                y = 0
                x += quests[i].quest_ui_icon.images[0].get_width()
                x += self.horizontal_margin
            if (last_parent_quest > previous_last_parent_quest) and (i == (len(quests) - 1)):
                y += quests[i].quest_ui_icon.images[0].get_height() / 2
                y += (number_of_quests_in_current_column // 2) * quests[i].quest_ui_icon.images[0].get_height()
                y += (number_of_quests_in_current_column // 2) * self.vertical_margin
                self.quests_positions.append((x,y))
            number_of_quests_in_current_column += 1
        self.set_position(previous_position_offset)
    
    def set_quest_completed(self, quest_id: int, is_completed: bool):
        quests[quest_id].is_completed = is_completed
        if is_completed:
            quests[quest_id].quest_ui_icon.set_background(quests[quest_id]._completed_quest_background)
        else:
            quests[quest_id].quest_ui_icon.set_background(quests[quest_id]._uncompleted_quest_background)
        for i in range(0,len(quests)):
            for parent_quest in quests[i].parent_quests:
                if parent_quest.id == quest_id:
                    quests[i].is_available = is_completed
                    quests[i].quest_ui_icon.set_quest_available(is_completed)
                    break
    
    #function made by u/plastic_astronomer on reddit
    def draw_arrow(self, surface: pygame.Surface, start: pygame.Vector2, end: pygame.Vector2, color: pygame.Color, body_width: int = 2, head_width: int = 4, head_height: int = 2):
        arrow = start - end
        angle = arrow.angle_to(pygame.Vector2(0, -1))
        body_length = arrow.length() - head_height

        # Create the triangle head around the origin
        head_verts = [
            pygame.Vector2(0, head_height / 2),  # Center
            pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
            pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
        ]
        # Rotate and translate the head into place
        translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
        for i in range(len(head_verts)):
            head_verts[i].rotate_ip(-angle)
            head_verts[i] += translation
            head_verts[i] += start

        pygame.draw.polygon(surface, color, head_verts)

        # Stop weird shapes when the arrow is shorter than arrow head
        if arrow.length() >= head_height:
            # Calculate the body rect, rotate and translate into place
            body_verts = [
                pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
                pygame.Vector2(body_width / 2, body_length / 2),  # Topright
                pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
                pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
            ]
            translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
            for i in range(len(body_verts)):
                body_verts[i].rotate_ip(-angle)
                body_verts[i] += translation
                body_verts[i] += start

            pygame.draw.polygon(surface, color, body_verts)    
            
    def draw(self, screen: pygame.Surface):
        for i in range(0,len(quests)):
            center_position_of_this_quest: pygame.Vector2 = pygame.Vector2(self.quests_positions[i][0], self.quests_positions[i][1] + (quests[i].quest_ui_icon.images[0].get_height() / 2))
            arrow_color = pygame.Color(0,0,0)
            if quests[i].is_completed:
                arrow_color = pygame.Color(0,255,0)
            elif quests[i].is_available:
                arrow_color = pygame.Color(255,255,255)
            for parent_quest in quests[i].parent_quests:
                center_position_of_parent_quest: pygame.Vector2 = pygame.Vector2(self.quests_positions[parent_quest.id][0] + (quests[parent_quest.id].quest_ui_icon.images[0].get_width() / 2), self.quests_positions[parent_quest.id][1] + (quests[parent_quest.id].quest_ui_icon.images[0].get_height() / 2))
                self.draw_arrow(screen, center_position_of_parent_quest, center_position_of_this_quest, arrow_color, self.arrows_size[0], self.arrows_size[1], self.arrows_size[2])
        
        for i in range(0,len(quests)):
            quests[i].quest_ui_icon.update_position(self.quests_positions[i])
            quests[i].quest_ui_icon.draw(screen)
            
global quest_line
quest_line = QuestLine()
