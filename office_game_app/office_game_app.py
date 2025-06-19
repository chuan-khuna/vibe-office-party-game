"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from office_game_app.pages.index import index
from office_game_app.pages.whats_behind import whats_behind

app = rx.App()
app.add_page(index, "/")
app.add_page(whats_behind, "/whats_behind")
