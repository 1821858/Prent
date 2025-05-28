import cv2
import numpy as np
import Filters

def polygonize_effect(frame, args):
    """
    Applies a polygonal effect to the frame.
    """
    # reduced_frame = Filters.reduce_colors(frame, args.num_colors) 
    reduced_frame = Filters.reduce_colors(frame, args.num_colors)
    polygon_frame = Filters.polygonize(reduced_frame, args.num_polygons)
    return polygon_frame

def red_view(frame, args):
    """
    """

    reduced_frame = Filters.red_view(frame, args.num_colors)
    polygon_frame = Filters.polygonize(reduced_frame, args.num_polygons)
    return polygon_frame

def color_reduction(frame, args):
    return Filters.reduce_colors(frame, args.num_colors)

def cartoon_effect(frame, args):
    """
    Applies a cartoon effect to the frame.
    """
    num_down = 2       # Number of downsampling steps
    num_bilateral = 7  # Number of bilateral filtering steps

    img_color = frame.copy()
    # Downsample image using Gaussian pyramid
    for _ in range(num_down):
        img_color = cv2.pyrDown(img_color)

    # Apply bilateral filter multiple times
    for _ in range(num_bilateral):
        img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=9, sigmaSpace=7)

    # Upsample image to original size
    for _ in range(num_down):
        img_color = cv2.pyrUp(img_color)

    # Convert to grayscale and apply median blur
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    # Detect and enhance edges
    img_edge = cv2.adaptiveThreshold(
        img_blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=9,
        C=2
    )

    # Convert back to color and combine with color image
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(img_color, img_edge)

    return cartoon

def sketch_effect(frame, args):
    """
    Applies a pencil sketch effect to the frame.
    """
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    inverted_gray_image = 255 - gray_image
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
    inverted_blurred_image = 255 - blurred_image
    sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
    sketch_image = cv2.cvtColor(sketch_image, cv2.COLOR_GRAY2BGR)
    return sketch_image

#def prototype_effect(frame, args):
#    int i = 0
#    if skip:


# Define the effects dictionary at module level
effects = {
    'polygonize': polygonize_effect,
    'cartoon': cartoon_effect,
    'sketch': sketch_effect,
    'reduce': color_reduction,
    'red_view': red_view,

    # Add more effects here
}

def get_effect_function(effect_name):
    return effects.get(effect_name)

def get_available_effects():
    return list(effects.keys())

