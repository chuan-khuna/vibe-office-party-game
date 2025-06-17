import reflex as rx
from PIL import Image

place_holder_image_path = 'assets/lucy.png'


def whats_behind() -> rx.Component:
    # what's behind game
    image = Image.open(place_holder_image_path)

    return rx.container(rx.vstack(rx.text("What's Behind Game"), rx.image(src=image)))
