import reflex as rx
from PIL import Image
import logging
import numpy as np

GAP_SIZE = "2px"


def _styled_image(image: Image.Image, hidden: bool = False, on_click=None) -> rx.Component:
    style = {"width": "100%", "height": "100%", "cursor": "pointer"}
    if hidden:
        # hidden effect
        # style.update({"filter": "grayscale(80%)", "opacity": "1.0"})

        # pillow image to black colour
        arr = np.zeros_like(np.array(image))
        image = Image.fromarray(arr)

    return rx.image(src=image, style=style, on_click=on_click)


def wrap_image(image: Image.Image, row_index: int, col_index: int, state: rx.State) -> rx.Component:
    hidden = state.cells[f"{row_index}_{col_index}"]
    return rx.cond(
        hidden,
        _styled_image(image, hidden=True, on_click=state.toggle_hidden(row=row_index, col=col_index)),
        _styled_image(image, hidden=False, on_click=state.toggle_hidden(row=row_index, col=col_index)),
    )


def image_grid(image: Image.Image, num_rows: int, num_cols: int, state: rx.State) -> rx.Component:
    # divide image into grid cells
    logging.info(f"image size: {image.size}, rows: {num_rows}, cols: {num_cols}")

    # resize image to have max width and height
    max_size = (800, 800)
    image.thumbnail(max_size)
    image = image.convert("RGB")  # ensure image is in RGB mode

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
                rx.hstack(
                    *[
                        wrap_image(image=cell_image, row_index=row_index, col_index=col_index, state=state)
                        for col_index, cell_image in enumerate(row_cells)
                    ],
                    style={"gap": GAP_SIZE},
                )
                for row_index, row_cells in enumerate(image_grid)
            ],
            style={"gap": GAP_SIZE},
        ),
    )
