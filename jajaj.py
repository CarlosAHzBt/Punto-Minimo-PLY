import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def read_xyz(file_path):
    with open(file_path, 'r') as file:
        points = []
        for line in file:
            x, y, z = map(float, line.strip().split(','))
            points.append((x, y, z))
    return points

def plot_points(points):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    xs, ys, zs = zip(*points)
    
    ax.scatter(xs, ys, zs, marker='o')
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    
    plt.show()

# Example usage:
# Assuming that 'output.xyz' is the file with the 3D coordinates.
points = read_xyz('Bache  Balbuena\Escaneo #1\Bache_2_11_36_16.xyz')
plot_points(points)
