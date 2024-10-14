from PIL import Image
import pytesseract

# Function to create a grid from an image
def create_grid_from_image(image_path):
    # Load the image
    img = Image.open(image_path)

    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(img)

    # Clean up the extracted text and split it into letters
    letters = []
    for char in extracted_text:
        if char.isalpha():  # Only keep alphabetical characters
            letters.append(char.upper())  # Convert to uppercase

    # Create a 15x15 grid (or whatever dimensions you need)
    grid_size = 15
    grid = []
    for i in range(grid_size):
        row = letters[i * grid_size:(i + 1) * grid_size]
        grid.extend(row)

    # If there are fewer letters than needed for a full grid, fill with empty spaces
    while len(grid) < grid_size * grid_size:
        grid.append(' ')  # You can replace ' ' with any character you want for empty spaces

    return grid

# Example usage
def main():
    image_path = "grid.png"  # Replace with your image path
    grid = create_grid_from_image(image_path)

    # Return the grid as a single list
    print(grid)

if __name__ == "__main__":
    main()
