from MarblingApp.core.effector import Effector
from MarblingApp.core.util import generate_circle_vertices, subdivide_polygon
import numpy as np




class Canvas:

    COLOR = (60, 120, 60)

    def __init__(self):

        # ALLE punkte in EINEM array
        self.vertices = np.empty((0, 2), dtype=np.float32)

        # polygon-bereiche
        self.shapes = []

    def add_drop(self, pos, radius, color=COLOR, resolution=100):

        # erst alle existierenden verformen
        if len(self.vertices) > 0:
            Effector.marble(self.vertices, np.array(pos), radius)

        # neue vertices erzeugen
        verts = generate_circle_vertices(pos, radius, resolution).astype(np.float32)

        start = len(self.vertices)
        end = start + len(verts)

        # anhängen
        self.vertices = np.vstack((self.vertices, verts))

        # polygon merken
        self.shapes.append((start, end, color))

        self.subdivide_all()

    def draw(self, polygon_function):

        for start, end, color in self.shapes:

            poly = self.vertices[start:end]

            polygon_function(poly, color)

    def get_polygons(self):
        for start, end, color in self.shapes:
            poly = self.vertices[start:end]
            yield poly, color

    def vertex_count(self):
        return self.vertices.size
    def drop_count(self):
        return len(self.shapes)

    def subdivide_all(self, max_dist=10):

        new_vertices = []
        new_shapes = []

        offset = 0

        for start, end, color in self.shapes:
            poly = self.vertices[start:end]

            poly = subdivide_polygon(poly, max_dist)

            new_start = offset
            new_end = offset + len(poly)

            new_shapes.append((new_start, new_end, color))

            new_vertices.append(poly)

            offset = new_end

        self.vertices = np.vstack(new_vertices)
        self.shapes = new_shapes