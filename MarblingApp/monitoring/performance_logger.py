import numpy as np
from datetime import datetime


class PerformanceLogger:
    def __init__(self):
        self.data = []

    def tick(self, fps, vertex_count, drop_count):
        self.data.append((fps, vertex_count, drop_count))

    def as_np_array(self):
        return np.array(self.data)

    def save(self, filename=None):
        arr = self.as_np_array()

        np.save(filename, arr)

        print(f"Saved {len(arr)} entries to '{filename}'")