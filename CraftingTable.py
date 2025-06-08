from CraftingRecipe import CraftingRecipe
from ElementType import ElementType
import Elements
import XpBar
from pygame.surface import Surface
import time

global crafting_table
crafting_table: tuple[CraftingRecipe] = (CraftingRecipe((), result= (ElementType.wood, 1), resulting_xp= 1, waiting_time= -1),
                                         CraftingRecipe((ElementType.wood, 3, True), result= (ElementType.fire, 1), resulting_xp= 3, waiting_time= -1),
                                         CraftingRecipe((), result= (ElementType.rock, 1), resulting_xp= 5, waiting_time= 1),
                                         CraftingRecipe((ElementType.fire, 3, True), (ElementType.rock, 5, True), result= (ElementType.iron, 1), resulting_xp= 15, waiting_time= -1),
                                         CraftingRecipe((ElementType.fire, 6, True), (ElementType.iron, 3, True), result= (ElementType.bucket, 1), resulting_xp= 50, waiting_time= -1),
                                         CraftingRecipe((ElementType.bucket, 1, False), result= (ElementType.water, 1), resulting_xp= 10, waiting_time= 1),
                                         CraftingRecipe((ElementType.iron, 3, True), (ElementType.wood, 2, True), result= (ElementType.iron_pickaxe, 1), resulting_xp= 25, waiting_time= -1),
                                         CraftingRecipe((ElementType.iron, 3, True), (ElementType.wood, 2, True), result= (ElementType.iron_hammer, 1), resulting_xp= 25, waiting_time= -1),
                                         CraftingRecipe((ElementType.iron, 3, True), (ElementType.wood, 2, True), result= (ElementType.iron_axe, 1), resulting_xp= 25, waiting_time= -1),
                                         CraftingRecipe((ElementType.iron, 3, True), (ElementType.wood, 2, True), result= (ElementType.iron_hoe, 1), resulting_xp= 25, waiting_time= -1),
                                         CraftingRecipe((ElementType.iron, 3, True), (ElementType.wood, 2, True), result= (ElementType.iron_shovel, 1), resulting_xp= 25, waiting_time= -1),
                                         CraftingRecipe((ElementType.iron, 3, True), (ElementType.wood, 2, True), result= (ElementType.iron_pitchfork, 1), resulting_xp= 25, waiting_time= -1),
                                         CraftingRecipe((ElementType.iron, 3, True), (ElementType.wood, 2, True), result= (ElementType.iron_sickle_scythe, 1), resulting_xp= 25, waiting_time= -1),
                                         CraftingRecipe((ElementType.iron_shovel, 1, False), result= (ElementType.dirt, 1), resulting_xp= 10, waiting_time= 1),
                                         CraftingRecipe((ElementType.iron_hammer, 1, False), (ElementType.rock, 1, True), result= (ElementType.gravil, 1), resulting_xp= 15, waiting_time= 1),
                                         CraftingRecipe((ElementType.iron_hammer, 5, False), (ElementType.gravil, 1, True), result= (ElementType.sand, 1), resulting_xp= 15, waiting_time= 1),
                                         CraftingRecipe((ElementType.dirt, 1, True), (ElementType.water, 1, True), (ElementType.iron_hoe, 1, False), result= (ElementType.farmland, 1), resulting_xp= 20, waiting_time= 2),
                                         CraftingRecipe((ElementType.dirt, 6, True), (ElementType.iron_hoe, 1, False), result= (ElementType.wheat_seeds, 1), resulting_xp= 25, waiting_time= 3),
                                         CraftingRecipe((ElementType.farmland, 1, True), (ElementType.wheat_seeds, 1, True), result= (ElementType.wheat_plant, 1), resulting_xp= 15, waiting_time= -1),
                                         CraftingRecipe((ElementType.wheat_plant, 1, True), (ElementType.iron_sickle_scythe, 1, False), result= (ElementType.harvested_wheat, 1), resulting_xp= 25, waiting_time= 2),
                                         CraftingRecipe((ElementType.harvested_wheat, 1, True), (ElementType.iron_pitchfork, 1, False), result= (ElementType.heybale, 1), resulting_xp= 10, waiting_time= 1.5))

crafting_timers: list[int] = []

for recipe in crafting_table:
    crafting_timers.append(-1)

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

def get_recipe_for(result: ElementType):
    for crafting_recipe in crafting_table:
        if crafting_recipe.result[0] == result:
            return crafting_recipe
    return None

def is_craftable(recipe: CraftingRecipe):
    if len(recipe.ingredients) == 0:
        return False
    if len(recipe.ingredients[0]) == 0:
        return True
    for ingredient in recipe.ingredients:
        if Elements.elements.elements[int(ingredient[0])].element_resource_amount < ingredient[1]:
            return False
    return True

def craft(recipe: CraftingRecipe, screen: Surface):
    if recipe.waiting_time <= 0:
        if len(recipe.ingredients[0]) != 0:
            for ingredient in recipe.ingredients:
                if ingredient[2]:
                    Elements.elements.elements[int(ingredient[0])].increase_element_amount(-ingredient[1], screen)
        Elements.elements.elements[int(recipe.result[0])].increase_element_amount(recipe.result[1], screen)
        XpBar.xp_bar.increase_xp(recipe.resulting_xp, screen)
    else:
        crafting_timers[int(recipe.result[0])] = time.time()