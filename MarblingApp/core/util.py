import math
import math
import numpy as np


def generate_circle_vertices(pos, radius, resolution):
    angles = np.linspace(0, np.pi * 2, resolution, endpoint=False)

    x = pos[0] + np.cos(angles) * radius
    y = pos[1] + np.sin(angles) * radius

    return np.column_stack((x, y))

def generate_star_vertices(center, outer_radius, inner_radius, points=5, resolution=10):
    cx, cy = center

    # Eckpunkte erzeugen
    vertices = []

    for i in range(points * 2):
        angle = i * np.pi / points - np.pi / 2

        if i % 2 == 0:
            r = outer_radius
        else:
            r = inner_radius

        x = cx + np.cos(angle) * r
        y = cy + np.sin(angle) * r

        vertices.append([x, y])

    vertices = np.array(vertices, dtype=np.float32)

    # Kanten auffüllen
    result = []

    for i in range(len(vertices)):
        a = vertices[i]
        b = vertices[(i + 1) % len(vertices)]

        t = np.linspace(0, 1, resolution, endpoint=False)
        edge = a + (b - a) * t[:, None]

        result.extend(edge)

    return np.array(result, dtype=np.float32)



def subdivide_polygon(points, max_dist):
    next_points = np.roll(points, -1, axis=0)

    edges = next_points - points

    dist2 = np.sum(edges * edges, axis=1)

    mask = dist2 > (max_dist * max_dist)

    if not np.any(mask):
        return points

    mids = (points + next_points) * 0.5

    n = len(points)

    out_mask = np.ones(n + np.count_nonzero(mask), dtype=bool)

    insert_pos = np.where(mask)[0] + np.arange(np.count_nonzero(mask)) + 1

    out_mask[insert_pos] = False

    result = np.empty((len(out_mask), 2), dtype=np.float32)

    result[out_mask] = points
    result[~out_mask] = mids[mask]

    return result