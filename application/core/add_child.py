import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker
import re

sys.path.append('database')

import vaccination_calendar

Builder.load_file("layouts/add_child.kv")


class AddChild(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def show_date_picker(self):
        date_dialog = MDDatePicker(title="Wybierz datę", title_input="Wpisz datę")
        date_dialog.bind(on_save=self.save_date)
        date_dialog.open()

    def save_date(self, instance, value, date_range):
        self.ids.date_field.ids.text_field.text = f"{value}"

    def validate_inputs(self):
        name = str(self.ids.name_field.text).strip()
        date = str(self.ids.date_field.ids.text_field.text).strip()

        if re.match(r"^[A-Z]?[a-z]+$", name) is not None:
            vaccination_calendar.add_child(name, date)
            self.ids.name_field.text = ""
            self.ids.date_field.ids.text_field.text = ""
            return True

        if not self.dialog:
            self.dialog = MDDialog(
                title="Błędne imię!",
                text="Imię musi składać się tylko i wyłącznie z liter oraz tylko pierwsza litera może być wielka",
                buttons=[
                    MDFlatButton(
                        text="POWRÓT",
                        on_release=self.close_dialog)])
        self.dialog.open()
        return False

    def close_dialog(self, obj):
        self.dialog.dismiss()
