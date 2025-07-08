from enum import IntEnum

class Event(IntEnum):
    update_marketplace_goods_availability = 1,
    money_amount_decrease = 2

global game_events
game_events: list[Event] = []
