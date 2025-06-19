import reflex as rx


def get_grid_bg(hidden: rx.State) -> str:
    if hidden:
        return "rgba(0, 0, 0, 1.0)"
    else:
        return "rgba(0, 0, 0, 0.0)"


def dynamic_grid(state: rx.State) -> rx.Component:
    return rx.box(
        # Background image
        rx.image(
            src=state.image,
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
                rx.Var.range(state.num_rows * state.num_cols),
                lambda index: rx.box(
                    rx.cond(
                        state.game_state[f"{index // state.num_cols}_{index % state.num_cols}"],
                        rx.text(
                            f"{(index // state.num_cols) + 1}, {(index % state.num_cols) + 1}",
                            font_size="clamp(8px, 1.5vw, 14px)",
                            color="white",
                            text_align="center",
                        ),
                        rx.text(""),
                    ),
                    background_color=rx.cond(
                        state.game_state[f"{index // state.num_cols}_{index % state.num_cols}"],
                        get_grid_bg(True),
                        get_grid_bg(False),
                    ),
                    on_click=state.toggle_hidden(row=index // state.num_cols, col=index % state.num_cols),
                    border="1px solid rgba(255, 255, 255, 0.2)",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    cursor="pointer",
                ),
            ),
            display="grid",
            grid_template_columns=f"repeat({state.num_cols}, 1fr)",
            grid_template_rows=f"repeat({state.num_rows}, 1fr)",
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
            state.image_width > 0,
            f"{state.image_width} / {state.image_height}",
            "16 / 9",  # Fallback
        ),
        overflow="hidden",
    )
