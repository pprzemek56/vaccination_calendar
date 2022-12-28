import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.pickers import MDDatePicker
import re

sys.path.append('database')

import vaccination_calendar

Builder.load_file("layouts/add_child.kv")


class AddChild(Screen):

    def show_date_picker(self):
        date_dialog = MDDatePicker(title="Wybierz datę", title_input="Wpisz datę")
        date_dialog.bind(on_save=self.save_date)
        date_dialog.open()

    def save_date(self, instance, value, date_range):
        self.ids.date_field.text = f"{value}"

    def validate_inputs(self):
        name = str(self.ids.name_field.text).strip()
        date = str(self.ids.date_field.text).strip()

        if re.match(r"^[A-Z]?[a-z]+$", name) is not None or re.match(r"^\d{4}-\d{2}-\d{2}$", date) is not None:
            vaccination_calendar.add_child(name, date)
            return True

        # TODO: Wyświetlenie kompunikatu o błędzie
        return False
