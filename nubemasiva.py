import pyrealsense2 as rs
import numpy as np
import open3d as o3d
import os

# Nombre del archivo .bag que contiene los datos
bag_file = 'nubes de puntos/20230920_085112.bag'

# Directorio donde se guardarán las nubes de puntos individuales (PLY)
output_directory = 'nubes_individuales'

# Crear el directorio si no existe
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Crear un objeto pipeline para leer el archivo .bag
pipeline = rs.pipeline()
config = rs.config()
config.enable_device_from_file(bag_file)
pipeline.start(config)

# Variable para almacenar las primeras 10 nubes de puntos
all_point_clouds = []

# Contador para rastrear cuántas nubes de puntos se han procesado
num_point_clouds_processed = 0

try:
    while num_point_clouds_processed < 10:  # Procesar solo las primeras 10 nubes de puntos
        # Esperar a que llegue un fotograma del archivo .bag
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # Obtener los datos de profundidad como un arreglo numpy
        depth_data = np.asanyarray(depth_frame.get_data())

        # Crear una nube de puntos utilizando Open3D
        pcd = o3d.geometry.PointCloud.create_from_depth_image(
            depth=o3d.geometry.Image(depth_data),
            intrinsic=o3d.camera.PinholeCameraIntrinsic(
                width=depth_frame.width,
                height=depth_frame.height,
                fx=depth_frame.width / 2,
                fy=depth_frame.height / 2,
                cx=depth_frame.width / 2,
                cy=depth_frame.height / 2
            )
        )

        # Guardar la nube de puntos individual en formato PLY
        output_file = os.path.join(output_directory, f'frame_{num_point_clouds_processed}.ply')
        o3d.io.write_point_cloud(output_file, pcd, write_ascii=True)  # Asegurarse de que se escriba en formato ASCII

        # Agregar la nube de puntos a la lista
        all_point_clouds.append(pcd)

        # Incrementar el contador
        num_point_clouds_processed += 1

except RuntimeError:
    pass

finally:
    pipeline.stop()

# Concatenar las nubes de puntos procesadas en una única nube de puntos
final_point_cloud = o3d.geometry.PointCloud()
for pcd in all_point_clouds:
    final_point_cloud += pcd

# Guardar la nube de puntos final en formato PLY
output_file_final = 'nube_puntos_final.ply'
o3d.io.write_point_cloud(output_file_final, final_point_cloud, write_ascii=True)  # Asegurarse de que se escriba en formato ASCII

print(f"Se han procesado y concatenado las primeras 10 nubes de puntos y se guardaron en {output_file_final}")
