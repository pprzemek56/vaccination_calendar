from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from datetime import date


month_name = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
              "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]

Builder.load_file("layouts/calendar.kv")


class Calendar(Screen):

    calendar_date = date.today()

    def on_enter(self, *args):
        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"

    def month_to_left(self):
        pass

    def month_to_right(self):
        pass

