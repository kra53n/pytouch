import pyxel


class Moving:
    def __init__(
            self,
            screen_w,
            screen_h,
            direction,
            element,
        ):
        """
        direction define in what place will move elements. Value in degrees.
        Up - 0 degrees. Right - 90 degrees. Down - 180 degrees.
        Left - 270 degrees.
        """
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.direction = direction
        self.element = element
        self.y = 0

    def draw(self):
        self.y -= 1
        for x in range(2, 160, 6):
            self.element(x, self.y % 120, x, (self.y + 20) % 120, 2)


if __name__ == "__main__":
    pyxel.init(160, 120)
    moving = Moving(
        screen_w  = 160,
        screen_h  = 120,
        direction = 90,
        element   = pyxel.line,
    )

    while True:
        pyxel.cls(3)

        if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()

        moving.draw()

        pyxel.flip()
