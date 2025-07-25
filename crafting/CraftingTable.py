from crafting.CraftingRecipe import CraftingRecipe
from main_game_screen.ElementType import ElementType


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
                                         CraftingRecipe((ElementType.iron_hammer, 1, False), (ElementType.rock, 1, True), result= (ElementType.gravel, 1), resulting_xp= 15, waiting_time= 1),
                                         CraftingRecipe((ElementType.iron_hammer, 5, False), (ElementType.gravel, 1, True), result= (ElementType.sand, 1), resulting_xp= 15, waiting_time= 1),
                                         CraftingRecipe((ElementType.dirt, 1, True), (ElementType.water, 1, True), (ElementType.iron_hoe, 1, False), result= (ElementType.farmland, 1), resulting_xp= 20, waiting_time= 2),
                                         CraftingRecipe((ElementType.dirt, 6, True), (ElementType.iron_hoe, 1, False), result= (ElementType.wheat_seeds, 1), resulting_xp= 25, waiting_time= 3),
                                         CraftingRecipe((ElementType.farmland, 1, True), (ElementType.wheat_seeds, 1, True), result= (ElementType.wheat_plant, 1), resulting_xp= 15, waiting_time= -1),
                                         CraftingRecipe((ElementType.wheat_plant, 1, True), (ElementType.iron_sickle_scythe, 1, False), result= (ElementType.harvested_wheat, 1), resulting_xp= 25, waiting_time= 2),
                                         CraftingRecipe((ElementType.harvested_wheat, 1, True), (ElementType.iron_pitchfork, 1, False), result= (ElementType.heybale, 1), resulting_xp= 10, waiting_time= 1.5),
                                         CraftingRecipe((ElementType.dirt, 3, True), (ElementType.water, 1, True), result= (ElementType.clay, 1), resulting_xp= 20, waiting_time= 1.5),
                                         CraftingRecipe((ElementType.clay, 1, True), (ElementType.fire, 3, True), result= (ElementType.brick, 1), resulting_xp= 20, waiting_time= 1.5),
                                         CraftingRecipe((ElementType.sand, 1, True), (ElementType.gravel, 1, True), result= (ElementType.cement, 2), resulting_xp= 20, waiting_time= 1.5),
                                         CraftingRecipe((ElementType.cement, 10, True), (ElementType.brick, 20, True), (ElementType.water, 10, True), (ElementType.iron, 10, True), (ElementType.fire, 10, True), result= (ElementType.factory_tier_one, 1), resulting_xp= 100, waiting_time= 4),
                                         CraftingRecipe((ElementType.factory_tier_one, 1, True), (ElementType.copper_ingot, 20, True), (ElementType.fire, 20, True), result= (ElementType.factory_tier_two, 1), resulting_xp= 150, waiting_time= 10),
                                         CraftingRecipe((ElementType.factory_tier_two, 1, True), (ElementType.gold_ingot, 20, True), (ElementType.fire, 20, True), result= (ElementType.factory_tier_three, 1), resulting_xp= 200, waiting_time= 20),
                                         CraftingRecipe((ElementType.gravel, 6, True), (ElementType.water, 1, True), result= (ElementType.copper_nuggets, 1), resulting_xp= 20, waiting_time= 1.5),
                                         CraftingRecipe((ElementType.sand, 15, True), (ElementType.water, 4, True), result= (ElementType.golden_nuggets, 1), resulting_xp= 40, waiting_time= 2),
                                         CraftingRecipe((ElementType.copper_nuggets, 4, True), (ElementType.fire, 3, True), result= (ElementType.copper_ingot, 1), resulting_xp= 10, waiting_time= 1),
                                         CraftingRecipe((ElementType.golden_nuggets, 3, True), (ElementType.copper_nuggets, 1, True), (ElementType.fire, 3, True), result= (ElementType.gold_ingot, 1), resulting_xp= 20, waiting_time= 1))

crafting_timers: list[int] = []

for recipe in crafting_table:
    crafting_timers.append(-1)

def get_recipe_for(result: ElementType):
    for crafting_recipe in crafting_table:
        if crafting_recipe.result[0] == result:
            return crafting_recipe
    return None

