import arcade

from MarblingApp.core.colors import PURPLE_PALETTE
from MarblingApp.core.canvas import Canvas


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Marbling test"

BG_COLOR = (10, 13, 20)

COLOR_PALETTE = PURPLE_PALETTE


class Game(arcade.Window):

    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
            antialiasing=True
        )

        arcade.set_background_color(BG_COLOR)

        self.canvas = Canvas()

        self.canvas.add_drop(
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            100
        )

        self.canvas.add_drop(
            (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2),
            100
        )

        self.current_color = COLOR_PALETTE.get_random()

    def new_drop(self, pos, radius,
                 color=(60, 120, 60),
                 resolution=1000):

        self.canvas.add_drop(
            pos,
            radius,
            color,
            resolution
        )

    def on_draw(self):

        self.clear()

        self.canvas.draw(lambda poly, color: arcade.draw_polygon_filled(poly.tolist(), color))

    def on_mouse_press(self, x, y, button, modifiers):

        self.current_color = COLOR_PALETTE.get_random()

        self.new_drop(
            (x, y),
            100,
            color=self.current_color
        )


if __name__ == "__main__":

    game = Game()

    arcade.run()