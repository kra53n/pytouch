from random import randrange

import pyxel

from constants import Screen
from elements import Text, Score, Circle, ReachCircle


class App:
    def __init__(self):
        pyxel.init(Screen.width, Screen.height)
        pyxel.mouse(True)

        self.circ = Circle()
        self.score = Score()
        self.reach_circ = ReachCircle()

        pyxel.run(self._update, self._draw)

    def _hit_checking(self):
        if abs(self.reach_circ.x - pyxel.mouse_x) < 20 and \
           abs(self.reach_circ.y - pyxel.mouse_y) < 20 and \
           abs(self.reach_circ.r - self.circ.r) < 20:
            return True

    def _update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # NOTE: delete code below
        # helps to check the colors 
        if pyxel.btnp(pyxel.KEY_C):
            with open('colors.txt', 'a') as f:
                f.writelines(f"bg: {Screen.bg}\tfg: {(Screen.bg -3) % 16}\t"
                        "score: {(Screen.bg - 2) % 16}\n")

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or \
           pyxel.btnp(pyxel.KEY_SPACE):
            #self.circ.col = (Screen.bg - 3) % 16
            #self.reach_circ.col = (Screen.bg - 3) % 16
            #Screen.bg = (Screen.bg + 1) % 16
            self.circ.col = randrange(16)
            self.reach_circ.col = randrange(16)
            Screen.bg = randrange(16)

            self.reach_circ.respawn()

            if self._hit_checking():
                self.score.increase()

            self.circ.zero()


    def _draw(self):
        pyxel.cls(Screen.bg)

        self.circ.increase()
        self.reach_circ.draw()
        self.circ.draw(pyxel.mouse_x, pyxel.mouse_y)
        self.score.draw()


if __name__ == '__main__':
    App()
