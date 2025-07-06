import pygame
import os
from main_game_screen.ElementType import ElementType
from main_game_screen.Elements import elements
from xpbar.XpBar import xp_bar
from utilities.UiElement import UiElement
from utilities import Screen
from marketplace_screen import Money
from crafting.CraftingManager import is_craftable
from crafting.CraftingTable import get_recipe_for
from math import floor
from utilities.BigNumberMap import order_of_magnitude_to_symbol_map
from marketplace_screen.Goods import goods

global transaction_button_buy_price_matched_unpressed_surface
global transaction_button_buy_price_matched_hovered_over_surface
global transaction_button_buy_price_matched_pressed_surface
global transaction_button_buy_price_not_matched_unpressed_surface
global transaction_button_buy_price_not_matched_hovered_over_surface

global transaction_button_sell_amount_matched_unpressed_surface
global transaction_button_sell_amount_matched_hovered_over_surface
global transaction_button_sell_amount_matched_pressed_surface
global transaction_button_sell_amount_not_matched_unpressed_surface
global transaction_button_sell_amount_not_matched_hovered_over_surface

transaction_button_buy_price_matched_unpressed_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace buying button price matched unpressed.png")).convert_alpha()
transaction_button_buy_price_matched_hovered_over_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace buying button price matched hovered over.png")).convert_alpha()
transaction_button_buy_price_matched_pressed_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace buying button price matched pressed.png")).convert_alpha()
transaction_button_buy_price_not_matched_unpressed_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace buying button price not matched unpressed.png")).convert_alpha()
transaction_button_buy_price_not_matched_hovered_over_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace buying button price not matched hovered over.png")).convert_alpha()
        
transaction_button_sell_amount_matched_unpressed_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace sell button amount matched unpressed.png")).convert_alpha()
transaction_button_sell_amount_matched_hovered_over_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace sell button amount matched hovered over.png")).convert_alpha()
transaction_button_sell_amount_matched_pressed_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace sell button amount matched pressed.png")).convert_alpha()
transaction_button_sell_amount_not_matched_unpressed_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace selling button amount not matched unpressed.png")).convert_alpha()
transaction_button_sell_amount_not_matched_hovered_over_surface = pygame.image.load(os.path.join("assets", "images" ,"marketplace selling button amount not matched hovered over.png")).convert_alpha()

