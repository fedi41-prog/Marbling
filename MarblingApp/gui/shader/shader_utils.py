import numpy as np
import mapbox_earcut as earcut

def normalize(points, screen_width, screen_height):
    points = points.astype("f4").copy()

    points[:, 0] = (points[:, 0] / screen_width) * 2.0 - 1.0
    points[:, 1] = 1.0 - (points[:, 1] / screen_height) * 2.0

    return points


def create_dashed_circle(pos, radius, resolution=256,
                         dash_length=6, gap_length=4):

    vertices = []

    cycle = dash_length + gap_length

    for i in range(resolution):

        if (i % cycle) >= dash_length:
            continue

        angle = (i / resolution) * np.pi * 2

        x = pos[0] + np.cos(angle) * radius
        y = pos[1] + np.sin(angle) * radius

        vertices.append((x, y))

    return np.array(vertices, dtype="f4")

def create_circle(center, radius, segments=64):
    vertices = []

    for i in range(segments + 1):
        angle = i / segments * 2 * np.pi
        x = center[0] + np.cos(angle) * radius
        y = center[1] + np.sin(angle) * radius
        vertices.append((x, y))

    return vertices

def triangulate_polygon(points):

    vertices = points.astype("f4")

    rings = np.array([len(vertices)], dtype=np.uint32)

    indices = earcut.triangulate_float32(
        vertices,
        rings
    )

    return vertices, indices

