import numpy as np
from PIL import Image

def embed_image(self):
    pixels = self.img.copy()
    height, width = pixels.shape
    
    # Precompute modulo operations
    pixel_mod_4 = pixels % 4
    pixel_mod_4_abs_3 = np.abs(pixel_mod_4 - 3)
    
    # Create masks for different conditions
    diff = np.abs(pixels[:, :-1:2] - pixels[:, 1::2])
    mask_128_192 = (128 <= diff) & (diff <= 192)
    mask_192_plus = diff > 192
    
    if self.avg_pixel_value > 150:
        kb = pixels[:, ::2] - pixel_mod_4[:, ::2]
        
        # Process 128 <= diff <= 192
        for y, x in zip(*np.where(mask_128_192)):
            if not self.queue_sml.empty():
                bit = int(self.queue_sml.get())
                d = self.eq8(bit, kb[y, x])
                dnew = self.eq10(d)
                dnewnew = self.eq11(dnew, bit)
                pixels[y, x*2] = self.eq12(dnewnew, kb[y, x])
        
        # Process diff > 192
        for y, x in zip(*np.where(mask_192_plus)):
            if not self.queue_big.empty():
                bit = int(self.queue_big.get())
                d = self.eq8(bit, kb[y, x])
                dnew = self.eq10(d)
                dnewnew = self.eq11(dnew, bit)
                pixels[y, x*2] = self.eq12(dnewnew, kb[y, x])
    else:
        ka = pixels[:, ::2] + pixel_mod_4_abs_3[:, ::2]
        
        # Process 128 <= diff <= 192
        for y, x in zip(*np.where(mask_128_192)):
            if not self.queue_sml.empty():
                bit = int(self.queue_sml.get())
                d = self.eq9(bit, ka[y, x])
                dnew = self.eq10(d)
                dnewnew = self.eq11(dnew, bit)
                pixels[y, x*2] = self.eq13(dnewnew, ka[y, x])
        
        # Process diff > 192
        for y, x in zip(*np.where(mask_192_plus)):
            if not self.queue_big.empty():
                bit = int(self.queue_big.get())
                d = self.eq9(bit, ka[y, x])
                dnew = self.eq10(d)
                dnewnew = self.eq11(dnew, bit)
                pixels[y, x*2] = self.eq13(dnewnew, ka[y, x])
    
    # Save the modified image
    new_image = Image.fromarray(pixels)
    new_image.save('Original_Dataset/new.png')