class GoodsLine:
    
    def __init__(self, bounding_box: pygame.Rect, goods_id: int):
        self.bounding_box = bounding_box
        
        self.goods_id = goods_id
        
        self.element_id = goods[goods_id][0]
        self.price_buy = goods[goods_id][1]
        self.price_sell = goods[goods_id][2]
        self.requirement_function = goods[goods_id][4]
        if goods[goods_id][3]:
            self.is_available = True
        else:
            if self.requirement_function(xp_bar.level, elements.elements):
                self.is_available = True
                goods[goods_id] = (goods[goods_id][0], goods[goods_id][1], goods[goods_id][2], True, goods[goods_id][4])
            else:
                self.is_available = False
        
        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)
        
        self.element_transaction_amount = 1
        
        self.is_transaction_sell = True
        
        self.is_transaction_button_highlighted = False
        
        self.is_transaction_button_pressed = False
        
        self.is_transaction_viable = (elements.elements[int(self.element_id)].element_resource_amount >= 1)
        
        self.resize_ui_elements()
        
    def set_bounding_box(self, bounding_box: pygame.Rect):
        self.bounding_box = bounding_box
        self.resize_ui_elements()
    
    def set_is_transaction_button_highlighted(self, is_highlighted: bool):
        if self.is_transaction_button_highlighted != is_highlighted:
            self.is_transaction_button_highlighted = is_highlighted
            self.check_transaction_button_surface()
            self.resize_transaction_button()
            
    def set_is_transaction_button_pressed(self, is_pressed: bool):
        if self.is_transaction_button_pressed != is_pressed:
            self.is_transaction_button_pressed = is_pressed
            self.check_transaction_button_surface()
            self.resize_transaction_button()
    
    def set_is_transaction_sell(self, is_transaction_sell: bool):
        if self.is_transaction_sell != is_transaction_sell:
            self.is_transaction_sell = is_transaction_sell
            self.check_transaction_button_surface()
            self.resize_transaction_button()
            if is_transaction_sell:
                self.is_transaction_viable = (elements.elements[int(self.element_id)].element_resource_amount >= self.element_transaction_amount)
            else:
                self.is_transaction_viable = (Money.money >= (self.price_buy * self.element_transaction_amount))
            self.redraw_element_price_number_text()
    
    def update_availability(self):
        new_availability = self.requirement_function(xp_bar.level, elements.elements)
        if (goods[self.goods_id][3] == False) and (new_availability == True):
            self.is_available = new_availability
            goods[self.goods_id] = (goods[self.goods_id][0], goods[self.goods_id][1], goods[self.goods_id][2], True, goods[self.goods_id][4])
            self.resize_ui_elements()
    
    def redraw_element_transaction_amount_text_surface(self):
        element_transaction_amount_text_surface = self.pixelated_font.render(f'({self.element_transaction_amount})', False, pygame.Color(255,255,255))
        
        self.element_transaction_amount_text  = UiElement([element_transaction_amount_text_surface], [(float(element_transaction_amount_text_surface.get_width()), float(element_transaction_amount_text_surface.get_height()))])
        self.element_transaction_amount_text.resize_ui_element((0.2 * float(self.bounding_box.width)) / float(element_transaction_amount_text_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(element_transaction_amount_text_surface.get_height()))

        self.reposition_ui_elements()
    
    def redraw_element_price_number_text(self):
        self.recheck_price_color()
        
        if self.is_transaction_sell:
            
            price_sell = self.price_sell * self.element_transaction_amount
            
            order_of_magnitude_symbol = ""
        
            order_of_magnitude_of_price_sell = self.__calculate_order_of_magnitude__(price_sell)
            if order_of_magnitude_of_price_sell >= 3:
                order_of_magnitude_symbol = order_of_magnitude_to_symbol_map[order_of_magnitude_of_price_sell - (order_of_magnitude_of_price_sell % 3)]
                non_rounded_price_sell = float(price_sell) / (10.0 ** (order_of_magnitude_of_price_sell - (order_of_magnitude_of_price_sell % 3)))
                price_sell = round(non_rounded_price_sell, 2 - self.__calculate_order_of_magnitude__(int(non_rounded_price_sell)))
                
            if float(floor(price_sell)) == price_sell:
                element_price_number_text_surface = self.pixelated_font.render(f'${int(price_sell)}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
            elif float(floor(price_sell * 10.0) / 10.0) == price_sell:
                element_price_number_text_surface = self.pixelated_font.render(f'${floor(price_sell * 10.0) / 10.0}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
            else:
                element_price_number_text_surface = self.pixelated_font.render(f'${floor(price_sell * 100.0) / 100.0}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
        else:
            price_buy = self.price_buy * self.element_transaction_amount
            
            order_of_magnitude_symbol = ""
        
            order_of_magnitude_of_price_buy = self.__calculate_order_of_magnitude__(price_buy)
            if order_of_magnitude_of_price_buy >= 3:
                order_of_magnitude_symbol = order_of_magnitude_to_symbol_map[order_of_magnitude_of_price_buy - (order_of_magnitude_of_price_buy % 3)]
                non_rounded_price_buy = float(price_buy) / (10.0 ** (order_of_magnitude_of_price_buy - (order_of_magnitude_of_price_buy % 3)))
                price_buy = round(non_rounded_price_buy, 2 - self.__calculate_order_of_magnitude__(int(non_rounded_price_buy)))
                
            if float(floor(price_buy)) == price_buy:
                element_price_number_text_surface = self.pixelated_font.render(f'${int(price_buy)}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
            elif float(floor(price_buy * 10.0) / 10.0) == price_buy:
                element_price_number_text_surface = self.pixelated_font.render(f'${floor(price_buy * 10.0) / 10.0}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
            else:
                element_price_number_text_surface = self.pixelated_font.render(f'${floor(price_buy * 100.0) / 100.0}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
        
        self.element_price_number_text = UiElement([element_price_number_text_surface], [(float(element_price_number_text_surface.get_width()), float(element_price_number_text_surface.get_height()))])
        self.element_price_number_text.resize_ui_element((0.2 * float(self.bounding_box.width)) / float(element_price_number_text_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(element_price_number_text_surface.get_height()))
        
        element_price_text_surface = self.pixelated_font.render("price:", False, self.price_color)
        
        self.element_price_text = UiElement([element_price_text_surface], [(float(element_price_text_surface.get_width()), float(element_price_text_surface.get_height()))])
        self.element_price_text.resize_ui_element(((0.2 * 0.6) * float(self.bounding_box.width)) / float(element_price_text_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(element_price_text_surface.get_height()))
        
        self.reposition_ui_elements()
        
    def resize_transaction_button(self):
        self.transaction_button.resize_ui_element((0.25 * float(self.bounding_box.width)) / float(self.transaction_button.sizes[0][0]), (float(self.bounding_box.height)) / float(self.transaction_button.sizes[0][1]))

    def check_transaction_button_surface(self):
        if self.is_transaction_sell:
            if elements.elements[int(self.element_id)].element_resource_amount >= self.element_transaction_amount:
                if self.is_transaction_button_pressed:
                    self.transaction_button = UiElement([transaction_button_sell_amount_matched_pressed_surface], [(float(transaction_button_sell_amount_matched_pressed_surface.get_width()), float(transaction_button_sell_amount_matched_pressed_surface.get_height()))])
                elif self.is_transaction_button_highlighted:
                    self.transaction_button = UiElement([transaction_button_sell_amount_matched_hovered_over_surface], [(float(transaction_button_sell_amount_matched_hovered_over_surface.get_width()), float(transaction_button_sell_amount_matched_hovered_over_surface.get_height()))])
                else:
                    self.transaction_button = UiElement([transaction_button_sell_amount_matched_unpressed_surface], [(float(transaction_button_sell_amount_matched_unpressed_surface.get_width()), float(transaction_button_sell_amount_matched_unpressed_surface.get_height()))])
            else:
                if self.is_transaction_button_highlighted:
                    self.transaction_button = UiElement([transaction_button_sell_amount_not_matched_hovered_over_surface], [(float(transaction_button_sell_amount_not_matched_hovered_over_surface.get_width()), float(transaction_button_sell_amount_not_matched_hovered_over_surface.get_height()))])
                else:
                    self.transaction_button = UiElement([transaction_button_sell_amount_not_matched_unpressed_surface], [(float(transaction_button_sell_amount_not_matched_unpressed_surface.get_width()), float(transaction_button_sell_amount_not_matched_unpressed_surface.get_height()))])
        else:
            if Money.money >= self.price_buy:
                if self.is_transaction_button_pressed:
                    self.transaction_button = UiElement([transaction_button_buy_price_matched_pressed_surface], [(float(transaction_button_buy_price_matched_pressed_surface.get_width()), float(transaction_button_buy_price_matched_pressed_surface.get_height()))])
                elif self.is_transaction_button_highlighted:
                    self.transaction_button = UiElement([transaction_button_buy_price_matched_hovered_over_surface], [(float(transaction_button_buy_price_matched_hovered_over_surface.get_width()), float(transaction_button_buy_price_matched_hovered_over_surface.get_height()))])
                else:
                    self.transaction_button = UiElement([transaction_button_buy_price_matched_unpressed_surface], [(float(transaction_button_buy_price_matched_unpressed_surface.get_width()), float(transaction_button_buy_price_matched_unpressed_surface.get_height()))])
            else:
                if self.is_transaction_button_highlighted:
                    self.transaction_button = UiElement([transaction_button_buy_price_not_matched_hovered_over_surface], [(float(transaction_button_buy_price_not_matched_hovered_over_surface.get_width()), float(transaction_button_buy_price_not_matched_hovered_over_surface.get_height()))])
                else:
                    self.transaction_button = UiElement([transaction_button_buy_price_not_matched_unpressed_surface], [(float(transaction_button_buy_price_not_matched_unpressed_surface.get_width()), float(transaction_button_buy_price_not_matched_unpressed_surface.get_height()))])

    def perform_transaction(self):
        if self.is_transaction_sell:
            elements.elements[int(self.element_id)].increase_element_amount(-self.element_transaction_amount, Screen.screen)
            Money.money += self.price_sell * self.element_transaction_amount
            self.is_transaction_viable = (elements.elements[int(self.element_id)].element_resource_amount >= self.element_transaction_amount)
        else:
            Money.money -= self.price_buy * self.element_transaction_amount
            elements.elements[int(self.element_id)].increase_element_amount(self.element_transaction_amount, Screen.screen)
            self.is_transaction_viable = (Money.money >= (self.price_buy * self.element_transaction_amount))
        
        for k in range(0, len(elements.elements)):
            elements.elements[k]._is_element_craftable = is_craftable(get_recipe_for(ElementType(k)))
        
        self.resize_ui_elements()

    def resize_ui_elements(self):
        
        self.recheck_price_color()
        
        self.element_icon = UiElement([pygame.transform.scale(elements.element_background, (int(float(self.bounding_box.width) / 4.0), int(float(self.bounding_box.width) / 4.0))), pygame.transform.scale(elements.elements[int(self.element_id)]._element_image.image, (int((3.0 / 4.0) * (float(self.bounding_box.width) / 4.0)), int((3.0 / 4.0) * (float(self.bounding_box.width) / 4.0))))], [(int(float(self.bounding_box.width) / 4.0), int(float(self.bounding_box.width) / 4.0)), (int((3.0 / 4.0) * (float(self.bounding_box.width) / 4.0)), int((3.0 / 4.0) * (float(self.bounding_box.width) / 4.0)))])
        
        element_icon_unavailable_surface = self.element_icon.images[1].copy()
        element_icon_unavailable_surface.fill((0, 0, 0), None, pygame.BLEND_RGBA_MULT)
        
        self.element_icon_unavailable = UiElement([self.element_icon.images[0], element_icon_unavailable_surface], [self.element_icon.sizes[0], self.element_icon.sizes[1]])
        
        element_name_text_surface = self.pixelated_font.render(elements.elements[int(self.element_id)].element_explanation_message.element_name, False, pygame.Color(255,255,255))
        
        self.element_name_text = UiElement([element_name_text_surface], [(float(element_name_text_surface.get_width()), float(element_name_text_surface.get_height()))])
        self.element_name_text.resize_ui_element((0.2 * float(self.bounding_box.width)) / float(element_name_text_surface.get_width()), (float(self.bounding_box.height) / 2.0) / float(element_name_text_surface.get_height()))
        
        element_transaction_amount_text_surface = self.pixelated_font.render(f'({self.element_transaction_amount})', False, pygame.Color(255,255,255))
        
        self.element_transaction_amount_text  = UiElement([element_transaction_amount_text_surface], [(float(element_transaction_amount_text_surface.get_width()), float(element_transaction_amount_text_surface.get_height()))])
        self.element_transaction_amount_text.resize_ui_element((0.2 * float(self.bounding_box.width)) / float(element_transaction_amount_text_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(element_transaction_amount_text_surface.get_height()))
        
        element_price_text_surface = self.pixelated_font.render("price:", False, self.price_color)
        
        self.element_price_text = UiElement([element_price_text_surface], [(float(element_price_text_surface.get_width()), float(element_price_text_surface.get_height()))])
        self.element_price_text.resize_ui_element(((0.2 * 0.6) * float(self.bounding_box.width)) / float(element_price_text_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(element_price_text_surface.get_height()))
        
        if self.is_transaction_sell:
            price_sell = self.price_sell * self.element_transaction_amount
            
            order_of_magnitude_symbol = ""
        
            order_of_magnitude_of_price_sell = self.__calculate_order_of_magnitude__(price_sell)
            if order_of_magnitude_of_price_sell >= 3:
                order_of_magnitude_symbol = order_of_magnitude_to_symbol_map[order_of_magnitude_of_price_sell - (order_of_magnitude_of_price_sell % 3)]
                non_rounded_price_sell = float(price_sell) / (10.0 ** (order_of_magnitude_of_price_sell - (order_of_magnitude_of_price_sell % 3)))
                price_sell = round(non_rounded_price_sell, 2 - self.__calculate_order_of_magnitude__(int(non_rounded_price_sell)))
                
            if float(floor(price_sell)) == price_sell:
                element_price_number_text_surface = self.pixelated_font.render(f'${int(price_sell)}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
            elif float(floor(price_sell * 10.0) / 10.0) == price_sell:
                element_price_number_text_surface = self.pixelated_font.render(f'${floor(price_sell * 10.0) / 10.0}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
            else:
                element_price_number_text_surface = self.pixelated_font.render(f'${floor(price_sell * 100.0) / 100.0}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
        else:
            price_buy = self.price_buy * self.element_transaction_amount
            
            order_of_magnitude_symbol = ""
        
            order_of_magnitude_of_price_buy = self.__calculate_order_of_magnitude__(price_buy)
            if order_of_magnitude_of_price_buy >= 3:
                order_of_magnitude_symbol = order_of_magnitude_to_symbol_map[order_of_magnitude_of_price_buy - (order_of_magnitude_of_price_buy % 3)]
                non_rounded_price_buy = float(price_buy) / (10.0 ** (order_of_magnitude_of_price_buy - (order_of_magnitude_of_price_buy % 3)))
                price_buy = round(non_rounded_price_buy, 2 - self.__calculate_order_of_magnitude__(int(non_rounded_price_buy)))
                
            if float(floor(price_buy)) == price_buy:
                element_price_number_text_surface = self.pixelated_font.render(f'${int(price_buy)}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
            elif float(floor(price_buy * 10.0) / 10.0) == price_buy:
                element_price_number_text_surface = self.pixelated_font.render(f'${floor(price_buy * 10.0) / 10.0}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
            else:
                element_price_number_text_surface = self.pixelated_font.render(f'${floor(price_buy * 100.0) / 100.0}' + order_of_magnitude_symbol,False, self.price_color).convert_alpha()
        
        self.element_price_number_text = UiElement([element_price_number_text_surface], [(float(element_price_number_text_surface.get_width()), float(element_price_number_text_surface.get_height()))])
        self.element_price_number_text.resize_ui_element((0.2 * float(self.bounding_box.width)) / float(element_price_number_text_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(element_price_number_text_surface.get_height()))
        
        element_amount_text_surface = self.pixelated_font.render("amount: ", False, pygame.Color(255,255,255))
        
        self.element_amount_text = UiElement([element_amount_text_surface], [(float(element_amount_text_surface.get_width()), float(element_amount_text_surface.get_height()))])
        self.element_amount_text.resize_ui_element(((0.2 * 0.9) * float(self.bounding_box.width)) / float(element_amount_text_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(element_amount_text_surface.get_height()))
        
        element_amount_number_text_surface = self.pixelated_font.render(f'{elements.elements[int(self.element_id)].element_resource_amount}', False, pygame.Color(255,255,255))
        
        self.element_amount_number_text = UiElement([element_amount_number_text_surface], [(float(element_amount_number_text_surface.get_width()), float(element_amount_number_text_surface.get_height()))])
        self.element_amount_number_text.resize_ui_element((0.2 * float(self.bounding_box.width)) / float(element_amount_number_text_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(element_amount_number_text_surface.get_height()))
        
        self.check_transaction_button_surface() 
        self.resize_transaction_button()
        
        self.reposition_ui_elements()
        
    def reposition_ui_elements(self):
        self.element_icon_rect = pygame.Rect(0.0, 0.0, self.element_icon.sizes[0][0], self.element_icon.sizes[0][1])
        self.element_name_text_rect = pygame.Rect(0.0, 0.0, self.element_name_text.sizes[0][0], self.element_name_text.sizes[0][1])
        self.element_transaction_amount_text_rect = pygame.Rect(0.0, 0.0, self.element_transaction_amount_text.sizes[0][0], self.element_transaction_amount_text.sizes[0][1])
        self.element_price_text_rect = pygame.Rect(0.0, 0.0, self.element_price_text.sizes[0][0], self.element_price_text.sizes[0][1])
        self.element_price_number_text_rect = pygame.Rect(0.0, 0.0, self.element_price_number_text.sizes[0][0], self.element_price_number_text.sizes[0][1])
        self.element_amount_text_rect = pygame.Rect(0.0, 0.0, self.element_amount_text.sizes[0][0], self.element_amount_text.sizes[0][1])
        self.element_amount_number_text_rect = pygame.Rect(0.0, 0.0, self.element_amount_number_text.sizes[0][0], self.element_amount_number_text.sizes[0][1])
        self.transaction_button_rect = pygame.Rect(0.0, 0.0, self.transaction_button.sizes[0][0], self.transaction_button.sizes[0][1])
        
        self.element_icon_rect.topleft = self.bounding_box.topleft
        self.element_name_text_rect.left = self.element_icon_rect.right + (0.05 * self.bounding_box.width)
        self.element_name_text_rect.top = self.bounding_box.top
        self.element_transaction_amount_text_rect.left = self.element_name_text_rect.right + (0.01 * self.bounding_box.width)
        self.element_transaction_amount_text_rect.centery = self.element_name_text_rect.centery
        self.element_price_text_rect.left = self.element_name_text_rect.left
        self.element_price_text_rect.top =self.element_name_text_rect.bottom + (0.025 * self.bounding_box.height)
        self.element_amount_text_rect.left = self.element_name_text_rect.left
        self.element_amount_text_rect.top = self.element_price_text_rect.bottom + (0.05 * self.bounding_box.height)
        self.element_amount_number_text_rect.left = self.element_amount_text_rect.right
        self.element_amount_number_text_rect.top = self.element_amount_text_rect.top
        
        money_symbol_surface = self.pixelated_font.render("$", False, pygame.Color(0,255,54))
        
        money_symbol_text = UiElement([money_symbol_surface], [(float(money_symbol_surface.get_width()), float(money_symbol_surface.get_height()))])
        money_symbol_text.resize_ui_element((0.2 * float(self.bounding_box.width)) / float(money_symbol_surface.get_width()), (float(self.element_name_text.sizes[0][1]) / 2.0) / float(money_symbol_surface.get_height()))
        
        self.element_price_number_text_rect.left = self.element_amount_number_text_rect.left - money_symbol_text.sizes[0][0]
        self.element_price_number_text_rect.top = self.element_price_text_rect.top
        
        self.transaction_button_rect.right = self.bounding_box.right
        self.transaction_button_rect.centery = self.bounding_box.centery
    
    def recheck_price_color(self):
        if self.is_transaction_sell:
            self.is_transaction_viable = (elements.elements[int(self.element_id)].element_resource_amount >= self.element_transaction_amount)
        else:
            self.is_transaction_viable = (Money.money >= (self.price_buy * self.element_transaction_amount))
        
        if self.is_transaction_viable:
            self.price_color = pygame.Color(0,255,54)
        else:
            self.price_color = pygame.Color(255,54,0)
            
    def draw(self, surface: pygame.Surface, scroll_offset: float = 0.0):
        rect = pygame.Rect(0.0, 0.0, surface.get_width(), surface.get_height())
        element_icon_image_rect = pygame.Rect((0,0), (self.element_icon.sizes[1][0], self.element_icon.sizes[1][1]))
        element_icon_image_rect.center = self.element_icon_rect.center
        element_icon_image_rect.top += scroll_offset
        
        element_icon_rect = self.element_icon_rect.copy()
        element_icon_rect.top += scroll_offset
        
        if rect.colliderect(element_icon_rect):
            if self.is_available:
                self.element_icon.draw(surface, [element_icon_rect.topleft, element_icon_image_rect.topleft])
            else:
                self.element_icon_unavailable.draw(surface, [element_icon_rect.topleft, element_icon_image_rect.topleft])
        
        if self.is_available:
            element_name_text_rect = self.element_name_text_rect.copy()
            element_name_text_rect.top += scroll_offset
            
            element_transaction_amount_text_rect = self.element_transaction_amount_text_rect.copy()
            element_transaction_amount_text_rect.top += scroll_offset
            
            element_price_text_rect = self.element_price_text_rect.copy()
            element_price_text_rect.top += scroll_offset
            
            element_price_number_text_rect = self.element_price_number_text_rect.copy()
            element_price_number_text_rect.top += scroll_offset
            
            element_amount_text_rect = self.element_amount_text_rect.copy()
            element_amount_text_rect.top += scroll_offset
            
            element_amount_number_text_rect = self.element_amount_number_text_rect.copy()
            element_amount_number_text_rect.top += scroll_offset
            
            transaction_button_rect = self.transaction_button_rect.copy()
            transaction_button_rect.top += scroll_offset
            
            if rect.colliderect(element_name_text_rect):
                self.element_name_text.draw(surface, [element_name_text_rect.topleft])
            if rect.colliderect(element_transaction_amount_text_rect):
                self.element_transaction_amount_text.draw(surface, [element_transaction_amount_text_rect.topleft])
            if rect.colliderect(element_price_text_rect):
                self.element_price_text.draw(surface, [element_price_text_rect.topleft])
            if rect.colliderect(element_price_number_text_rect):
                self.element_price_number_text.draw(surface, [element_price_number_text_rect.topleft])
            if rect.colliderect(element_amount_text_rect):
                self.element_amount_text.draw(surface, [element_amount_text_rect.topleft])
            if rect.colliderect(element_amount_number_text_rect):
                self.element_amount_number_text.draw(surface, [element_amount_number_text_rect.topleft])
            if rect.colliderect(transaction_button_rect):
                self.transaction_button.draw(surface, [transaction_button_rect.topleft])
        
    def __calculate_order_of_magnitude__(self, number: int):
        order_of_magnitude = 0
        while number > 0:
            number = number // 10
            if number > 0:
                order_of_magnitude += 1
        return order_of_magnitude
