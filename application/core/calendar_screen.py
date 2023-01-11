import sys
from calendar import monthcalendar, weekheader
from datetime import date

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDIconButton
from kivymd.uix.pickers import MDDatePicker

sys.path.append('database')

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
        year = self.calendar_date.year
        month = self.calendar_date.month

        previous_month = monthcalendar(year - 1 if month == 1 else year, 12 if month == 1 else month - 1)[
            len(monthcalendar(year - 1 if month == 1 else year, 12 if month == 1 else month - 1)) - 1]
        next_month = monthcalendar(year + 1 if month == 12 else year, 1 if month == 12 else month + 1)[0]
        current_month = monthcalendar(year, month)

        for i in range(6):
            for j in range(7):
                try:
                    self.ids.calendar_layout.add_widget(
                        MDIconButton(id=str(date(year, month, current_month[i][j])),
                                     icon=f"images/icons/{current_month[i][j]}.png",
                                     size_hint=(1, 1)))
                except ValueError:
                    if i == 0:
                        self.ids.calendar_layout.add_widget(
                            MDIconButton(id=str(date(
                                year if month != 1 else year - 1,
                                month - 1 if month != 1 else 12,
                                previous_month[j])),
                                icon=f"images/icons/{previous_month[j]}s.png",
                                size_hint=(1, 1)))

                    elif i == 4 or i == 5:
                        self.ids.calendar_layout.add_widget(
                            MDIconButton(id=str(date(
                                year if month != 12 else year + 1,
                                month + 1 if month != 12 else 1,
                                next_month[j])),
                                icon=f"images/icons/{next_month[j]}s.png",
                                size_hint=(1, 1)))
                except IndexError:
                    break

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


def minus_month(current_date):
    if current_date.month == 1:
        return current_date.replace(month=12, year=current_date.year - 1)

    return current_date.replace(month=current_date.month - 1)


def plus_month(current_date):
    if current_date.month == 12:
        return current_date.replace(month=1, year=current_date.year + 1)

    return current_date.replace(month=current_date.month + 1)
