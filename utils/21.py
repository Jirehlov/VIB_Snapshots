import pandas as pd
import numpy as np
from PIL import Image
import matplotlib
def csv_to_color_pixel_image(csv_path, output_image_path, colormap='viridis'):
    data = pd.read_csv(csv_path, encoding='utf-8-sig')
    data = data.apply(pd.to_numeric, errors='coerce')
    data = data.fillna(0)
    data = data.astype(float)
    scaled_data = np.log1p(data)
    max_value = scaled_data.max().max()
    min_value = scaled_data.min().min()
    normalized_data = (scaled_data - min_value) / (max_value - min_value)
    colormap = matplotlib.colormaps.get_cmap(colormap)
    colored_data = colormap(normalized_data)
    image_data = (colored_data[:, :, :3] * 255).astype(np.uint8)
    img = Image.fromarray(image_data)
    img.save(output_image_path)
csv_to_color_pixel_image('sorted1.csv', '21.png', colormap='viridis')
