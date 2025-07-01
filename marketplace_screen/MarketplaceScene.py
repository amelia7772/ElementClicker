import pygame
import os
from utilities import Screen
from utilities.Scene import Scene
from quest_screen.QuestButton import QuestButton
from marketplace_screen.MarketplaceButton import MarketplaceButton
from utilities.UiElement import UiElement
from marketplace_screen import Money
from utilities.BigNumberMap import order_of_magnitude_to_symbol_map
from marketplace_screen.GoodsLine import GoodsLine
from main_game_screen.ElementType import ElementType
from main_game_screen.Elements import elements
from math import floor
import math

class MarketplaceScene:
    
    def __init__(self, background_image: pygame.Surface):
        self.background_image = background_image.copy()
        
        self._amount_per_transaction_is_one__surface = pygame.image.load(os.path.join("assets", "images" ,"one element per transaction button icon.png")).convert_alpha()
        self._amount_per_transaction_is_ten__surface = pygame.image.load(os.path.join("assets", "images" ,"ten element per transaction button icon.png")).convert_alpha()
        self._amount_per_transaction_is_hundred__surface = pygame.image.load(os.path.join("assets", "images" ,"hundred element per transaction button icon.png")).convert_alpha()
        self._amount_per_transaction_is_max__surface = pygame.image.load(os.path.join("assets", "images" ,"max amount per transaction button icon.png")).convert_alpha()
        
        self._type_of_transaction_is_sell__surface = pygame.image.load(os.path.join("assets", "images" ,"transaction type sell button icon.png")).convert_alpha()
        self._type_of_transaction_is_buy__surface = pygame.image.load(os.path.join("assets", "images" ,"transaction type buy button icon.png")).convert_alpha()
        
        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)
        
        self.quest_button = QuestButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"quest button icon.png")).convert_alpha())
        self.marketplace_button = MarketplaceButton(pygame.image.load(os.path.join("assets", "images" ,"quest button background.png")).convert_alpha(), pygame.image.load(os.path.join("assets", "images" ,"marketplace button icon.png")).convert_alpha())
        
        self.scroll_offset = 0.0
        
        self.scroll_initial_offset = self.scroll_offset
        
        self.scroll_acceleration = 0.0
        
        self.scroll_speed = 0.0
        
        self.scroll_target_height = 0.0
        
        self.redraw()
        
        self.screen_size = Screen.screen.get_size()
        self.previous_size = self.screen_size
        
        self.active_scene = Scene.main
    
    def update_money_amount_text(self):
        money_amount = Money.money
        
        order_of_magnitude_symbol = ""
        
        order_of_magnitude_of_money_amount = self.__calculate_order_of_magnitude__(money_amount)
        if order_of_magnitude_of_money_amount >= 3:
            order_of_magnitude_symbol = order_of_magnitude_to_symbol_map[order_of_magnitude_of_money_amount - (order_of_magnitude_of_money_amount % 3)]
            non_rounded_money_amount = float(money_amount) / (10.0 ** (order_of_magnitude_of_money_amount - (order_of_magnitude_of_money_amount % 3)))
            money_amount = round(non_rounded_money_amount, 2 - self.__calculate_order_of_magnitude__(int(non_rounded_money_amount)))
        if float(floor(money_amount)) == money_amount:
            money_amount_text_surface = self.pixelated_font.render(f'${int(money_amount)}' + order_of_magnitude_symbol,False,pygame.Color(0, 255, 0)).convert_alpha()
        elif float(floor(money_amount * 10.0) / 10.0) == money_amount:
            money_amount_text_surface = self.pixelated_font.render(f'${floor(money_amount * 10.0) / 10.0}' + order_of_magnitude_symbol,False,pygame.Color(0, 255, 0)).convert_alpha()
        else:
            money_amount_text_surface = self.pixelated_font.render(f'${floor(money_amount * 100.0) / 100.0}' + order_of_magnitude_symbol,False,pygame.Color(0, 255, 0)).convert_alpha()
            
        shadow_bounding_box_rect = pygame.Rect((float(Screen.screen.get_width()) / 2) - (0.5 * float(self.shadow_bounding_box_surface.get_width())), 0.0,float(self.shadow_bounding_box_surface.get_width()), float(self.shadow_bounding_box_surface.get_height()))
        
        self.money_amount_text = UiElement([money_amount_text_surface], [(float(money_amount_text_surface.get_width()), float(money_amount_text_surface.get_height()))])
        self.money_amount_text.resize_ui_element((float(shadow_bounding_box_rect.width) * 0.4) / self.money_amount_text.sizes[0][0], (float(shadow_bounding_box_rect.height) * (7.0 / 56.0)) / self.money_amount_text.sizes[0][1])
        
        ui_elements_above_goods_scroll_line_bounding_box = pygame.Rect(shadow_bounding_box_rect.topleft, (shadow_bounding_box_rect.width, int(float(shadow_bounding_box_rect.height) * (7.0 / 56.0))))
        
        self.money_amount_text_rect = pygame.Rect(0.0,0.0, self.money_amount_text.sizes[0][0],self.money_amount_text.sizes[0][1])
        self.money_amount_text_rect.centerx = shadow_bounding_box_rect.centerx
        self.money_amount_text_rect.centery = ui_elements_above_goods_scroll_line_bounding_box.centery
    
    def set_amount_per_transaction_option(self, amount_per_transaction_option: int):
        if self.amount_per_transaction_option != amount_per_transaction_option:
            self.amount_per_transaction_option = amount_per_transaction_option
            
            if self.amount_per_transaction_option == 0:
                for goods_line in self.goods_lines:
                    goods_line.element_transaction_amount = 1
                    goods_line.redraw_element_transaction_amount_text_surface()
                    goods_line.redraw_element_price_number_text()
                self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_one__surface], [(float(self._amount_per_transaction_is_one__surface.get_width()), float(self._amount_per_transaction_is_one__surface.get_height()))], True)
            elif self.amount_per_transaction_option == 1:
                for goods_line in self.goods_lines:
                    goods_line.element_transaction_amount = 10
                    goods_line.redraw_element_transaction_amount_text_surface()
                    goods_line.redraw_element_price_number_text()
                self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_ten__surface], [(float(self._amount_per_transaction_is_ten__surface.get_width()), float(self._amount_per_transaction_is_ten__surface.get_height()))], True)
            elif self.amount_per_transaction_option == 2:
                for goods_line in self.goods_lines:
                    goods_line.element_transaction_amount = 100
                    goods_line.redraw_element_transaction_amount_text_surface()
                    goods_line.redraw_element_price_number_text()
                self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_hundred__surface], [(float(self._amount_per_transaction_is_hundred__surface.get_width()), float(self._amount_per_transaction_is_hundred__surface.get_height()))], True)
            else:
                for goods_line in self.goods_lines:
                    if goods_line.is_transaction_sell:
                        goods_line.element_transaction_amount = max(1, elements.elements[int(goods_line.element_id)].element_resource_amount)
                    else:
                        goods_line.element_transaction_amount = max(1, floor(float(Money.money) / float(goods_line.price_buy)))
                    goods_line.redraw_element_transaction_amount_text_surface()
                    goods_line.redraw_element_price_number_text()
                self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_max__surface], [(float(self._amount_per_transaction_is_max__surface.get_width()), float(self._amount_per_transaction_is_max__surface.get_height()))], True)
            
            self.amount_per_transaction_button.resize_ui_element((float(self.shadow_bounding_box_rect.width) / 5.0) / float(self.amount_per_transaction_button.sizes[0][0]), (float(self.shadow_bounding_box_rect.width) / 7.0) / float(self.amount_per_transaction_button.sizes[0][1]))
        
            self.amount_per_transaction_button_rect = pygame.Rect(0.0, 0.0, self.amount_per_transaction_button.sizes[0][0], self.amount_per_transaction_button.sizes[0][1])
            self.amount_per_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) - ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)))
            self.amount_per_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)))
    
    def set_type_of_transaction_sell(self, is_type_of_transaction_sell: bool):
        if self.is_type_of_transaction_sell != is_type_of_transaction_sell:
            self.is_type_of_transaction_sell = is_type_of_transaction_sell
            if self.is_type_of_transaction_sell:
                self.type_of_transaction_button = UiElement([self._type_of_transaction_is_buy__surface], [(float(self._type_of_transaction_is_buy__surface.get_width()), float(self._type_of_transaction_is_buy__surface.get_height()))], True)
            else:
                self.type_of_transaction_button = UiElement([self._type_of_transaction_is_sell__surface], [(float(self._type_of_transaction_is_sell__surface.get_width()), float(self._type_of_transaction_is_sell__surface.get_height()))], True)
            self.type_of_transaction_button.resize_ui_element(float(self.amount_per_transaction_button_rect.width) / float(self.type_of_transaction_button.sizes[0][0]), float(self.amount_per_transaction_button_rect.height) / float(self.type_of_transaction_button.sizes[0][1]))
        
            self.type_of_transaction_button_rect = pygame.Rect(0.0, 0.0, self.type_of_transaction_button.sizes[0][0], self.type_of_transaction_button.sizes[0][1])
            self.type_of_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) + ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)))
            self.type_of_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)))

            for goods_line in self.goods_lines:
                if self.amount_per_transaction_option == 3:
                    if is_type_of_transaction_sell:
                        goods_line.element_transaction_amount = max(1, elements.elements[int(goods_line.element_id)].element_resource_amount)
                    else:
                        goods_line.element_transaction_amount = max(1, floor(float(Money.money) / float(goods_line.price_buy)))
                    goods_line.redraw_element_transaction_amount_text_surface()
                goods_line.set_is_transaction_sell(is_type_of_transaction_sell)
            
    def set_scroll_offset(self, scroll_offset: float):
        self.scroll_offset = scroll_offset
        self.reposition_ui()
    
    def get_scroll_offset(self):
        return self.scroll_offset
    
    def reposition_ui(self):
        self.shadow_bounding_box_rect = pygame.Rect((float(Screen.screen.get_width()) / 2) - (0.5 * float(self.shadow_bounding_box_surface.get_width())), 0.0,float(self.shadow_bounding_box_surface.get_width()), float(self.shadow_bounding_box_surface.get_height()))

        ui_elements_above_goods_scroll_line_bounding_box = pygame.Rect(self.shadow_bounding_box_rect.topleft, (self.shadow_bounding_box_rect.width, int(float(self.shadow_bounding_box_rect.height) * (7.0 / 56.0))))

        self.money_amount_text_rect = pygame.Rect(0.0,0.0, self.money_amount_text.sizes[0][0],self.money_amount_text.sizes[0][1])
        self.money_amount_text_rect.centerx = self.shadow_bounding_box_rect.centerx
        self.money_amount_text_rect.centery = ui_elements_above_goods_scroll_line_bounding_box.centery
        
        self.amount_per_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) - ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)))
        self.amount_per_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)))
        
        self.type_of_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) + ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)))
        self.type_of_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)))
        
        self.goods_scroll_rect.topleft = (float(self.shadow_bounding_box_rect.left) + 0.05 * float(self.shadow_bounding_box_rect.width), self.money_amount_text_rect.bottom + (float(self.shadow_bounding_box_rect.height) / 16.0))
    
    def update_scroll_offset(self, dt):
        self.scroll_acceleration = (30 * (float(Screen.screen.get_height()) / 400.0)) * ((self.scroll_initial_offset + ((self.scroll_target_height - self.scroll_initial_offset) / 2.0)) - self.scroll_offset)
        
        next_scroll_offset = self.scroll_offset + ((0.5 * self.scroll_acceleration * (dt * dt)) + (self.scroll_speed * dt))
        
        if (((self.scroll_target_height - self.scroll_initial_offset) > 0 and (next_scroll_offset <= self.scroll_target_height))\
            or ((self.scroll_target_height - self.scroll_initial_offset) < 0 and (next_scroll_offset >= self.scroll_target_height))):
        
            self.scroll_offset = next_scroll_offset
        
            self.scroll_speed += self.scroll_acceleration * dt
        else:
            self.scroll_speed = 0.0
            self.scroll_offset = self.scroll_target_height
            self.scroll_initial_offset = self.scroll_offset
    
    def update(self, dt, events):
        Screen.screen.fill((46, 46, 46))
        
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                self.quest_button.is_highlighted = self.quest_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.marketplace_button.is_highlighted = self.marketplace_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.amount_per_transaction_button.is_highlighted = self.amount_per_transaction_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))
                self.type_of_transaction_button.is_highlighted = self.type_of_transaction_button._hightliter_ellipse.collide_point(float(mouse_position[0]), float(mouse_position[1]))

                for i in range(0, len(self.goods_lines)):
                    transaction_button_rect = self.goods_lines[i].transaction_button_rect.copy()
                    transaction_button_rect.top += self.goods_scroll_rect.top + self.scroll_offset
                    transaction_button_rect.left += self.goods_scroll_rect.left
                    self.goods_lines[i].set_is_transaction_button_highlighted(transaction_button_rect.collidepoint(float(mouse_position[0]), float(mouse_position[1])))
            
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if self.quest_button.is_highlighted and not self.quest_button.is_ui_element_pressed():
                    self.quest_button.set_ui_element_is_pressed(True)
                if self.marketplace_button.is_highlighted and not self.marketplace_button.is_ui_element_pressed():
                    self.marketplace_button.set_ui_element_is_pressed(True)
                if self.amount_per_transaction_button.is_highlighted and not self.amount_per_transaction_button.is_ui_element_pressed():
                    self.amount_per_transaction_button.set_ui_element_is_pressed(True)
                if self.type_of_transaction_button.is_highlighted and not self.type_of_transaction_button.is_ui_element_pressed():
                    self.type_of_transaction_button.set_ui_element_is_pressed(True)
                
                for i in range(0, len(self.goods_lines)):
                    if self.goods_lines[i].is_transaction_button_highlighted and not self.goods_lines[i].is_transaction_button_pressed and self.goods_lines[i].is_transaction_viable:
                        self.goods_lines[i].set_is_transaction_button_pressed(True)
            
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
                
                for i in range(0, len(self.goods_lines)):
                    if self.goods_lines[i].is_transaction_button_pressed:
                        self.goods_lines[i].set_is_transaction_button_pressed(False)
                        self.goods_lines[i].perform_transaction()
                        self.update_money_amount_text()
                        if self.amount_per_transaction_option == 3:
                            for goods_line in self.goods_lines:
                                if goods_line.is_transaction_sell:
                                    goods_line.element_transaction_amount = max(1, elements.elements[int(goods_line.element_id)].element_resource_amount)
                                else:
                                    goods_line.element_transaction_amount = max(1, floor(float(Money.money) / float(goods_line.price_buy)))
                                goods_line.redraw_element_transaction_amount_text_surface()
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_initial_offset = self.scroll_offset
                self.scroll_target_height = min(0.0, max(-float(self.goods_lines[len(self.goods_lines) - 1].bounding_box.bottom) - float(self.goods_lines[0].bounding_box.height) + float(self.goods_scroll_rect.height), self.scroll_target_height + float((event.y) * 20)))
                if event.y > 0:
                    self.scroll_acceleration = min(300 * (float(Screen.screen.get_height()) / 400.0), self.scroll_acceleration + (30 * (float(Screen.screen.get_height()) / 400.0)))
                else:
                    self.scroll_acceleration = max(-300 * (float(Screen.screen.get_height()) / 400.0), self.scroll_acceleration - (30 * (float(Screen.screen.get_height()) / 400.0)))
        
        if pygame.key.get_pressed()[pygame.key.key_code("w")]:
            self.scroll_initial_offset = self.scroll_offset
            self.scroll_target_height = min(0.0, max(-float(self.goods_lines[len(self.goods_lines) - 1].bounding_box.bottom) - float(self.goods_lines[0].bounding_box.height) + float(self.goods_scroll_rect.height), self.scroll_target_height + 5.0))
            self.scroll_acceleration = min(300 * (float(Screen.screen.get_height()) / 400.0), self.scroll_acceleration + (30 * (float(Screen.screen.get_height()) / 400.0)))
        if pygame.key.get_pressed()[pygame.key.key_code("s")]:
            self.scroll_initial_offset = self.scroll_offset
            self.scroll_target_height = min(0.0, max(-float(self.goods_lines[len(self.goods_lines) - 1].bounding_box.bottom) - float(self.goods_lines[0].bounding_box.height) + float(self.goods_scroll_rect.height), self.scroll_target_height  - 5.0))
            self.scroll_acceleration = max(-300 * (float(Screen.screen.get_height()) / 400.0), self.scroll_acceleration - (30 * (float(Screen.screen.get_height()) / 400.0)))
        
        self.update_scroll_offset(dt)
        
        for x in range(0, Screen.screen.get_width(), self.background_image.get_width()):
            for y in range(0, Screen.screen.get_height(), self.background_image.get_height()):
                Screen.screen.blit(self.background_image, (x,y))
        
        self.quest_button.draw(Screen.screen)
        self.marketplace_button.draw(Screen.screen)
        
        Screen.screen.blit(self.shadow_bounding_box_surface, self.shadow_bounding_box_rect)
        self.money_amount_text.draw(Screen.screen, [self.money_amount_text_rect.topleft])
        self.amount_per_transaction_button.draw(Screen.screen, [self.amount_per_transaction_button_rect.topleft])
        self.type_of_transaction_button.draw(Screen.screen, [self.type_of_transaction_button_rect.topleft])
        
        self.goods_scroll_surface = pygame.Surface(self.goods_scroll_rect.size, pygame.SRCALPHA)
        
        for goods_line in self.goods_lines:
            goods_line.draw(self.goods_scroll_surface, self.scroll_offset)
        
        Screen.screen.blit(self.goods_scroll_surface, self.goods_scroll_rect)
        
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

    def redraw(self):
        self.shadow_bounding_box_surface = pygame.Surface((int(float(Screen.screen.get_width()) * 0.6), Screen.screen.get_height() * 2),pygame.SRCALPHA)
        
        self.shadow_bounding_box_surface.fill((0,0,0,int(0.4 * 255)))
        
        self.shadow_bounding_box_rect = pygame.Rect((float(Screen.screen.get_width()) / 2) - (0.5 * float(self.shadow_bounding_box_surface.get_width())), 0.0,float(self.shadow_bounding_box_surface.get_width()), float(self.shadow_bounding_box_surface.get_height()))
        
        self.update_money_amount_text()
        
        self.amount_per_transaction_option = 0

        self.amount_per_transaction_button = UiElement([self._amount_per_transaction_is_one__surface], [(float(self._amount_per_transaction_is_one__surface.get_width()), float(self._amount_per_transaction_is_one__surface.get_height()))], True)
        self.amount_per_transaction_button.resize_ui_element((float(self.shadow_bounding_box_rect.width) / 5.0) / float(self.amount_per_transaction_button.sizes[0][0]), (float(self.shadow_bounding_box_rect.width) / 7.0) / float(self.amount_per_transaction_button.sizes[0][1]))
        
        self.amount_per_transaction_button_rect = pygame.Rect(0.0, 0.0, self.amount_per_transaction_button.sizes[0][0], self.amount_per_transaction_button.sizes[0][1])
        self.amount_per_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) - ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)))
        self.amount_per_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)))
        
        self.is_type_of_transaction_sell = True
        
        self.type_of_transaction_button = UiElement([self._type_of_transaction_is_buy__surface], [(float(self._type_of_transaction_is_buy__surface.get_width()), float(self._type_of_transaction_is_buy__surface.get_height()))], True)
        self.type_of_transaction_button.resize_ui_element(float(self.amount_per_transaction_button_rect.width) / float(self.type_of_transaction_button.sizes[0][0]), float(self.amount_per_transaction_button_rect.height) / float(self.type_of_transaction_button.sizes[0][1]))
        
        self.type_of_transaction_button_rect = pygame.Rect(0.0, 0.0, self.type_of_transaction_button.sizes[0][0], self.type_of_transaction_button.sizes[0][1])
        self.type_of_transaction_button_rect.centerx = int(float(self.shadow_bounding_box_rect.centerx) + ((0.5 * (2.0/3.0)) * float(self.shadow_bounding_box_rect.width)))
        self.type_of_transaction_button_rect.top = int(float(self.money_amount_text_rect.top) + (0.25 * float(self.money_amount_text_rect.height)))
        
        
        goods: list[tuple[ElementType,float, float]] = [(ElementType.wood, 1, 1), (ElementType.rock, 2, 1), (ElementType.water, 10, 3), (ElementType.dirt, 10, 3)]
        
        self.goods_scroll_surface = pygame.Surface((0.9 * float(self.shadow_bounding_box_rect.width), Screen.screen.get_height() - (float(self.money_amount_text_rect.bottom) + (float(self.shadow_bounding_box_rect.height) / 16.0))), pygame.SRCALPHA).convert_alpha()
        self.goods_scroll_rect = pygame.Rect(float(self.shadow_bounding_box_rect.left) + 0.05 * float(self.shadow_bounding_box_rect.width), float(self.money_amount_text_rect.bottom) + (float(self.shadow_bounding_box_rect.height) / 16.0), self.goods_scroll_surface.get_width(), self.goods_scroll_surface.get_height())
        
        self.goods_lines: list[GoodsLine] = []
        
        y = 0.0
        
        for i in range(0, len(goods)):
            bounding_box = pygame.Rect(0, y, 0.9 * float(self.shadow_bounding_box_rect.width), (0.9 * float(self.shadow_bounding_box_rect.width)) / 4.0)
            self.goods_lines.append(GoodsLine(bounding_box, goods[i][0], goods[i][1], goods[i][2]))
            y += bounding_box.height + ((0.9 * float(self.shadow_bounding_box_rect.width)) / 16.0)

    def resize_scene(self, new_size: tuple[int,int]):
        self.quest_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))
        self.marketplace_button.resize_ui_element(float(new_size[0]) / float(self.previous_size[0]), float(new_size[1]) / float(self.previous_size[1]))

        self.shadow_bounding_box_surface = pygame.Surface((int(float(Screen.screen.get_width()) * 0.6), Screen.screen.get_height() * 2),pygame.SRCALPHA)
        
        self.shadow_bounding_box_surface.fill((0,0,0,int(0.4 * 255)))
        
        self.shadow_bounding_box_rect = pygame.Rect((float(Screen.screen.get_width()) / 2) - (0.5 * float(self.shadow_bounding_box_surface.get_width())), 0.0,float(self.shadow_bounding_box_surface.get_width()), float(self.shadow_bounding_box_surface.get_height()))
        
        self.update_money_amount_text()
        
        self.amount_per_transaction_button.resize_ui_element((float(self.shadow_bounding_box_rect.width) / 5.0) / float(self.amount_per_transaction_button.sizes[0][0]), (float(self.shadow_bounding_box_rect.width) / 7.0) / float(self.amount_per_transaction_button.sizes[0][1]))
        self.amount_per_transaction_button_rect = pygame.Rect(0.0, 0.0, self.amount_per_transaction_button.sizes[0][0], self.amount_per_transaction_button.sizes[0][1])
        
        self.type_of_transaction_button.resize_ui_element(float(self.amount_per_transaction_button_rect.width) / float(self.type_of_transaction_button.sizes[0][0]), float(self.amount_per_transaction_button_rect.height) / float(self.type_of_transaction_button.sizes[0][1]))
        self.type_of_transaction_button_rect = pygame.Rect(0.0, 0.0, self.type_of_transaction_button.sizes[0][0], self.type_of_transaction_button.sizes[0][1])
        
        self.goods_scroll_surface = pygame.Surface((0.9 * float(self.shadow_bounding_box_rect.width), Screen.screen.get_height() - (float(self.money_amount_text_rect.bottom) + (float(self.shadow_bounding_box_rect.height) / 16.0))), pygame.SRCALPHA).convert_alpha()
        self.goods_scroll_rect = pygame.Rect(float(self.shadow_bounding_box_rect.left) + 0.05 * float(self.shadow_bounding_box_rect.width), float(self.money_amount_text_rect.bottom) + (float(self.shadow_bounding_box_rect.height) / 16.0), self.goods_scroll_surface.get_width(), self.goods_scroll_surface.get_height())
        
        y = 0.0

        for i in range(0, len(self.goods_lines)):
            bounding_box = pygame.Rect(0.0, y, 0.9 * float(self.shadow_bounding_box_rect.width), (0.9 * float(self.shadow_bounding_box_rect.width)) / 4.0)
            self.goods_lines[i].set_bounding_box(bounding_box)
            y += float(bounding_box.height) + ((0.9 * float(self.shadow_bounding_box_rect.width)) / 16.0)
            
        
        self.screen_size = Screen.screen.get_size()
        self.reposition_ui()
