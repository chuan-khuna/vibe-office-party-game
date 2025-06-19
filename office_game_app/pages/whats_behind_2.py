import reflex as rx
from PIL import Image
import logging
import io

from office_game_app.components.whats_behind.cell_config import upload_input, cell_config_input

DEFAULT_NUM_ROWS = 10
DEFAULT_NUM_COLS = 10
place_holder_image_path = 'assets/lucy.png'
MAX_SIZE = (1080, 1080)  # Maximum size for the image thumbnail


class GameState(rx.State):
    num_rows: int = DEFAULT_NUM_ROWS
    num_cols: int = DEFAULT_NUM_COLS

    # hidden state for each cell in the grid
    game_state: dict[str, bool] = {
        f"{row}_{col}": True for row in range(DEFAULT_NUM_ROWS) for col in range(DEFAULT_NUM_COLS)
    }

    image: Image.Image = Image.open(place_holder_image_path)

    @rx.event
    def toggle_hidden(self, row: int, col: int):
        key = f"{row}_{col}"
        if key in self.game_state:
            self.game_state[key] = not self.game_state[key]

    @rx.event
    def show_all(self):
        for k, v in self.game_state.items():
            self.game_state[k] = False

    @rx.event
    def hide_all(self):
        for k, v in self.game_state.items():
            self.game_state[k] = True

    @rx.event
    def set_num_rows(self, value: list[int | float]):
        # set the number of rows
        self.num_rows = value[0]
        self.reset_game_state()

    @rx.event
    def set_num_cols(self, value: list[int | float]):
        # set the number of columns
        self.num_cols = value[0]
        self.reset_game_state()

    @rx.event
    def reset_game_state(self):
        # reset all cells to hidden
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                key = f"{row}_{col}"
                self.game_state[key] = True
                logging.info(f"Reset cell {key} to hidden.")

    @rx.event
    def reset_game_to_default(self):
        # Reset the game state to default values
        self.num_rows = DEFAULT_NUM_ROWS
        self.num_cols = DEFAULT_NUM_COLS
        self.game_state = {f"{row}_{col}": True for row in range(DEFAULT_NUM_ROWS) for col in range(DEFAULT_NUM_COLS)}
        self.image = Image.open(place_holder_image_path)
        logging.info("Game state reset to default values.")

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        first_file = files[0]
        upload_data = await first_file.read()
        self.image = Image.open(io.BytesIO(upload_data))
        self.image = self.image.convert("RGB")  # Ensure the image is in RGB format
        self.image.thumbnail(MAX_SIZE)  # Resize the image to fit within 1080x1080

    @rx.var
    def image_width(self) -> int:
        return self.image.width if self.image else 0

    @rx.var
    def image_height(self) -> int:
        return self.image.height if self.image else 0


def get_grid_bg(hidden: rx.State) -> str:
    if hidden:
        return "rgba(0, 0, 0, 1.0)"
    else:
        return "rgba(0, 0, 0, 0.0)"


def whats_behind_2():
    grid_dynamic = rx.box(
        # Background image
        rx.image(
            src=GameState.image,
            width="100%",
            height="100%",
            object_fit="cover",
            position="absolute",
            top="0",
            left="0",
            z_index="1",
        ),
        # Grid overlay
        rx.box(
            rx.foreach(
                rx.Var.range(GameState.num_rows * GameState.num_cols),
                lambda index: rx.box(
                    rx.cond(
                        GameState.game_state[f"{index // GameState.num_cols}_{index % GameState.num_cols}"],
                        rx.text(
                            f"{(index // GameState.num_cols) + 1}, {(index % GameState.num_cols) + 1}",
                            font_size="clamp(8px, 1.5vw, 14px)",
                            color="white",
                            text_align="center",
                        ),
                        rx.text(""),
                    ),
                    background_color=rx.cond(
                        GameState.game_state[f"{index // GameState.num_cols}_{index % GameState.num_cols}"],
                        get_grid_bg(True),
                        get_grid_bg(False),
                    ),
                    on_click=GameState.toggle_hidden(row=index // GameState.num_cols, col=index % GameState.num_cols),
                    border="1px solid rgba(255, 255, 255, 0.2)",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    cursor="pointer",
                ),
            ),
            display="grid",
            grid_template_columns=f"repeat({GameState.num_cols}, 1fr)",
            grid_template_rows=f"repeat({GameState.num_rows}, 1fr)",
            position="absolute",
            top="0",
            left="0",
            width="100%",
            height="100%",
            z_index="2",
        ),
        position="relative",
        width="100%",
        # Dynamic aspect ratio calculation
        aspect_ratio=rx.cond(
            GameState.image_width > 0,
            f"{GameState.image_width} / {GameState.image_height}",
            "16 / 9",  # Fallback
        ),
        overflow="hidden",
    )

    return rx.container(rx.vstack(cell_config_input(GameState), grid_dynamic))
