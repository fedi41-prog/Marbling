from MarblingApp.core.brushes import CurrentBrush
from MarblingApp.core.effector import Effector
from MarblingApp.core.util import generate_circle_vertices, subdivide_polygon, triangulate_polygon, subdivide_mesh
import numpy as np




class Canvas:

    COLOR = (60, 120, 60)

    def __init__(self):

        # vertices
        self.vertices = np.empty((0, 2), dtype=np.float32)
        # triangles
        self.indices = np.empty(0, dtype=np.int32)
        # colors
        self.colors = np.empty((0, 3), dtype=np.float32)

        # polygon-bereiche
        #self.shapes = []

        self.dirty = False

        self.current_brush = CurrentBrush(self)

    #def draw(self, polygon_function):
#
    #    for start, end, color in self.shapes:
#
    #        poly = self.vertices[start:end]
#
    #        polygon_function(poly, color)

    #def get_polygons(self):
    #    for start, end, color in self.shapes:
    #        poly = self.vertices[start:end]
    #        yield poly, color

    def vertex_count(self):
        return self.vertices.shape[0]
    #def drop_count(self):
    #    return len(self.shapes)

    def after_effect(self):
        self.vertices, self.colors, self.indices  = subdivide_mesh(
            self.vertices,
            self.colors,
            self.indices,

            15
        )
        self.dirty = True

    def reset_dirty_flag(self):
        self.dirty = False

    def add_shape(self, outline, color=(40, 60, 40)):
        vertices, indices = triangulate_polygon(outline)

        colors = np.full((len(vertices), 3), np.array(color)/255)

        indices += len(self.vertices)

        self.vertices = np.concatenate((self.vertices, vertices))
        self.indices = np.concatenate((self.indices, indices))
        self.colors = np.concatenate((self.colors, colors))




    #def __subdivide_all(self, max_dist=10):
#
    #    new_vertices = []
    #    new_shapes = []
#
    #    offset = 0
#
    #    for start, end, color in self.shapes:
    #        poly = self.vertices[start:end]
#
    #        poly = subdivide_polygon(poly, max_dist)
#
    #        new_start = offset
    #        new_end = offset + len(poly)
#
    #        new_shapes.append((new_start, new_end, color))
#
    #        new_vertices.append(poly)
#
    #        offset = new_end
#
    #    self.vertices = np.vstack(new_vertices)
    #    self.shapes = new_shapes