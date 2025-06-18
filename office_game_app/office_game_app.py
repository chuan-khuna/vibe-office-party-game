"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from office_game_app.pages.index import index
from office_game_app.pages.whats_behind import whats_behind
from office_game_app.pages.whats_behind_2 import whats_behind_2

app = rx.App()
app.add_page(index, "/")
app.add_page(whats_behind, "/whats_behind")
app.add_page(whats_behind_2, "/whats_behind_2")
