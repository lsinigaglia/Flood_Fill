from PIL import Image
import os
import concurrent.futures

def adjust_pixel_color(pixel, threshold=63):
    r, g, b = pixel
    if (r + g + b) // 3 > threshold:
        return (255, 255, 255)  # white
    else:
        return (0, 0, 0)  # black

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

def process_image(image_path):
    image = Image.open(image_path)
    width, height = image.size

    # Adjust image to be black and white based on the threshold
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            image.putpixel((x, y), adjust_pixel_color(pixel))

    # Mark edge-connected black pixels as visited
    visited = set()
    mark_edge_connected_black_pixels(image, visited)

    # Fill holes using flood_fill algorithm
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel == (0, 0, 0) and (x, y) not in visited:
                flood_fill(image, x, y, (0, 0, 0), (255, 255, 255), visited)

    # Save the processed image
    # (No changes needed in this part)

    #output_path = os.path.splitext(image_path)[0] + "_processed.png"
    output_path = os.path.join(os.path.dirname(image_path), "processed_" + os.path.basename(image_path))
    output_path = os.path.splitext(output_path)[0] + ".png"
    image.save(output_path)
    print(f"Processed image saved to: {output_path}")

def main():
    cwd = os.getcwd()
    subdir_name = "Test_images"
    input_dir = os.path.join(cwd, subdir_name)
    image_paths = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            file_path = os.path.join(input_dir, filename)
            image_paths.append(file_path)
        else:
            continue

    # Set the maximum number of concurrent threads
    max_threads = 4

    # Use ThreadPoolExecutor to run tasks concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(process_image, image_paths)

    print("All images processed.")

if __name__ == "__main__":
    main()