import reflex as rx
from PIL import Image

DEFAULT_NUM_ROWS = 10
DEFAULT_NUM_COLS = 10
place_holder_image_path = 'assets/lucy.png'


class GameState(rx.State):
    num_rows: int = DEFAULT_NUM_ROWS
    num_cols: int = DEFAULT_NUM_COLS

    # initialise the game state
    game_state: dict[str, bool] = {
        f"{row}_{col}": True for row in range(DEFAULT_NUM_ROWS) for col in range(DEFAULT_NUM_COLS)
    }

    image: Image.Image = Image.open(place_holder_image_path)


def whats_behind_2():
    text_component = rx.text("What's behind?")
    image_bg = rx.box(
        rx.image(src=GameState.image, width="100%", height="100%"),
    )

    grid = rx.vstack(
        rx.foreach(
            rx.Var.range(GameState.num_rows),
            lambda row_index: rx.hstack(
                rx.foreach(
                    rx.Var.range(GameState.num_cols),
                    lambda col_index: rx.box(
                        rx.text(f"{row_index + 1}, {col_index + 1}"),
                        background_color="cyan",
                        border="1px solid white",
                        width="100px",
                        height="100px",
                    ),
                ),
                spacing="0",
            ),
        ),
        width="100%",
        spacing="0",
    )

    return rx.container(rx.vstack(text_component, grid, image_bg))
