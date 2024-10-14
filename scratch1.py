from PIL import Image, ImageDraw, ImageFont
import pytesseract

# Function to create a grid from an image
def create_grid_from_image(image_path, grid_size=15):
    # Load the image
    img = Image.open(image_path)

    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(img)

    # Clean up the extracted text and split it into letters
    letters = [char.upper() for char in extracted_text if char.isalpha()]

    # Create the grid
    grid = []
    for i in range(grid_size):
        row = letters[i * grid_size:(i + 1) * grid_size]
        grid.extend(row)

    # Fill with empty spaces if fewer letters are available
    grid.extend([' '] * (grid_size * grid_size - len(grid)))

    return grid

# Define the directions to search
DIRECTIONS = [
    (0, 1),   # right
    (1, 0),   # down
    (1, 1),   # down-right
    (1, -1),  # down-left
    (0, -1),  # left
    (-1, 0),  # up
    (-1, -1), # up-left
    (-1, 1)   # up-right
]

# Function to check if a word is present starting at a specific coordinate
def find_word(word, start_row, start_col, direction, grid, num_cols):
    d_row, d_col = direction
    for i in range(len(word)):
        r = start_row + i * d_row
        c = start_col + i * d_col
        if r < 0 or r >= len(grid) // num_cols or c < 0 or c >= num_cols:
            return False
        if grid[r * num_cols + c] != word[i]:
            return False
    return True

# Search for words in the grid
def search_words(grid, words, num_cols):
    found_words = {}
    for word in words:
        word_found = False
        for row in range(len(grid) // num_cols):
            for col in range(num_cols):
                for direction in DIRECTIONS:
                    if find_word(word, row, col, direction, grid, num_cols):
                        found_words[word] = (row, col, direction)
                        word_found = True
                        break
                    if find_word(word[::-1], row, col, direction, grid, num_cols):
                        found_words[word] = (row, col, direction)
                        word_found = True
                        break
                if word_found:
                    break
            if word_found:
                break
    return found_words

# Create an image with the highlighted words and separated grid
def create_image(words, grid, found_words, num_cols):
    cell_size = 40
    img_width = num_cols * cell_size
    img_height = (len(grid) // num_cols + 1) * cell_size  # Extra row for words

    # Create a blank white image
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Use a default font for simplicity
    font = ImageFont.load_default()

    # Draw the words to find at the top of the image
    for i, word in enumerate(words):
        x = i * cell_size + cell_size // 4
        y = cell_size // 4
        draw.text((x, y), word, fill="black", font=font)

    # Draw the grid lines and letters
    for row in range(len(grid) // num_cols):
        for col in range(num_cols):
            # Calculate the position for each cell
            x1, y1 = col * cell_size, (row + 1) * cell_size
            x2, y2 = (col + 1) * cell_size, (row + 2) * cell_size
            draw.rectangle([x1, y1, x2, y2], outline="black", width=1)
            # Draw each letter in the center of its cell
            x_text = x1 + cell_size // 4
            y_text = y1 + cell_size // 4
            draw.text((x_text, y_text), grid[row * num_cols + col], fill="black", font=font)

    # Highlight the found words
    for word, (start_row, start_col, direction) in found_words.items():
        d_row, d_col = direction
        for i in range(len(word)):
            r = start_row + i * d_row
            c = start_col + i * d_col
            x1, y1 = c * cell_size, (r + 1) * cell_size
            x2, y2 = (c + 1) * cell_size, (r + 2) * cell_size
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

    return img

# Main execution
def main():
    image_path = "grid.png"  # Replace with your image path
    grid = create_grid_from_image(image_path)  # Create grid from the image

    # Define words to search for
    words = [
        "COMMUNITY", "EXAMS", "GRADE", "PANORAMA", "PASTPAPER", "PROFESSORS",
        "PUBLICATIONS", "QUALIFICATIONS", "RESULTS", "VISTAS"
    ]

    # Search for words in the grid
    found_words = search_words(grid, words, num_cols=15)

    # Debugging output for found words
    if not found_words:
        print("No words found!")
    else:
        for word, location in found_words.items():
            print(f"Found word '{word}' at {location}")

    # Create and save the highlighted image
    highlighted_img = create_image(words, grid, found_words, num_cols=15)
    output_image_path = "highlighted_word_search.png"
    highlighted_img.save(output_image_path)

    print(f"Output image saved as '{output_image_path}'.")

if __name__ == "__main__":
    main()
