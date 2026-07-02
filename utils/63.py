import os
import re
from PIL import Image
def extract_lines(file_path, marker, num_lines):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    marker_pos = content.find(marker)
    if marker_pos == -1:
        raise ValueError(f"Marker '{marker}' not found in file.")
    return content[marker_pos:].strip().split('\n')[1:num_lines + 1]
def process_images(image_paths):
    images = [Image.open(path) for path in image_paths]
    widths, heights = zip(*(img.size for img in images))
    max_height = max(heights)
    new_images = [img.resize((int(img.width * max_height / img.height), max_height), resample=Image.LANCZOS) for img in images]
    total_width = sum(img.width for img in new_images)
    final_image = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for img in new_images:
        final_image.paste(img, (x_offset, 0))
        x_offset += img.width
    return final_image
def main():
    txt_file = 'hitnrun.txt'
    output_file = 'hitnrun.jpg'
    marker = '总变化：'
    num_lines = 10
    image_folder = 'covers'
    lines = extract_lines(txt_file, marker, num_lines)
    image_paths = [os.path.join(image_folder, f"{re.match(r'(\d+),', line).group(1)}.jpg") for line in lines if os.path.exists(os.path.join(image_folder, f"{re.match(r'(\d+),', line).group(1)}.jpg"))]
    if image_paths:
        final_image = process_images(image_paths)
        final_image = final_image.resize((int(final_image.width / 2.5), int(final_image.height / 2.5)), resample=Image.LANCZOS)
        final_image.save(output_file, format='JPEG')
        print(f"Output saved to {output_file}.")
    else:
        print("No images to process.")
if __name__ == "__main__":
    main()
