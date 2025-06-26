import pygame
import os

from crafting.CraftingRecipe import CraftingRecipe

class ElementExplanationMessage(pygame.sprite.Sprite):
    def __init__(self, element_name: str, element_description: str, recipe: CraftingRecipe,image: pygame.Surface, rect: pygame.Rect):
        super().__init__()
        self.background_image = image.copy()
        self.image = image.copy()
        self.original_image = image.copy()
        self.rect = rect
        self.original_size = rect.size
        self.element_name = element_name
        self.element_description = element_description
        self.recipe = recipe
        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), 50)
            
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
    
    def redraw(self, elements):
        size_scaler = 2
        
        element_name_image_surface_size = (540 * size_scaler, 200 * size_scaler)
        element_description_image_surface_size = (540 * size_scaler, 200 * size_scaler)
        element_name_position = (25 * size_scaler,10 * size_scaler)
        element_description_position = (25 * size_scaler, 2 * size_scaler)
        ingredient_text_position = (25 * size_scaler, 0)
        ingredients_starting_x = 25 * size_scaler
        ingredient_image_size = (50 * size_scaler,50 * size_scaler)
        ingredients_horizontal_margin = 5 * size_scaler
        ingredients_vertical_margin = 5 * size_scaler
        background_image_bottom_margin = 50 * size_scaler
        font_size = 50 * size_scaler
        
        maximum_x_drawn_on = 0
        maximum_y_drawn_on = 0
        
        self.pixelated_font = pygame.font.Font(os.path.join("assets", "fonts" ,"minecraft chmc.ttf"), font_size)
        
        temp_image = pygame.Surface((self.background_image.get_width() * 2 * size_scaler, self.background_image.get_height() * 2 * size_scaler), pygame.SRCALPHA)
        self.element_name_image = pygame.Surface(element_name_image_surface_size, pygame.SRCALPHA).convert_alpha()
        element_name_height = self.blit_text(self.element_name_image, self.element_name + ":", (0,0), self.pixelated_font)
        
        self.element_name_image = pygame.transform.scale_by(self.element_name_image.subsurface((0,0), (((self.background_image.get_width() * size_scaler) * (1.0/0.75)) - 25,element_name_height)), 0.75)
        element_name_height = float(element_name_height) * 0.75
        
        self.element_description_image = pygame.Surface(element_description_image_surface_size, pygame.SRCALPHA).convert_alpha()
        element_description_height = self.blit_text(self.element_description_image, self.element_description, (0,0), self.pixelated_font)
        self.element_description_image = pygame.transform.scale_by(self.element_description_image, 0.5)
        element_description_height = float(element_description_height) * 0.5
        
        if len(self.recipe.ingredients[0]) > 0:
            self.ingredients_text_image = self.pixelated_font.render("Ingredients:", False, "White").convert_alpha()
            self.plus_symbol_image = self.pixelated_font.render(" + ", False, "White").convert_alpha()
            self.ingredients_text_image = pygame.transform.scale_by(self.ingredients_text_image, 0.6)
        
        self.element_name_rect = pygame.Rect(element_name_position, (self.element_name_image.get_rect().width, element_name_height))
        self.element_description_rect = pygame.Rect((element_description_position[0], element_description_position[1] + element_name_height), (self.element_description_image.get_rect().width, element_description_height))
        if len(self.recipe.ingredients[0]) > 0:
            self.ingredients_text_rect = pygame.Rect((ingredient_text_position[0], ingredient_text_position[1] + self.element_description_rect.top + element_description_height), self.ingredients_text_image.get_rect().size)
        temp_image.blit(self.element_name_image, self.element_name_rect)
        maximum_x_drawn_on = max(maximum_x_drawn_on, self.element_name_rect.left + self.element_name_image.get_width())
        maximum_y_drawn_on = max(maximum_y_drawn_on, self.element_name_rect.top + self.element_name_image.get_height())
        temp_image.blit(self.element_description_image, self.element_description_rect)
        maximum_x_drawn_on = max(maximum_x_drawn_on, self.element_description_rect.left + self.element_description_image.get_width())
        maximum_y_drawn_on = max(maximum_y_drawn_on, self.element_description_rect.top + self.element_description_image.get_height())
        if len(self.recipe.ingredients[0]) > 0:
            temp_ingredients_surface = pygame.Surface((temp_image.get_rect().size[0], temp_image.get_rect().size[1]), pygame.SRCALPHA)
            temp_image.blit(self.ingredients_text_image, self.ingredients_text_rect)
            counter = 0
            x = ingredients_starting_x
            y = self.ingredients_text_rect.top + self.ingredients_text_rect.height
            for ingredient in self.recipe.ingredients:
                if counter > 0:
                    if counter % 3 == 0:
                        y += ingredient_image_size[1] + ingredients_vertical_margin
                        x = ingredients_starting_x
                        temp_ingredients_surface.blit(self.plus_symbol_image, (x, y))
                        x += self.plus_symbol_image.get_rect().width
                    else:
                        temp_ingredients_surface.blit(self.plus_symbol_image, (x, y))
                        x += self.plus_symbol_image.get_rect().width
                ingredient_image = pygame.transform.scale(elements[int(ingredient[0])]._element_image._element_image_original, ingredient_image_size)
                ingredient_required_amount = self.pixelated_font.render(str(ingredient[1]), False, "White").convert_alpha()
                temp_ingredients_surface.blit(ingredient_image, (x, y))
                x += ingredient_image.get_rect().width + ingredients_horizontal_margin
                temp_ingredients_surface.blit(ingredient_required_amount, (x, y))
                x += ingredient_required_amount.get_rect().width + ingredients_horizontal_margin
                counter += 1
            temp_ingredients_surface = pygame.transform.scale_by(temp_ingredients_surface.subsurface((ingredients_starting_x, self.ingredients_text_rect.top + self.ingredients_text_rect.height), (temp_ingredients_surface.get_width() - ingredients_starting_x,y)).copy(), 0.5)
            temp_image.blit(temp_ingredients_surface, (ingredients_starting_x, self.ingredients_text_rect.top + self.ingredients_text_rect.height))
            maximum_x_drawn_on = max(maximum_x_drawn_on, ingredients_starting_x + temp_ingredients_surface.get_width())
            maximum_y_drawn_on = max(maximum_y_drawn_on, (self.ingredients_text_rect.top + self.ingredients_text_rect.height) + temp_ingredients_surface.get_height())
        temp_image = temp_image.subsurface((0,0),(maximum_x_drawn_on, maximum_y_drawn_on))
        ratio_of_change_in_size = min(float(self.background_image.get_width() * size_scaler) / float(temp_image.get_width()), float((self.background_image.get_height() * size_scaler) - background_image_bottom_margin) / float(temp_image.get_height()))
        temp_image = pygame.transform.scale_by(temp_image, ratio_of_change_in_size)
        self.image = pygame.transform.scale_by(self.background_image.copy(), size_scaler)
        self.image.blit(temp_image, (0,0))
        self.original_image = self.image.copy()
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
