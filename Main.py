import cv2
import numpy as np
import argparse
import Filters
import Effects
import os
import cProfile
from ArgParse import *
import cProfile

def render(args):
    # Incorrect input handling
    if args.help_effects or args.input_file is None or args.effect_name is None:
        parser.print_help()
        return

    # Check if input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        return

    # Determine if the input is an image or a video
    input_ext = os.path.splitext(args.input_file)[1].lower()
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    is_image = input_ext in image_extensions

    # Determine output filename
    input_dir, input_filename = os.path.split(args.input_file)
    name, ext = os.path.splitext(input_filename)
    output_filename = f"{name}_{args.effect_name}{ext}"
    output_path = os.path.join(input_dir, output_filename)

    # Select the effect function based on effect_name
    effect_name = args.effect_name.lower()
    effect_function = Effects.get_effect_function(effect_name)
    if effect_function is None:
        print(f"Error: Effect '{args.effect_name}' not recognized.")
        print("Use '--help_effects' to see the list of available effects.")
        return

    if is_image:
        # Process a single image
        image = cv2.imread(args.input_file)
        if image is None:
            print(f"Error: Unable to read image '{args.input_file}'.")
            return

        # Apply effect
        processed_image = effect_function(image, args)

        # Save the output image
        cv2.imwrite(output_path, processed_image)
        print(f"Processed image saved as '{output_path}'.")

    else:
        # Open the input video file
        cap = cv2.VideoCapture(args.input_file)
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
        output_video_ext = '.mp4'
        output_filename = f"{name}_{args.effect_name}{output_video_ext}"
        output_path = os.path.join(input_dir, output_filename)
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Process the frame using the selected effect
            processed_frame = effect_function(frame, args)

            # Write the frame to the output video
            out.write(processed_frame)

            frame_count += 1
            print(f"Processing frame {frame_count}/{total_frames}", end="\r")

        # Release resources
        cap.release()
        out.release()
        print(f"\nVideo processing complete. Output saved as '{output_path}'.")

# Main
# Calls the argument parser then calls the render helper method
def main():
    args = create_parser().parse_args()
    cProfile.runctx("render(args)", globals(), locals(), 'profiler_output')

# Only execute if it is executed directly, not as a module in another script
if __name__ == "__main__":
    main()
