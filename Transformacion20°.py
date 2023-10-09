import open3d as o3d
import numpy as np
import math

def transform_point(point, angle, height):
    """
    Transforma un punto considerando una inclinación.
    
    :param point: Array [x, y, z] que representa el punto.
    :param angle: Ángulo de inclinación del sensor (en grados).
    :param height: Altura del sensor respecto a la superficie.
    
    :return: Array [x', y', z'] del punto transformado.
    """
    x, y, z = point
    
    # Cálculo del factor de corrección debido a la inclinación.
    correction_factor = height / math.cos(math.radians(angle))
    
    # Ajuste en la coordenada z
    delta_z = (height - z) * math.tan(math.radians(angle))
    
    # Ajustamos las coordenadas.
    new_x = x * correction_factor
    new_y = y * correction_factor
    new_z = z + delta_z
    
    return [new_x, new_y, new_z]

def transform_point_cloud(pcd, angle, height):
    """
    Transforma una nube de puntos.
    
    :param pcd: Nube de puntos (objeto PointCloud de Open3D).
    :param angle: Ángulo de inclinación del sensor (en grados).
    :param height: Altura del sensor respecto a la superficie.
    
    :return: Nueva nube de puntos transformada (objeto PointCloud de Open3D).
    """
    points = np.asarray(pcd.points)
    transformed_points = np.apply_along_axis(transform_point, 1, points, angle, height)
    pcd.points = o3d.utility.Vector3dVector(transformed_points)
    return pcd

# Leer la nube de puntos del archivo PLY
pcd = o3d.io.read_point_cloud("Bache_tec_2_17_09_42.ply")

# Aplicar la transformación
angle = 40
height = 1
transformed_pcd = transform_point_cloud(pcd, angle, height)

# Guardar la nube de puntos transformada en otro archivo PLY
o3d.io.write_point_cloud("transformed_outputk1k.ply", transformed_pcd)
