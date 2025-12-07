import sys
from PIL import Image
import argparse

# 1. Define the ASCII characters from darkest to lightest
# You can experiment with different sets of characters!
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    """
    Resizes the image while maintaining aspect ratio.
    Note: ASCII characters are roughly twice as tall as they are wide,
    so we adjust the height by a factor of 0.55 to prevent the image from looking squished.
    """
    width, height = image.size
    ratio = height / width / 1.65  # Adjust this value (1.65) to tune the aspect ratio
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    """Converts the image to grayscale."""
    return image.convert("L")

def pixels_to_ascii(image):
    """Maps each pixel's grayscale value to an ASCII character."""
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("image_path", help="The path to the image file you want to convert.")
    parser.add_argument("--width", type=int, default=100, help="The width of the output ASCII art (default: 100).")
    parser.add_argument("--save", type=str, help="Optional: File path to save the output text.")

    args = parser.parse_args()

    try:
        image = Image.open(args.image_path)
    except Exception as e:
        print(f"Unable to find image: {e}")
        return

    # Process the image pipeline
    new_image_data = pixels_to_ascii(grayify(resize_image(image, args.width)))

    # Format the string into multiple lines based on the new width
    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[index:(index + args.width)] for index in range(0, pixel_count, args.width)])

    # Print to console
    print(ascii_image)

    # Optional: Save to file
    if args.save:
        with open(args.save, "w") as f:
            f.write(ascii_image)
        print(f"\n[+] ASCII art saved to {args.save}")

if __name__ == "__main__":
    main()
