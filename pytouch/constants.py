from enum import Enum


GAP_BETWEEN_RADII = 5

# size of symbol drawing by pyxel.text()
SYMBOL_HGT = 5
SYMBOL_WDT = 3
SYMBOL_SPACE = 1


class Screen:
    width = 192
    height = 108
    bg = 0


class State(Enum):
    MENU = 1
    PLAY = 2
    SETTINGS = 3

