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
        elif self.avg_diff * 0.3 <= diff < self.avg_diff * 0.8:
            return self._embed_bit(pixel1, self.queue_sml)
        elif self.avg_diff * 1.0 <= diff < self.avg_diff * 1.6:
            return self._embed_bit(pixel1, self.queue_big)
        else:
            return self._embed_bit(pixel1, self.queue_vbig)

    def _process_dark(self, pixel1, diff):
        # Use the average difference to determine the embedding logic
        if diff < self.avg_diff * 0.3:
            return self._embed_bit(pixel1, self.queue_vsml, False)
        elif self.avg_diff * 0.3 <= diff < self.avg_diff * 0.8:
            return self._embed_bit(pixel1, self.queue_sml, False)
        elif self.avg_diff * 1.0 <= diff < self.avg_diff * 1.6:
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

            if newpx is not None:
                pixels[x, y] = np.clip(newpx, 0, 255)
                self.embedded_bits_count += 8

        array = np.array(pixels, dtype=np.uint8)
        new_image = Image.fromarray(array)
        print("Average difference: ", self.avg_diff)
        print("queue sizes after embedding: ",self.queue_vbig.qsize(),self.queue_big.qsize(),self.queue_sml.qsize(),self.queue_vsml.qsize())
        if not self.queue_vbig.empty() or not self.queue_big.empty() or not self.queue_sml.empty() or not self.queue_vsml.empty():
            print("Some data is still in the queues")
        else:
            print("Data embedding complete")
        new_image.save('Original_Dataset\\new100.png')

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
    image_path = "Original_Dataset\\Pixel ruler.tiff"
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite("Original_Dataset\\old.png", img)
    if img is None:
        print(f"Image at path {image_path} could not be found.")
        return
    
    mode = input("Choose mode (embed or extract): ")
    if mode == "embed":
        with open('input_bit\\random-binary_100Kb.txt', 'r') as file:
            bits = file.read().strip()
        var = input_processing.calculate_grayscale_image_variance(img)
        queue_vbig, queue_big, queue_sml, queue_vsml, queue_map = input_processing.create_queue(bits, var)
        print("queue sizes before embedding: ",queue_vbig.qsize(),queue_big.qsize(),queue_sml.qsize(),queue_vsml.qsize())
        qg = qgdec(img, queue_vbig, queue_big, queue_sml, queue_vsml, queue_map)
        qg.embed_image()
    elif mode == "extract":
        LM = input("What's the LM: ")
        qg = qgdec(img, None, None, None)  
        block = qg.createblock()
        new_block, bits = qg.extracting(block, LM)
        print(bits)
    else:
        print("Invalid mode. Please choose either embed or extract.")

if __name__ == "__main__":
    main()
