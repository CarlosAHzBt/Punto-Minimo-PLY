import pyrealsense2 as rs

def main():
    # Inicializa el dispositivo RealSense
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)

    # Obtiene la profundidad y la imagen RGB
    depth_frame = pipeline.wait_for_frames().get_depth_frame()
    color_frame = pipeline.wait_for_frames().get_color_frame()

    # Ajusta la densidad de puntos al máximo
    config.depth_points_density = rs.config.DepthPointsDensity.MAXIMUM

    # Transmite la imagen de profundidad en tiempo real
    depth_image = np.asanyarray(depth_frame.get_data())
    cv2.imshow("Depth", depth_image)
    cv2.waitKey(1)

    # Transmite la imagen RGB en tiempo real
    color_image = np.asanyarray(color_frame.get_data())
    cv2.imshow("Color", color_image)
    cv2.waitKey(1)

    # Detiene el dispositivo RealSense
    pipeline.stop()

if __name__ == "__main__":
    main()
