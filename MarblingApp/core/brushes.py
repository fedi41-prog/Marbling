import numpy as np

from MarblingApp.core.effector import Effector
from MarblingApp.core.util import generate_circle_vertices, generate_star_vertices


class Brush:
    def __init__(self, canvas):
        self.canvas = canvas
        self.radius = 100
        self.color = (60, 120, 60)

    def update_stats(self, radius, color):
        self.radius = radius
        self.color = color

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

class DynamicDropBrush(Brush):
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

        self.canvas.after_effect()
    def on_hold_lmb(self, pos):
        Effector.push(self.canvas.vertices, pos, self.radius)
        self.canvas.after_effect()


class CircleBrush(Brush):
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

        self.canvas.after_effect()

class OverlayDropBrush(Brush):
    def on_click_lmb(self, pos):
        # neue vertices erzeugen
        verts = generate_circle_vertices(pos, self.radius, 200).astype(np.float32)

        start = len(self.canvas.vertices)
        end = start + len(verts)

        # anhängen
        self.canvas.vertices = np.vstack((self.canvas.vertices, verts))

        # polygon merken
        self.canvas.shapes.append((start, end, self.color))

        self.canvas.after_effect()

class StarBrush(Brush):
    def on_click_lmb(self, pos):
        # erst alle existierenden verformen
        if len(self.canvas.vertices) > 0:
            Effector.marble(self.canvas.vertices, np.array(pos), self.radius)

        # neue vertices erzeugen
        verts = generate_star_vertices(pos, self.radius, self.radius/2.5, 5, 200)

        start = len(self.canvas.vertices)
        end = start + len(verts)

        # anhängen
        self.canvas.vertices = np.vstack((self.canvas.vertices, verts))

        # polygon merken
        self.canvas.shapes.append((start, end, self.color))

        self.canvas.after_effect()

class ExpandBrush(Brush):
    def on_hold_lmb(self, pos):
        Effector.push(self.canvas.vertices, pos, self.radius)
        self.canvas.after_effect()

class TineLineBrush(Brush):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.drag_start = None
        self.z = 100
        self.c = 100

    def on_drag_start(self, pos):
        self.drag_start = np.array(pos)

    def on_drag_end(self, pos):
        pos = np.array(pos)

        pl = pos - self.drag_start
        norm = np.linalg.norm(pl)
        if norm < 1e-8:
            return

        m = pl / norm
        n = np.array([-m[1], m[0]])

        pb = self.canvas.vertices - self.drag_start

        d = np.abs(np.dot(pb, n))

        u = 0.5 * (1 / self.c)

        factor = np.pow(u, d) * self.z
        self.canvas.vertices += m * factor[:, None]

        self.canvas.after_effect()


class CurrentBrush:
    def __init__(self, canvas):
        self.canvas = canvas

        self.radius = 100
        self.color = (60, 120, 60)

        self._current_id = 0
        self._brushes = [
            CircleBrush(canvas),
            OverlayDropBrush(canvas),
            StarBrush(canvas),
            ExpandBrush(canvas)
        ]

    def update_brushes(self):
        for b in self._brushes:
            b.update_stats(self.radius, self.color)

    def set_brush_id(self, idx):
        self._current_id = idx
        print(self._brushes[self._current_id].__class__.__name__)

    def next_brush(self):
        self._current_id += 1
        if self._current_id >= len(self._brushes): self._current_id = 0
        print(type(self._brushes[self._current_id]))

    def get(self):
        return self._brushes[self._current_id]


