import os
import glob
from datetime import datetime
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import time

def fetch_image_file(base_name="original_image", extensions=("png","jpg","jpeg")):
    """"Fetch the image file with the given base name and extensions."""""
    for ext in extensions:
        pattern = f"{base_name}.{ext}"
        matching_files = glob.glob(pattern)

        if matching_files:
            # Return the first matching file
            return matching_files[0]
        
    return None

def print_with_delay(message, delay=0):
    """Print a message with a delay."""
    print(message)
    time.sleep(delay)

def resize_and_crop_image(image_path, target_size, background_color=(255, 255, 255)):
    print_with_delay(f"Resizing and cropping image to {target_size} with background color {background_color}...")
    img = Image.open(image_path)
    img.thumbnail(target_size, Image.Resampling.LANCZOS)  # Resize while maintaining aspect ratio

    # Create a new image with the target size and white background
    new_img = Image.new("RGB", target_size, background_color)

    # Calculate position to paste the resized image on the new image
    paste_position = (
        (new_img.width - img.width) // 2,
        (new_img.height - img.height) // 2
    )

    new_img.paste(img, paste_position)
    return new_img

def resize_and_crop_passport_image(image_path, background_color=(255, 255, 255)):
    print_with_delay("Resizing passport image...")
    dpi = 300  # Standard print DPI
    resize_size = (int(45 / 25.4 * dpi), int(45 / 25.4 * dpi))  # 45mm x 45mm
    crop_width = int(35 / 25.4 * dpi)  # 35mm

    img = Image.open(image_path)
    img.thumbnail(resize_size, Image.Resampling.LANCZOS)  # Resize while maintaining aspect ratio

    # Crop the image to 35mm width, keeping the 45mm height
    left = (img.width - crop_width) / 2
    right = (img.width + crop_width) / 2

    img = img.crop((left, 0, right, img.height))  # Crop only the width, keeping the height

    # Create a new image with the target size and white background
    target_size = (crop_width, img.height)
    new_img = Image.new("RGB", target_size, background_color)

    # Calculate position to paste the resized image on the new image
    paste_position = (
        (new_img.width - img.width) // 2,
        (new_img.height - img.height) // 2
    )

    new_img.paste(img, paste_position)
    return new_img

def add_border(image, border_size=1, border_color=(0, 0, 0)):
    print_with_delay(f"Adding border of size {border_size} and color {border_color} to image...")
    return ImageOps.expand(image, border=border_size, fill=border_color)

def create_folder_structure(create_2x2=False, create_1x1=False, create_passport=False):
    print("Creating folder structure for saving images...")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    folders = {}
    
    if create_2x2:
        folders["2x2"] = os.path.join("2x2", f"PID_{timestamp}")
    if create_1x1:
        folders["1x1"] = os.path.join("1x1", f"PID_{timestamp}")
    if create_passport:
        folders["passport"] = os.path.join("passport", f"PID_{timestamp}")

    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)

    return folders

def generate_and_save_images(image_path, folders):
    print_with_delay("Generating and saving images directly to folders...")
    dpi = 300  # Standard print DPI
    size_2x2 = (2 * dpi, 2 * dpi)  # 2x2 inches
    size_1x1 = (1 * dpi, 1 * dpi)  # 1x1 inches

    image_2x2 = resize_and_crop_image(image_path, size_2x2)
    image_1x1 = resize_and_crop_image(image_path, size_1x1)
    image_passport = resize_and_crop_passport_image(image_path)

    image_2x2 = add_border(image_2x2, border_size=2, border_color=(0, 0, 0))
    image_1x1 = add_border(image_1x1, border_size=2, border_color=(0, 0, 0))
    image_passport = add_border(image_passport, border_size=2, border_color=(0, 0, 0))

    all_images = []

    for idx in range(4):
        image_2x2_path = os.path.join(folders["2x2"], f"2x2_image_{idx + 1}.png")
        print_with_delay(f"Saving 2x2 image {idx + 1} to {image_2x2_path}...")
        image_2x2.save(image_2x2_path, dpi=(300, 300))
        all_images.append(image_2x2_path)

    for idx in range(8):
        image_1x1_path = os.path.join(folders["1x1"], f"1x1_image_{idx + 1}.png")
        print_with_delay(f"Saving 1x1 image {idx + 1} to {image_1x1_path}...")
        image_1x1.save(image_1x1_path, dpi=(300, 300))
        all_images.append(image_1x1_path)

    for idx in range(5):
        image_passport_path = os.path.join(folders["passport"], f"passport_image_{idx + 1}.png")
        print_with_delay(f"Saving passport image {idx + 1} to {image_passport_path}...")
        image_passport.save(image_passport_path, dpi=(300, 300))
        all_images.append(image_passport_path)

    return all_images

def save_pdf(images, output_file):
    print_with_delay("Saving images to PDF file...")
    c = canvas.Canvas(output_file, pagesize=A4)
    page_width, page_height = A4

    dpi = 74
    dimensions = [
        (2 * dpi, 2 * dpi),
        (1 * dpi, 1 * dpi),
        (int(35 / 25.4 * dpi), int(45 / 25.4 * dpi))
    ]

    x = 1
    y = page_height - 1

    for idx, image_path in enumerate(images):
        if idx < 4:
            img_width, img_height = dimensions[0]
        elif idx < 12:
            img_width, img_height = dimensions[1]
        else:
            img_width, img_height = dimensions[2]

        c.drawImage(image_path, x, y - img_height, width=img_width, height=img_height)

        x += img_width
        if x + img_width > page_width:
            x = 1
            y -= img_height

    c.save()
    print_with_delay("PDF file saved.")
    os.startfile(output_file)

if __name__ == "__main__":
    #Fetch the image file
    image_path = fetch_image_file() # This will search for "original_image" with .png, .jpg, or .jpeg extension

    if not image_path:
        print("No image file named 'orginal_image' found with the specified extensions.")
    else:
        print_with_delay("Starting script...")

        folders = create_folder_structure()
        all_images = generate_and_save_images(image_path, folders)
        save_pdf(all_images, "all_images.pdf")

        print_with_delay("Script completed.")