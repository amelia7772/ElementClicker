import pygame
from main_game_screen.ElementLine import ElementLine
from typing import List
from main_game_screen.ElementType import ElementType
from main_game_screen.ElementExplanationMessage import ElementExplanationMessage
from crafting.CraftingTable import crafting_table
import os

def get_recipe_for(result: ElementType):
    for crafting_recipe in crafting_table:
        if crafting_recipe.result[0] == result:
            return crafting_recipe
    return None

class Elements(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.element_background = pygame.image.load(os.path.join("assets", "images" ,"element background.png")).convert_alpha()
        self.element_explanation_background = pygame.image.load(os.path.join("assets", "images" ,"element explanation background.png")).convert_alpha()
        self.elements: List[ElementLine] = list()
        self.elements.append(ElementLine((400,50), os.path.join("assets", "images" ,"wood log 16-bit.png"), self.element_background, ElementExplanationMessage("Wood", "You punch a tree, you get wood!", get_recipe_for(ElementType.wood), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements[0].is_available = True
        self.elements.append(ElementLine((125,50), os.path.join("assets", "images" ,"fire 16-bit.png"), self.element_background, ElementExplanationMessage("Fire", "The first element!", get_recipe_for(ElementType.fire), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((675,50), os.path.join("assets", "images" ,"rock.png"), self.element_background, ElementExplanationMessage("Rock", "... Are you sure you want to punch it bare-handed?!", get_recipe_for(ElementType.rock), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((125,200), os.path.join("assets", "images" ,"iron ingot 16-bit.png"), self.element_background, ElementExplanationMessage("Iron", "Burn the rocks until you uncover the iron in them!", get_recipe_for(ElementType.iron), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((400,200), os.path.join("assets", "images" ,"bucket.png"), self.element_background, ElementExplanationMessage("Bucket", "A man cannot own a Bucket, it's man who shall kneel before The Bucket!!", get_recipe_for(ElementType.bucket), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((675,200), os.path.join("assets", "images" ,"water.png"), self.element_background, ElementExplanationMessage("Water", "Also known as hydroxic acid, killed more people than cyanide!", get_recipe_for(ElementType.water), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((125,350), os.path.join("assets", "images" ,"iron pickaxe.png"), self.element_background, ElementExplanationMessage("Iron Pickaxe", "Makes punching rocks far easier!", get_recipe_for(ElementType.iron_pickaxe), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((400,350), os.path.join("assets", "images" ,"iron hammer.png"), self.element_background, ElementExplanationMessage("Iron Hammer", "Crushes rocks into dust... don't ask why...", get_recipe_for(ElementType.iron_hammer), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((675,350), os.path.join("assets", "images" ,"iron axe.png"), self.element_background, ElementExplanationMessage("Iron Axe", "Pffft, who needs that?! fists do the job far more naturally!", get_recipe_for(ElementType.iron_axe), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((125,-100), os.path.join("assets", "images" ,"iron hoe.png"), self.element_background, ElementExplanationMessage("Iron Hoe", "... What? You need an explanation of what a hoe is?!", get_recipe_for(ElementType.iron_hoe), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((400,-100), os.path.join("assets", "images" ,"iron shovel.png"), self.element_background, ElementExplanationMessage("Iron Shovel", "Diggy diggy hole, digging a hole!", get_recipe_for(ElementType.iron_shovel), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((675,-100), os.path.join("assets", "images" ,"iron pitchfork.png"), self.element_background, ElementExplanationMessage("Iron Pitchfork", "The thing you use when a movie is offensively generic.", get_recipe_for(ElementType.iron_pitchfork), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-125,50), os.path.join("assets", "images" ,"iron sickle scythe.png"), self.element_background, ElementExplanationMessage("Iron Sickle Scythe", "Yes, I had to look up its name.", get_recipe_for(ElementType.iron_sickle_scythe), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-125,200), os.path.join("assets", "images" ,"dirt.png"), self.element_background, ElementExplanationMessage("Dirt", "The energy drink of miners!", get_recipe_for(ElementType.dirt), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-125,350), os.path.join("assets", "images" ,"gravil.png"), self.element_background, ElementExplanationMessage("Gravil", "Might contain small traces of gold, copper, and... cookies?!", get_recipe_for(ElementType.gravil), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-125,500), os.path.join("assets", "images" ,"sand.png"), self.element_background, ElementExplanationMessage("Sand", "... No, you can't make glass from sand alone.", get_recipe_for(ElementType.sand), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-400,50), os.path.join("assets", "images" ,"farmland.png"), self.element_background, ElementExplanationMessage("Farmland", "The unpaid internship offices of medieval ages!", get_recipe_for(ElementType.farmland), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-400,200), os.path.join("assets", "images" ,"wheat seeds.png"), self.element_background, ElementExplanationMessage("Wheat Seeds", "The seeds of the holy crop!", get_recipe_for(ElementType.wheat_seeds), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-400,350), os.path.join("assets", "images" ,"wheat plant.png"), self.element_background, ElementExplanationMessage("Wheat Plant", "How do I get the plants off the farmlands?!", get_recipe_for(ElementType.wheat_plant), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-400,500), os.path.join("assets", "images" ,"harvested wheat.png"), self.element_background, ElementExplanationMessage("Harvested Wheat", "You need more than 3 to make bread.", get_recipe_for(ElementType.harvested_wheat), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        self.elements.append(ElementLine((-675,50), os.path.join("assets", "images" ,"heybale.png"), self.element_background, ElementExplanationMessage("Heybale", "Feed it to the animals!", get_recipe_for(ElementType.heybale), self.element_explanation_background, pygame.Rect((100,0), (300, 217)))))
        
        
        for element in self.elements:
            element.element_explanation_message.redraw(self.elements)
        
    def reevaluate_availability(self, level):
        if level >= 1:
            self.elements[int(ElementType.fire)].is_available = True
        if level >= 3:
            self.elements[int(ElementType.rock)].is_available = True
        if level >= 5 and self.elements[int(ElementType.iron)].is_available:
            self.elements[int(ElementType.bucket)].is_available = True
        if self.elements[int(ElementType.rock)].element_resource_amount >= 5 and self.elements[int(ElementType.fire)].element_resource_amount >= 3:
            self.elements[int(ElementType.iron)].is_available = True
        if self.elements[int(ElementType.bucket)].element_resource_amount >= 1:
            self.elements[int(ElementType.water)].is_available = True
        if self.elements[int(ElementType.iron)].element_resource_amount >= 1:
            self.elements[int(ElementType.iron_pickaxe)].is_available = True
            self.elements[int(ElementType.iron_hammer)].is_available = True
            self.elements[int(ElementType.iron_axe)].is_available = True
            self.elements[int(ElementType.iron_hoe)].is_available = True
            self.elements[int(ElementType.iron_shovel)].is_available = True
            self.elements[int(ElementType.iron_pitchfork)].is_available = True
            self.elements[int(ElementType.iron_sickle_scythe)].is_available = True
        if self.elements[int(ElementType.iron_hammer)].element_resource_amount >= 1:
            self.elements[int(ElementType.gravil)].is_available = True
            self.elements[int(ElementType.sand)].is_available = True
        if self.elements[int(ElementType.iron_shovel)].element_resource_amount >= 1:
            self.elements[int(ElementType.dirt)].is_available = True
        if self.elements[int(ElementType.iron_hoe)].element_resource_amount >= 1:
            self.elements[int(ElementType.farmland)].is_available = True
            self.elements[int(ElementType.wheat_seeds)].is_available = True
        if self.elements[int(ElementType.wheat_seeds)].element_resource_amount >= 1:
            self.elements[int(ElementType.wheat_plant)].is_available = True
        if self.elements[int(ElementType.wheat_plant)].element_resource_amount >= 1:
            self.elements[int(ElementType.harvested_wheat)].is_available = True
        if self.elements[int(ElementType.harvested_wheat)].element_resource_amount >= 1:
            self.elements[int(ElementType.heybale)].is_available = True
    def draw(self, surface: pygame.surface.Surface):
        for element in self.elements:
            element.draw(surface)
            
global elements
elements = Elements()