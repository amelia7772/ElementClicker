import pygame
import os
from utilities import Screen
from utilities.Scene import Scene
from quest_screen.QuestButton import QuestButton
from marketplace_screen.MarketplaceButton import MarketplaceButton
from utilities.UiElement import UiElement
from marketplace_screen import Money
from utilities.BigNumberMap import order_of_magnitude_to_symbol_map

class MarketplaceScene:
    
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        self.marketplace_button = MarketplaceButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"marketplace button icon.png")).convert_alpha())
        
        shadow_bounding_box_surface = pygame.Surface((int(float(Screen.screen.get_width()) * 0.6), Screen.screen.get_height() * 2),pygame.SRCALPHA)
        
        shadow_bounding_box_surface.fill((0,0,0,int(0.4 * 255)))
        
        self.shadow_bounding_box = UiElement([shadow_bounding_box_surface], [(float(shadow_bounding_box_surface.get_width()), float(shadow_bounding_box_surface.get_height()))])
        
        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)
        
        self.position_offset = (0.0,0.0)
        
        self.shadow_bounding_box_rect = pygame.Rect((float(Screen.screen.get_width()) / 2) - (0.5 * float(shadow_bounding_box_surface.get_width())) + self.position_offset[0], self.position_offset[1],float(shadow_bounding_box_surface.get_width()), float(shadow_bounding_box_surface.get_height()))
        
        money_amount = Money.money
        
        order_of_magnitude_of_money_amount = self.__calculate_order_of_magnitude__(money_amount)
        if order_of_magnitude_of_money_amount >= 3:
            symbol = order_of_magnitude_to_symbol_map[order_of_magnitude_of_money_amount - (order_of_magnitude_of_money_amount % 3)]
            non_rounded_money_amount = float(money_amount) / (10.0 ** (order_of_magnitude_of_money_amount - (order_of_magnitude_of_money_amount % 3)))
            money_amount = round(non_rounded_money_amount, 2 - self.__calculate_order_of_magnitude__(int(non_rounded_money_amount)))
        
        money_amount_text_surface = self.pixelated_font.render(f'${money_amount}' + symbol,False,pygame.Color(0, 255, 0)).convert_alpha()
        
        self.money_amount_text = UiElement([money_amount_text_surface], [(float(money_amount_text_surface.get_width()), float(money_amount_text_surface.get_height()))])
        self.money_amount_text.resize_ui_element((float(self.shadow_bounding_box_rect.width) * (7.0 / 56.0)) / self.money_amount_text.sizes[0][0], (float(self.shadow_bounding_box_rect.height) * (7.0 / 56.0)) / self.money_amount_text.sizes[0][1])
        self.money_amount_text_rect = pygame.Rect(0.0,0.0, self.money_amount_text.sizes[0][0],self.money_amount_text.sizes[0][1])
        self.money_amount_text_rect.centerx = self.shadow_bounding_box_rect.centerx + int(self.position_offset[0])
        self.money_amount_text_rect.top = self.shadow_bounding_box_rect.top + int(self.position_offset[1])
        
        self.amount_per_transaction_option = 0
        
        self._amount_per_transaction_is_one__surface = pygame.image.load(os.path.join("assets", "images" ,"one element per transaction button icon.png")).convert_alpha()
        self._amount_per_transaction_is_ten__surface = pygame.image.load(os.path.join("assets", "images" ,"ten element per transaction button icon.png")).convert_alpha()
        self._amount_per_transaction_is_hundred__surface = pygame.image.load(os.path.join("assets", "images" ,"hundred element per transaction button icon.png")).convert_alpha()
        self._amount_per_transaction_is_max__surface = pygame.image.load(os.path.join("assets", "images" ,"max amount per transaction button icon.png")).convert_alpha()

        self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_one__surface], [(float(self._amount_per_transaction_is_one__surface.get_width()), float(self._amount_per_transaction_is_one__surface.get_height()))], True)
        self.amount_per_transaction_button.resize_ui_element(float(self.money_amount_text_rect.width) / float(self.amount_per_transaction_button.sizes[0][0]), float(self.money_amount_text_rect.height) / (0.75 * float(self.amount_per_transaction_button.sizes[0][1])))
        
        self.amount_per_transaction_button_rect = pygame.Rect(0.0, 0.0, self.amount_per_transaction_button.sizes[0][0], self.amount_per_transaction_button.sizes[0][1])
        self.amount_per_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) - ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)) + self.position_offset[0])
        self.amount_per_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)) + self.position_offset[1])
        
        self.is_type_of_transaction_sell = True
        
        self._type_of_transaction_is_sell__surface = pygame.image.load(os.path.join("assets", "images" ,"transaction type sell button icon.png")).convert_alpha()
        self._type_of_transaction_is_buy__surface = pygame.image.load(os.path.join("assets", "images" ,"transaction type buy button icon.png")).convert_alpha()
        
        self.type_of_transaction_button = UiElement([self._type_of_transaction_is_sell__surface], [(float(self._type_of_transaction_is_sell__surface.get_width()), float(self._type_of_transaction_is_sell__surface.get_height()))], True)
        self.type_of_transaction_button.resize_ui_element(float(self.money_amount_text_rect.width) / float(self.type_of_transaction_button.sizes[0][0]), float(self.money_amount_text_rect.height) / (0.75 * float(self.type_of_transaction_button.sizes[0][1])))
        
        self.type_of_transaction_button_rect = pygame.Rect(0.0, 0.0, self.type_of_transaction_button.sizes[0][0], self.type_of_transaction_button.sizes[0][1])
        self.type_of_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) + ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)) + self.position_offset[0])
        self.type_of_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)) + self.position_offset[1])
        
        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        
        self.active_scene = Scene.main
    
    def set_amount_per_transaction_option(self, amount_per_transaction_option: int):
        if self.amount_per_transaction_option != amount_per_transaction_option:
            self.amount_per_transaction_option = amount_per_transaction_option
            
            if self.amount_per_transaction_option == 0:
                self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_one__surface], [(float(self._amount_per_transaction_is_one__surface.get_width()), float(self._amount_per_transaction_is_one__surface.get_height()))], True)
            elif self.amount_per_transaction_option == 1:
                self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_ten__surface], [(float(self._amount_per_transaction_is_ten__surface.get_width()), float(self._amount_per_transaction_is_ten__surface.get_height()))], True)
            elif self.amount_per_transaction_option == 2:
                self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_hundred__surface], [(float(self._amount_per_transaction_is_hundred__surface.get_width()), float(self._amount_per_transaction_is_hundred__surface.get_height()))], True)
            else:
                self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_max__surface], [(float(self._amount_per_transaction_is_max__surface.get_width()), float(self._amount_per_transaction_is_max__surface.get_height()))], True)
            
            self.amount_per_transaction_button.resize_ui_element(float(self.money_amount_text_rect.width) / float(self.amount_per_transaction_button.sizes[0][0]), float(self.money_amount_text_rect.height) / (0.75 * float(self.amount_per_transaction_button.sizes[0][1])))
        
            self.amount_per_transaction_button_rect = pygame.Rect(0.0, 0.0, self.amount_per_transaction_button.sizes[0][0], self.amount_per_transaction_button.sizes[0][1])
            self.amount_per_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) - ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)) + self.position_offset[0])
            self.amount_per_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)) + self.position_offset[1])
    
    def set_type_of_transaction_sell(self, is_type_of_transaction_sell: bool):
        if self.is_type_of_transaction_sell != is_type_of_transaction_sell:
            self.is_type_of_transaction_sell = is_type_of_transaction_sell
            if self.is_type_of_transaction_sell:
                self.type_of_transaction_button = UiElement([self._type_of_transaction_is_sell__surface], [(float(self._type_of_transaction_is_sell__surface.get_width()), float(self._type_of_transaction_is_sell__surface.get_height()))], True)
            else:
                self.type_of_transaction_button = UiElement([self._type_of_transaction_is_buy__surface], [(float(self._type_of_transaction_is_buy__surface.get_width()), float(self._type_of_transaction_is_buy__surface.get_height()))], True)
            self.type_of_transaction_button.resize_ui_element(float(self.money_amount_text_rect.width) / float(self.type_of_transaction_button.sizes[0][0]), float(self.money_amount_text_rect.height) / (0.75 * float(self.type_of_transaction_button.sizes[0][1])))
        
            self.type_of_transaction_button_rect = pygame.Rect(0.0, 0.0, self.type_of_transaction_button.sizes[0][0], self.type_of_transaction_button.sizes[0][1])
            self.type_of_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) + ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)) + self.position_offset[0])
            self.type_of_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)) + self.position_offset[1])

            
    def set_position_offset(self, position_offset: tuple[float, float]):
        self.position_offset = position_offset
        self.reposition_ui()
    
    def get_position_offset(self):
        return self.position_offset
    
    def reposition_ui(self):
        self.shadow_bounding_box_rect = pygame.Rect(((float(Screen.screen.get_width()) / 2) - (0.5 * float(self.shadow_bounding_box.sizes[0][0])) + self.position_offset[0], self.position_offset[1]), self.shadow_bounding_box.sizes[0])

        self.money_amount_text_rect.centerx = self.shadow_bounding_box_rect.centerx + int(self.position_offset[0])
        self.money_amount_text_rect.top = self.shadow_bounding_box_rect.top + int(self.position_offset[1])
        
        self.amount_per_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) - ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)) + self.position_offset[0])
        self.amount_per_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)) + self.position_offset[1])
        
        self.type_of_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) + ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)) + self.position_offset[0])
        self.type_of_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)) + self.position_offset[1])
        
    def update(self, dt, events):
        Screen.screen.fill((46, 46, 46))
        
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.amount_per_transaction_button.is_highlighted = self.amount_per_transaction_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.type_of_transaction_button.is_highlighted = self.type_of_transaction_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))

            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
                if self.marketplace_button.is_highlighted and not self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(True)
                if self.amount_per_transaction_button.is_highlighted and not self.amount_per_transaction_button.is_ui_element_pressed():
                    self.amount_per_transaction_button.set_ui_element_is_pressed(True)
                if self.type_of_transaction_button.is_highlighted and not self.type_of_transaction_button.is_ui_element_pressed():
                    self.type_of_transaction_button.set_ui_element_is_pressed(True)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.quest_scene
                if self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(False)
                    self.active_scene = Scene.main
                if self.amount_per_transaction_button.is_ui_element_pressed():
                    self.amount_per_transaction_button.set_ui_element_is_pressed(False)
                    if self.amount_per_transaction_option < 3:
                        self.set_amount_per_transaction_option(self.amount_per_transaction_option + 1)
                    else:
                        self.set_amount_per_transaction_option(0)
                if self.type_of_transaction_button.is_ui_element_pressed():
                    self.type_of_transaction_button.set_ui_element_is_pressed(False)
                    self.set_type_of_transaction_sell(not self.is_type_of_transaction_sell)
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        self.quest_button.draw(Screen.screen)
        self.marketplace_button.draw(Screen.screen)
        
        self.shadow_bounding_box.draw(Screen.screen, [self.shadow_bounding_box_rect.topleft])
        self.money_amount_text.draw(Screen.screen, [self.money_amount_text_rect.topleft])
        self.amount_per_transaction_button.draw(Screen.screen, [self.amount_per_transaction_button_rect.topleft])
        self.type_of_transaction_button.draw(Screen.screen, [self.type_of_transaction_button_rect.topleft])
        
    def set_active_scene(self, active_scene: Scene):
        if self.active_scene != active_scene:
            mouse_position = pygame.mouse.get_pos()
            self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
            self.active_scene = active_scene
            
    def get_active_scene(self):
        return self.active_scene
    
    def __calculate_order_of_magnitude__(self, number: int):
        order_of_magnitude = 0
        while number > 0:
            number = number // 10
            if number > 0:
                order_of_magnitude += 1
        return order_of_magnitude
    
    def resize_scene(self, new_size: tuple[int,int]):
        self.quest_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.marketplace_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))

        self.shadow_bounding_box.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.shadow_bounding_box_rect = pygame.Rect((0,0), (int(self.shadow_bounding_box.sizes[0][0]), int(self.shadow_bounding_box.sizes[0][0])))
        
        self.money_amount_text.resize_ui_element((float(self.shadow_bounding_box_rect.width) * (7.0 / 56.0)) / self.money_amount_text.sizes[0][0], (float(self.shadow_bounding_box_rect.height) * (7.0 / 56.0)) / self.money_amount_text.sizes[0][1])
        self.money_amount_text_rect = pygame.Rect((0.0, 0.0), (int(self.money_amount_text.sizes[0][0]), int(self.money_amount_text.sizes[0][0])))
        
        self.amount_per_transaction_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.amount_per_transaction_button_rect = pygame.Rect(0.0, 0.0, self.amount_per_transaction_button.sizes[0][0], self.amount_per_transaction_button.sizes[0][1])
        
        self.type_of_transaction_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.type_of_transaction_button_rect = pygame.Rect(0.0, 0.0, self.type_of_transaction_button.sizes[0][0], self.type_of_transaction_button.sizes[0][1])
        
        
        self.screen_size = Screen.screen.get_size()
        self.reposition_ui()
