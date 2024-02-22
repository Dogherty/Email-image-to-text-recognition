# Recognizing Email addresses on photos

This Python script employs `OpenCV` and `Tesseract OCR` to extract email addresses from images. It provides a comprehensive solution by preprocessing images to enhance text recognition, extracting emails using `Tesseract OCR`, and writing the results to an output file. Ideal for automating email extraction tasks from image-based documents or scans.

## Code structure

### ImageProcessor Class:

1. Reads an image file using `OpenCV`.
2. Preprocesses the image for better OCR results:
3. Resizes the image.
4. Converts it to grayscale.
5. Enhances contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization).
6. Reduces noise with median blurring.
7. Sharpens edges.
8. Binarizes the image using thresholding.

### EmailExtractor Class:

1. Utilizes `Tesseract OCR` to extract text from the preprocessed image.
2. Applies regular expressions to identify email addresses in the extracted text.

### EmailWriter Class:

1. Writes the extracted email addresses to an output file.

### Main Execution:

1. Specifies paths to the image file, output file, and Tesseract executable.
2. Initializes `ImageProcessor`, `EmailExtractor`, and `EmailWriter`.
3. Reads the image, preprocesses it, extracts emails, and writes them to the output file.

## Requirements

You will need the following dependencies listed in the `requirements.txt` file to successfully run the project:

- pytesseract 0.3.10
- opencv-python 4.9.0.80
- numpy 1.26.4

Also you need to download `Tesseract OCR` from the official [website](https://tesseract-ocr.github.io/). [Download for Windows](https://github.com/UB-Mannheim/tesseract/wiki)

## Installation

1. Clone the project repository to your local computer:
   
	```bash
	git clone https://github.com/Dogherty/Email-image-to-text-recognition.git

2. Install the Python dependencies specified in requirements.txt:
   
	```bash
	pip install -r requirements.txt

3. Specify the path to the installed `Tesseract OCR`:
   
	```bash
	TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

## Note

For best text recognition, letters should be about 35 pixels high
