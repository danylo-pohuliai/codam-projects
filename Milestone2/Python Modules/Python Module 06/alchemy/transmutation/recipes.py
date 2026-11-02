from elements import create_fire
from ..elements import create_air
from alchemy import strength_potion


def lead_to_gold() -> str:
    return f"Recipe transmuting Lead to Gold: brew " \
           f"’{create_air()}’ and ’{strength_potion()}’ " \
           f"mixed with ’{create_fire()}’"
