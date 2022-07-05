import pyxel as px

from elements import OptionChooser
from colors import get_filenames
from constants import Screen


class Settings:
    def __init__(self):
        self.color_chooser = OptionChooser('Colors: ', 15, 13, get_filenames(),
            Screen.width // 2 - 30)
        self.objs = (self.color_chooser, )

    def process(self):
        for obj in self.objs:
            obj.process()

    def draw(self):
        px.cls(14)
        for obj in self.objs:
            obj.draw()

