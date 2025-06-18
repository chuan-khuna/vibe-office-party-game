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
        f"{row}_{col}": False for row in range(DEFAULT_NUM_ROWS) for col in range(DEFAULT_NUM_COLS)
    }

    image: Image.Image = Image.open(place_holder_image_path)

    @rx.event
    def toggle_hidden(self, row: int, col: int):
        key = f"{row}_{col}"
        if key in self.game_state:
            self.game_state[key] = not self.game_state[key]


def get_grid_bg(hidden: rx.State) -> str:
    if hidden:
        return "rgba(0, 0, 255, 0.8)"
    else:
        return "rgba(164, 224, 174, 0.2)"


def whats_behind_2():
    text_component = rx.text("What's behind?")
    image_bg = rx.image(src=GameState.image, width="100%", height="100%")

    grid = rx.vstack(
        rx.foreach(
            rx.Var.range(GameState.num_rows),
            lambda row_index: rx.hstack(
                rx.foreach(
                    rx.Var.range(GameState.num_cols),
                    lambda col_index: rx.box(
                        rx.cond(
                            GameState.game_state[f"{row_index}_{col_index}"],
                            rx.text(f"{row_index + 1}, {col_index + 1}"),
                            rx.text(""),
                        ),
                        background_color=rx.cond(
                            GameState.game_state[f"{row_index}_{col_index}"],
                            get_grid_bg(True),
                            get_grid_bg(False),
                        ),
                        on_click=GameState.toggle_hidden(row=row_index, col=col_index),
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

    # Use a box with relative positioning to contain both image and grid
    return rx.container(
        rx.box(
            image_bg,  # Background image
            rx.box(
                grid,
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                z_index="1",
            ),
            position="relative",
            width="100%",
        )
    )
