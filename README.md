# Image Processing and Merging Script

This script is designed to process and merge multiple images. It is developed using Python and the Python Imaging Library (PIL).

## Functionality

The script performs the following operations:

1. **Merges multiple images**: The script merges multiple images into one. The images are merged such that the resulting image is the lightest color at each pixel from all the images.

2. **Converts images to black and white**: The script converts the merged image to black and white based on a color threshold.

3. **Fills holes in the image**: The script identifies black pixels that are not connected to the edge of the image and fills them in, effectively filling in holes in the image.

## How to Use

The script is designed to be run from the command line. It processes all PNG images in a specified directory. The images to be merged should be named in the format `base_name_x_y_z.png`, where `base_name` is the name for the group of images that should be merged together, and `x`, `y`, and `z` can be any string.

The script will output a merged image for each group of images, named `base_name_merged.png`.

## Technologies Used

This script is developed using Python and the Python Imaging Library (PIL). It also uses the concurrent.futures module for parallel processing of image groups.
