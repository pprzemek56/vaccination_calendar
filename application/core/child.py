from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file("layouts/child.kv")


class Child(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_id = None

    def on_enter(self, *args):
        print(self.ids)

    def show_date_picker(self):
        pass
