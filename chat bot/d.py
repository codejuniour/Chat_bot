from PIL import Image
import pytesseract

# Load the image
image_path = "/mnt/data/1721140039823.png"
image = Image.open(image_path)

# Extract text using OCR
extracted_text = pytesseract.image_to_string(image)

# Display a snippet of the extracted text
extracted_text[:1000]  # Showing first 1000 characters to check extraction quality
