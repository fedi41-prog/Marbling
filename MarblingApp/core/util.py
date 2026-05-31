import math
import math
import numpy as np
import mapbox_earcut as earcut

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

def triangulate_polygon(points):

    vertices = points.astype("f4")

    rings = np.array([len(vertices)], dtype=np.uint32)

    indices = earcut.triangulate_float32(
        vertices,
        rings
    )

    return vertices, indices




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





def subdivide_mesh(vertices, colors, indices, max_length):
    indices = indices.astype(np.int32, copy=False)
    triangles = indices.reshape(-1, 3)

    # Alle Kanten sammeln
    edges = np.concatenate([
        triangles[:, [0, 1]],
        triangles[:, [1, 2]],
        triangles[:, [2, 0]]
    ])

    # Reihenfolge normalisieren
    edges_sorted = np.sort(edges, axis=1)

    # Doppelte Kanten entfernen
    unique_edges = np.unique(edges_sorted, axis=0)

    # Kantenlängen berechnen
    p1 = vertices[unique_edges[:, 0]]
    p2 = vertices[unique_edges[:, 1]]

    lengths = np.linalg.norm(p2 - p1, axis=1)

    # Zu lange Kanten finden
    split_mask = lengths > max_length

    if not np.any(split_mask):
        return vertices, colors, indices

    split_edges = unique_edges[split_mask]

    # Mittelpunkte der neuen Vertices
    midpoints = (
        vertices[split_edges[:, 0]]
        + vertices[split_edges[:, 1]]
    ) * 0.5

    # Farben interpolieren
    midpoint_colors = (
        colors[split_edges[:, 0]]
        + colors[split_edges[:, 1]]
    ) * 0.5

    midpoint_ids = np.arange(
        len(vertices),
        len(vertices) + len(midpoints)
    )

    edge_to_midpoint = {
        tuple(edge): idx
        for edge, idx in zip(split_edges, midpoint_ids)
    }

    # Neue Vertices/Farben anhängen
    vertices = np.vstack([vertices, midpoints])
    colors = np.vstack([colors, midpoint_colors])

    new_triangles = []

    for a, b, c in triangles:

        mids = {}

        ab = tuple(sorted((a, b)))
        bc = tuple(sorted((b, c)))
        ca = tuple(sorted((c, a)))

        if ab in edge_to_midpoint:
            mids[ab] = edge_to_midpoint[ab]

        if bc in edge_to_midpoint:
            mids[bc] = edge_to_midpoint[bc]

        if ca in edge_to_midpoint:
            mids[ca] = edge_to_midpoint[ca]

        count = len(mids)

        # Keine Kante zu lang
        if count == 0:
            new_triangles.append([a, b, c])

        # Eine Kante splitten
        elif count == 1:

            if ab in mids:
                m = mids[ab]
                new_triangles.extend([
                    [a, m, c],
                    [m, b, c]
                ])

            elif bc in mids:
                m = mids[bc]
                new_triangles.extend([
                    [a, b, m],
                    [a, m, c]
                ])

            else:
                m = mids[ca]
                new_triangles.extend([
                    [a, b, m],
                    [m, b, c]
                ])

        # Alle drei Kanten gesplittet
        elif count == 3:

            mab = mids[ab]
            mbc = mids[bc]
            mca = mids[ca]

            new_triangles.extend([
                [a, mab, mca],
                [mab, b, mbc],
                [mca, mbc, c],
                [mab, mbc, mca]
            ])

        # 2 Kanten gesplittet
        else:
            # Einfachheitshalber erstmal unverändert lassen
            # (kann man später sauber behandeln)
            new_triangles.append([a, b, c])

    return (
        vertices.astype(np.float32),
        colors.astype(np.float32),
        np.array(new_triangles, dtype=np.int32).flatten()
    )