import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Import functions from GSnaPx
from GSnapX import fetch_image_file, print_with_delay, resize_and_crop_image, resize_and_crop_passport_image, add_border, create_folder_structure

def generate_and_save_images(image_path, folders):
    print_with_delay("Generating and saving images directly to folders...")
    # Define DPI and sizes in inches
    dpi = 300  # Standard print DPI
    size_2x2 = (2 * dpi, 2 * dpi)  # 2x2 inches
    size_1x1 = (1 * dpi, 1 * dpi)  # 1x1 inches

    # Generate 2x2 and 1x1 images using resize_and_crop_image function
    image_2x2 = resize_and_crop_image(image_path, size_2x2)
    image_1x1 = resize_and_crop_image(image_path, size_1x1)

    # Generate passport size image using resize_and_crop_passport_image function
    image_passport = resize_and_crop_passport_image(image_path)

    # Add borders to the images
    image_2x2 = add_border(image_2x2, border_size=2, border_color=(0, 0, 0))
    image_1x1 = add_border(image_1x1, border_size=2, border_color=(0, 0, 0))
    image_passport = add_border(image_passport, border_size=2, border_color=(0, 0, 0))

    all_images = []

    # Duplicate and save images directly to folders
    for idx in range(3):
        image_2x2_path = os.path.join(folders["2x2"], f"2x2_image_{idx + 1}.png")
        print_with_delay(f"Saving 2x2 image {idx + 1} to {image_2x2_path}...")
        image_2x2.save(image_2x2_path, dpi=(300, 300))
        all_images.append(image_2x2_path)

    for idx in range(4):
        image_1x1_path = os.path.join(folders["1x1"], f"1x1_image_{idx + 1}.png")
        print_with_delay(f"Saving 1x1 image {idx + 1} to {image_1x1_path}...")
        image_1x1.save(image_1x1_path, dpi=(300, 300))
        all_images.append(image_1x1_path)

    for idx in range(0):
        image_passport_path = os.path.join(folders["passport"], f"passport_image_{idx + 1}.png")
        image_passport.save(image_passport_path, dpi=(300, 300))
        all_images.append(image_passport_path)

    return all_images

def save_pdf(images, output_file):
    print_with_delay("Saving images to PDF file...")
    c = canvas.Canvas(output_file, pagesize=A4)
    page_width, page_height = A4

    # Define dimensions for each type of image
    dpi = 74
    dimensions = [
        (2 * dpi, 2 * dpi),  # 2x2 inches
        (1 * dpi, 1 * dpi),  # 1x1 inches
        (int(35 / 25.4 * dpi), int(45 / 25.4 * dpi))   # Passport size (35mm x 45mm)
    ]

    # Initial positions
    x = 1
    y = page_height - 1

    # Add images to PDF
    for idx, image_path in enumerate(images):
        # Determine dimensions based on the image index
        if idx < 3:
            img_width, img_height = dimensions[0]
        elif idx < 7:
            img_width, img_height = dimensions[1]
        # else:
        #     img_width, img_height = dimensions[2]

        # Add spacer
        if idx == 5:  # Add spacer after the first 3 2x2 and 2 1x1 image 
            x += img_width * 6  # Spacer equivalent to 6 1x1 images

        # Draw the image
        c.drawImage(image_path, x, y - img_height, width=img_width, height=img_height)

        # Update x and y positions
        x += img_width
        if x + img_width > page_width:
            x = 1
            y -= img_height

    c.save()
    print_with_delay("PDF file saved.")

    # Automatically open the PDF file after saving
    os.startfile(output_file)    

if __name__ == "__main__":
    #Fetch the image file
    image_path = fetch_image_file() # This will search for "original_image" with .png, .jpg, or .jpeg extension

    if not image_path:
        print("No image file named 'orginal_image' found with the specified extensions.")
    else:
        print_with_delay("Starting script...")
 
        folders = create_folder_structure(create_2x2=True, create_1x1=True)
        print(folders)

        all_images = generate_and_save_images(image_path, folders)
        save_pdf(all_images, "all_images.pdf")

        print_with_delay("Script completed.")






