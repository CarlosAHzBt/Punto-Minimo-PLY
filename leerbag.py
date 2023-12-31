# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

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

# Create opencv window to render image in
cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)

# Create colorizer object
colorizer = rs.colorizer()

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
    # if pressed escape exit program
    if key == 27:
        cv2.destroyAllWindows()
        break
