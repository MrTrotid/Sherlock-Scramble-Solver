from PIL import Image, ImageDraw, ImageFont

# Define the grid as a list of lists (2D array)
grid = 

NUM_ROWS = len(grid)
NUM_COLS = len(grid[0])

# Set cell size for the image
cell_size = 40  # Set to an appropriate size

# Use the same search words and directions
DIRECTIONS = [
    (0, 1),  # right
    (1, 0),  # down
    (1, 1),  # down-right
    (1, -1),  # down-left
    (0, -1),  # left
    (-1, 0),  # up
    (-1, -1),  # up-left
    (-1, 1)  # up-right
]

# Define a list of colors for highlighting
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255),  # Cyan
    (255, 192, 203), # Pink
    (165, 42, 42),  # Brown
    (128, 128, 0),  # Olive
]

# Function to check if a word is present starting at a specific coordinate
def find_word(word, start_row, start_col, direction, grid):
    d_row, d_col = direction
    for i in range(len(word)):
        r = start_row + i * d_row
        c = start_col + i * d_col
        if r < 0 or r >= NUM_ROWS or c < 0 or c >= NUM_COLS:
            return False
        if grid[r][c] != word[i]:  # Access grid as 2D list
            return False
    return True

# Search for words in the grid
def search_words(grid, words):
    found_words = {}
    for word in words:
        word_found = False
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                for direction in DIRECTIONS:
                    if find_word(word, row, col, direction, grid):
                        found_words[word] = (row, col, direction)
                        word_found = True
                        break
                    if find_word(word[::-1], row, col, direction, grid):
                        found_words[word] = (row, col, direction)
                        word_found = True
                        break
                if word_found:
                    break
            if word_found:
                break
    return found_words

# Create an image with highlighted words
def create_image(words, grid, found_words):
    img_width = NUM_COLS * cell_size
    img_height = NUM_ROWS * cell_size

    # Use a dark background color
    img = Image.new("RGB", (img_width, img_height), "#1C1C1C")  # Dark background
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()

    # Draw the grid and letters with light colors
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = (col + 1) * cell_size, (row + 1) * cell_size
            draw.rectangle([x1, y1, x2, y2], outline="black", width=2)  # Outline in black

            # Center the text in the cell
            text = grid[row][col]
            bbox = draw.textbbox((0, 0), text, font=font)  # Get bounding box
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x_text = x1 + (cell_size - text_width) / 2
            y_text = y1 + (cell_size - text_height) / 2
            draw.text((x_text, y_text), text, fill="white", font=font)  # Text in white

    # Highlight found words with different colors
    for i, (word, (start_row, start_col, direction)) in enumerate(found_words.items()):
        d_row, d_col = direction
        color = COLORS[i % len(COLORS)]  # Cycle through colors
        for j in range(len(word)):
            r = start_row + j * d_row
            c = start_col + j * d_col
            x1, y1 = c * cell_size, r * cell_size
            x2, y2 = (c + 1) * cell_size, (r + 1) * cell_size
            draw.rectangle([x1, y1, x2, y2], outline=color, width=4)  # Highlighted word outline

    return img

# Main execution
def main():
    # Define a fixed list of words to search for
    words_from_image = 

    found_words = search_words(grid, words_from_image)

    if not found_words:
        print("No words found!")
    else:
        for word, location in found_words.items():
            print(f"Found word '{word}' at {location}")

    highlighted_img = create_image(words_from_image, grid, found_words)

    output_image_path = "highlighted_word_search.png"
    highlighted_img.save(output_image_path)

    print(f"Output image saved as '{output_image_path}'.")

if __name__ == "__main__":
    main()
