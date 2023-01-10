import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from datetime import date
from calendar import monthcalendar, weekheader

from kivymd.uix.button import MDIconButton, MDFloatingActionButton, MDRectangleFlatIconButton
from kivymd.uix.pickers import MDDatePicker

sys.path.append('database')
import vaccination_calendar

month_name = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
              "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]

Builder.load_file("layouts/calendar.kv")


class Calendar(Screen):
    calendar_date = date.today()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calendar_sheets = None
        self.first_enter = True

    def on_enter(self, *args):
        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"

        if self.first_enter:
            for weekday in weekheader(3).split(" "):
                label = MDIconButton(icon=f"images/icons/{weekday}.png", size_hint=(1, 1), disabled=True)
                self.ids.weekdays_layout.add_widget(label)

            self.generate_calendar()

            self.first_enter = False

    def set_date(self):
        date_dialog = MDDatePicker(title="Wybierz datę", title_input="Wpisz datę")
        date_dialog.bind(on_save=self.save_date)
        date_dialog.open()

    def save_date(self, instance, value, date_range):
        self.calendar_date = self.calendar_date.replace(year=value.year, month=value.month, day=value.day)
        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"
        self.generate_calendar()

    def generate_calendar(self):
        self.ids.calendar_layout.clear_widgets()
        calendar = get_calendar(self.calendar_date.year, self.calendar_date.month)

        try:
            self.calendar_sheets = vaccination_calendar.get_sheets_between_dates(calendar[0][0]["id"],
                                                                                 calendar[5][6]["id"])
        except TypeError:
            self.calendar_sheets = vaccination_calendar.get_sheets_between_dates(calendar[0][0]["id"],
                                                                                 calendar[4][6]["id"])
        for i in range(6):
            for j in range(7):
                btn = None
                try:
                    btn = MDIconButton(icon="images/icons/1c.png", size_hint=(1, 1))
                except TypeError:
                    break

                self.ids.calendar_layout.add_widget(btn)

    def change_month(self, side):
        active_month = self.calendar_date.month
        if side == "left":
            if active_month == 1:
                self.calendar_date = self.calendar_date.replace(month=self.calendar_date.month + 11)
            else:
                self.calendar_date = self.calendar_date.replace(month=self.calendar_date.month - 1)
        else:
            if active_month == 12:
                self.calendar_date = self.calendar_date.replace(month=self.calendar_date.month - 11)
            else:
                self.calendar_date = self.calendar_date.replace(month=self.calendar_date.month + 1)

        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"
        self.generate_calendar()

    def change_year(self, side):

        if side == "left":
            self.calendar_date = self.calendar_date.replace(year=self.calendar_date.year - 1)
        else:
            self.calendar_date = self.calendar_date.replace(year=self.calendar_date.year + 1)

        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.generate_calendar()


def get_calendar(year, month):
    previous_month = monthcalendar(year - 1 if month == 1 else year,
                                   12 if month == 1 else month - 1)[
        len(monthcalendar(year - 1 if month == 1 else year, 12 if month == 1 else month - 1)) - 1]
    next_month = monthcalendar(year + 1 if month == 12 else year, 1 if month == 12 else month + 1)[0]
    current_month = monthcalendar(year, month)

    calendar = [[_ for _ in range(7)] for _ in range(6)]

    for i in range(6):
        for j in range(7):
            try:
                calendar[i][j] = {"id": str(date(year, month, current_month[i][j])), "icon": current_month[i][j]}
            except IndexError:
                break
            except ValueError:
                calendar[i][j] = {"id": 0, "icon": 0}

            if i == 0:
                if calendar[i][j]["id"] == 0:
                    calendar[i][j] = {"id": str(date(
                        year if month != 1 else year - 1, month - 1 if month != 1 else 12, previous_month[j])),
                        "icon": f"{previous_month[j]}w"}
            elif i == 5 or i == 4:
                if calendar[i][j]["id"] == 0:
                    calendar[i][j] = {"id": str(date(
                        year if month != 12 else year + 1, month + 1 if month != 12 else 1, next_month[j])),
                        "icon": f"{next_month[j]}w"}
    return calendar


def minus_month(current_date):
    if current_date.month == 1:
        return current_date.replace(month=12, year=current_date.year - 1)

    return current_date.replace(month=current_date.month - 1)


def plus_month(current_date):
    if current_date.month == 12:
        return current_date.replace(month=1, year=current_date.year + 1)

    return current_date.replace(month=current_date.month + 1)
