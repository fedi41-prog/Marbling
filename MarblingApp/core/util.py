import math
import math
import numpy as np


def generate_circle_vertices(pos, radius, resolution):
    angles = np.linspace(0, np.pi * 2, resolution, endpoint=False)

    x = pos[0] + np.cos(angles) * radius
    y = pos[1] + np.sin(angles) * radius

    return np.column_stack((x, y))




def subdivide_polygon(points, max_dist):
    """
    points: (N,2) float32
    """

    next_points = np.roll(points, -1, axis=0)

    edges = next_points - points

    dist2 = np.sum(edges * edges, axis=1)

    mask = dist2 > (max_dist * max_dist)

    if not np.any(mask):
        return points

    mids = (points + next_points) * 0.5

    result = np.empty((len(points) + np.count_nonzero(mask), 2), dtype=np.float32)

    write = 0

    for i in range(len(points)):

        result[write] = points[i]
        write += 1

        if mask[i]:
            result[write] = mids[i]
            write += 1

    return result