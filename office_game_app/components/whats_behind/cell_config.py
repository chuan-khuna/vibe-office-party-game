import reflex as rx


def cell_config_input(state: rx.State) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(f"{state.num_cols} x {state.num_rows}"),
            rx.vstack(
                rx.text("Number of Rows"),
                rx.slider(min=3, max=10, value=[state.num_rows], on_change=state.set_num_rows, width="200px"),
            ),
            rx.vstack(
                rx.text("Number of Columns"),
                rx.slider(min=3, max=10, value=[state.num_cols], on_change=state.set_num_cols, width="200px"),
            ),
            rx.button("Reset Cells", on_click=state.reset_cell, width="200px"),
        ),
        width="100%",
    )
