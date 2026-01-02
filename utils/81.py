import os
import json
from PIL import Image
def extract_arrays(file_path, num_elements):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    def traverse(data, path=[]):
        arrays = []
        if isinstance(data, list) and len(data) == num_elements:
            arrays.append((data, path))
        elif isinstance(data, dict):
            for key, value in data.items():
                arrays.extend(traverse(value, path + [key]))
        elif isinstance(data, list):
            for index, item in enumerate(data):
                arrays.extend(traverse(item, path + [index]))
        return arrays
    return traverse(data)
def process_images(image_paths):
    images = [Image.open(path) for path in image_paths]
    widths, heights = zip(*(img.size for img in images))
    avg_width = sum(widths) // len(widths)
    avg_height = sum(heights) // len(heights)
    new_images = [img.resize((avg_width, avg_height), resample=Image.LANCZOS) for img in images]
    total_width = sum(img.width for img in new_images)
    final_image = Image.new('RGB', (total_width, avg_height))
    x_offset = 0
    for img in new_images:
        final_image.paste(img, (x_offset, 0))
        x_offset += img.width
    return final_image
def main():
    json_file = 'year_end_report.json'
    output_folder = 'year_end_report'
    num_elements = 10
    image_folder = 'covers'
    arrays = extract_arrays(json_file, num_elements)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for array, path in arrays:
        subjects = [str(item['subject']) for item in array]
        image_paths = [os.path.join(image_folder, f"{subject}.jpg") for subject in subjects if os.path.exists(os.path.join(image_folder, f"{subject}.jpg"))]
        
        if image_paths:
            final_image = process_images(image_paths)
            path_str = '_'.join(map(str, path))
            output_file = os.path.join(output_folder, f"{path_str}.jpg")
            final_image.save(output_file, format='JPEG')
            print(f"Output saved to {output_file}.")
        else:
            print("No images to process.")
if __name__ == "__main__":
    main()
