import reflex as rx
from PIL import Image
import logging
import numpy as np

GAP_SIZE = "1px"


def _styled_image(image: Image.Image, hidden: bool = False, event_handler_fn=None) -> rx.Component:
    style = {"width": "100%", "height": "100%", "cursor": "pointer"}
    if hidden:
        style.update({"filter": "brightness(0%)", "opacity": "1.0"})

    return rx.image(src=image, style=style, on_click=event_handler_fn)


def wrap_image(image: Image.Image, row_index: int, col_index: int, state: rx.State) -> rx.Component:
    hidden = state.cells[f"{row_index}_{col_index}"]
    return rx.cond(
        hidden,
        _styled_image(image, hidden=True, event_handler_fn=state.toggle_hidden(row=row_index, col=col_index)),
        _styled_image(image, hidden=False, event_handler_fn=state.toggle_hidden(row=row_index, col=col_index)),
    )


def image_grid_component(state: rx.State) -> rx.Component:
    return rx.vstack(
        rx.text(f"Image Grid: {state.num_rows} rows, {state.num_cols} cols"),
        rx.vstack(
            rx.foreach(
                state.image_grid,
                lambda row_cells, row_index: rx.hstack(
                    rx.foreach(
                        row_cells,
                        lambda cell_image, col_index: wrap_image(
                            image=cell_image,
                            row_index=row_index,
                            col_index=col_index,
                            state=state,
                        ),
                    ),
                    style={"gap": GAP_SIZE},
                ),
            ),
            style={"gap": GAP_SIZE},
        ),
    )
