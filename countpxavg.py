from PIL import Image
import numpy as np

# Specify the path to your image file
image_path = 'path_to_your_image.jpg'  # Replace with your image file path

# Open the image using PIL
try:
    image = Image.open(image_path)
except FileNotFoundError:
    print(f"Error: The file at {image_path} was not found.")
    exit()

# Convert the image to a NumPy array
image_array = np.array(image)

# Check if the image is grayscale or color
if image_array.ndim == 2:
    # Grayscale image
    average_pixel_value = image_array.mean()
    print(f"The average pixel value of the grayscale image is: {average_pixel_value:.2f}")
elif image_array.ndim == 3:
    # Color image
    # Calculate the average per channel (R, G, B)
    average_per_channel = image_array.mean(axis=(0, 1))
    print("The average pixel values per channel are:")
    print(f"  Red:   {average_per_channel[0]:.2f}")
    print(f"  Green: {average_per_channel[1]:.2f}")
    print(f"  Blue:  {average_per_channel[2]:.2f}")
    # Calculate the overall average pixel value
    overall_average = image_array.mean()
    print(f"The overall average pixel value of the color image is: {overall_average:.2f}")
else:
    print("Unsupported image format.")
