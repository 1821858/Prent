import argparse
import Effects

effects_list = Effects.get_available_effects()
effects_str = ', '.join(effects_list)

parser = argparse.ArgumentParser(
    description="Video/Image Effect Renderer",
    epilog=(
        f"Available effects: {effects_str}\n\n"
        "Example usage:\n"
        "  python Main.py input_video.mp4 polygonize --num_polygons 150 --num_colors 10\n"
        "  python Main.py input_image.jpg sketch\n"
        "  python Main.py input_video.mp4 cartoon"
    ),
    formatter_class=argparse.RawDescriptionHelpFormatter
)

def create_parser():

    parser.add_argument("input_file", nargs='?', help="Path to input video or image file")
    parser.add_argument("effect_name", nargs='?', help="Name of the effect to apply")
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
    parser.add_argument(
        "--help_effects",
        action='store_true',
        help="Show available effects and example usage"
    )
    parser.add_argument('--profile', action= 'store_true')
    args = parser.parse_args()

    return parser
