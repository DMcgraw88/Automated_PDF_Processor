# DESCRIPTION:
# This script monitors a designated folder for incoming PDF files. 
# Upon detecting a new PDF file, it extracts information from predefined regions using OCR. Job name, order number, and dealer name are extracted.
# The extracted text is sanitized to ensure valid characters for file naming.
# Order number and job name are used to rename the file.
# Dealer name is used to moved the renamed file to a destination folder specific to that name.
# The script requires the following configurations and setup to work properly:

# REQUIREMENTS:
# 1. Python Environment: Ensure Python is installed on your system.
# 2. Libraries: Install the required libraries using `pip`:
#    - `pdf2image`: For converting PDF files to images.
#    - `pytesseract`: For performing OCR (Optical Character Recognition).
#    - `watchdog`: For monitoring file system events.
# 3. Tesseract OCR: Install Tesseract OCR and set the path (if not done already):
#    - Download and install Tesseract OCR from https://github.com/tesseract-ocr/tesseract.
#    - Set the Tesseract path in the script or as an environment variable.
# 4. Input Folder: Define the path to the folder where incoming PDFs will be dropped.
# 5. Output Folder: Define the path to the folder where renamed and categorized PDFs will be moved.
# 6. OCR Configuration: Define the coordinates (`x1, y1, x2, y2`) for the regions to extract text from within the PDFs.
# 7. File Structure: Ensure the input folder follows the desired structure and only contains PDF files
#    with the expected content layout for successful OCR.

import os
import string
import unicodedata
from pdf2image import convert_from_path
import pytesseract
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def sanitize_text(text):
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    normalized_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    # Filter out characters not in valid_chars
    sanitized_text = ''.join(c if c in valid_chars else '' for c in normalized_text)
    return sanitized_text

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:  # Skip directories
            return
        if event.src_path.endswith('.pdf'):  # Process only PDF files
            process_file(event.src_path)

def process_file(pdf_path):
    # Convert the first page of the PDF to an image
    pages = convert_from_path(pdf_path, first_page=1, last_page=1)

    # Assuming x1, y1, x2, y2 are the coordinates of the regions you want to extract text from
    x1_1, y1_1, x2_1, y2_1 = 1300, 250, 1500, 400
    x1_2, y1_2, x2_2, y2_2 = 250, 760, 600, 800
    x1_3, y1_3, x2_3, y2_3 = 90, 500, 600, 557

    # Extract text from the specified regions
    for i, page in enumerate(pages):
        # Crop regions from the page image
        region1 = page.crop((x1_1, y1_1, x2_1, y2_1))
        region2 = page.crop((x1_2, y1_2, x2_2, y2_2))
        region3 = page.crop((x1_3, y1_3, x2_3, y2_3))

        # Perform OCR on cropped regions
        OrderNumber = pytesseract.image_to_string(region1)
        JobName = pytesseract.image_to_string(region2)
        DealerName = pytesseract.image_to_string(region3)

        # Rename the file using extracted variables
        base_name, extension = os.path.splitext(pdf_path)
        new_file_name = f"{sanitize_text(OrderNumber)}_{sanitize_text(JobName)}{extension}"
        os.rename(pdf_path, new_file_name)

        # For debugging
        #print(f"Text from Region 1 on page {i + 1}:")
        #print(OrderNumber)
        #print(f"Text from Region 2 on page {i + 1}:")
        #print(JobName)
        #print(f"Text from Region 3 on page {i + 1}:")
        #print(DealerName)

        # Generate the destination folder based on DealerName
        dealer_folder = sanitize_text(DealerName)  # Sanitize the DealerName for folder naming
        destination_folder = f'/Users/destination_path/{dealer_folder}' # Replace with output folder path

        # Create the dealer-specific folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        # Move the file to the dealer-specific folder
        shutil.move(new_file_name, os.path.join(destination_folder, new_file_name))

if __name__ == "__main__":
    folder_to_watch = '/Users/file/to/monitor/path'  # Replace with folder to monitor

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
