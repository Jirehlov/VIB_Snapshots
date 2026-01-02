import pandas as pd
import numpy as np
from PIL import Image
import sympy
def csv_to_prime_black_white_image(csv_path, output_image_path):
    data = pd.read_csv(csv_path, encoding='utf-8-sig')
    data = data.apply(pd.to_numeric, errors='coerce')
    data = data.fillna(0)
    data = data.astype(int)
    image_data = np.full((data.shape[0], data.shape[1], 3), 255, dtype=np.uint8)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = data.iat[i, j]
            if sympy.isprime(value):
                image_data[i, j] = [0, 0, 0]
    img = Image.fromarray(image_data)
    img.save(output_image_path)
csv_to_prime_black_white_image('sorted1.csv', '75.png')
