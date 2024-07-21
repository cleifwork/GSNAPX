import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Import functions from GSnaPx
from GSnapX import fetch_image_file, print_with_delay, create_folder_structure, generate_and_save_images

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
        if idx < 4:
            img_width, img_height = dimensions[0]
        elif idx < 8:
            img_width, img_height = dimensions[2]
        else:
            img_width, img_height = dimensions[1]

         # Add spacer
        if idx == 10:  # Add spacer after the four 2x2 and four passport image 
            x += dimensions[2][0] * 4  # Passport spacer equivalent to 4 images

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
        print("No image file named 'orginal_image' found in the root folder.")
    else:
        print_with_delay("Starting script...")

        folders = create_folder_structure(create_2x2=True, create_1x1=True, create_passport=True)
        print(folders)

        all_images = generate_and_save_images(image_path, folders, qty_2x2=4, qty_1x1=4, qty_passport=4)

        save_pdf(all_images, "all_images.pdf")

        print_with_delay("Script completed.")





