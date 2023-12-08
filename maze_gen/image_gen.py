# Open and read the maze file
maze_file = open("example_maze.txt", "r")
text_maze = maze_file.read()

# Split the maze into lines
text_lines = text_maze.splitlines()

from PIL import Image, ImageDraw

# Define the size of the maze
maze_size = (3, 3)

# Define the number of pixels per unit
pixels_per_unit = 20

# Define the wall thickness in units
wall_thickness = 0.05

# Calculate the size of the image in pixels
image_size = (maze_size[0] * pixels_per_unit, (maze_size[1] + 2) * pixels_per_unit)

# Create a new image with the size of the maze
image = Image.new("RGB", image_size, "white")

# Create a draw object
draw = ImageDraw.Draw(image)

# Loop through each line of the maze
for i, line in enumerate(text_lines):
    # Loop through each character in the line
    for j, char in enumerate(line):
        # Calculate the position of the rectangle in pixels
        # Calculate the size of the rectangle in pixels
        size = (pixels_per_unit, pixels_per_unit)
        # If the character is a horizontal wall, draw a black rectangle
        if char == "-":
            y_pos = ((i - 1) / 2) + 1
            x_pos = (j - 1) / 2
            draw.rectangle(
                (
                    x_pos * pixels_per_unit,
                    (y_pos * pixels_per_unit) - (wall_thickness * pixels_per_unit / 2),
                    (x_pos * pixels_per_unit) + pixels_per_unit,
                    (y_pos * pixels_per_unit) + (wall_thickness * pixels_per_unit / 2),
                ),
                fill="black",
            )
        # If the character is an empty space, draw a white rectangle
        elif char == "|":
            y_pos = i / 2
            x_pos = j / 2
            draw.rectangle(
                (
                    x_pos * pixels_per_unit - (wall_thickness * pixels_per_unit / 2),
                    (y_pos * pixels_per_unit),
                    (x_pos * pixels_per_unit) + (wall_thickness * pixels_per_unit / 2),
                    (y_pos * pixels_per_unit) + pixels_per_unit,
                ),
                fill="black",
            )

# Save the image
image.save("maze.png")
