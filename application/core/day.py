import sys
from datetime import date

from kivy.graphics import Color, Rectangle, Line
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel, MDIcon

sys.path.append('database')
import vaccination_calendar

Builder.load_file("layouts/day.kv")


class CarouselItem(GridLayout):
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
        self.ids.current_date.text = str(self.current_id)

        for vaccination in vaccinations:
            carousel_item = CarouselItem()
            carousel_item.add_widget(MDLabel(text=f"Imię: "))
            carousel_item.add_widget(MDLabel(text=f"{vaccination['name']}"))
            carousel_item.add_widget(MDLabel(text=f"Szczepienie przeciw: "))
            carousel_item.add_widget(MDLabel(text=f"{vaccination['title']}"))
            carousel_item.add_widget(MDLabel(text=f"Należy wykonać do: "))
            carousel_item.add_widget(MDLabel(text=f"{vaccination['finish_date']}"))
            carousel_item.add_widget(MDLabel(text=f"Dawka: "))
            carousel_item.add_widget(MDLabel(text=f"{vaccination['dose']}"))
            carousel_item.add_widget(MDLabel(text=f"Obowiązkowe: "))
            carousel_item.add_widget(
                MDIcon(icon="check-bold", theme_text_color="Custom", text_color=(0, 1, 0, 1), pos_hint={"center_x": 1})
                if vaccination['finish_date'] else
                MDIcon(icon="close-thick", theme_text_color="Custom", text_color=(1, 0, 0, 1)))
            carousel_item.add_widget(MDLabel(text=f"Wykonane: "))
            carousel_item.add_widget(MDIcon(icon="check-bold", theme_text_color="Custom", text_color=(0, 1, 0, 1))
                                     if vaccination['done'] else
                                     MDIcon(icon="close-thick", theme_text_color="Custom", text_color=(1, 0, 0, 1)))
            self.ids.carousel.add_widget(carousel_item)
