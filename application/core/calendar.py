from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from datetime import date

from kivymd.uix.label import MDLabel

month_name = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
              "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]

Builder.load_file("layouts/calendar.kv")


class Calendar(Screen):

    calendar_date = date.today()

    def on_enter(self, *args):
        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"

        for i in range(7):
            for j in range(7):
                self.ids.calendar_layout.add_widget(Label(text=f"{i}:{j}", size_hint=(.142, .142), color=(0, 0, 0, 1)))

    def month_to_left(self):
        pass

    def month_to_right(self):
        pass

