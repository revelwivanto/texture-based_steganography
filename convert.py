import os
import cv2

def convert_tiff_to_png(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all .tiff files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.tiff')]

    # Loop through each .tiff file
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)

        # Load the .tiff image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read {image_file}")
            continue

        # Extract file name without extension
        base_name = os.path.splitext(image_file)[0]  # This safely handles multiple dots

        # Create the output file path (change extension to .png)
        output_image_path = os.path.join(output_folder, f"{base_name}.png")

        # Save the image as .png
        cv2.imwrite(output_image_path, image)

        print(f"Converted {image_file} to {output_image_path}")

def main():
    input_folder = "Stego_Images"  # Folder containing .tiff images
    output_folder = "Stego_Images_png"  # Folder where .png images will be saved

    # Convert all .tiff images to .png and save them in the output folder
    convert_tiff_to_png(input_folder, output_folder)

if __name__ == "__main__":
    main()
