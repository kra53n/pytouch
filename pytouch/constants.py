from dataclasses import dataclass
from pathlib import Path
from enum import Enum


GAP_BETWEEN_RADII = 5

# size of symbol drawing by pyxel.text()
SYMBOL_HGT = 5
SYMBOL_WDT = 3
SYMBOL_SPACE = 1

MENU_BUTTONS_PADDING = 15

COLORS_PATH = Path(__file__).parent / 'config'
DATA_PATH = Path(__file__).parent / 'data'

@dataclass
class ColorIndexes:
    bg = 0
    user_circ = 2
    reach_circ = 3


@dataclass
class Screen:
    width = 192
    height = 108
    bg = 0


class State(Enum):
    MENU = 'menu'
    PLAY = 'play'
    GAMEOVER = 'gameover'
    SETTINGS = 'settings'
