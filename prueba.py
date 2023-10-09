import open3d as o3d
import numpy as np

def parse_ply(file_path):
    with open(file_path, 'rb') as f:
        if b"ply" not in f.readline():
            raise ValueError("The file does not appear to be a PLY file.")
        
        vertex_count = 0
        while True:
            line = f.readline().strip()
            if b"element vertex" in line:
                vertex_count = int(line.split()[2])
            elif b"end_header" in line:
                break
        
        dtype = np.dtype([
            ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
            ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')
        ])
        data = np.fromfile(f, dtype=dtype, count=vertex_count)
        return data['x'], data['y'], data['z'], data['red'], data['green'], data['blue']

# Parse the PLY file
x, y, z, _, _, _ = parse_ply('C:/Users/carlo/Documents/repetidas 90 cm/2.ply')

# Convert points to a numpy array
points = np.vstack((x, y, z)).T

# Create a PointCloud object
pcd_original = o3d.geometry.PointCloud()
pcd_original.points = o3d.utility.Vector3dVector(points)

# Visualize the original point cloud
o3d.visualization.draw_geometries([pcd_original], window_name='Original Point Cloud')

# Rotation matrix
theta = np.deg2rad(-20) 
rotation_matrix = np.array([
    [1, 0, 0],
    [0, np.cos(theta), -np.sin(theta)],
    [0, np.sin(theta), np.cos(theta)]
])

# Apply rotation
rotated_points = np.dot(points, rotation_matrix.T)

# Create a PointCloud object for rotated points
pcd_rotated = o3d.geometry.PointCloud()
pcd_rotated.points = o3d.utility.Vector3dVector(rotated_points)

# Visualize the rotated point cloud
o3d.visualization.draw_geometries([pcd_rotated], window_name='Rotated Point Cloud')
