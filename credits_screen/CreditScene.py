import pygame
import os
from utilities import Screen
from utilities.Scene import Scene
from utilities.UiElement import UiElement
from quest_screen.QuestButton import QuestButton
from marketplace_screen.MarketplaceButton import MarketplaceButton
from settings_screen.SettingsButton import SettingsButton
from credits_screen.CreditsButton import CreditsButton

class CreditsScene:
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        self.marketplace_button = MarketplaceButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"marketplace button icon.png")).convert_alpha())
        self.setting_buttons = SettingsButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"settings button icon.png")).convert_alpha())
        self.credits_buttons = CreditsButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"credits button icon.png")).convert_alpha())

        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)
        
        self.scroll_offset = 0.0
        
        self.scroll_initial_offset = self.scroll_offset
        
        self.scroll_acceleration = 0.0
        
        self.scroll_speed = 0.0
        
        self.scroll_target_height = 0.0
        
        self.is_mouse_wheel_moving = False
        
        self.redraw_scene()
        
        self.initial_bounding_box_height = float(self.how_to_play_title_rect.height + self.how_to_play_description_rect.height + self.credits_title_rect.height + self.credits_main_rect.height)
        
        self.active_scene = Scene.main
        
        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
    
    def update_scroll_offset(self, dt):
        self.scroll_acceleration = (30.0 * (float(Screen.screen.get_height()) / 400.0)) * ((self.scroll_initial_offset + ((self.scroll_target_height - self.scroll_initial_offset) / 2.0)) - self.scroll_offset)
        
        next_scroll_offset = self.scroll_offset + ((0.5 * self.scroll_acceleration * (dt * dt)) + (self.scroll_speed * dt))
        
        if (((self.scroll_target_height - self.scroll_initial_offset) > 0 and (next_scroll_offset <= self.scroll_target_height))\
            or ((self.scroll_target_height - self.scroll_initial_offset) < 0 and (next_scroll_offset >= self.scroll_target_height))):
        
            self.scroll_offset = next_scroll_offset
        
            self.scroll_speed += self.scroll_acceleration * dt
        elif (not pygame.key.get_pressed()[pygame.key.key_code("w")]) and (not pygame.key.get_pressed()[pygame.key.key_code("s")]):
            self.scroll_speed = 0.0
            self.scroll_offset = self.scroll_target_height
            self.scroll_initial_offset = self.scroll_offset
    
    def update(self, dt, events):
        Screen.screen.fill((46, 46, 46))
        
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.is_mouse_wheel_moving = True
                ratio_of_stretch_of_scrolling_surface = (float(self.how_to_play_title_rect.height + self.how_to_play_description_rect.height + self.credits_title_rect.height + self.credits_main_rect.height) / self.initial_bounding_box_height)
                self.scroll_initial_offset = self.scroll_offset
                self.scroll_target_height = min(0.0, max((float(Screen.screen.get_height()) * 0.9) - float(self.how_to_play_title_rect.height + self.how_to_play_description_rect.height + self.credits_title_rect.height + self.credits_main_rect.height), self.scroll_target_height + float((event.y) * 20.0 * ratio_of_stretch_of_scrolling_surface)))
                if event.y > 0:
                    self.scroll_acceleration = min(300.0, self.scroll_acceleration + (30.0))
                else:
                    self.scroll_acceleration = max(-300.0, self.scroll_acceleration - (30.0))
            else:
                self.is_mouse_wheel_moving = False
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.setting_buttons.is_highlighted = self.setting_buttons._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.credits_buttons.is_highlighted = self.credits_buttons._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
                if self.marketplace_button.is_highlighted and not self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(True)
                if self.setting_buttons.is_highlighted and not self.setting_buttons.is_ui_element_pressed():
                    self.setting_buttons.set_ui_element_is_pressed(True)
                if self.credits_buttons.is_highlighted and not self.credits_buttons.is_ui_element_pressed():
                    self.credits_buttons.set_ui_element_is_pressed(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.quest_scene
                if self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.marketplace_scene
                if self.setting_buttons.is_ui_element_pressed():
                    self.setting_buttons.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.settings_scene
                if self.credits_buttons.is_ui_element_pressed():
                    self.credits_buttons.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.main
        
        if pygame.key.get_pressed()[pygame.key.key_code("w")]:
            ratio_of_stretch_of_scrolling_surface = (float(self.how_to_play_title_rect.height + self.how_to_play_description_rect.height + self.credits_title_rect.height + self.credits_main_rect.height) / self.initial_bounding_box_height)
            self.scroll_initial_offset = self.scroll_offset
            self.scroll_target_height = min(0.0, max((float(Screen.screen.get_height()) * 0.9) - float(self.how_to_play_title_rect.height + self.how_to_play_description_rect.height + self.credits_title_rect.height + self.credits_main_rect.height), self.scroll_target_height + (5.0 * ratio_of_stretch_of_scrolling_surface)))
            self.scroll_acceleration = min(300.0, self.scroll_acceleration + (30.0))
        if pygame.key.get_pressed()[pygame.key.key_code("s")]:
            ratio_of_stretch_of_scrolling_surface = (float(self.how_to_play_title_rect.height + self.how_to_play_description_rect.height + self.credits_title_rect.height + self.credits_main_rect.height) / self.initial_bounding_box_height)
            self.scroll_initial_offset = self.scroll_offset
            self.scroll_target_height = min(0.0, max((float(Screen.screen.get_height()) * 0.9) - float(self.how_to_play_title_rect.height + self.how_to_play_description_rect.height + self.credits_title_rect.height + self.credits_main_rect.height), self.scroll_target_height - (5.0 * ratio_of_stretch_of_scrolling_surface)))
            self.scroll_acceleration = max(-300.0, self.scroll_acceleration - (30.0))
        
        self.update_scroll_offset(dt)
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        Screen.screen.blit(self.shadow_bounding_surface, self.shadow_bounding_box)
        Screen.screen.blit(self.how_to_play_title_surface, (self.how_to_play_title_rect.left, self.how_to_play_title_rect.top + int(self.scroll_offset)))
        Screen.screen.blit(self.how_to_play_description_surface, (self.how_to_play_description_rect.left, self.how_to_play_description_rect.top + int(self.scroll_offset)))
        Screen.screen.blit(self.credits_title_surface, (self.credits_title_rect.left, self.credits_title_rect.top + int(self.scroll_offset)))
        Screen.screen.blit(self.credits_main_surface, (self.credits_main_rect.left, self.credits_main_rect.top + int(self.scroll_offset)))
        
        self.quest_button.draw(Screen.screen)
        self.marketplace_button.draw(Screen.screen)
        self.setting_buttons.draw(Screen.screen)
        self.credits_buttons.draw(Screen.screen)
        
    
    def set_active_scene(self, active_scene: Scene):
        if self.active_scene != active_scene:
            mouse_position = pygame.mouse.get_pos()
            self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.setting_buttons.is_highlighted = self.setting_buttons._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.credits_buttons.is_highlighted = self.credits_buttons._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.active_scene = active_scene
    
    def get_active_scene(self):
        return self.active_scene
    
    def redraw_scene(self):
        self.shadow_bounding_box = pygame.Rect(0.0, 0.0, float(Screen.screen.get_width()) / 1.5, float(Screen.screen.get_height()))
        self.shadow_bounding_surface = pygame.Surface(self.shadow_bounding_box.size, pygame.SRCALPHA)
        self.shadow_bounding_surface.fill((0,0,0,102))
        
        self.how_to_play_title_text = "How To Play"
        self.how_to_play_description_text = \
"""1) mouse scroll to scroll up and down here.
alternatively you can press w to scroll up
or s to scroll down

2) use the WASD keys
or left click and drag the background\nto move the camera.

3) mouse scroll to zoom in/out.

4) left click an element
to collect/craft it.

5) right click an element
to see its explanation message.

6) to the left bottom of your screen
is the marketplace button,
press it to enter/exit
from the marketplace.

7) within the marketplace:
*)mouse scroll to scroll down or up.
*) w to scroll up.
*) s to scroll down.
*) the button to the left
of the money amount
is the transaction amount button,
press it to change the amount of elements
bought/sold per transaction.
*) the button to the right
of the price amount
is the transaction type button,
press to change transaction type
to sell or buy.
*) to the right of each element
is the transaction button,
press to buy/sell the element.

8) to the right bottom of your screen
is the quest tree button,
press it to enter/exit
from the quest tree.

9) in the quest tree:
*) use the WASD keys
or left click and drag the background
to move the camera.
*) mouse scroll to zoom in/out.
*) left click any quest
to see its explanation message.
10) to the right top of your screen
is the settings button,
press it to enter/exit
from the settings page.

11) in the settings page:
*) mouse scroll to scroll up or down.
*) w to scroll up.
*) s to scroll down.
*) left click any triangle
facing left, to decrease the number
of the setting/go to
the previous option of that setting.
*) left click any triangle
facing right, to increse the number
of the setting/go to
the previous option of that setting."""
        self.credits_title_text = "Credits"
        self.credits_main_text = \
"""Game developed by amelia
in the programming language Python,
using the Pygame library.

Assets generated by AI (Copilot)."""
        self.how_to_play_title_surface = pygame.Surface((int(float(self.shadow_bounding_box.width) * 0.9), self.shadow_bounding_box.height), pygame.SRCALPHA)
        
        self.how_to_play_titles_bounding_box = self.blit_center_aligned_text(self.how_to_play_title_surface, self.how_to_play_title_text, (0, 0), self.pixelated_font)
        self.how_to_play_description_surface = self.render_center_aligned_text(self.how_to_play_description_text, self.pixelated_font)
        
        self.credits_title_surface = pygame.Surface((int(float(self.shadow_bounding_box.width) * 0.9), self.how_to_play_titles_bounding_box.height), pygame.SRCALPHA)
        
        self.credits_titles_bounding_box = self.blit_center_aligned_text(self.credits_title_surface, self.credits_title_text, (0, 0), self.pixelated_font)
        self.credits_title_surface = self.credits_title_surface.subsurface((0,0), self.credits_titles_bounding_box.size)
        self.credits_main_surface = self.render_center_aligned_text(self.credits_main_text, self.pixelated_font)
        
        text_ui_element = UiElement([self.how_to_play_description_surface], [(float(self.how_to_play_description_surface.get_width()), float(self.how_to_play_description_surface.get_height()))])
        text_ui_element.resize_ui_element(float(self.how_to_play_title_surface.get_width()) / float(self.how_to_play_description_surface.get_width()), 1.0)
        self.how_to_play_description_surface = text_ui_element.images[0].copy()
        
        text_ui_element = UiElement([self.credits_main_surface], [(float(self.credits_main_surface.get_width()), float(self.credits_main_surface.get_height()))])
        text_ui_element.resize_ui_element(float(self.how_to_play_title_surface.get_width()) / float(self.credits_main_surface.get_width()), 1.0)
        self.credits_main_surface = text_ui_element.images[0].copy()
        
        self.reposition_scene()
    
    def blit_center_aligned_text(self, surface: pygame.Surface, text: str, pos: tuple[int, int], font: pygame.font.Font, color=pygame.Color("White")) -> pygame.Rect:
        most_wide_lines_width = -1
        most_high_lines_height = -1
        combined_height_of_text = 0
        
        for line in text.splitlines():
            size_of_line = font.size(line)
            most_wide_lines_width = max(most_wide_lines_width, size_of_line[0])
            most_high_lines_height = max(most_high_lines_height, size_of_line[1])
            combined_height_of_text += size_of_line[1]
        texts_bounding_box = pygame.Rect(0.0, 0.0, most_wide_lines_width, most_high_lines_height)
        
        surface_the_same_size_as_text = pygame.Surface((most_wide_lines_width, combined_height_of_text), pygame.SRCALPHA)
        
        y = 0.0
        for line in text.splitlines():
            size_of_line = font.size(line)
            lines_bounding_box = pygame.Rect(0.0, y, float(size_of_line[0]), float(size_of_line[1]))
            lines_bounding_box.centerx = texts_bounding_box.centerx
            surface_the_same_size_as_text.blit(font.render(line, False, color).convert_alpha(), lines_bounding_box)
            y += float(size_of_line[1])
        
        text_ui_element = UiElement([surface_the_same_size_as_text], [(float(most_wide_lines_width), float(combined_height_of_text))])
        text_ui_element.resize_ui_element(float(surface.get_width()) / float(most_wide_lines_width), float(surface.get_height()) / float(combined_height_of_text))
    
        text_ui_element.draw(surface, [pos])
        return pygame.Rect(float(pos[0]), float(pos[1]), text_ui_element.sizes[0][0], text_ui_element.sizes[0][1])
    
    def render_center_aligned_text(self, text: str, font: pygame.font.Font, color=pygame.Color("White")):
        most_wide_lines_width = -1
        most_high_lines_height = -1
        combined_height_of_text = 0
        
        for line in text.splitlines():
            size_of_line = font.size(line)
            most_wide_lines_width = max(most_wide_lines_width, size_of_line[0])
            most_high_lines_height = max(most_high_lines_height, size_of_line[1])
            combined_height_of_text += size_of_line[1]
        texts_bounding_box = pygame.Rect(0.0, 0.0, most_wide_lines_width, most_high_lines_height)
        
        surface_the_same_size_as_text = pygame.Surface((most_wide_lines_width, combined_height_of_text), pygame.SRCALPHA)
        
        y = 0.0
        for line in text.splitlines():
            size_of_line = font.size(line)
            lines_bounding_box = pygame.Rect(0.0, y, float(size_of_line[0]), float(size_of_line[1]))
            lines_bounding_box.centerx = texts_bounding_box.centerx
            surface_the_same_size_as_text.blit(font.render(line, False, color).convert_alpha(), lines_bounding_box)
            y += float(size_of_line[1])
        
        return surface_the_same_size_as_text
    
    def reposition_scene(self):
        self.shadow_bounding_box.center = Screen.screen.get_rect().center
        self.how_to_play_title_rect = pygame.Rect(0.0, 0.0, float(self.how_to_play_titles_bounding_box.width), float(self.how_to_play_titles_bounding_box.height))
        self.how_to_play_title_rect.centerx = self.shadow_bounding_box.centerx
        self.how_to_play_description_rect = pygame.Rect(0.0, 0.0, float(self.how_to_play_description_surface.get_width()), float(self.how_to_play_description_surface.get_height()))
        self.how_to_play_description_rect.top = self.how_to_play_titles_bounding_box.bottom
        self.how_to_play_description_rect.centerx = self.shadow_bounding_box.centerx
        self.credits_title_rect = pygame.Rect(0.0, 0.0, float(self.credits_title_surface.get_width()), float(self.credits_title_surface.get_height()))
        self.credits_title_rect.top = self.how_to_play_description_rect.bottom
        self.credits_title_rect.centerx = self.shadow_bounding_box.centerx
        self.credits_main_rect = pygame.Rect(0.0, 0.0, float(self.credits_main_surface.get_width()), float(self.credits_main_surface.get_height()))
        self.credits_main_rect.top = self.credits_title_rect.bottom
        self.credits_main_rect.centerx = self.shadow_bounding_box.centerx
        
    def resize_scene(self, new_size: tuple[int, int]):
        self.quest_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.marketplace_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.setting_buttons.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.credits_buttons.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        
        self.redraw_scene()
        
        self.screen_size = Screen.screen.get_size()
