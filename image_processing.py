import cv2
import numpy as np
import os

def calculate_ratios(image_path, output_dir):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Thresholding to segment the object
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    # Draw contours on a copy of the grayscale image
    image_copy = gray.copy()
    cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Draw circles on contour points
    image_copy2 = gray.copy()
    for contour in contours:
        for contour_point in contour:
            cv2.circle(image_copy2, (contour_point[0][0], contour_point[0][1]), 2, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Threshold again for binary image
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Detect edges to find boundaries
    edges = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
    
    # Create output images for object, boundary, and background
    background = np.ones_like(binary) * 255 - binary - edges
    
    # Save the images in the specified directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cv2.imwrite(os.path.join(output_dir, 'object.png'), image_copy2)
    cv2.imwrite(os.path.join(output_dir, 'boundary.png'), edges)
    cv2.imwrite(os.path.join(output_dir, 'background.png'), background)
    
    # Display the images to verify
    cv2.imshow('Object', image_copy2)
    cv2.imshow('Boundary', edges)
    cv2.imshow('Background', background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = 'Original_Dataset/Lena.jfif'
output_dir = 'Original_Dataset'

calculate_ratios(image_path, output_dir)
