import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker
import re
import datetime

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

        # Walidacja imienia
        if re.match(r"^[A-Z]?[a-z]+$", name) is None:
            self.dialog = MDDialog(
                title="Błędne dane",
                text=f"Imię musi składać się tylko i wyłącznie z liter oraz tylko pierwsza litera może być wielka",
                buttons=[
                    MDFlatButton(
                        text="POWRÓT",
                        on_release=self.close_dialog)])
            self.dialog.open()
            return False

        # Walidacja daty
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date) is None:
            self.dialog = MDDialog(
                title="Błędne dane",
                text=f"Data musi być podana w formacie: RRRR-MM-DD, uwzgledniając przy tym poprawność daty",
                buttons=[
                    MDFlatButton(
                        text="POWRÓT",
                        on_release=self.close_dialog)])
            self.dialog.open()
            return False

        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            self.dialog = MDDialog(
                title="Błędne dane",
                text=f"Niepoprawne dane",
                buttons=[
                    MDFlatButton(
                        text="POWRÓT",
                        on_release=self.close_dialog)])
            self.dialog.open()
            return False

        vaccination_calendar.add_child(name, date)
        self.ids.name_field.text = ""
        self.ids.date_field.ids.text_field.text = ""
        return True

    def close_dialog(self, obj):
        self.dialog.dismiss()
