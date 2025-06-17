import reflex as rx
from PIL import Image

from office_game_app.components.whats_behind.image_grid import image_grid_component
from office_game_app.components.whats_behind.cell_config import cell_config_input
import logging
import io


place_holder_image_path = 'assets/lucy.png'
default_num_rows = 3
default_num_cols = 3


class CellState(rx.State):
    num_rows: int = default_num_rows
    num_cols: int = default_num_cols
    cells: dict[str, bool] = {
        f"{row}_{col}": True for row in range(default_num_rows) for col in range(default_num_cols)
    }
    image: Image.Image = Image.open(place_holder_image_path)

    @rx.event
    def toggle_hidden(self, row: int, col: int):
        # toggle the hidden state of a cell
        key = f"{row}_{col}"
        if key in self.cells:
            self.cells[key] = not self.cells[key]

    @rx.event
    def set_num_rows(self, value: list[int | float]):
        # set the number of rows
        self.num_rows = value[0]

    @rx.event
    def set_num_cols(self, value: list[int | float]):
        # set the number of columns
        self.num_cols = value[0]

    @rx.event
    def reset_cell(self):
        # reset all cells to hidden
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                key = f"{row}_{col}"
                self.cells[key] = True
                logging.info(f"Reset cell {key} to hidden.")

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        first_file = files[0]
        upload_data = await first_file.read()
        self.image = Image.open(io.BytesIO(upload_data))
        self.image = self.image.convert("RGB")  # Ensure the image is in RGB format

    @rx.var(cache=True)
    def image_grid(self) -> list[list[Image.Image]]:
        image_grid = []

        image = self.image.convert("RGB")
        max_size = (1080, 1080)
        image.thumbnail(max_size)

        cell_width = image.width // self.num_cols
        cell_height = image.height // self.num_rows
        for row in range(self.num_rows):
            row_cells = []
            for col in range(self.num_cols):
                left = col * cell_width
                upper = row * cell_height
                right = left + cell_width
                lower = upper + cell_height
                cell_image = image.crop((left, upper, right, lower))
                row_cells.append(cell_image)
            image_grid.append(row_cells)
        return image_grid

    @rx.var
    def cell_width(self) -> int:
        return self.image.width // self.num_cols if self.image else 0

    @rx.var
    def cell_height(self) -> int:
        return self.image.height // self.num_rows if self.image else 0

    @rx.event
    def reset_game_to_default(self):
        # Reset the game state to default values
        self.num_rows = default_num_rows
        self.num_cols = default_num_cols
        self.cells = {f"{row}_{col}": True for row in range(default_num_rows) for col in range(default_num_cols)}
        self.image = Image.open(place_holder_image_path)
        logging.info("Game state reset to default values.")

    @rx.event
    def show_all(self):
        for k, v in self.cells.items():
            self.cells[k] = False

    @rx.event
    def hide_all(self):
        for k, v in self.cells.items():
            self.cells[k] = True


def whats_behind() -> rx.Component:
    return rx.container(
        rx.vstack(rx.text("What's Behind Game"), cell_config_input(CellState), image_grid_component(CellState))
    )
