from PIL import Image, ImageDraw
import trimesh
import numpy as np

# trimesh needs "pip install "pyglet<2"", "pip install manifold3d"

# Open and read the maze file
maze_file = open("large_example.txt", "r")
text_maze = maze_file.read()

# Split the maze into lines
text_lines = text_maze.splitlines()

# Define the size of the maze
maze_size = (10, 10)

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

boxes = []

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
            bounds = np.array(
                [
                    [
                        x_pos,
                        (y_pos) - (wall_thickness / 2),
                        0,
                    ],
                    [
                        (x_pos) + 1,
                        (y_pos) + (wall_thickness / 2),
                        1,
                    ],
                ]
            )
            box = trimesh.creation.box(bounds=bounds)
            boxes.append(box)
        # If the character is a vertical wall, draw a black rectangle
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
            bounds = np.array(
                [
                    [
                        x_pos - (wall_thickness / 2),
                        (y_pos),
                        0,
                    ],
                    [
                        (x_pos) + (wall_thickness / 2),
                        (y_pos) + 1,
                        1,
                    ],
                ]
            )
            box = trimesh.creation.box(bounds=bounds)
            boxes.append(box)

# Combine all of the boxes together
maze_mesh = trimesh.util.concatenate(boxes)
boolean_maze = trimesh.boolean.union(boxes)
boolean_maze.apply_scale(1000)
boolean_maze.export("maze.stl")

# Save the image
image.save("maze.png")
