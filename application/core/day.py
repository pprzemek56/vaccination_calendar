import sys
from datetime import date

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel

sys.path.append('database')
import vaccination_calendar

Builder.load_file("layouts/day.kv")


class CarouselItem(BoxLayout):
    pass


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

    def on_enter(self, *args):
        vaccinations = vaccination_calendar.get_notifications(date.fromisoformat(self.current_id))

        for vaccination in vaccinations:
            box_layout = BoxLayout()
            box_layout.add_widget(MDLabel(text=f"{vaccination['name']}"))
            self.ids.carousel.add_widget(box_layout)
