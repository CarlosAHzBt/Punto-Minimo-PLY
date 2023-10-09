import pyrealsense2 as rs

# Declare pointcloud object, for calculating point clouds and texture mappings
pc = rs.pointcloud()
# We want the points object to be persistent so we can display the last cloud when a frame drops
points = rs.points()

# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()
config = rs.config()
# Enable depth stream
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

# Start streaming with chosen configuration
profile = pipe.start(config)

# Load configurations from a JSON file
device = profile.get_device()
advanced_mode = rs.rs400_advanced_mode(device)
with open("configHD1280.json", "r") as file:
    json_string = file.read().strip()
    advanced_mode.load_json(json_string)

# Iniciar filtros
decimation = rs.decimation_filter()
decimation.set_option(rs.option.filter_magnitude,1)

threshold = rs.threshold_filter(min_dist=0.3, max_dist=3) # Puedes ajustar estos valores

spatial = rs.spatial_filter()
spatial.set_option(rs.option.filter_magnitude, 2)
spatial.set_option(rs.option.filter_smooth_alpha, 0.25)
spatial.set_option(rs.option.filter_smooth_delta,50)

temporal = rs.temporal_filter()
temporal.set_option(rs.option.filter_smooth_alpha, 1)
temporal.set_option(rs.option.filter_smooth_delta, 100)

hole_filling = rs.hole_filling_filter()
hole_filling.set_option(rs.option.holes_fill, 1)  # Puedes variar el valor: 0, 1 o 2

disparity_transform = rs.disparity_transform(True)
disparity_transform_back = rs.disparity_transform(False)


# We'll use the colorizer to generate texture for our PLY
# (alternatively, texture can be obtained from color or infrared stream)
colorizer = rs.colorizer()

try:
    # Wait for the next set of frames from the camera
    #frames = pipe.wait_for_frames()
    depth_frame = pipe.wait_for_frames()

    # Aplicar los filtrosx

    depth_frame = decimation.process(depth_frame)
    depth_frame = hole_filling.process(depth_frame)
    depth_frame = threshold.process(depth_frame)
    depth_frame = spatial.process(depth_frame)
   #depth_frame = temporal.process(depth_frame)
   #depth_frame = disparity_transform.process(depth_frame)
   #depth_frame = disparity_transform_back.process(depth_frame)
#
    colorized = colorizer.process(depth_frame)

    # Create save_to_ply object
    ply = rs.save_to_ply("1.ply")

    # Set options to the desired values
    # In this example, we'll generate a textual PLY with normals (mesh is already created by default)
    ply.set_option(rs.save_to_ply.option_ply_binary, False)
    ply.set_option(rs.save_to_ply.option_ply_normals, True)

    print("Saving to 1.ply...")
    # Apply the processing block to the frameset which contains the depth frame and the texture
    ply.process(colorized)
    print("Done")
finally:
    pipe.stop()
