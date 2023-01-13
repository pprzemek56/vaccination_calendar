from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file("layouts/day.kv")


class Day(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
