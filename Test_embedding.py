import cv2
import numpy as np
import math
from PIL import Image
import os
from collections import deque
import input_processing

class qgdec:

    def __init__(self, im, queue_vbig, queue_big, queue_sml, queue_vsml, queue_map):
        self.img = im
        self.queue_vbig = queue_vbig
        self.queue_big = queue_big
        self.queue_sml = queue_sml
        self.queue_vsml = queue_vsml
        self.queue_map = queue_map
        self.avg_pixel_value = np.average(im)
        self.total_bits = self.queue_vbig.qsize() + self.queue_big.qsize() + self.queue_sml.qsize() + self.queue_vsml.qsize()
        self.embedded_bits_count = 0  # Counter for embedded bits
        self.avg_diff = self.calculate_avg_diff()

    def process_bit(self, pixel1, diff, is_bright):
        if is_bright:
            return self._process_bright(pixel1, diff)
        else:
            return self._process_dark(pixel1, diff)

    def calculate_avg_diff(self):
        total_diff = 0
        count = 0
        for y in range(self.img.shape[0]):
            for x in range(0, self.img.shape[1] - 1, 2):  # Step by 2 to get neighboring pixels
                pixel1 = int(self.img[y, x])  # Fixed to access (y, x) correctly
                pixel2 = int(self.img[y, x + 1])
                diff = np.abs(pixel1 - pixel2)
                total_diff += diff
                count += 1
        return total_diff / count if count > 0 else 0

    def _process_bright(self, pixel1, diff):
        # Use the average difference to determine the embedding logic
        if diff < self.avg_diff * 0.3:
            return self._embed_bit(pixel1, self.queue_vsml)
        elif self.avg_diff * 0.3 <= diff < self.avg_diff * 0.7:
            return self._embed_bit(pixel1, self.queue_sml)
        elif self.avg_diff * 0.7 <= diff < self.avg_diff * 1.0:
            return self._embed_bit(pixel1, self.queue_big)
        else:
            return self._embed_bit(pixel1, self.queue_vbig)

    def _process_dark(self, pixel1, diff):
        # Use the average difference to determine the embedding logic
        if diff < self.avg_diff * 0.3:
            return self._embed_bit(pixel1, self.queue_vsml, False)
        elif self.avg_diff * 0.3 <= diff < self.avg_diff * 0.5:
            return self._embed_bit(pixel1, self.queue_sml, False)
        elif self.avg_diff * 0.5 <= diff < self.avg_diff * 1.3:
            return self._embed_bit(pixel1, self.queue_big, False)
        else:
            return self._embed_bit(pixel1, self.queue_vbig, False)

    def _embed_bit(self, pixel1, queue, is_bright=True):
        if queue.empty():
            return None

        bit = int(queue.get())
        if is_bright:
            kb = pixel1 - (pixel1 % 4)
            return self._perform_embed_operations(bit, kb)
        else:
            ka = pixel1 + abs((pixel1 % 4) - 3)
            return self._perform_embed_operations(bit, ka, False)

    def _perform_embed_operations(self, bit, pixel_value, is_bright=True):
        if is_bright:
            d = self.eq8(bit, pixel_value)
        else:
            d = self.eq9(bit, pixel_value)
        dnew = self.eq10(d)
        dnewnew = self.eq11(dnew, bit)
        if is_bright:
            return self.eq12(dnewnew, pixel_value)
        else:
            return self.eq13(dnewnew, pixel_value)

    def embed_image(self):
        pixels = self.img
        is_bright = self.avg_pixel_value > 150

        for y in range(self.img.shape[0]):
            for x in range(0, self.img.shape[1] - 1, 2):
                pixel1 = int(pixels[x, y])
                pixel2 = int(pixels[x + 1, y])
                diff = np.abs(pixel1 - pixel2)
                newpx = self.process_bit(pixel1, diff, is_bright)
                print(newpx)

            if newpx is not None:
                pixels[x, y] = np.clip(newpx, 0, 255)
                self.embedded_bits_count += 8

        array = np.array(pixels, dtype=np.uint8)
        new_image = Image.fromarray(array)
        print(self.avg_diff)
        print(self.total_bits, self.embedded_bits_count)
        print(self.queue_vbig.qsize(),self.queue_big.qsize(),self.queue_sml.qsize(),self.queue_vsml.qsize())
        return new_image

    @staticmethod
    def eq8(pxval, kb):
        d = pxval - kb 
        return d

    @staticmethod
    def eq9(pxval, ka):
        d = ka - pxval
        return d

    @staticmethod
    def eq10(d):
        if d <= 2:
            dnew = 0
        else:
            dnew = d - 2 ** math.floor(math.log2(d))
        return dnew

    @staticmethod
    def eq11(dnew, bits):
        return 2 * dnew + bits

    @staticmethod
    def eq12(dnewnew, kb):
        return dnewnew + kb

    @staticmethod
    def eq13(dnewnew, ka):
        return ka - dnewnew

    def createblock(self):
        # Placeholder method for creating a block, to be implemented
        pass

    def extracting(self, block, LM):
        # Placeholder method for extracting data, to be implemented
        pass

def main():

        # Define the paths
    image_folder = "Original_Dataset"
    input_bit_folder = "input_bit"
    output_folder = "Stego_Images"

    # List of image names and their corresponding file extensions
    image_names = [
        "Aerial.tiff", "Airplane.tiff", "Car and APCs.tiff", "Fishing Boat.tiff",
        "Pixel ruler.tiff", "Stream and bridge.tiff", "Tank.tiff", "Truck.tiff"
    ]

    # List of input bit files
    input_bit_files = [
        "random-binary_1Kb.txt", "random-binary_10Kb.txt", "random-binary_20Kb.txt", "random-binary_30Kb.txt",
        "random-binary_40Kb.txt", "random-binary_50Kb.txt", "random-binary_60Kb.txt", "random-binary_70Kb.txt",
        "random-binary_80Kb.txt", "random-binary_90Kb.txt", "random-binary_100Kb.txt"
    ]
    for image_name in image_names:
        image_path = os.path.join(image_folder, image_name)
        
        for bit_file in input_bit_files:
            bit_file_path = os.path.join(input_bit_folder, bit_file)
            
            # Create output file path
            output_image_name = f"{os.path.splitext(image_name)[0]}_{os.path.splitext(bit_file)[0]}.tiff"
            output_image_path = os.path.join(output_folder, output_image_name)
            
            # Embed bits into the image
            print(f"Embedding {bit_file} into {image_name}")
            with open(bit_file_path, 'r') as file:
                bits = file.read().strip()
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            var = input_processing.calculate_grayscale_image_variance(img)
            queue_vbig, queue_big, queue_sml, queue_vsml, queue_map = input_processing.create_queue(bits, var)
            print(queue_vbig.qsize(),queue_big.qsize(),queue_sml.qsize(),queue_vsml.qsize())
            qg = qgdec(img, queue_vbig, queue_big, queue_sml, queue_vsml, queue_map)
            result = qg.embed_image()
            result.save(output_image_path)

if __name__ == "__main__":
    main()
