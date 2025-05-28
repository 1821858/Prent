import cv2
import numpy as np
import h2o
from h2o.estimators.kmeans import H2OKMeansEstimator

def reduce_colors_cv(image, num_colors):
    
    #Reduces the number of colors in an image using K-means clustering.
    
    # Reshape the image to a 2D array of pixels
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Define criteria, number of clusters(K), and apply KMeans
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


def reduce_colors(image, num_colors):
    
    # Approximate color quantization to 'num_colors' total colors.
    
    # Estimate levels per channel assuming uniform grid in RGB space
    levels = int(round(num_colors ** (1/3)))  # Cube root since RGB = 3 channels
    levels = max(1, min(levels, 256))         # Clamp to valid range

    factor = 256 // levels
    quantized = (image // factor * factor).astype(np.uint8)
    return quantized

def red_view(image, num_colors):
    levels = int(round(num_colors ** (1/3)))
    if (levels > 256):
        levels = 256
    if (levels < 1):
        levels = 1

    factor = 255 // levels
    quantized = (image // factor * factor).astype(np.uint8)
    return quantized

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

# Additional filters can be added here
