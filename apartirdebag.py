import pyrealsense2 as rs
import numpy as np
import os

# Carpeta de destino para las nubes de puntos
output_dir = "pointclouds"

# Verifica si la carpeta existe, si no, la crea
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Configuración de la secuencia
pipeline = rs.pipeline()
config = rs.config()

# Configuramos la fuente de datos para que use el archivo .bag
rs.config.enable_device_from_file(config, "20230920_085112.bag")

# Configuramos para obtener stream de profundidad y color
config.enable_stream(rs.stream.depth)
config.enable_stream(rs.stream.color)

# Inicia la secuencia
profile = pipeline.start(config)

# Decimador para mejorar el rendimiento
decimation = rs.decimation_filter()
decimation.set_option(rs.option.filter_magnitude, 1)

# Definimos la alineación entre color y profundidad
align_to = rs.stream.color
align = rs.align(align_to)

frame_count = 0
try:
    while True:
        # Obtenemos los frames
        frames = pipeline.wait_for_frames()

        # Alineamos la imagen de profundidad a la de color
        aligned_frames = align.process(frames)

        # Tomamos la imagen de profundidad y color
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Decimamos el frame para mejorar rendimiento
        depth_frame = decimation.process(depth_frame)

        # Generamos nube de puntos
        pointcloud = rs.pointcloud()
        points = pointcloud.calculate(depth_frame)
        pointcloud.map_to(color_frame)  # asociar el color a la nube de puntos
        
        # Nombre del archivo y ruta completa
        ply_file = f"frame_{frame_count}.ply"
        full_path = os.path.join(output_dir, ply_file)
        
        # Guardamos en formato .ply en modo textual
        ply_exporter = rs.save_to_ply(full_path)
        ply_exporter.set_option(rs.save_to_ply.option_ply_binary, False)
        ply_exporter.process(points)  # Ahora solo pasamos la nube de puntos
        
        print(f"Saved {full_path}")
        
        frame_count += 1

except Exception as e:
    print(str(e))
finally:
    # Detenemos la secuencia
    pipeline.stop()

