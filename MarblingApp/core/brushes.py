from arcade.examples.happy_face import radius

from MarblingApp.core.effector import Effector


class Brush:
    def __init__(self, canvas):
        self.canvas = canvas


    def on_click_lmb(self, pos):
        pass

    def on_drag_start(self, pos):
        pass

    def on_drag(self, pos):
        pass

    def on_drag_end(self, pos):
        pass

class NewDropBrush(Brush):
    def __init__(self, canvas, radius, color):
        super().__init__(canvas)
        self.radius = radius
        self.color = color

    def on_click_lmb(self, pos):
        self.canvas.add_drop(pos, self.radius, self.color)

class ExpandBrush(Brush):
    def __init__(self, canvas, radius):
        super().__init__(canvas)
        self.drag_start_pos = (0, 0)
        self.radius = radius

    def on_click_lmb(self, pos):
        Effector.push(self.canvas.vertices, pos, radius)

