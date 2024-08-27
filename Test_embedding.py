import numpy as np

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
    
    # Convert queues to arrays for faster access
    bits_sml = np.array(list(self.queue_sml), dtype=int)
    bits_big = np.array(list(self.queue_big), dtype=int)
    
    if self.avg_pixel_value > 150:
        kb = pixels[:, ::2] - pixel_mod_4[:, ::2]
        
        # Process 128 <= diff <= 192
        idx_sml = np.where(mask_128_192)
        d_sml = self.eq8(bits_sml[:len(idx_sml[0])], kb[idx_sml])
        dnew_sml = self.eq10(d_sml)
        dnewnew_sml = self.eq11(dnew_sml, bits_sml[:len(idx_sml[0])])
        pixels[idx_sml[0], idx_sml[1]*2] = self.eq12(dnewnew_sml, kb[idx_sml])
        
        # Process diff > 192
        idx_big = np.where(mask_192_plus)
        d_big = self.eq8(bits_big[:len(idx_big[0])], kb[idx_big])
        dnew_big = self.eq10(d_big)
        dnewnew_big = self.eq11(dnew_big, bits_big[:len(idx_big[0])])
        pixels[idx_big[0], idx_big[1]*2] = self.eq12(dnewnew_big, kb[idx_big])
    else:
        ka = pixels[:, ::2] + pixel_mod_4_abs_3[:, ::2]
        
        # Process 128 <= diff <= 192
        idx_sml = np.where(mask_128_192)
        d_sml = self.eq9(bits_sml[:len(idx_sml[0])], ka[idx_sml])
        dnew_sml = self.eq10(d_sml)
        dnewnew_sml = self.eq11(dnew_sml, bits_sml[:len(idx_sml[0])])
        pixels[idx_sml[0], idx_sml[1]*2] = self.eq13(dnewnew_sml, ka[idx_sml])
        
        # Process diff > 192
        idx_big = np.where(mask_192_plus)
        d_big = self.eq9(bits_big[:len(idx_big[0])], ka[idx_big])
        dnew_big = self.eq10(d_big)
        dnewnew_big = self.eq11(dnew_big, bits_big[:len(idx_big[0])])
        pixels[idx_big[0], idx_big[1]*2] = self.eq13(dnewnew_big, ka[idx_big])
    
    # Save the modified image
    new_image = Image.fromarray(pixels)
    new_image.save('Original_Dataset/new.png')
