import pygame
import os
from quest_screen.Quest import Quest
from main_game_screen.ElementType import *
from utilities import Screen

global quests
quests: list[Quest] = []
class QuestLine:
    
    def __init__(self):
        quests.append(Quest(len(quests),"Start Your Adventure", os.path.join("assets", "images" ,"wood log 16-bit.png"), "Collect a wooden log", lambda elements, level: elements[int(ElementType.wood)].element_resource_amount >= 1, [], True))
        quests.append(Quest(len(quests),"wait, this clicker game has xp?", os.path.join("assets", "images" ,"XP quest icon.png"), "collect 10 xp (you'll level up to level 1)", lambda elements, level: level >= 1, [quests[0]]))
        quests.append(Quest(len(quests),"you really hate your hands, don't you?", os.path.join("assets", "images" ,"rock.png"), "Collect 15 rocks", lambda elements, level: elements[int(ElementType.rock)].element_resource_amount >= 15, [quests[1]]))
        quests.append(Quest(len(quests),"burn your enemies with the fires of your passion!!\nor make smores, your choice really", os.path.join("assets", "images" ,"fire 16-bit.png"), "Collect 9 fires", lambda elements, level: elements[int(ElementType.fire)].element_resource_amount >= 9, [quests[1]]))
        quests.append(Quest(len(quests),"The Iron Age", os.path.join("assets", "images" ,"iron ingot 16-bit.png"), "Collect an iron bar", lambda elements, level: elements[int(ElementType.iron)].element_resource_amount >= 1, [quests[2], quests[3]]))
        quests.append(Quest(len(quests),"yes, an iron pickaxe can break obsedien", os.path.join("assets", "images" ,"iron pickaxe.png"), "Collect an iron pickaxe", lambda elements, level: elements[int(ElementType.iron_pickaxe)].element_resource_amount >= 1, [quests[4]]))
        quests.append(Quest(len(quests),"may contain traces of iron, wood, and... cookies?", os.path.join("assets", "images" ,"iron hammer.png"), "Collect an iron hammer", lambda elements, level: elements[int(ElementType.iron_hammer)].element_resource_amount >= 1, [quests[4]]))
        quests.append(Quest(len(quests),"steve would be sooo disappointed", os.path.join("assets", "images" ,"iron axe.png"), "Collect an iron axe", lambda elements, level: elements[int(ElementType.iron_axe)].element_resource_amount >= 1, [quests[4]]))
        quests.append(Quest(len(quests),"come on, everyone loves hoes!", os.path.join("assets", "images" ,"iron hoe.png"), "Collect an iron hoe", lambda elements, level: elements[int(ElementType.iron_hoe)].element_resource_amount >= 1, [quests[4]]))
        quests.append(Quest(len(quests),"give it to a child...\nfor the sand pit in kindergarten of course", os.path.join("assets", "images" ,"iron shovel.png"), "Collect an iron shovel", lambda elements, level: elements[int(ElementType.iron_shovel)].element_resource_amount >= 1, [quests[4]]))
        quests.append(Quest(len(quests),"Quick! someone said game of thrones is bad!", os.path.join("assets", "images" ,"iron pitchfork.png"), "Collect an iron pitchfork", lambda elements, level: elements[int(ElementType.iron_pitchfork)].element_resource_amount >= 1, [quests[4]]))
        quests.append(Quest(len(quests),"no actually, it's not just for grim reaper cosplay", os.path.join("assets", "images" ,"iron sickle scythe.png"), "Collect an iron sickle scythe", lambda elements, level: elements[int(ElementType.iron_sickle_scythe)].element_resource_amount >= 1, [quests[4]]))
        quests.append(Quest(len(quests),"... well, at least you have a pickaxe", os.path.join("assets", "images" ,"rock.png"), "Collect 100 rocks (the more pickaxes you have the faster breaking rocks is)", lambda elements, level: elements[int(ElementType.rock)].element_resource_amount >= 100, [quests[5]]))
        quests.append(Quest(len(quests),"the mountains are made of pebbles", os.path.join("assets", "images" ,"gravil.png"), "Collect a batch of gravil", lambda elements, level: elements[int(ElementType.gravil)].element_resource_amount >= 1, [quests[6]]))
        quests.append(Quest(len(quests),"the start of the gold hunt!", os.path.join("assets", "images" ,"sand.png"), "Collect a batch of sand", lambda elements, level: elements[int(ElementType.sand)].element_resource_amount >= 1, [quests[13]]))
        
        self.vertical_margin = 20
        self.horizontal_margin = 100
        self.position_offset = (0,0)
        self.arrows_size = (4, 12, 8)
        self.calculate_quests_positions_in_the_quest_line()
        self.set_position((200,125))
        
        self._displayed_quest_descriptions_quest_index = -1 #-1 is no displayed quest description
        self._quest_description_background = pygame.image.load(os.path.join("assets", "images" ,"quest explanation background.png")).convert_alpha()
        self._quest_description_background_original = self._quest_description_background.copy()
        self._ratio_of_change_in_width = 1.0
        self._ratio_of_change_in_height = 1.0
        self._pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)
        self._quest_description_text = pygame.Surface((self._quest_description_background.get_size()[0] - (self._quest_description_background.get_size()[0] / 10), self._quest_description_background.get_size()[1]), pygame.SRCALPHA)
    
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
        self._ratio_of_change_in_width *= change_in_width
        self._ratio_of_change_in_height *= change_in_height
        self.position_offset = (self.position_offset[0] * change_in_width, self.position_offset[1] * change_in_height)
        self.display_quest_explanation_message(self._displayed_quest_descriptions_quest_index)
        self.calculate_quests_positions_in_the_quest_line()
        
    def calculate_quests_positions_in_the_quest_line(self):
        quests_column_row_position: list[list[int]] = [[]]
        for i in range(0, len(quests)):
            if len(quests[i].parent_quests) == 0:
                quests_column_row_position[0].append(quests[i].id)
                continue
            possible_columns: list[int] = []
            for x in range(0, len(quests[i].parent_quests)):
                for j in range(0,len(quests_column_row_position)):
                    for k in range(0,len(quests_column_row_position[j])):
                        if quests_column_row_position[j][k] == quests[i].parent_quests[x].id:
                            possible_columns.append(j + 1)
            current_column = max(possible_columns)
            if current_column < len(quests_column_row_position):
                quests_column_row_position[current_column].append(quests[i].id)
            else:
                quests_column_row_position.append([quests[i].id])
        
        self.quests_positions: list[tuple[int, int]] = []
        previous_position_offset = self.position_offset
        self.position_offset = (0,0)
        x, y = 0, 0
        for i in range(0, len(quests_column_row_position)):
            if (len(quests_column_row_position[i]) % 2) == 0:
                y += self.vertical_margin / 2
                y += (self.vertical_margin * ((len(quests_column_row_position[i]) // 2) - 1))
                y += quests[0].quest_ui_icon.images[0].get_height() * (len(quests_column_row_position[i]) // 2)
            else:
                y += quests[0].quest_ui_icon.images[0].get_height() / 2
                y += (self.vertical_margin * (len(quests_column_row_position[i]) // 2))
                y += quests[0].quest_ui_icon.images[0].get_height() * (len(quests_column_row_position[i]) // 2)
            for j in range(0,len(quests_column_row_position[i])):
                self.quests_positions.append((x,y))
                y -= quests[0].quest_ui_icon.images[0].get_height()
                y -= self.vertical_margin
            y = 0
            x += quests[0].quest_ui_icon.images[0].get_width()
            x += self.horizontal_margin
        self.set_position(previous_position_offset)
    
    def set_quest_completed(self, quest_id: int, is_completed: bool):
        quests[quest_id].is_completed = is_completed
        previous_background_size = quests[quest_id].quest_ui_icon.images[0].get_size()
        if is_completed:
            quests[quest_id].quest_ui_icon.set_background(quests[quest_id]._completed_quest_background)
        else:
            quests[quest_id].quest_ui_icon.set_background(quests[quest_id]._uncompleted_quest_background)
        quests[quest_id].quest_ui_icon.images[0] = pygame.transform.scale(quests[quest_id].quest_ui_icon.images[0], previous_background_size)
        for i in range(0,len(quests)):
            for parent_quest in quests[i].parent_quests:
                if parent_quest.id == quest_id:
                    quests[i].is_available = is_completed
                    previous_ui_icon_image_size = quests[i].quest_ui_icon.images[1].get_size()
                    quests[i].quest_ui_icon.set_quest_available(is_completed)
                    quests[i].quest_ui_icon.images[1] = pygame.transform.scale(quests[i].quest_ui_icon.images[1], previous_ui_icon_image_size)
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
            
    #from: https://stackoverflow.com/a/42015712
    def blit_text(self, surface: pygame.Surface, text: str, pos: tuple[float, float], font: pygame.font.Font, color=pygame.Color("White")):
        words = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0]
        max_width = surface.get_size()[0]
        word_width, word_height = (0,0)
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, False, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height
        return y
    
    def __get_the_length_of_longest_line_in_text__(self, text: str):
        length_of_longest_line = 0
        length_of_current_line = 0
        for character in text:
            if character == '\n':
                length_of_longest_line = max(length_of_longest_line, length_of_current_line)
                length_of_current_line = 0
            else:
                length_of_current_line += 1
        return length_of_longest_line
    
    def display_quest_explanation_message(self, quest_id: int):
        self._displayed_quest_descriptions_quest_index = quest_id
        
        longest_line_in_quest_description = max(self.__get_the_length_of_longest_line_in_text__(quests[quest_id].name), self.__get_the_length_of_longest_line_in_text__(quests[quest_id].description))
        font_size = 50.0 * min(self._ratio_of_change_in_width, self._ratio_of_change_in_height)
        for i in range(0, longest_line_in_quest_description, 10):
            font_size *= 0.975
        self._pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), int(font_size))
        
        self._quest_description_text = pygame.Surface(((self._quest_description_background.get_size()[0] - (self._quest_description_background.get_size()[0] / 10)) * 1.5, Screen.screen.get_height() * 1.5), pygame.SRCALPHA)
        explanation_text_surface = pygame.Surface(self._quest_description_text.get_size(), pygame.SRCALPHA)
        quest_explanation_text_height = self.blit_text(self._quest_description_text, quests[quest_id].name, (0,0), self._pixelated_font)
        explanation_text_surface_height = self.blit_text(explanation_text_surface, quests[quest_id].description, (0,0), self._pixelated_font)
        explanation_text_surface = pygame.transform.scale_by(explanation_text_surface, 0.75)
        self._quest_description_text.blit(explanation_text_surface,(0,quest_explanation_text_height + (quest_explanation_text_height / 10)))
        quest_explanation_text_height += explanation_text_surface_height
        self._quest_description_background = pygame.transform.scale(self._quest_description_background_original, (300, max(quest_explanation_text_height + (quest_explanation_text_height / 10), 300)))
        if not (self._ratio_of_change_in_width == 1.0 and self._ratio_of_change_in_height == 1.0):
            self._quest_description_background = pygame.transform.scale_by(self._quest_description_background, (self._ratio_of_change_in_width, self._ratio_of_change_in_height))
        self._quest_description_text = pygame.transform.scale(self._quest_description_text, (int(self._quest_description_background.get_width() * (8.0/10.0)), int( int(self._quest_description_background.get_width() * (8.0/10.0)) * (float(self._quest_description_text.get_height()) / float(self._quest_description_text.get_width())))))
            
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
        
        if self._displayed_quest_descriptions_quest_index >= 0:
            defocus_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            defocus_surface.fill(pygame.Color(0, 0, 0, 128))
            screen.blit(defocus_surface, (0,0))
            screen.blit(self._quest_description_background, ((screen.get_width() / 2) - (self._quest_description_background.get_width() / 2), (screen.get_height() / 2) - (self._quest_description_background.get_height() / 2)))
            screen.blit(self._quest_description_text, ((screen.get_width() / 2) - (self._quest_description_background.get_width() / 2) + (self._quest_description_background.get_width() / 10), (screen.get_height() / 2) - (self._quest_description_background.get_height() / 2) + (self._quest_description_background.get_height() / 10)))
            
global quest_line
quest_line = QuestLine()
