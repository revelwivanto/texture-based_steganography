import os
import cv2
import numpy as np

def compress_intensity_array(intensity_array):
    rows = intensity_array.shape[0]
    cols = intensity_array.shape[1]

    int_string = np.zeros((rows * cols))
    idx = 0

    # Creating a string of all intensity values
    for i in range(0, rows):
        for j in range(0, cols):
            int_string[idx] = intensity_array[i, j]
            idx = idx + 1

    crs = ""  # currently recognized sequence
    curr = ""  # current sequence

    output = {}
    out_idx = 0

    dict_val = {}
    dict_idx = 0

    # Initialize dictionary with single values
    for i in range(0, 256):
        dict_val[str(i)] = i

    dict_idx = 256  # Next unused location in the dictionary
    curr = int_string[0]
    crs = str(int(curr))

    # Compression algorithm (similar to LZW)
    for i in range(1, idx):
        curr = int_string[i]
        t_str = crs + "-" + str(int(curr))

        if t_str in dict_val:
            crs = t_str
        else:
            output[out_idx] = dict_val[crs]
            out_idx = out_idx + 1
            crs = str(int(curr))
            dict_val[t_str] = dict_idx
            dict_idx = dict_idx + 1

    # Last entry
    if crs in dict_val:
        output[out_idx] = dict_val[crs]
        out_idx = out_idx + 1

    # Return the compressed output
    return output


def save_compressed_image(compressed_output, shape, output_image_path):
    # Convert the compressed data into a numpy array for image representation
    compressed_values = list(compressed_output.values())
    compressed_array = np.array(compressed_values, dtype=np.uint8)

    # Reshape the compressed array into the original image shape
    # If necessary, adjust the size here for proper reshaping (padding/truncating)
    compressed_array = np.resize(compressed_array, shape)

    # Save the compressed array as an image
    cv2.imwrite(output_image_path, compressed_array)


def main():
    # Define the input folder and output folder
    input_folder = "Stego_Images"
    output_folder = "Compressed_Images"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.tiff') or f.endswith('.png') or f.endswith('.jpg')]

    # Loop through each image file
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)

        # Load the image in grayscale mode
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Could not read {image_file}")
            continue

        # Compress the intensity array of the image
        compressed_output = compress_intensity_array(image)

        # Save the compressed image
        output_image_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_compressed.png")

        # Save the compressed output as an image
        save_compressed_image(compressed_output, image.shape, output_image_path)

        print(f"Compressed and saved {image_file} at {output_image_path}")


if __name__ == "__main__":
    main()
