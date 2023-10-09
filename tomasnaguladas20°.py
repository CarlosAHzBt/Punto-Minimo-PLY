import numpy as np
import open3d as o3d

def transformar_puntos(pcd, angulo_grados):
    angulo_rad = -np.deg2rad(angulo_grados)
    R = o3d.geometry.get_rotation_matrix_from_axis_angle([1 * angulo_rad, 0, 0]) # Suponiendo que el eje de rotación es x
    pcd.rotate(R)
    return pcd

def ajustar_plano(pcd):
    plano_modelo, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
    return plano_modelo

def calcular_distancia_al_plano(punto, plano):
    a, b, c, d = plano
    x, y, z = punto
    return abs(a*x + b*y + c*z + d) / np.sqrt(a*a + b*b + c*c)

def visualizar_punto_profundo(pcd, idx):
    rosa = [1, 0, 1]  # Color rosa (RGB)
    colores = np.asarray(pcd.colors)
    colores[idx] = rosa
    pcd.colors = o3d.utility.Vector3dVector(colores)
    o3d.visualization.draw_geometries([pcd])

def visualizar_pcd(pcd, titulo="Nube de Puntos"):
    o3d.visualization.draw_geometries([pcd], window_name=titulo)

def eliminar_outliers(pcd, nb_neighbors=100, std_ratio=1):
    pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    return pcd
def guardar_ply_girado(pcd, angulo_grados):
    angulo_rad = -np.deg2rad(angulo_grados)
    R = o3d.geometry.get_rotation_matrix_from_axis_angle([1 * angulo_rad, 0, 0]) # Suponiendo que el eje de rotación es x
    pcd.rotate(R)
    o3d.io.write_point_cloud("girado20grados", pcd)
    return pcd

if __name__ == "__main__":
    pcd = o3d.io.read_point_cloud("1mt 20grados/1.ply")
      # Eliminar outliers
    pcd = eliminar_outliers(pcd)

    # Visualizar la nube de puntos original
    visualizar_pcd(pcd, "Original")
  
    pcd_transformado = transformar_puntos(pcd, -20)

    # Visualizar la nube de puntos transformada
    #visualizar_pcd(pcd_transformado, "Transformado")
    
    plano = ajustar_plano(pcd_transformado)
    distancias = [calcular_distancia_al_plano(punto, plano) for punto in np.asarray(pcd_transformado.points)]
    idx_punto_mas_profundo = np.argmin(distancias)

    profundidad = 1 - distancias[idx_punto_mas_profundo]
    print(f"Profundidad del punto más profundo relativa al suelo: {profundidad:.4f} unidades")

    visualizar_punto_profundo(pcd_transformado, idx_punto_mas_profundo)

    # Guardar la nube de puntos transformada
    o3d.io.write_point_cloud("girado20grados.ply", pcd_transformado)
    
