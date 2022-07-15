import pyxel as px

from elements import Text, Score, Health, Circle, ReachCircle, one_of_keys
from constants import Screen, State
from colors import ColorPalette
from settings import Settings
from music import Music
from menu import Menu


class Game:
    def __init__(self):
        px.init(Screen.width, Screen.height, quit_key=False)
        px.load('assets/assets.pyxres')
        px.mouse(True)

        self.state = State.MENU
        self.color_palette = ColorPalette()
        self.music = Music()
        self.menu = Menu()
        self.settings = Settings()
        self.score = Score()
        self.health = Health()
        self.user_circ = Circle()
        self.reach_circ = ReachCircle()

        px.run(self._update, self._draw)

    def _reload_game(self):
        self.score.score = 0
        self.user_circ.r = 0
        self.health.health = self.health.max_health
        self.state = State.PLAY

    def _update(self):
        self.menu.update(self)

        match self.state:
            case State.PLAY:
                if one_of_keys(px.MOUSE_BUTTON_LEFT, px.KEY_SPACE):
                    if self.reach_circ.is_collided_with_circ(self.user_circ):
                        self.score.score += 1
                        self.music.play('user_reach')
                    else:
                        self.health.health -= 1
                        self.music.play('user_missed')
                    self.color_palette.update()
                    self.reach_circ.respawn()
                    self.user_circ.r = 0
                self.user_circ.r += 1
                if self.health.is_gameover():
                    self.state = State.GAMEOVER

            case State.GAMEOVER:
                if px.btnp(px.KEY_ESCAPE):
                    px.mouse(True)
                    self.state = State.MENU
                if one_of_keys(px.KEY_R, px.KEY_RETURN):
                    self._reload_game()

            case State.SETTINGS:
                if px.btnp(px.KEY_ESCAPE) and self.settings.state == self.settings.state.NONSELECTED:
                    filename = self.settings.color_chooser.get_option()
                    self.color_palette.colors = f'{filename}.yaml'
                    self.state = State.MENU
                    px.mouse(True)

    def _draw(self):
        match self.state:
            case State.MENU:
                self.menu.draw()
            case State.PLAY:
                px.cls(Screen.bg)
                self.score.draw()
                self.health.draw()
                self.reach_circ.draw()
                self.user_circ.draw(px.mouse_x, px.mouse_y)
            case State.GAMEOVER:
                px.cls(Screen.bg)
                Text(f'Your score: {self.score.score}\nPress R to reload game!').draw()
            case State.SETTINGS:
                self.settings.update(self)
                self.settings.draw()


if __name__ == '__main__':
    Game()
