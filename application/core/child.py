import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

sys.path.append('database')
import vaccination_calendar

Builder.load_file("layouts/child.kv")


class Child(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_id = None

    @property
    def current_id(self):
        return self._current_id

    @current_id.setter
    def current_id(self, current_id):
        self._current_id = current_id

    def on_enter(self, *args):
        pass
        # self.ids.edit_name.ids.text_field.text =

    def show_date_picker(self):
        pass
