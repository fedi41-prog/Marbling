import numpy as np
import matplotlib.pyplot as plt

# Datei laden
data = np.load("performance_data.npy")

# Spalten extrahieren
fps = data[:, 0]
vertex_count = data[:, 1]
drop_count = data[:, 2]

print("Einträge:", len(data))

print("\nFPS:")
print(" Durchschnitt:", np.mean(fps))
print(" Minimum:", np.min(fps))
print(" Maximum:", np.max(fps))

print("\nVertices:")
print(" Durchschnitt:", np.mean(vertex_count))
print(" Maximum:", np.max(vertex_count))

print("\nDrops:")
print(" Durchschnitt:", np.mean(drop_count))
print(" Maximum:", np.max(drop_count))

# Graphen
plt.figure(figsize=(10, 6))

plt.plot(fps, label="FPS")
plt.plot(vertex_count / 10000, label="Vertices / 10 000")
plt.plot(drop_count, label="Drops")

plt.legend()
plt.xlabel("Tick")
plt.ylabel("Value")
plt.title("Performance Analysis")

plt.show()