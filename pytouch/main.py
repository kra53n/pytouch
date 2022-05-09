from random import randrange

import pyxel

from constants import Screen
from menu import Menu
from elements import Text, Score, Circle, ReachCircle


class App:
    def __init__(self):
        pyxel.init(Screen.width, Screen.height, quit_key=False)
        pyxel.mouse(True)

        self.menu = Menu()
        self.circ = Circle()
        self.score = Score()
        self.reach_circ = ReachCircle()

        pyxel.run(self._update, self._draw)

    def _update(self):
        self.menu.update()

        # NOTE: delete code below
        # helps to check the colors 
        if pyxel.btnp(pyxel.KEY_C):
            with open('colors.txt', 'a') as f:
                f.writelines(f"bg: {Screen.bg}\tfg: {(Screen.bg -3) % 16}\t"
                             f"score: {(Screen.bg - 2) % 16}\n")

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
            if (self.reach_circ.is_collided_with_circ(self.circ)):
                self.score.score += 1

            self.circ.col = randrange(16)
            self.reach_circ.col = randrange(16)
            Screen.bg = randrange(16)

            self.reach_circ.respawn()
            self.circ.r = 0

        self.circ.r += 1

    def _draw(self):
        if self.menu.is_drawing:
            self.menu.draw()
            return

        pyxel.cls(Screen.bg)

        self.reach_circ.draw()
        self.circ.draw(pyxel.mouse_x, pyxel.mouse_y)
        self.score.draw()


if __name__ == '__main__':
    App()
