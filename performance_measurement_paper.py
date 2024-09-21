import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os
from math import log10, sqrt 
  
def calculate_psnr(original, compressed): 
    mse = np.mean((original - compressed) ** 2) 
    if(mse == 0):  # MSE is zero means no noise is present in the signal . 
                  # Therefore PSNR have no importance. 
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse)) 
    return psnr 

def main():
    # Define the paths
    image_folder = "Original_Dataset"
    stego_folder = "Stego_Images"
    
    # List of image names and their corresponding file extensions
    image_names = [
        "Aerial.tiff", "Airplane.tiff", "Car and APCs.tiff", "Fishing Boat.tiff",
        "Pixel ruler.tiff", "Stream and bridge.tiff", "Tank.tiff", "Truck.tiff"
    ]
    
    # List of bit file suffixes
    input_bit_files = [
        "random-binary_1Kb", "random-binary_10Kb", "random-binary_20Kb", "random-binary_30Kb",
        "random-binary_40Kb", "random-binary_50Kb", "random-binary_60Kb", "random-binary_70Kb",
        "random-binary_80Kb", "random-binary_90Kb", "random-binary_100Kb"
    ]
    
    # Iterate over each image and compare the original with its corresponding stego image
    for image_name in image_names:
        original_image_path = os.path.join(image_folder, image_name)
        
        # Load the original image in grayscale mode
        img1 = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
        if img1 is None:
            print(f"Original image {image_name} not found.")
            continue
        
        # Iterate over each stego image
        for bit_file_suffix in input_bit_files:
            stego_image_name = f"{os.path.splitext(image_name)[0]}_{bit_file_suffix}.tiff"
            stego_image_path = os.path.join(stego_folder, stego_image_name)
            
            # Load the stego image in grayscale mode
            img2 = cv2.imread(stego_image_path, cv2.IMREAD_GRAYSCALE)
            if img2 is None:
                print(f"Stego image {stego_image_name} not found.")
                continue
            
            # Ensure that both images have the same shape
            if img1.shape != img2.shape:
                print(f"The images {image_name} and {stego_image_name} do not have the same dimensions. Skipping comparison.")
                continue
            
            # Calculate PSNR
            psnr_value = calculate_psnr(img1, img2)
            print(f"PSNR between {image_name} and {stego_image_name}: {psnr_value:.2f} dB")
            
            # Calculate SSIM
            ssim_value = ssim(img1, img2)
            print(f"SSIM between {image_name} and {stego_image_name}: {ssim_value:.4f}")

if __name__ == "__main__":
    main()
