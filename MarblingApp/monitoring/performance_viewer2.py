import numpy as np
import matplotlib.pyplot as plt

data = np.load("performance_data.npy")

fps = data[:, 0]
vertices = data[:, 1]
drops = data[:, 2]

# Nach FPS sortieren
sort_idx = np.argsort(fps)

fps = fps[sort_idx]
vertices = vertices[sort_idx]
drops = drops[sort_idx]

# Plot
plt.figure(figsize=(10, 6))
#
#plt.scatter(fps, vertices, s=5, label="Vertices")
#plt.scatter(fps, drops * 1000, s=5, label="Drops * 1000")

plt.scatter(vertices, fps, s=3)

#plt.plot(fps, vertices)

plt.xlabel("vertices")
plt.ylabel("FPS")
plt.title("Performance vs FPS")

plt.legend()
plt.grid(True)

plt.show()