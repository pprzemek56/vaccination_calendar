import sys
from datetime import date

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon

sys.path.append('database')
import vaccination_calendar

Builder.load_file("layouts/day.kv")


class Dot(MDBoxLayout):
    pass


class Dots(MDBoxLayout):
    pass


class CarouselItem(GridLayout):
    pass


class Day(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_id = None
        self.app = App.get_running_app()

    @property
    def current_id(self):
        return self._current_id

    @current_id.setter
    def current_id(self, current_id):
        self._current_id = current_id

    def on_enter(self, *args):
        vaccinations = vaccination_calendar.get_notifications(date.fromisoformat(self.current_id))
        self.ids.current_date.text = str(self.current_id)
        dots_amount = len(vaccinations)

        for i in range(dots_amount):
            dot = Dot()
            dot.index = i
            if i == 0:
                dot.md_bg_color = "#2e8b2e"
            self.ids.dots.add_widget(dot)

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
            carousel_item.add_widget(
                MDIcon(icon="check-bold", theme_text_color="Custom", text_color=(0, 1, 0, 1), pos_hint={"center_x": 1})
                if vaccination['done'] else
                MDIcon(icon="close-thick", theme_text_color="Custom", text_color=(1, 0, 0, 1)))
            self.ids.carousel.add_widget(carousel_item)

    def on_leave(self, *args):
        self.ids.carousel._index = 0
        self.ids.dots.clear_widgets()
        self.ids.carousel.clear_widgets()

    def on_index(self, index: int) -> None:
        for instance_dot in self.ids.dots.children:
            if instance_dot.index == index:
                instance_dot.md_bg_color = "#3f9c3f"
            else:
                instance_dot.md_bg_color = "#90a390"
