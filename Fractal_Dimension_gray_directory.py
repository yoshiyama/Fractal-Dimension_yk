import os
import cv2
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm

def calculate_fractal_dimension(image_path):
    im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    M, G = im.shape

    scale = []
    Nr = []
    l = 2

    while l < (M / 2):
        r = l
        blockSizeR = r
        blockSizeC = r
        ld = (l * G) / M
        nr = 0
        for row in np.arange(0, M, blockSizeR):
            for col in np.arange(0, M, blockSizeC):
                oneBlock = im[row:row+blockSizeR, col:col+blockSizeC]
                maxI, minI = np.max(oneBlock), np.min(oneBlock)

                nb = np.ceil(float(maxI) / ld)
                nr += 1 if maxI == minI else nb

        Nr.append(np.sum(nr))
        scale.append(M / l)
        l = l * 2

    N = np.log(Nr) / np.log(2)
    S = np.log(scale) / np.log(2)
    p = np.polyfit(S, N, 1)
    m, c = p[0], p[1]

    x = (((m * S) + c) - N) / (1 + (m * m))
    E = (1 / len(N)) * np.sqrt(np.sum(np.abs(x)))

    return p[0]

def process_image(filename):
    dimension = calculate_fractal_dimension(filename)
    return f'{filename}: {dimension}'

def process_images(directory):
    output_file = 'fractal_dimensions.txt'
    filenames = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(('.jpg', '.jpeg', '.png'))]
    with Pool() as p:
        results = list(tqdm(p.imap(process_image, filenames), total=len(filenames)))
    with open(output_file, 'w') as f:
        for result in results:
            f.write(f'{result}\n')

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python calculate_fractal_dimension.py [directory]")
        sys.exit(1)

    directory = sys.argv[1]
    process_images(directory)
