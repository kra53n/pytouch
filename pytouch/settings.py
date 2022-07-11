import pyxel as px

from elements import OptionChooser
from colors import get_filenames as get_colors_filenames
from constants import Screen


class Settings:
    def __init__(self):
        x = Screen.width // 2 - 30
        
        self.objs = {
            'color_chooser': OptionChooser('Colors: ', 15, 13,
                get_colors_filenames(), x, 20),
            'sound_level': OptionChooser('Sound level: ', 15, 13,
                tuple(f'{round(100 * i / 7)}%' for i in range(8)), x, 40),
            'effects_level': OptionChooser('Effects level: ', 15, 13,
                tuple(f'{round(100 * i / 7)}%' for i in range(8)), x, 60),
        }

    def process(self):
        for obj in self.objs.values():
            obj.process()

    def draw(self):
        px.cls(14)
        for obj in self.objs.values():
            obj.draw()

