from PIL import Image
from PIL import ImageChops
import os
from PIL.Image import core as _imaging
from PIL import Image
from PIL import ImageChops
import concurrent.futures
from collections import defaultdict


def adjust_pixel_color(pixel, threshold=63):
    r, g, b = pixel
    if (r + g + b) // 3 > threshold:
        return (255, 255, 255)  # white with original alpha
    else:
        return (0, 0, 0)  # black with original alpha


def flood_fill(image, x, y, target_color, replacement_color, visited):
    stack = [(x, y)]

    while stack:
        x, y = stack.pop()
        if x < 0 or x >= image.width or y < 0 or y >= image.height:
            continue
        pixel = image.getpixel((x, y))
        if pixel != target_color or (x, y) in visited:
            continue

        visited.add((x, y))
        image.putpixel((x, y), replacement_color)

        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if (nx, ny) not in visited:
                stack.append((nx, ny))





def mark_edge_connected_black_pixels(image, visited):
    width, height = image.size
    edge_pixels = []

    # Get edge pixels
    for x in range(width):
        edge_pixels.append((x, 0))
        edge_pixels.append((x, height - 1))
    for y in range(height):
        edge_pixels.append((0, y))
        edge_pixels.append((width - 1, y))

    # Mark edge-connected black pixels as visited
    for x, y in edge_pixels:
        pixel = image.getpixel((x, y))
        if pixel == (0, 0, 0):
            flood_fill(image, x, y, (0, 0, 0), (0, 0, 0), visited)

'''function with no PIL library the complexity is O(N*W*H) in both cases 
   but the one but the underlying implementation of the uncommented one
   is optimized in C for better performance
def merge_images(image_group): 
    base_image = image_group[0]
    width, height = base_image.size

    for other_image in image_group[1:]:
        for x in range(width):
            for y in range(height):
                base_pixel = base_image.getpixel((x, y))
                other_pixel = other_image.getpixel((x, y))

                if other_pixel == (255, 255, 255):
                    base_image.putpixel((x, y), other_pixel)

    return base_image'''
    

def merge_images(image_group):
    base_image = image_group[0]

    for other_image in image_group[1:]:
        base_image = ImageChops.lighter(base_image, other_image)

    return base_image



def merge_and_process(image_paths, base_name):
    images = [Image.open(image_path).convert("RGB") for image_path in image_paths]

    # Merge images
    merged_image = merge_images(images)

    # Process merged image
    width, height = merged_image.size

    # Adjust image to be black and white based on the threshold
    for x in range(width):
        for y in range(height):
            pixel = merged_image.getpixel((x, y))
            merged_image.putpixel((x, y), adjust_pixel_color(pixel))

    # Mark edge-connected black pixels as visited
    visited = set()
    mark_edge_connected_black_pixels(merged_image, visited)

    # Fill holes using flood_fill algorithm
    for x in range(width):
        for y in range(height):
            pixel = merged_image.getpixel((x, y))
            if pixel == (0, 0, 0) and (x, y) not in visited:
                flood_fill(merged_image, x, y, (0, 0, 0), (255, 255, 255), visited)

    output_path = os.path.join(os.path.dirname(image_paths[0]), f"{base_name}_merged.png")
    merged_image.save(output_path)
    print(f"Merged image saved to: {output_path}")


def main():
    cwd = os.getcwd()
    subdir_name = "Test_images"
    input_dir = os.path.join(cwd, subdir_name)
    image_groups = defaultdict(list)

    for filename in os.listdir(input_dir):
        print(f"Checking file: {filename}")
        if filename.endswith(".png"):
            file_path = os.path.join(input_dir, filename)
            base_name = "_".join(filename.split("_")[:-3])
            image_groups[base_name].append(file_path)
        else:
            continue

    # Set the maximum number of concurrent threads
    max_threads = 4

    # Use ThreadPoolExecutor to run tasks concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for base_name, image_paths in image_groups.items():
            executor.submit(merge_and_process, image_paths, base_name)

    print("All images processed and merged.")


if __name__ == "__main__":
    main()





