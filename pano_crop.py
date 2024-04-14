import argparse
from pathlib import Path
from PIL import Image
import math


def parse_and_validate_args(passed_args=None):

    parser = argparse.ArgumentParser(description="Process an image file.")

    parser.add_argument('--image_path',  
                        required=True,
                        type=Path,
                        help='Path to the image file')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--aspect_ratio',
                       type=int,
                       nargs=2, metavar=('HEIGHT', 'WIDTH'),
                        help='Values for reference aspect ratio. If this is provided, num_parts will be calculated based on this '
                             'aspect ratio. Any extra space in the last part will be filled with black.')

    group.add_argument('--ref_image_path',
                       type=Path,
                       help='Path to a reference image. If this is provided, aspect_ratio and num_parts will be calculated based on this '
                            'image. Any extra space in the last part will be filled with black.')

    group.add_argument('--num_parts',
                       type=int,
                       help='Number of parts to split the image into. If this is provided, aspect_ratio will be calculated '
                            'based on this number of parts.')
    
    parser.add_argument('--output_dir',  
                        required=True,
                        type=Path,
                        help='Path to the output directory')

    args = parser.parse_args(passed_args)

    # Check if image_path exists and is a file
    if not args.image_path.is_file():
        raise FileNotFoundError(f"The image_path '{args.image_path}' does not exist or is not a file.")

    # Check if ref_image_path exists and is a file
    if args.ref_image_path and not args.ref_image_path.is_file():
        raise FileNotFoundError(f"The ref_image_path '{args.ref_image_path}' does not exist or is not a file.")

    # Check if output_dir exists and is a directory
    if not args.output_dir.is_dir():
        raise NotADirectoryError(f"The output_dir '{args.output_dir}' does not exist or is not a directory.")

    # If ref_image_path is provided, calculate the aspect ratio based on the reference image
    if args.ref_image_path:
        with Image.open(args.ref_image_path) as img:
            width, height = img.size
            args.aspect_ratio = (height, width)

    return args


def split_image_based_on_num_parts(image, args):
    
    # Get the width and height of the image
    width, height = image.size

    # Calculate the width of each part
    part_width = width // args.num_parts

    # Split the image horizontally into parts
    for i in range(args.num_parts):

        # Calculate the starting and ending x coordinates for each part
        start_x = i * part_width
        end_x = start_x + part_width

        # Crop the image
        cropped_image = image.crop((start_x, 0, end_x, height))

        # Generate the output file name
        output_file_name = f"{args.image_path.stem}-pano_split-{i}{args.image_path.suffix}"

        # Save the cropped image to the output directory
        output_path = args.output_dir / output_file_name
        cropped_image.save(output_path)


def split_image_based_on_asepect_ratio(image, args):

    # Get the width and height of the image
    width, height = image.size

    # Calculate the number of parts based on the aspect ratio
    aspect_ratio_height, aspect_ratio_width = args.aspect_ratio
    num_parts = math.ceil(width / aspect_ratio_width)

    # Calculate the width of each partbased on the height and aspect ratio
    part_width = height * aspect_ratio_width / aspect_ratio_height

    # Split the image horizontally into parts
    for i in range(num_parts):

        # Calculate the starting and ending x coordinates for each part
        start_x = i * part_width
        end_x = start_x + part_width

        # Crop the image
        cropped_image = image.crop((start_x, 0, end_x, height))

        # Generate the output file name
        output_file_name = f"{args.image_path.stem}-pano_split-{i}{args.image_path.suffix}"

        # Save the cropped image to the output directory
        output_path = args.output_dir / output_file_name
        cropped_image.save(output_path)


def main(passed_args=None):

    args = parse_and_validate_args(passed_args)

    # Open the image
    image = Image.open(args.image_path)

    if args.num_parts:
        split_image_based_on_num_parts(image, args)
    else:
        split_image_based_on_asepect_ratio(image, args)


if __name__ == "__main__":

    main()