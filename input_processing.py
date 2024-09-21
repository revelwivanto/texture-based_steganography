from queue import Queue
from PIL import Image
import cv2
import numpy as np

def calculate_grayscale_image_variance(image):

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Confirm the image array is 2D (grayscale)
    if image_array.ndim != 2:
        raise ValueError("The image is not a grayscale image.")

    # Calculate the variance of pixel values
    variance_pixel_value = image_array.var()
    return variance_pixel_value

def create_queue(bit_string, var):
    """
    Processes a bit string into queues based on the decimal value of its 8-bit segments.
    If 'var' <= 6000.00, the function categorizes values into 4 queues.
    If 'var' > 6000.00, the function categorizes values into 2 queues.

    Returns:
        tuple: A tuple containing the queues and the queue_map.
    """
    # Clean the bit_string to remove any non-binary characters
    bit_string = ''.join(filter(lambda x: x in '01', bit_string))

    # Ensure the bit string length is a multiple of 8
    if len(bit_string) % 8 != 0:
        bit_string = bit_string.ljust(len(bit_string) + (8 - len(bit_string) % 8), '0')

    # Group the bit string into 8-bit segments
    groups = [bit_string[i:i+8] for i in range(0, len(bit_string), 8)]

    # Initialize all queues
    queue_vbig = Queue()
    queue_big = Queue()
    queue_sml = Queue()
    queue_vsml = Queue()
    queue_map = Queue()

    if var <= 6000.00:
        # Process groups into 4 queues
        for group in groups:
            decimal_value = int(group, 2)
            if 0 <= decimal_value <= 63:
                queue_vsml.put(decimal_value)
                queue_map.put('vsml')
            elif 64 <= decimal_value <= 127:
                queue_sml.put(decimal_value)
                queue_map.put('sml')
            elif 128 <= decimal_value <= 191:
                queue_big.put(decimal_value)
                queue_map.put('big')
            elif 192 <= decimal_value <= 255:
                queue_vbig.put(decimal_value)
                queue_map.put('vbig')
    else:
        # Process groups into 2 queues
        for group in groups:
            decimal_value = int(group, 2)
            if 0 <= decimal_value <= 127:
                queue_vsml.put(decimal_value)  # Reusing queue_sml as 'small'
                queue_map.put('vsml')
            elif 128 <= decimal_value <= 255:
                queue_vbig.put(decimal_value)
                queue_map.put('vbig')
        # The other queues remain empty

    return queue_vbig, queue_big, queue_sml, queue_vsml, queue_map
# Example usage for testing
bit_string = "100001010111010111110010001011010101111000111011100011001000010101100101111110111001110101110011001101110100000110000011000000010010111011010010011100100101001011001100000100101101010110010100000011000000101001111101111001011101111100000011100010100011010110011000110011100000"
image_path = "Original_Dataset\\Pixel ruler.tiff"
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
var = calculate_grayscale_image_variance(img)
queue_vbig, queue_big, queue_sml, queue_vsml, queue_map = create_queue(bit_string, var)

# Print the contents of each queue for debugging

print("\nQueue vbig:")
while not queue_vbig.empty():
    print(queue_vbig.get())

print("\nQueue big:")
while not queue_big.empty():
    print(queue_big.get())

print("\nQueue sml:")
while not queue_sml.empty():
    print(queue_sml.get())

print("\nQueue vsml:")
while not queue_vsml.empty():
    print(queue_vsml.get())

print("\nQueue map:")
while not queue_map.empty():
    print(queue_map.get())