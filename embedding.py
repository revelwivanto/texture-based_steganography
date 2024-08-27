import cv2
import numpy as np
import math
from PIL import Image
import os
from collections import deque
import input_processing

class qgdec:

    def __init__(self, im, queue_big, queue_sml, queue_map):
        self.img = im
        self.queue_big = queue_big
        self.queue_sml = queue_sml
        self.queue_map = queue_map
        self.avg_pixel_value = np.average(im)

    def embed_image(self):
        pixels = self.img

        # Iterate over the image pixels
        for y in range(self.img.shape[0]):
            for x in range(0, self.img.shape[1] - 1, 2):  # Step by 2 to get neighboring pixels
                pixel1 = int(pixels[x, y])  # Convert to int to prevent overflow
                pixel2 = int(pixels[x + 1, y])  # Convert to int to prevent overflow
                # Calculate the difference between neighboring pixels
                diff = np.abs(pixel1 - pixel2)
                if self.avg_pixel_value > 150:
                    if diff < 10:
                        continue  # Do nothing if the difference is less than 128
                    elif 10 <= diff <= 20:
                        bit = self.queue_sml.get() if not self.queue_sml.empty() else None
                        if bit is not None:
                            bit = int(bit)
                            kb = pixel1 - (pixel1 % 4)
                            d = self.eq8(bit, kb)
                            dnew = self.eq10(d)
                            dnewnew = self.eq11(dnew, bit)
                            newpx = self.eq12(dnewnew, kb)
                            pixels[x, y] = newpx
                    elif diff > 20:
                        bit = self.queue_big.get() if not self.queue_big.empty() else None
                        if bit is not None:
                            bit = int(bit)
                            kb = pixel1 - (pixel1 % 4)
                            d = self.eq8(bit, kb)
                            dnew = self.eq10(d)
                            dnewnew = self.eq11(dnew, bit)
                            newpx = self.eq12(dnewnew, kb)
                            pixels[x, y] = newpx
                else:
                    if diff < 10:
                        continue  # Do nothing if the difference is less than 128
                    elif 10 <= diff <= 20:
                        bit = self.queue_sml.get() if not self.queue_sml.empty() else None
                        if bit is not None:
                            bit = int(bit)
                            ka = pixel1 + abs((pixel1 % 4) - 3)
                            d = self.eq9(bit, ka)
                            dnew = self.eq10(d)
                            dnewnew = self.eq11(dnew, bit)
                            newpx = self.eq13(dnewnew, ka)
                            pixels[x, y] = newpx
                    elif diff > 20:
                        bit = self.queue_big.get() if not self.queue_big.empty() else None
                        if bit is not None:
                            bit = int(bit)
                            ka = pixel1 + abs((pixel1 % 4) - 3)
                            d = self.eq9(bit, ka)
                            dnew = self.eq10(d)
                            dnewnew = self.eq11(dnew, bit)
                            newpx = self.eq13(dnewnew, ka)
                            pixels[x, y] = newpx

        # Convert the pixels into an array using numpy
        array = np.array(pixels, dtype=np.uint8)

        # Use PIL to create an image from the new array of pixels
        new_image = Image.fromarray(array)
        new_image.save('Original_Dataset\\new.png')

    @staticmethod
    def eq8(pxval, kb):
        d = pxval - kb 
        print("pxval",pxval)
        print(d)
        return d

    @staticmethod
    def eq9(pxval, ka):
        d = ka - pxval
        print("pxval",pxval)
        print(d)
        return d

    @staticmethod
    def eq10(d):
        if d <= 2:
            dnew = 0
        else:
            dnew = d - 2 ** math.floor(math.log2(d))
        print(dnew)
        return dnew

    @staticmethod
    def eq11(dnew, bits):
        dnewnew = 2 * dnew + bits
        print(dnewnew)
        return dnewnew

    @staticmethod
    def eq12(dnewnew, kb):
        stegpx = dnewnew + kb
        print("stgpx",stegpx)
        return stegpx

    @staticmethod
    def eq13(dnewnew, ka):
        stegpx = ka - dnewnew
        print("stgpx",stegpx)
        return stegpx

    @staticmethod        
    def eq14(d):
        binary_d = bin(d)[2:]
        return [int(bit) for bit in binary_d]

    @staticmethod        
    def eq15(d):
        dnew = math.floor(d / 2)
        return dnew

    @staticmethod
    def eq16(LM, pxval):
        if LM == '00':
            return 0
        elif LM == '10':
            return pxval + 2 ** math.log2(2 * pxval + 1) + 1
        elif LM == '11':
            return pxval + 2 ** math.log2(2 * pxval + 1)
        else:
            raise ValueError("Invalid LM value. LM should be '00', '10', or '11'.")

    def createblock(self):
        # Placeholder method for creating a block, to be implemented
        pass

    def extracting(self, block, LM):
        # Placeholder method for extracting data, to be implemented
        pass

def main():
    image_path = "Original_Dataset\\Lena.png"
    # Load the image in grayscale mode
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite("Original_Dataset\\old.png", img)
    if img is None:
        print(f"Image at path {image_path} could not be found.")
        return
    
    mode = input("Choose mode (embed or extract): ")
    if mode == "embed":
        bits = input("Enter bits to embed: ")
        queue_big, queue_sml, queue_map = input_processing.create_queue(bits)
        qg = qgdec(img, queue_big, queue_sml, queue_map)
        qg.embed_image()
    elif mode == "extract":
        LM = input("What's the LM: ")
        qg = qgdec(img, None, None, None)  # Pass None for queues during extraction
        block = qg.createblock()
        new_block, bits = qg.extracting(block, LM)
        print(bits)
    else:
        print("Invalid mode. Please choose either embed or extract.")

if __name__ == "__main__":
    main()
