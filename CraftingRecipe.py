from ElementType import ElementType

class CraftingRecipe:
    def __init__(self, *ingredients: tuple[ElementType, int, bool], result: tuple[ElementType, int], resulting_xp: int, waiting_time: float):
        self.ingredients = ingredients
        self.result = result
        self.resulting_xp = resulting_xp
        self.waiting_time = waiting_time
        self.original_waiting_time = waiting_time