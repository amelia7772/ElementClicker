from enum import IntEnum

class Event(IntEnum):
    update_marketplace_goods_availability = 1

global game_events
game_events: list[Event] = []