import reflex as rx
from PIL import Image

from office_game_app.components.whats_behind.image_grid import image_grid

place_holder_image_path = 'assets/lucy.png'
default_num_rows = 5
default_num_cols = 5


class CellState(rx.State):
    num_rows: int = default_num_rows
    num_cols: int = default_num_cols
    cells: dict[str, bool] = {
        f"{row}_{col}": True for row in range(default_num_rows) for col in range(default_num_cols)
    }

    @rx.event
    def toggle_hidden(self, row: int, col: int):
        # toggle the hidden state of a cell
        key = f"{row}_{col}"
        if key in self.cells:
            self.cells[key] = not self.cells[key]
        else:
            rx.log(f"Cell {key} not found in state.")


def whats_behind() -> rx.Component:
    # what's behind game
    image = Image.open(place_holder_image_path)

    return rx.container(
        rx.vstack(
            rx.text("What's Behind Game"),
            image_grid(image, num_rows=default_num_rows, num_cols=default_num_cols, state=CellState),
        )
    )
