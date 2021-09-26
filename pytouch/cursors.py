import pyxel


def plus_sign(x, y, cols, number_of_plus_signs=2, size=10):
    """
    cols - sequence of colors
    """
    inner_padding = 2
    size = 10
    for plus in range(number_of_plus_signs):
        pyxel.rect(
            x, y - (size //  2), size, size, cols[plus % len(cols)]
        ) # vertical
        pyxel.rect(
            x - (size // 2), y, size, size, cols[plus % len(cols)]
        ) # horizontal
