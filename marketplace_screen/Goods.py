from main_game_screen.ElementType import ElementType

global goods
#element_id, price_buy, price_sell, is_available, level_requirement, element_unlocking_requirement (list of elements that should be unlocked and their amounts)
goods: list[tuple[ElementType, float, float, bool, int, list[tuple[ElementType, int]]]] = \
[\
(ElementType.wood, 1, 1, False, 0, []),\
(ElementType.rock, 2, 1, False, 5, [(ElementType.rock, 1)]), \
(ElementType.water, 10, 3, False, 7, [(ElementType.bucket, 1)]), \
(ElementType.dirt, 10, 3, False, 10, [(ElementType.iron_shovel, 1)])\
]
