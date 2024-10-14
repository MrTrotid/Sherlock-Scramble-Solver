    import pytesseract
    from PIL import Image

    def extract_words_from_image(image_path="words.png"):
        """Extracts words from an image using pytesseract.

        Args:
            image_path (str): The path to the image file.

        Returns:
            list: A list of words extracted from the image.
        """
        try:
            # Load the image
            img = Image.open(image_path)

            # Optionally preprocess the image (convert to grayscale)
            img = img.convert("L")  # Convert to grayscale

            # Extract text using pytesseract
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img, config=custom_config)

            # Split the extracted text into words and filter unwanted characters
            words = [word for word in text.split() if all(char.isalpha() for char in word)]
            return words

        except Exception as e:
            print(f"Error: {e}")
            return []

    # Example usage
    if __name__ == "__main__":
        words = extract_words_from_image("words.png")
        print(words)
