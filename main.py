import cv2
import pytesseract
import numpy as np
import re
import os

# Клас для обробки зображення
# Class for processing the image
class ImageProcessor:
    def __init__(self, image_path, output_file, tesseract_path):
        self.image_path = image_path
        self.output_file = output_file
        self.tesseract_cmd_path = tesseract_path

    def read_image(self):
        # Перевірка, чи існує файл зображення
        # Check if the image file exists
        if not os.path.exists(self.image_path):
            raise FileNotFoundError("Failed to read the image.")
        # Зчитати зображення за допомогою OpenCV
        # Read the image using OpenCV
        image = cv2.imread(self.image_path)
        # Перевірка успішності зчитування зображення
        # Check if the image is successfully read
        if image is None:
            raise FileNotFoundError("Failed to read the image.")
        return image

    def preprocess_image(self, image):
        # Зміна розміру зображення для поліпшення обробки
        # Resize the image to improve processing
        height, width, _ = image.shape
        scale_factor = max(1, min(5, 2000 / max(height, width)))
        image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

        # Конвертувати зображення у відтінки сірого
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Застосування адаптивного гістограмного вирівнювання обмеженої контрастності (CLAHE) для підвищення контрастності
        # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) to enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(gray)

        # Застосування медіанного згладжування для зменшення шуму
        # Apply median blurring to reduce noise
        denoised = cv2.medianBlur(contrast_enhanced, 3)

        # Застосування відзначення граней для підвищення різкості
        # Apply sharpening to enhance edges
        sharpening_kernel = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
        sharp = cv2.filter2D(denoised, -1, sharpening_kernel)

        # Застосування порогової обробки для бінаризації зображення
        # Apply thresholding to binarize the image
        _, thresh = cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return thresh

# Клас для вилучення електронних адрес з обробленого зображення
# Class for extracting emails from the processed image
class EmailExtractor:
    def __init__(self, tesseract_cmd_path, language='eng'):
        self.tesseract_cmd_path = tesseract_cmd_path
        self.language = language

        # Встановлення шляху до Tesseract
        # Set the Tesseract command path
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    def extract_emails(self, image):
        # Використання Tesseract для вилучення тексту з зображення
        # Use Tesseract to extract text from the image
        text = pytesseract.image_to_string(image, lang=self.language)

        # Використання регулярних виразів для пошуку електронних адрес у вилученому тексті
        # Use regular expression to find email addresses in the extracted text
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        return emails

# Клас для запису вилучених електронних адрес у файл
# Class for writing extracted emails to a file
class EmailWriter:
    def __init__(self, output_file):
        self.output_file = output_file

    def write_emails(self, emails):
        # Запис вилучених електронних адрес у вихідний файл
        # Write the extracted emails to the output file
        with open(self.output_file, 'w') as file:
            if emails:
                for email in emails:
                    file.write(email + '\n')
                print(f'Found {len(emails)} E-mail addresses. Saved in {self.output_file}')
            else:
                print('No e-mail address found.')

if __name__ == "__main__":
    # Шлях до Tesseract та імена файлів
    # Paths to Tesseract and file names
    IMAGE_PATH = 'your_image_path.jpg'
    OUTPUT_FILE = 'emails.txt'
    TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Ініціалізація ImageProcessor та обробка зображення
    # Initialize ImageProcessor and process the image
    image_processor = ImageProcessor(IMAGE_PATH, OUTPUT_FILE, TESSERACT_PATH)
    image = image_processor.read_image()
    processed_image = image_processor.preprocess_image(image)

    # Ініціалізація EmailExtractor та вилучення електронних адрес з обробленого зображення
    # Initialize EmailExtractor and extract emails from the processed image
    email_extractor = EmailExtractor(TESSERACT_PATH)
    emails = email_extractor.extract_emails(processed_image)

    # Ініціалізація EmailWriter та запис вилучених електронних адрес у файл
    # Initialize EmailWriter and write the extracted emails to a file
    email_writer = EmailWriter(OUTPUT_FILE)
    email_writer.write_emails(emails)