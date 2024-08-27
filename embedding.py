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
                pixel1 = pixels[x, y]
                pixel2 = pixels[x + 1, y]

                # Calculate the difference between neighboring pixels
                diff = abs(pixel1 - pixel2)
                if self.avg_pixel_value > 150:
                    if diff < 128:
                        continue  # Do nothing if the difference is less than 128
                    elif 128 <= diff <= 192:
                        bit = self.queue_sml.get() if self.queue_sml else None
                        bit = int(bit)
                        if bit is not None:
                            kb = self.img[x, y] - (self.img[x, y] % 4)
                            d = self.eq8(bit,kb)
                            dnew = self.eq10(d)
                            dnewnew = self.eq11(dnew, bit)
                            newpx = self.eq12(dnewnew, kb)
                            pixels[x, y] = newpx
                    elif diff > 192:
                        bit = self.queue_big.get() if self.queue_big else None
                        bit = int(bit)
                        if bit is not None:
                            kb = self.img[x, y] - (self.img[x, y] % 4)
                            d = self.eq8(bit,kb)
                            dnew = self.eq10(d)
                            dnewnew = self.eq11(dnew, bit)
                            newpx = self.eq12(dnewnew, kb)
                            pixels[x, y] = newpx
                else:
                    if diff < 128:
                        continue  # Do nothing if the difference is less than 128
                    elif 128 <= diff <= 192:
                        bit = self.queue_sml.get() if self.queue_sml else None
                        bit = int(bit)
                        if bit is not None:
                            ka = self.img[x, y] + abs((self.img[x, y] % 4) - 3)
                            d = self.eq9(bit,ka)
                            dnew = self.eq10(d)
                            dnewnew = self.eq11(dnew, bit)
                            newpx = self.eq13(dnewnew, ka)
                            pixels[x, y] = newpx
                    elif diff > 192:
                        bit = self.queue_big.get() if self.queue_big else None
                        bit = int(bit)
                        if bit is not None:
                            ka = self.img[x, y] + abs((self.img[x, y] % 4) - 3)
                            d = self.eq9(bit,ka)
                            dnew = self.eq10(d)
                            dnewnew = self.eq11(dnew, bit)
                            newpx = self.eq13(dnewnew, ka)
                            pixels[x, y] = newpx
        # Convert the pixels into an array using numpy
        array = np.array(pixels, dtype=np.uint8)

        # Use PIL to create an image from the new array of pixels
        new_image = Image.fromarray(array)
        new_image.save('Original_Dataset\new.png')        

    def embed(self, bits, k):
        if self.avg_pixel_value < 150:
            d = self.eq8(bits,k)
            dnew = self.eq10(d)
            dnewnew = self.eq11(dnew)
            newpx = self.eq12(dnewnew)
            return newpx
        else:
            d = self.eq9(bits,)
            dnew = self.eq10(d)
            dnewnew = self.eq11(dnew)
            newpx = self.eq13(dnewnew)
            return newpx
        
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
        if d <=2:
            dnew =0
        else:
            dnew = d - 2 ** math.floor(math.log2(d))
        return dnew
        
    def eq11(self, dnew, bits):
        dnewnew = 2 * dnew + bits
        return dnewnew

    @staticmethod
    def eq12(dnewnew, kb):
        stegpx = dnewnew + kb
        return stegpx
    
    @staticmethod
    def eq13(dnewnew, ka):
        stegpx = ka - dnewnew
        return stegpx

    @staticmethod        
    def eq14(self, d):
        # Convert d to binary and remove the '0b' prefix
        binary_d = bin(d)[2:]
        
        # If message is not already a list, initialize it as one
        if not hasattr(self, 'message'):
            self.message = []
        
        # Push the binary value onto the stack
        for bit in binary_d:
            self.message.append(bit)
        
        return self.message

    
    @staticmethod        
    def eq15(d):
        dnew = math.floor(d/2)
        return dnew
    
    @staticmethod
    def eq16(LM, pxval):
        if LM == '00':
            return 0
        elif LM == '10':
            return pxval + 2 ^ math.log2(2 * pxval + 1) + 1
        elif LM == '11':
            return pxval + 2 ^ math.log2(2 * pxval + 1)
        else:
            raise ValueError("Invalid LM value. LM should be '00', '10', or '11'.")
"""
    def extracting(pxval, LM):
        avg_pixblock = np.mean(block)
        if avg_pixblock <= 150:
            kb = [b - (b % 4) for b in block]
            d = qgdec.eq8(block, kb)
            lsb = qgdec.eq14(d)
            dnew= qgdec.eq15(d)
            dnewnew=qgdec.eq16(dnew, LM)
            orgpxl = qgdec.eq8(dnewnew, kb)
        else:
            ka = [b + abs((b % 4) - 3) for b in block]
            d = qgdec.eq9(block)
            lsb = qgdec.eq14(block)
            dnew= qgdec.eq15(d)
            dnewnew=qgdec.eq16(dnew, LM)
            orgpxl = qgdec.eq9(dnewnew, ka)
        return orgpxl, lsb
   """
    
def main():
    image_path = "Original_Dataset\OIP.jfif"
    # Load the image in grayscale mode
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # If the image path is not valid, the img will be None
    if img is None:
        print(f"Image at path {image_path} could not be found.")
        return
    
    mode = input("Choose mode (embed or extract): ")
    if mode == "embed":
        bits = input("Enter bits to embed: ")
        queue_big, queue_sml, queue_map = input_processing.create_queue(bits)
        print(queue_big.get())
        print(queue_sml.get())
        print(queue_map.get())
        qg = qgdec(img, queue_big, queue_sml, queue_map)  # Create an instance of qgdec
        qg.embed_image()
    elif mode == "extract":
        LM = input("What's the LM: ")
        qg = qgdec(img, "")  # Create an instance with empty bits for extraction
        block = qg.createblock()  # Get a block
        new_block, bits = qg.extracting(block, LM)
        print(bits)
    else:
        print("Invalid mode. Please choose either embed or extract.")
        return

if __name__=="__main__":
    main()
