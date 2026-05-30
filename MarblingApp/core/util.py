import math
import math
import numpy as np


def generate_circle_vertices(pos, radius, resolution):
    angles = np.linspace(0, np.pi * 2, resolution, endpoint=False)

    x = pos[0] + np.cos(angles) * radius
    y = pos[1] + np.sin(angles) * radius

    return np.column_stack((x, y))




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