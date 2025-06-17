import reflex as rx
from PIL import Image
import logging

GAP_SIZE = "2px"


def image_grid(image: Image.Image, num_rows: int, num_cols: int) -> rx.Component:
    # divide image into grid cells
    logging.info(f"image size: {image.size}, rows: {num_rows}, cols: {num_cols}")

    cell_width = image.width // num_cols
    cell_height = image.height // num_rows

    image_grid = []
    for row in range(num_rows):
        row_cells = []
        for col in range(num_cols):
            left = col * cell_width
            upper = row * cell_height
            right = left + cell_width
            lower = upper + cell_height
            cell_image = image.crop((left, upper, right, lower))
            row_cells.append(cell_image)
        image_grid.append(row_cells)

    return rx.vstack(
        rx.text(f"Image Grid: {num_rows} rows, {num_cols} cols"),
        rx.vstack(
            *[
                rx.hstack(*[rx.image(src=cell_image) for cell_image in row_cells], style={"gap": GAP_SIZE})
                for row_cells in image_grid
            ],
            style={"gap": GAP_SIZE},
        ),
    )
