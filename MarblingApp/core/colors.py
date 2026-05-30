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

SUMMER_PALETTE = ColorPalette(
    [
        (237, 174, 73),
        (209, 73, 91),
        (0, 121, 140),
        (48, 99, 142),
        (0, 61, 91)
    ]
)

WHITE_PALETTE = ColorPalette(
    [(255,255,255)]
)