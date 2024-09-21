import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_psnr(img1, img2):
    # Compute the Mean Squared Error (MSE)
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:  # MSE is zero means no noise is present in the signal
        return float('inf')
    # Calculate PSNR
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr

def calculate_ssim(img1, img2):
    # Calculate SSIM
    ssim_index, _ = ssim(img1, img2, full=True)
    return ssim_index

def main():
    # Load the old and new images in grayscale mode
    img1 = cv2.imread("Original_Dataset\\old.png", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread("Compressed_Images\\new10.png", cv2.IMREAD_GRAYSCALE)
    
    # Ensure that both images have the same shape
    if img1.shape != img2.shape:
        print("The images do not have the same dimensions. Please check the input images.")
        return
    
    # Calculate PSNR
    psnr_value = calculate_psnr(img1, img2)
    print(f"PSNR between the images: {psnr_value:.2f} dB")
    
    # Calculate SSIM
    ssim_value = calculate_ssim(img1, img2)
    print(f"SSIM between the images: {ssim_value:.4f}")

if __name__ == "__main__":
    main()
