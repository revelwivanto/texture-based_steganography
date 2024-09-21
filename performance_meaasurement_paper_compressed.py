import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os
from math import log10, sqrt

# Function to calculate PSNR
def calculate_psnr(original, compressed): 
    mse = np.mean((original - compressed) ** 2) 
    if(mse == 0):  # MSE is zero means no noise is present in the signal . 
                  # Therefore PSNR have no importance. 
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse)) 
    return psnr 

def main():
    # Define the input folders
    original_folder = "Original_Dataset"
    compressed_folder = "Compressed_Images"

    # List of image names and bit suffixes
    image_names = [
        "Aerial.tiff", "Airplane.tiff", "Car and APCs.tiff", "Fishing Boat.tiff",
        "Pixel ruler.tiff", "Stream and bridge.tiff", "Tank.tiff", "Truck.tiff"
    ]
    input_bit_files = [
        "random-binary_1Kb", "random-binary_10Kb", "random-binary_20Kb", "random-binary_30Kb",
        "random-binary_40Kb", "random-binary_50Kb", "random-binary_60Kb", "random-binary_70Kb",
        "random-binary_80Kb", "random-binary_90Kb", "random-binary_100Kb"
    ]
    
    # Loop through each image
    for image_name in image_names:
        original_image_path = os.path.join(original_folder, image_name)
        
        # Load the original image in grayscale
        original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
        if original_image is None:
            print(f"Original image {image_name} not found.")
            continue
        
        for bit_file_suffix in input_bit_files:
            compressed_image_name = f"{os.path.splitext(image_name)[0]}_{bit_file_suffix}.png"
            compressed_image_path = os.path.join(compressed_folder, compressed_image_name)
            
            # Load the compressed stego image in grayscale
            compressed_image = cv2.imread(compressed_image_path, cv2.IMREAD_GRAYSCALE)
            if compressed_image is None:
                print(f"Compressed image {compressed_image_name} not found.")
                continue
            
            # Calculate PSNR and SSIM between original image and compressed stego image
            psnr_value = calculate_psnr(original_image, compressed_image)
            ssim_value = ssim(original_image, compressed_image)
            
            # Print results
            print(f"PSNR between {image_name} and {compressed_image_name}: {psnr_value:.2f} dB")
            print(f"SSIM between {image_name} and {compressed_image_name}: {ssim_value:.4f}")

if __name__ == "__main__":
    main()
