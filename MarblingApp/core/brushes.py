import numpy as np

from MarblingApp.core.effector import Effector
from MarblingApp.core.util import generate_circle_vertices


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

    def on_hold_lmb(self, pos):
        pass

class NewDropBrush(Brush):
    def __init__(self, canvas, radius, color):
        super().__init__(canvas)
        self.radius = radius
        self.color = color

    def on_click_lmb(self, pos):
        # erst alle existierenden verformen
        if len(self.canvas.vertices) > 0:
            Effector.marble(self.canvas.vertices, np.array(pos), self.radius)

        # neue vertices erzeugen
        verts = generate_circle_vertices(pos, self.radius, 200).astype(np.float32)

        start = len(self.canvas.vertices)
        end = start + len(verts)

        # anhängen
        self.canvas.vertices = np.vstack((self.canvas.vertices, verts))

        # polygon merken
        self.canvas.shapes.append((start, end, self.color))

        self.canvas.subdivide_all()
    def on_hold_lmb(self, pos):
        Effector.push(self.canvas.vertices, pos, self.radius)
        self.canvas.subdivide_all()

class ExpandBrush(Brush):
    def __init__(self, canvas, radius):
        super().__init__(canvas)
        self.drag_start_pos = (0, 0)
        self.radius = radius

    def on_hold_lmb(self, pos):
        Effector.push(self.canvas.vertices, pos, self.radius)
        self.canvas.subdivide_all()

class BrushManager:
    def __init__(self, canvas):
        self.canvas = canvas


        self.current = 0
        self.brushes = [
            NewDropBrush(canvas, 60, (60, 120, 60)),
            ExpandBrush(canvas, 20)
        ]
    def set_brush_id(self, idx):
        self.current = idx

    def next_brush(self):
        self.current += 1
        if self.current >= len(self.brushes): self.current = 0

    def current_brush(self):
        return self.brushes[self.current]


