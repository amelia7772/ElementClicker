from main_game_screen.ElementType import ElementType
from types import FunctionType

global goods
goods: list[tuple[ElementType, float, float, bool,FunctionType]] = [(ElementType.wood, 1, 1, False, lambda level, elements: True), (ElementType.rock, 2, 1, False, lambda level, elements: (elements[ElementType.rock].element_resource_amount >= 1 and level >= 5)), (ElementType.water, 10, 3, False, lambda level, elements: (elements[ElementType.bucket].element_resource_amount >= 1 and level >= 7)), (ElementType.dirt, 10, 3, False, lambda level, elements: (elements[ElementType.iron_shovel].element_resource_amount >= 1 and level >= 10))]