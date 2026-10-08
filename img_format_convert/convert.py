import os.path

from PIL import Image


def png_to_jpg(input_path, output_path):
    if os.path.isfile(input_path) and os.path.isfile(output_path):
        image = Image.open(input_path)
        image.convert('RGB').save(output_path, 'JPEG')
    elif os.path.isdir(input_path) and os.path.isdir(output_path):
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.png'):
                    image = Image.open(os.path.join(root, file))
                    image.convert('RGB').save(os.path.join(output_path, file.replace('.png', '.jpg')), 'JPEG')
