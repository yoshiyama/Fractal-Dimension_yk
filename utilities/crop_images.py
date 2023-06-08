#python crop_images.py ./images 256


import os
import sys
from PIL import Image

def crop_images(directory, size):
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(directory, filename)
            output_directory = os.path.dirname(file_path)  # 入力画像と同じディレクトリを取得
            print(file_path)
            try:
                with Image.open(file_path) as image:
                    width, height = image.size
                    left = (width - size) // 2
                    top = (height - size) // 2
                    right = (width + size) // 2
                    bottom = (height + size) // 2
                    cropped_image = image.crop((left, top, right, bottom))
                    output_path = os.path.join(output_directory, f"cropped_{filename}")
                    cropped_image.save(output_path)
            except IOError:
                print(f"Unable to process image: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python crop_images.py [directory] [size]")
        sys.exit(1)

    directory = sys.argv[1]
    size = int(sys.argv[2])
    crop_images(directory, size)
