from crafting.CraftingTable import crafting_table
from crafting.CraftingTable import crafting_timers
from crafting.CraftingRecipe import CraftingRecipe
from main_game_screen.ElementType import ElementType
from main_game_screen import Elements
from xpbar import XpBar
from quest_screen import QuestLine
import pygame
import time

def reevaluate_recipes_waiting_time():
    crafting_table[int(ElementType.rock)].waiting_time = crafting_table[int(ElementType.rock)].original_waiting_time
    crafting_table[int(ElementType.water)].waiting_time = crafting_table[int(ElementType.water)].original_waiting_time
    crafting_table[int(ElementType.gravil)].waiting_time = crafting_table[int(ElementType.gravil)].original_waiting_time
    crafting_table[int(ElementType.sand)].waiting_time = crafting_table[int(ElementType.sand)].original_waiting_time
    crafting_table[int(ElementType.dirt)].waiting_time = crafting_table[int(ElementType.dirt)].original_waiting_time
    
    crafting_table[int(ElementType.farmland)].waiting_time = crafting_table[int(ElementType.farmland)].original_waiting_time
    crafting_table[int(ElementType.wheat_seeds)].waiting_time = crafting_table[int(ElementType.wheat_seeds)].original_waiting_time
    crafting_table[int(ElementType.harvested_wheat)].waiting_time = crafting_table[int(ElementType.harvested_wheat)].original_waiting_time
    crafting_table[int(ElementType.heybale)].waiting_time = crafting_table[int(ElementType.heybale)].original_waiting_time
    
    amount_of_iron_pickaxes = Elements.elements.elements[int(ElementType.iron_pickaxe)].element_resource_amount
    while amount_of_iron_pickaxes > 0:
        crafting_table[int(ElementType.rock)].waiting_time -= crafting_table[int(ElementType.rock)].original_waiting_time * (5/100)
        amount_of_iron_pickaxes -= 1
    
    amount_of_buckets = Elements.elements.elements[int(ElementType.bucket)].element_resource_amount - 1
    while amount_of_buckets > 0:
        crafting_table[int(ElementType.water)].waiting_time -= crafting_table[int(ElementType.water)].original_waiting_time * (5/100)
        amount_of_buckets -= 1
    
    amount_of_iron_hammer = Elements.elements.elements[int(ElementType.iron_hammer)].element_resource_amount - 1
    while amount_of_iron_hammer > 0:
        crafting_table[int(ElementType.gravil)].waiting_time -= crafting_table[int(ElementType.gravil)].original_waiting_time * (5/100)
        amount_of_iron_hammer -= 1
    
    amount_of_iron_hammer = Elements.elements.elements[int(ElementType.iron_hammer)].element_resource_amount - 5
    while amount_of_iron_hammer > 0:
        crafting_table[int(ElementType.sand)].waiting_time -= crafting_table[int(ElementType.sand)].original_waiting_time * (5/100)
        amount_of_iron_hammer -= 1
    
    amount_of_iron_shovel = Elements.elements.elements[int(ElementType.iron_shovel)].element_resource_amount - 1
    while amount_of_iron_shovel > 0:
        crafting_table[int(ElementType.dirt)].waiting_time -= crafting_table[int(ElementType.dirt)].original_waiting_time * (5/100)
        amount_of_iron_shovel -= 1
    
    amount_of_iron_hoe = Elements.elements.elements[int(ElementType.iron_hoe)].element_resource_amount - 1
    while amount_of_iron_hoe > 0:
        crafting_table[int(ElementType.farmland)].waiting_time -= crafting_table[int(ElementType.farmland)].original_waiting_time * (5/100)
        crafting_table[int(ElementType.wheat_seeds)].waiting_time -= crafting_table[int(ElementType.wheat_seeds)].original_waiting_time * (5/100)
        amount_of_iron_hoe -= 1
    
    amount_of_iron_sickle_scythe = Elements.elements.elements[int(ElementType.iron_sickle_scythe)].element_resource_amount - 1
    while amount_of_iron_sickle_scythe > 0:
        crafting_table[int(ElementType.harvested_wheat)].waiting_time -= crafting_table[int(ElementType.harvested_wheat)].original_waiting_time * (5/100)
        amount_of_iron_sickle_scythe -= 1
    
    amount_of_iron_pitchfork = Elements.elements.elements[int(ElementType.iron_pitchfork)].element_resource_amount - 1
    while amount_of_iron_pitchfork > 0:
        crafting_table[int(ElementType.heybale)].waiting_time -= crafting_table[int(ElementType.heybale)].original_waiting_time * (5/100)
        amount_of_iron_pitchfork -= 1
    
    amount_of_iron_axe = Elements.elements.elements[int(ElementType.iron_axe)].element_resource_amount
    crafting_table[int(ElementType.wood)].result = (ElementType.wood, 1 + amount_of_iron_axe)

def is_craftable(recipe: CraftingRecipe):
    if len(recipe.ingredients) == 0:
        return False
    if len(recipe.ingredients[0]) == 0:
        return True
    for ingredient in recipe.ingredients:
        if Elements.elements.elements[int(ingredient[0])].element_resource_amount < ingredient[1]:
            return False
    return True

def craft(recipe: CraftingRecipe, screen: pygame.Surface):
    if recipe.waiting_time <= 0:
        if len(recipe.ingredients[0]) != 0:
            for ingredient in recipe.ingredients:
                if ingredient[2]:
                    Elements.elements.elements[int(ingredient[0])].increase_element_amount(-ingredient[1], screen)
        Elements.elements.elements[int(recipe.result[0])].increase_element_amount(recipe.result[1], screen)
        XpBar.xp_bar.increase_xp(recipe.resulting_xp, screen)
        for quest in QuestLine.quests:
            if (quest.condition(Elements.elements.elements, XpBar.xp_bar.level)) and (not quest.is_completed):
                QuestLine.quest_line.set_quest_completed(quest.id, True)
    else:
        crafting_timers[int(recipe.result[0])] = time.time()
