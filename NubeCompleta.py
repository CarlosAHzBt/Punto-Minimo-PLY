import open3d as o3d
import numpy as np

# Cargar el archivo PLY
def cargar_ply(nombre_archivo):
    pcd = o3d.io.read_point_cloud(nombre_archivo)
    return pcd

def eliminar_outliers(pcd, nb_neighbors=1000, std_ratio=0.5):
    pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    return pcd

if __name__ == "__main__":
    nombre_archivo_ply = "merged/Merged mesh1.ply"
    pcd = cargar_ply(nombre_archivo_ply)

    # Eliminar outliers
    pcd = eliminar_outliers(pcd)

    # Definir la superficie fija
    superficie_fija = 0.90  # 1 metro

    # Obtener las coordenadas de los puntos
    puntos = np.asarray(pcd.points)

    # Encontrar el índice del punto con la coordenada Z más baja (punto más profundo)
    idx_punto_mas_profundo = np.argmin(puntos[:, 2])
    # Calcular la superficie estimada (moda de alturas)
    superficie_estimada = np.median(puntos[:, 2])  # Puedes usar median o mean según tu necesidad

    print(f"Superficie estimada: {superficie_estimada:.4f} unidades")

    # Calcular la profundidad del agujero en base a la superficie fija
    profundidad_agujero = puntos[idx_punto_mas_profundo, 2] + superficie_fija

    print(f"Profundidad del agujero desde la superficie fija: {profundidad_agujero:.4f} unidades")
    print(np.min(puntos[:, 0]), np.max(puntos[:,0]))
    # Cambiar el color del punto más profundo a rosa
    rosa = [0.2, 1, 0]  # Color rosa (RGB)
    pcd.colors[idx_punto_mas_profundo] = rosa

    # Crear una ventana para visualizar toda la nube de puntos
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)

    # Configurar la vista para centrarse en la nube de puntos
    vista = vis.get_view_control()
    vista.set_lookat(pcd.get_center())  # Enfocar la vista en el centro de la nube de puntos
    vista.set_up([0, -1, 0])            # Asegurar que el eje Y esté hacia arriba (ajusta según tu preferencia)

    vis.run()  # Iniciar la visualización
    vis.destroy_window()  # Cerrar la ventana cuando termines
