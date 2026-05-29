import random


class ColorPalette:
    def __init__(self, colors:list[tuple[int,int,int]]):

        self.colors = colors

    def get_random(self) -> tuple[int,int,int]:
        return random.choice(self.colors)

PURPLE_PALETTE = ColorPalette(
    [
        (54, 5, 104),
        (91, 42, 134),
        (119, 133, 172),
        (154, 198, 197),
        (165, 230, 186)
    ]
)