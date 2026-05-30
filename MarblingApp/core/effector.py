import numpy as np


class Effector:
    @staticmethod
    def marble(vertices, pos, radius):

        diff = vertices - pos

        dist2 = np.sum(diff * diff, axis=1)

        dist2 = np.maximum(dist2, 0.0001)

        factor = np.sqrt(1 + (radius * radius) / dist2)

        vertices += diff * (factor[:, None] - 1)

    @staticmethod
    def push(vertices, pos, force):

        diff = vertices - pos

        dist2 = np.sum(diff * diff, axis=1)

        forces = force / (dist2 + 1)

        vertices += diff * forces[:, None]

    @staticmethod
    def pull(vertices, pos, force):

        diff = vertices - pos

        dist2 = np.sum(diff * diff, axis=1)

        forces = force / (dist2 + 1)

        vertices -= diff * forces[:, None]

