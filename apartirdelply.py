import open3d as o3d
import numpy as np

# Cargar el archivo PLY
def cargar_ply(nombre_archivo):
    pcd = o3d.io.read_point_cloud(nombre_archivo)
    return pcd

# Segmentar una región de interés (ROI) en la nube de puntos
def segmentar_roi(pcd, roi_min, roi_max):
    aabb = o3d.geometry.AxisAlignedBoundingBox(min_bound=roi_min, max_bound=roi_max)
    roi = pcd.crop(aabb)
    return roi

if __name__ == "__main__":
    nombre_archivo_ply = "nubes de puntos/6-90.ply"  # Reemplaza con la ruta de tu archivo PLY

    pcd = cargar_ply(nombre_archivo_ply)

    # Definir las coordenadas de la región de interés (ROI)
    roi_min = np.array([-0.08, -0.08, -0.99])  # Reemplaza con las coordenadas mínimas de la ROI
    roi_max = np.array([0.08, 0.08, -0.7])    # Reemplaza con las coordenadas máximas de la ROI

    # Segmentar la región de interés (ROI)
    roi = segmentar_roi(pcd, roi_min, roi_max)

    # Obtener las coordenadas de los puntos dentro de la ROI
    puntos_roi = np.asarray(roi.points)

    # Encontrar el índice del punto con la coordenada Z más baja (punto más profundo)
    idx_punto_mas_profundo = np.argmin(puntos_roi[:, 2])

    # Cambiar el color del punto más profundo a rosa
    rosa = [1, 0.75, 0.8]  # Color rosa (RGB)
    roi.colors[idx_punto_mas_profundo] = rosa

    # Crear una ventana para visualizar la región de interés (ROI)
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(roi)

    # Configurar la vista para centrarse en la ROI
    vista = vis.get_view_control()
    vista.set_lookat(roi.get_center())  # Enfocar la vista en el centro de la ROI
    vista.set_up([0.8, 1, 1])             # Asegurar que el eje Z esté hacia arriba

    vis.run()  # Iniciar la visualización
    vis.destroy_window()  # Cerrar la ventana cuando termines