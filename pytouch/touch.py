import pyxel
from random import randint


SCREEN = {
    "width" : 192,
    "height": 108,
    "bg"    : 0,
}


class Score:
    def __init__(self, padding_right=2, padding_top=2):
        self.padding_right = padding_right
        self.padding_top   = padding_top
        self.score         = 0

    def increase(self):
        self.score += 1

    def reduce(self):
        self.score -= 1

    def draw(self):
        pyxel.text(
            self.padding_right,
            self.padding_top,
            f"Score: {self.score}",
            (SCREEN["bg"] - 2) % 16
        )


class Circle:
    def __init__(self):
        self._r   = 0
        self._col = (SCREEN["bg"] - 1) % 16

    def zero(self):
        self._r = 0

    def increase(self, size=1):
        self._r += size

    @property
    def r(self):
        return self._r
    
    @r.setter
    def r(self, r):
        self._r = r

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, color):
        self._col = color

    def draw(self, x, y):
        pyxel.circ(x, y, self._r, self._col)


class ReachCircle(Circle):
    def __init__(self):
        super().__init__()
        self.respawn()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def respawn(self):
        self._r = randint(20, min(SCREEN["width"], SCREEN["height"]) // 2) - 4
        self._x = randint(self._r, SCREEN["width"] - self._r)
        self._y = randint(self._r, SCREEN["height"] - self._r)

    def draw(self):
        pyxel.circ(self._x, self._y, self._r, self._col)
        pyxel.circ(self._x, self._y, self._r - 2, SCREEN["bg"])


class App:
    def __init__(self):
        pyxel.init(SCREEN["width"], SCREEN["height"])
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

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.circ.col = (SCREEN["bg"] - 3) % 16
            self.reach_circ.col = (SCREEN["bg"] - 3) % 16
            self.reach_circ.respawn()

            SCREEN["bg"] = (SCREEN["bg"] + 1) % 16

            if self._hit_checking():
                self.score.increase()

            self.circ.zero()

    def _draw(self):
        pyxel.cls(SCREEN["bg"])

        self.circ.increase()
        self.reach_circ.draw()
        self.circ.draw(pyxel.mouse_x, pyxel.mouse_y)
        self.score.draw()


if __name__ == "__main__":
    App()
