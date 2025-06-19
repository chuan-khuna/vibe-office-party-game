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
