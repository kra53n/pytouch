from random import randrange

import pyxel as px

from elements import Score, Circle, ReachCircle
from constants import Screen, State
from colors import select_colors
from menu import Menu



class Game:
    def __init__(self):
        px.init(Screen.width, Screen.height, quit_key=False)
        px.mouse(True)

        self.state = State.MENU
        self.menu = Menu()
        self.colors = select_colors()
        self.circ = Circle()
        self.reach_circ = ReachCircle()
        self.score = Score()

        px.run(self._update, self._draw)

    def _process_keys(self):
        if px.btnp(px.KEY_ESCAPE):
            self.state = State.MENU

        if px.btnp(px.MOUSE_BUTTON_LEFT) or px.btnp(px.KEY_SPACE):
            if self.reach_circ.is_collided_with_circ(self.circ):
                self.score.score += 1

            ###########################################################################
            # NOTE: delete this code block
            self.circ.col = randrange(16)
            self.reach_circ.col = randrange(16)
            Screen.bg = randrange(16)
            ###########################################################################

            self.reach_circ.respawn()
            self.circ.r = 0

    def _update(self):
        ###########################################################################
        # NOTE: delete code below
        # helps to check the colors
        if px.btnp(px.KEY_C):
            with open('colors.txt', 'a') as f:
                f.writelines(f"bg: {Screen.bg}\tfg: {(Screen.bg -3) % 16}\t"
                             f"score: {(Screen.bg - 2) % 16}\n")
        ###########################################################################

        self.menu.update(self)
        self._process_keys()
        self.circ.r += 1

    def _draw(self):
        match self.state:
            case State.MENU:
                self.menu.draw()
            case State.PLAY:
                px.cls(Screen.bg)
                self.reach_circ.draw()
                self.circ.draw(px.mouse_x, px.mouse_y)
                self.score.draw()


if __name__ == '__main__':
    Game()
