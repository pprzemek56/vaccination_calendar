from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file("layouts/day.kv")


class Day(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_id = None

    @property
    def current_id(self):
        return self._current_id

    @current_id.setter
    def current_id(self, current_id):
        self._current_id = current_id
