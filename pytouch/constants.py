from enum import Enum


GAP_BETWEEN_RADII = 5

# size of text letter drawing by pyxel.text()
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


colors = [
    {"bg": 0,  "fg": 13, "score": 14,},
    {"bg": 1,  "fg": 14, "score": 15,},
    {"bg": 2,  "fg": 15, "score": 0,},
    {"bg": 3,  "fg": 0,  "score": 1,},
    {"bg": 5,  "fg": 2,  "score": 3,},
    {"bg": 7,  "fg": 4,  "score": 5,},
    {"bg": 11, "fg": 8,  "score": 9,},
    {"bg": 14, "fg": 11, "score": 12,},
    {"bg": 15, "fg": 12, "score": 13,},
]
