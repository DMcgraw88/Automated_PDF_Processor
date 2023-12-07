Automated_PDF_Processor


This Python script monitors a specified folder for incoming PDF files, processes them using OCR (Optical Character Recognition),extracts data from target areas, and categorizes the extracted data into designated folders based on extracted information.

Features:

* Monitors a designated folder for incoming PDF files.
* Extracts text content from specific regions of the PDF using OCR.
* Renames processed files based on extracted information.
* Sorts processed files into folders based on extracted details.
  
Requirements:

* Python 3.x
* pdf2image
* pytesseract
* watchdog

Usage:

1. Ensure the required Python libraries are installed.
2. Specify folder to monitor and output folder path
3. Specify coordinates for info to be extracted
4. Run the script
5. Drop PDF files into the monitored folder to initiate processing.
