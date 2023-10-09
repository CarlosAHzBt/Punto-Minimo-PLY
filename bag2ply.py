# First import library
import pyrealsense2 as rs
import numpy as np
import cv2
import argparse
import os.path
import open3d as o3d  # Importa open3d

# Aquí asigna la ruta del archivo bag directamente en el código
bag_file_path = "20230920_085112.bag"

# Create pipeline
pipeline = rs.pipeline()

# Create a config object
config = rs.config()

# Tell config that we will use a recorded device from the specified bag file
rs.config.enable_device_from_file(config, bag_file_path)

# Configure the pipeline to stream the depth stream
# Change this parameters according to the recorded bag file resolution
config.enable_stream(rs.stream.depth, rs.format.z16, 30)

# Start streaming from file
pipeline.start(config)

# Create colorizer object
colorizer = rs.colorizer()

# Variable para verificar si es el primer frame
first_frame = True

# Streaming loop
while True:
    # Get frameset of depth
    frames = pipeline.wait_for_frames()

    # Get depth frame
    depth_frame = frames.get_depth_frame()

    # Colorize depth frame to jet colormap
    depth_color_frame = colorizer.colorize(depth_frame)

    # Convert depth_frame to numpy array to render image in opencv
    depth_color_image = np.asanyarray(depth_color_frame.get_data())

    # Render image in opencv window
    cv2.imshow("Depth Stream", depth_color_image)
    key = cv2.waitKey(1)
    
    if first_frame and depth_frame:
        # Si es el primer frame y hay un frame de profundidad
        points = rs.pointcloud()
        points.map_to(depth_frame)
        pc = points.calculate(depth_frame)
        # Obtener los vértices de la nube de puntos como un arreglo NumPy
        vertices = np.asarray(pcd.points)

        # Convertir la nube de puntos a un objeto open3d
        pointcloud = o3d.geometry.PointCloud()
        pointcloud.points = o3d.utility.Vector3dVector(np.asarray(pc.get_vertices()))
        
        # Guardar la nube de puntos en un archivo PLY
        o3d.io.write_point_cloud("primer_frame.ply", pointcloud)
        
        first_frame = False
    
    # Si se presiona Escape, salir del programa
    if key == 27:
        cv2.destroyAllWindows()
        break
