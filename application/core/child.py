import re
import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker
from kivy.metrics import dp

sys.path.append('database')
import vaccination_calendar

Builder.load_file("layouts/child.kv")


class Child(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_id = None
        self.child = None
        self.dialog = None

    @property
    def current_id(self):
        return self._current_id

    @current_id.setter
    def current_id(self, current_id):
        self._current_id = current_id

    @property
    def child(self):
        return self._child

    @child.setter
    def child(self, child):
        self._child = child

    def on_enter(self, *args):
        self.init_text_fields()

    def on_leave(self, *args):
        self.ids.child_layout.remove_widget(self.table)

    def init_text_fields(self):
        self.child = vaccination_calendar.get_child(self.current_id)
        self.ids.edit_name.ids.text_field.text = self.child["name"]
        self.ids.edit_name.ids.text_field.icon_left = "account"
        self.ids.edit_name.ids.edit_btn.on_release = self.edit_name_btn
        self.ids.edit_name.ids.save_btn.on_release = self.save_name_btn
        self.ids.edit_date.ids.text_field.text = self.child["birth_date"]
        self.ids.edit_date.ids.text_field.icon_left = "calendar"
        self.ids.edit_date.ids.edit_btn.on_release = self.edit_date_btn
        self.ids.edit_date.ids.save_btn.on_release = self.save_date_btn
        self.ids.edit_name.ids.save_btn.disabled = True
        self.ids.edit_date.ids.save_btn.disabled = True
        self.ids.edit_name.ids.edit_btn.icon = "pencil-lock"
        self.ids.edit_name.ids.text_field.disabled = True
        self.ids.edit_date.ids.text_field.disabled = True

    def edit_name_btn(self):
        if self.ids.edit_name.ids.edit_btn.icon == "pencil-lock":
            self.ids.edit_name.ids.edit_btn.icon = "pencil"
            self.ids.edit_name.ids.text_field.disabled = False
            self.ids.edit_name.ids.text_field.focus = True
            self.ids.edit_name.ids.save_btn.disabled = False
        else:
            self.ids.edit_name.ids.edit_btn.icon = "pencil-lock"
            self.ids.edit_name.ids.text_field.disabled = True
            self.ids.edit_name.ids.text_field.text = self.child["name"]
            self.ids.edit_name.ids.save_btn.disabled = True

    def edit_date_btn(self):
        if self.ids.edit_date.ids.edit_btn.icon == "pencil-lock":
            self.show_date_picker()
            self.ids.edit_date.ids.edit_btn.icon = "pencil"
            self.ids.edit_date.ids.save_btn.disabled = False
        else:
            self.ids.edit_date.ids.edit_btn.icon = "pencil-lock"
            self.ids.edit_date.ids.text_field.text = self.child["birth_date"]
            self.ids.edit_date.ids.save_btn.disabled = True

    def show_date_picker(self):
        date_dialog = MDDatePicker(title="Wybierz datę", title_input="Wpisz datę")
        date_dialog.bind(on_save=self.save_date, on_cancel=self.cancel_date)
        date_dialog.open()

    def save_date(self, instance, value, date_range):
        self.ids.edit_date.ids.text_field.text = f"{value}"
        self.ids.edit_date.ids.edit_btn.icon = "pencil-lock"

    def cancel_date(self, instance, time):
        self.ids.edit_date.ids.edit_btn.icon = "pencil-lock"
        self.ids.edit_date.ids.save_btn.disabled = True
        self.ids.edit_date.ids.text_field.text = self.child["birth_date"]
        self.ids.edit_date.ids.text_field.focus = False

    def save_name_btn(self):
        name = str(self.ids.edit_name.ids.text_field.text).strip()
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
            return

        vaccination_calendar.update_name(self.child["id"], name)
        self.ids.edit_name.ids.save_btn.disabled = True
        self.ids.edit_name.ids.edit_btn.icon = "pencil-lock"

    def save_date_btn(self):
        date = str(self.ids.edit_date.ids.text_field.text).strip()

        vaccination_calendar.update_date(self.child["id"], date)
        self.ids.edit_date.ids.save_btn.disabled = True
        self.ids.edit_date.ids.edit_btn.icon = "pencil-lock"

    def close_dialog(self, obj):
        self.dialog.dismiss()


def convert_time(start, end):
    if end <= 1:
        return f"Do 24h po narodzinach"

    if start <= 450:
        start_f = f"{int(start / 30) + 1} miesiąca"
    else:
        start_f = f"{int(start / 365)} roku"

    if end <= 540:
        end_f = f"{int(end / 30) + 1} miesiąca"
    else:
        end_f = f"{int(end / 365)} roku"

    return f"Od {start_f}, do {end_f} życia"


def convert_dose(dose):
    x, y = str(dose).split("/")

    return f"{x} z {y}"
