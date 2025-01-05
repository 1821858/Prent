import cv2
import numpy as np
import argparse

def reduce_colors(image, num_colors):
    """
    Reduces the number of colors in an image using K-means clustering.
    """
    # Reshape the image to a 2D array of pixels
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Define criteria, number of clusters(K) and apply KMeans
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
    _, labels, centers = cv2.kmeans(
        pixel_values, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    # Convert back to 8-bit colors
    centers = np.uint8(centers)
    labels = labels.flatten()
    reduced_image = centers[labels.flatten()]
    reduced_image = reduced_image.reshape(image.shape)

    return reduced_image

def polygonize(image, num_polygons):
    """
    Converts an image into a polygonal representation.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours from edges
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Sort contours by area and select the top 'num_polygons' contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:num_polygons]

    # Create a blank image to draw polygons
    polygon_image = np.zeros_like(image)

    # Draw and fill contours on the blank image
    cv2.drawContours(polygon_image, contours, -1, (255, 255, 255), cv2.FILLED)

    # Mask the original image with the polygon image
    masked_image = cv2.bitwise_and(image, polygon_image)

    return masked_image

def process_frame(frame, num_colors, num_polygons):
    """
    Processes a single video frame to reduce colors and apply polygonal effect.
    """
    reduced_frame = reduce_colors(frame, num_colors)
    polygon_frame = polygonize(reduced_frame, num_polygons)
    return polygon_frame

def main():
    parser = argparse.ArgumentParser(description="Polygonal Video Renderer")
    parser.add_argument("input_video", help="Path to input video file")
    parser.add_argument("output_video", help="Path to output video file")
    parser.add_argument(
        "--num_polygons",
        type=int,
        default=100,
        help="Number of polygons per frame (default: 100)",
    )
    parser.add_argument(
        "--num_colors",
        type=int,
        default=8,
        help="Number of colors per frame (default: 8)",
    )
    args = parser.parse_args()

    # Open the input video file
    cap = cv2.VideoCapture(args.input_video)
    if not cap.isOpened():
        print("Error: Cannot open the video file.")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(args.output_video, fourcc, fps, (width, height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame
        processed_frame = process_frame(
            frame, args.num_colors, args.num_polygons
        )

        # Write the frame to the output video
        out.write(processed_frame)

        frame_count += 1
        print(
            f"Processing frame {frame_count}/{total_frames}", end="\r"
        )

    # Release resources
    cap.release()
    out.release()
    print("\nVideo processing complete.")

if __name__ == "__main__":
    main()
