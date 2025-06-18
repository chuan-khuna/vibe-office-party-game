import reflex as rx

color = "rgb(107,99,246)"


def upload_input(state: rx.State) -> rx.Component:
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text("Drag and drop files here or click to select files"),
                rx.hover_card.root(
                    rx.hover_card.trigger(rx.link("Hover to view uploaded file path")),
                    rx.hover_card.content(
                        rx.text(rx.selected_files("upload1")),
                        side="top",
                    ),
                ),
            ),
            id="upload1",
            max_files=1,
            border=f"1px dotted {color}",
            padding="5em",
        ),
        rx.hstack(
            rx.button(
                "Upload",
                on_click=state.handle_upload(rx.upload_files(upload_id="upload1")),
            ),
            rx.button(
                "Remove Selected File",
                on_click=rx.clear_selected_files("upload1"),
                color_scheme="red",
            ),
        ),
    )


def cell_config_input(state: rx.State) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.heading(f"{state.num_cols} x {state.num_rows}"),
                rx.vstack(
                    rx.text("Number of Rows"),
                    rx.slider(
                        min=3, max=10, value=[state.num_rows], on_change=state.set_num_rows.throttle(20), width="200px"
                    ),
                ),
                rx.vstack(
                    rx.text("Number of Columns"),
                    rx.slider(
                        min=3, max=10, value=[state.num_cols], on_change=state.set_num_cols.throttle(20), width="200px"
                    ),
                ),
                # rx.button("Reset State", on_click=state.reset_cell, width="200px", color_scheme="cyan"),
                rx.button(
                    "Reset Game to Default",
                    on_click=state.reset_game_to_default,
                    width="200px",
                    color_scheme="cyan",
                ),
                rx.hstack(
                    rx.button(
                        "Show all",
                        on_double_click=state.show_all,
                        width="50%",
                        color_scheme="gray",
                    ),
                    rx.button(
                        "Hide all",
                        on_click=state.hide_all,
                        width="50%",
                        color_scheme="gray",
                    ),
                ),
            ),
            upload_input(state),
            style={"gap": "2em", "align-items": "center"},
        ),
        width="100%",
    )
